from negmas import SAOMechanism, TimeBasedConcedingNegotiator, MappingUtilityFunction ,AspirationNegotiator
import random  # for generating random ufuns
import negmas
from negmas import (
    make_issue,
    SAOMechanism,
    NaiveTitForTatNegotiator,
    TimeBasedConcedingNegotiator,
)
from negmas.preferences import LinearAdditiveUtilityFunction as LUFun
from negmas.preferences.value_fun import LinearFun, IdentityFun, AffineFun

import matplotlib.pyplot as plt
import random
import numpy as np
from negmas.sao import SAONegotiator, SAOResponse
from negmas import Outcome, ResponseType
import time
from negmas.preferences import pareto_frontier, nash_points
import os
import math
from scipy.optimize import curve_fit
### 复刻ANL的框架...除了ufun无法转过来，用了之前的线性函数代替，其他都通了.

### generate 部分不让步

static_cnt = 0
cnt_start = 0

def aspiration_function(t, mx, rv, e, c):
    """A monotonically decreasing curve starting at mx (t=0) and ending at rv (t=1)"""
    return (mx - rv) * (1.0 - c * np.power(t, e)) + rv




class AANegotiatior(SAONegotiator):

    """A simple curve fitting modeling agent"""
    # 要调用的协商器的第一个方法是__init__方法，该方法通常在ufun设置之前创建协商器时调用。可以使用此方法构造协商器，为运行代理所需的任何变量设置初始值。
    # 这里需要注意的一件重要的事情是，你的协商器必须将它不使用的任何参数传递给它的父对象，以确保对象被正确构造。
    def __init__(self, *args, e: float = 5.0, **kwargs):
        """Initialization"""
        # 为谈判者设置变量
        super().__init__(*args, **kwargs)
        self.e = e #存储我们将使用的让步曲线的指数
        # keeps track of times at which the opponent offers
        self.opponent_times: list[float] = [] #对手出价时间
        # keeps track of opponent utilities of its offers
        self.opponent_utilities: list[float] = [] #对手效用
        
        # keeps track of our last estimate of the opponent reserved value
        #（使用对手建模函数拟合）
        self._past_oppnent_rv = 0.0 # 我们开始假设对手的保留值为零。这是一个乐观的假设，因为这意味着任何对我们来说合理的事情对对手来说也是合理的，所以我们有更多的谈判能力。
        # keeps track of the rational outcome set given our estimate of the
        # opponent reserved value and our knowledge of ours
        self._rational: list[tuple[float, float, Outcome]] = [] #我们将在这里存储需要让步的理性结果列表。对于每个结果，我们将存储自己的效用，对手的效用和结果本身(按此顺序)。
        self.current_segment = None  # Initialize the segment index to None
        self.current_segment_index = None
        self.total_segments = 0
        self._type_name = "AANegotiatior"
        self._nash_util = 0.0
        self._opponent_nash_util = 0.0
        # 当前月日时分秒
        self.negotiation_round = 0  # Initialize negotiation round
        self.last_generated_offer = None  # Initialize the last generated offer
        # self.writer = open(f'./{folder_name}/negotiation_agent_test_{negotiation_round}.txt', 'w+')
        self.negotiation_started = False  # 新增标志
        self.enumerated_outcomes = None  # Initialize to None
        self.opponent_tough = False  # Initialize to False
        self.last_checked_time = 0.0

        
        

    
    
    def on_negotiation_start(self, state):
        self.enumerated_outcomes = list(self.ufun.outcome_space.enumerate_or_sample())
        global static_cnt
        static_cnt+=1

        
        print("-aaaaaaaa--")

        # self.ufun = self.normalize_utility_function(self.ufun, self.nmi.outcome_space)
        # self.opponent_ufun = self.normalize_utility_function(self.opponent_ufun, self.nmi.outcome_space)
        # print('reserved_value:')
        
        # print(self.ufun.reserved_value)
        # assert False
        #### 注意 目前数据集ufun是不提供保留值的，两个保留值都是-inf###
        self.negotiation_stage = 'early'  # Initialize the negotiation stage
        self.ufun = self.ufun.normalize()
        if self.opponent_ufun is None:
            raise ValueError("The opponent utility function is not set.")
        self.opponent_ufun1 = self.opponent_ufun.normalize()
        
        # print(self.ufun)
        # print(self.opponent_ufun)
        # assert False
        # print("Negotiation started. Utility functions normalized.")
        ###----From CARCAgent----####
        ufuns = (self.ufun, self.opponent_ufun1)
        outcomes = list(self.ufun.outcome_space.enumerate_or_sample())
        # print('outcomes:')
        # for i in outcomes:
        #     print(i,end=',')
        # print()
        # assert False
        frontier_utils, _ = pareto_frontier(ufuns, outcomes)
        # global static_cnt
        # static_cnt += 1
        # print(static_cnt,"ufuns" , ufuns)
        # print("outcomes" , outcomes)
        # print(static_cnt,"frontier_utils" , frontier_utils)
        # assert False
        # print('frontier_utils:')
        # for i in frontier_utils:
        #     print(i,end=',')
        # print()
        # assert False
        # print(f"Number of points in frontier_utils: {len(frontier_utils)}")  # 确认点的数量
        nash_point = nash_points(ufuns, frontier_utils)
        if nash_point:
            self._nash_util = nash_point[0][0][0]
            self._opponent_nash_util = nash_point[0][0][1]
        else:
            self._nash_util = (self.ufun.minmax()[0] + self.ufun.minmax()[1]) / 2.0
            self._opponent_nash_util = (self.opponent_ufun1.minmax()[0] + self.opponent_ufun1.minmax()[1]) / 2.0

        self.opponent_ufun1.reserved_value = self.ufun.reserved_value
        
        self.initialize_segments()

        # ####这个rational还需要调整，画图时暂时不采用###
        # self._rational = sorted(
        #         [
        #             (my_util, opp_util, _)
        #             for _ in self.nmi.outcome_space.enumerate_or_sample(
        #                 levels=10, max_cardinality=100_000
        #             ) 
        #             if (my_util := float(self.ufun(_))) >= max(self.ufun.reserved_value, self._nash_util * 0.8)
        #             and (opp_util := float(self.opponent_ufun(_))) <= max(self.opponent_ufun.reserved_value, self._opponent_nash_util) * 1.2
        #         ],
        #     )
        # ###----End: From CARCAgent----####
        # ###----画点图----####
      
        

        ### 获取并验证边界点
        # print("-----")
        # print(frontier_utils)
        # 确保 frontier_utils 包含所有帕累托前沿的点
        if len(frontier_utils[0]) != len(frontier_utils[1]):
            # print(len(frontier_utils[0]))
            # print(len(frontier_utils[1]))
            raise ValueError("frontier_utils 的 x 和 y 长度不匹配")

        # 将所有点打包成 tuple 列表
        
        # frontier_points = list(zip(frontier_utils[0], frontier_utils[1]))
        # frontier_points = list([[i[0] for i in frontier_utils],[i[1] for i in frontier_utils]])
        # 打印点的数量来确认是否正确
        # print(f"Number of points in frontier: {len(frontier_points[0])},{len(frontier_points[1])}")  # 确认点的数量

        # 对点进行排序，通常按 x 坐标排序
        sorted_frontier_points = sorted(frontier_utils, key=lambda p: p[0])

        # 解包 x 和 y 坐标
        x, y = list([[i[0] for i in sorted_frontier_points],[i[1] for i in sorted_frontier_points]])
        # print("x,y,.....")
        # print(x, y )

        # 获取理性点
         ### 处理所有outcomes点的绘制
        utility_A = []
        utility_B = []
        for outcome in outcomes:
            my_util = self.ufun(outcome)
            opp_util = self.opponent_ufun1(outcome)
            utility_A.append(my_util)
            utility_B.append(opp_util)

        # plt.clf()
        # # 绘制普通点（所有outcomes）
        # plt.scatter(utility_A, utility_B, label='Outcomes', alpha=0.6)

        # # 绘制帕累托前沿
        # plt.plot(x, y, label='Pareto Frontier', color='lime', linestyle='--')

        # # 绘制纳什点
        # plt.plot(self._nash_util, self._opponent_nash_util, 'o', label='Nash Point', color='red')
        

        # # 添加图例和显示图表
        # plt.legend()
        # plt.xlabel("Utility A")
        # plt.ylabel("Utility B")
        # plt.title("Utility Space with Pareto Frontier and Nash Point")

        # # 保存和显示图像
        # plt.savefig('scenarios_points_4.png')
        # plt.show()

        # ###----End：画点图----####

        return self.opponent_ufun1

        # # self.writer.write(f'{state.relative_time},on_negotiation_start,{self.ufun.best()}\n')
        # # self.writer.write(f'n_steps:{self.nmi.n_steps}\n')

    
    def initialize_segments(self, max_points_per_grid=0.01):
        """
        Discretize the negotiation space into segments and prepare for regret calculation.
        """
        # Sample the outcome space
        outcomes = self.enumerated_outcomes

        # Evaluate utility functions for both sides
        self.ufun_values = np.array([self.ufun(outcome) for outcome in outcomes])
        self.opponent_ufun_values = np.array([self.opponent_ufun1(outcome) for outcome in outcomes])

        # Determine the number of points in each grid
        total_points = len(outcomes)
        points_per_grid = int(total_points * max_points_per_grid)

        # Slice the utility values into grids
        sorted_indices = np.argsort(self.ufun_values)
        self.ufun_grid = np.array_split(sorted_indices, np.ceil(total_points / points_per_grid))

         # Calculate the average regret for each grid
        self.segment_regrets = self.calculate_average_regret()
        
        self.total_segments = len(self.ufun_grid)

        # Print statements for validation
        # print("Total points:", total_points)
        # print("Points per grid:", points_per_grid)
        # print("Number of grids:", len(self.ufun_grid))

        

        return self.ufun_grid
    # def action_abstraction(self,state , opponent_ufun1 , max_points_per_grid = 0.01):
    #     # Slice the utility function list to grid
    #     #  # Sample the outcome space
    #     outcome_space = self.nmi.outcome_space
    #     outcomes = outcome_space.enumerate_or_sample(levels=10, max_cardinality=100_000)

    #     # Evaluate utility functions for both sides
    #     ufun_values = np.array([self.ufun(outcome) for outcome in outcomes])
    #     # opponent_ufun_values = np.array([opponent_ufun1(outcome) for outcome in outcomes])
    #     # print('opponent_ufun:')
    #     # for i in opponent_ufun_values:
    #     #     print(i,end=',')
    #     # print()
    #     # assert False

    #     # Determine the number of points in each grid
    #     total_points = len(outcomes)
    #     points_per_grid = int(total_points * max_points_per_grid)
        

    #     # Slice the utility values into grids
    #     sorted_ufun_indices = np.argsort(ufun_values)
    #     # sorted_opponent_ufun_indices = np.argsort(opponent_ufun_values)
        
    #     ufun_grid = np.array_split(sorted_ufun_indices, np.ceil(total_points / points_per_grid))
    #     # opponent_ufun_grid = np.array_split(sorted_opponent_ufun_indices, np.ceil(total_points / points_per_grid))
        
    #     # Print statements for validation
    #     print("Total points:", total_points)
    #     print("Points per grid:", points_per_grid)
    #     print("Number of ufun grids:", len(ufun_grid))
    #     # print("Number of opponent ufun grids:", len(opponent_ufun_grid))

    #     # Print the ufun and opponent ufun values of the first grid 打印第一个grid的ufun
    #     # first_grid_indices = ufun_grid[0]
    #     # print("ufun values of the first grid:", ufun_values[first_grid_indices])
    #     # print("opponent ufun values of the first grid:", opponent_ufun_values[first_grid_indices])

    #     # print('ufun:')
    #     # for i in ufun_values:
    #     #     print(i,end=',')
    #     # print()

    #     ###验证被切分完成

    
    #     #return ufun_grid, opponent_ufun_grid
    #     return ufun_grid

    def calculate_average_regret(self):
        """
        Calculate the average regret for each segment based on the difference between expected utility and actual utility.
        """
        segment_regrets = []

        # print("Calculating average regrets for each segment...\n")
        for idx, grid in enumerate(self.ufun_grid):
            expected_utilities = self.get_expected_utility(grid)
            action_utilities = self.ufun_values[grid]

            # Calculate the regret for each point in the grid
            regrets = expected_utilities - action_utilities

            # Boost the regret for segments where the utility is higher than the Nash point
            nash_boost_factor = 3.0  # Factor to boost regret for segments with utility higher than Nash value
            if np.mean(action_utilities) > self._nash_util:
                regrets *= nash_boost_factor

            # Calculate the average regret for this grid
            average_regret = np.mean(regrets)
            segment_regrets.append(average_regret)

            # Print information for verification
            # print(f"Segment {idx+1}:") # 方便识别正在处理的段
            #print(f"  Expected Utilities: {expected_utilities}") # 期望效用:计算出的区段中所有点的期望效用
            #print(f"  Action Utilities: {action_utilities}")  # 动作效用:细分中提供的实际效用值
            #print(f"  Regrets: {regrets}") # 遗憾:计算每个点的遗憾。
            # print(f"  Average Regret: {average_regret}\n") #平均遗憾:该片段的最终平均遗憾

        return segment_regrets

    def get_expected_utility(self, grid):
        """
        Calculate the expected utility based on the negotiation stage.
        This function calculates U_expected based on Pareto optimality in the early stage,
        Nash Equilibrium utility in the mid-stage, and time-decayed utility in the late stage.
        """
        num_points = len(grid)
        # print(f"\nCalculating expected utilities for grid with {num_points} points...")

        expected_utilities = np.zeros(num_points)

        # Determine the expected utility based on the current negotiation stage
        if self.negotiation_stage == 'early':
            # Early Stage: Set all utilities to the maximum utility value
            expected_utilities.fill(max(self.ufun_values))
            # print(f"  [Early Stage] Setting expected utility to max value: {max(self.ufun_values)}")

        elif self.negotiation_stage == 'mid':
            # Mid Stage: Set all utilities to the Nash Equilibrium utility
            expected_utilities.fill(self._nash_util)
            # print(f"  [Mid Stage] Setting expected utility to Nash value: {self._nash_util}")

        return expected_utilities




    def assign_selection_probabilities(self, relative_time):
        """Step 2.2: Probability Distribution Based on Regret
        根据遗憾值分配选择每个分段的概率。
        遗憾值较低的分段应该有更高的选择概率。
        """
        
        early_stage_threshold = 0.95
        # print(self.segment_regrets)

        # 计算每个分段的正遗憾值
        positive_regrets = np.maximum(self.segment_regrets, 0)
        

        ### Add a verification
        # print("\nInitial positive regrets:", positive_regrets)




        # print("\nUpdated positive regrets after adjustment:", positive_regrets)
        # 计算正遗憾值的总和
        total_positive_regret = np.sum(positive_regrets)

        if total_positive_regret == 0:
            # 如果所有遗憾值都为非正数，则分配相等的概率
            selection_probabilities = np.ones(len(self.segment_regrets)) / len(self.segment_regrets)
        else:
            # 基于遗憾值计算初始选择概率
            selection_probabilities = positive_regrets / total_positive_regret

        # 反转选择概率：保持比例，但反转趋势
        selection_probabilities = np.max(selection_probabilities) - selection_probabilities

        # 确保反转后的选择概率没有负值
        selection_probabilities = np.maximum(selection_probabilities, 0)

        for idx in range(len(selection_probabilities)):
            if idx < (self.total_segments // 2):
                selection_probabilities[idx] = 0
        

        if self.opponent_tough:
             #     # We will consider the higher half of the segments, but still prioritize higher utilities
            max_utility = max(np.mean(self.ufun_values[self.ufun_grid[idx]]) for idx in range(len(self.ufun_grid)))
            min_utility = min(np.mean(self.ufun_values[self.ufun_grid[idx]]) for idx in range(len(self.ufun_grid)))
            for idx in range(len(self.ufun_grid)):
                if idx < (self.total_segments * 10 // 11): 
                    selection_probabilities[idx] = 0  # Ignore lower half segments
                else:
                    # Give segments with higher than Nash utility better weights
                    avg_segment_utility = np.mean(self.ufun_values[self.ufun_grid[idx]])
                    # normalized_utility = (avg_segment_utility - min_utility) / (max_utility - min_utility)
                    # selection_probabilities[idx] = normalized_utility


                    if avg_segment_utility > self._nash_util:
                        selection_probabilities[idx] *= 2  # Increase importance for utility > Nash
        else:
            # print("Early Stage: Ignoring segments with utility lower than Nash value.")
            highest_segment_index = None
            highest_segment_utility = float('-inf')
            # Set probability to 0 for segments where utility is below the Nash value
            for idx, grid in enumerate(self.ufun_grid):
                max_segment_utility = np.max(self.ufun_values[grid])
                # avg_segment_utility = np.mean(self.ufun_values[grid])
                if max_segment_utility > highest_segment_utility:
                    highest_segment_utility = max_segment_utility
                    highest_segment_index = idx
                ### Add a verification
                # print(f"Segment {idx+1} average utility: {avg_segment_utility}, Nash utility: {self._nash_util}")



                if relative_time < 0.8:
                    if max_segment_utility < max(self._nash_util, 0.95):
                        # print(f"Segment {idx+1} ignored (utility < Nash)")
                        selection_probabilities[idx] = 0  # Ignore segments with utility below Nash
                elif relative_time < 0.9:
                    if max_segment_utility < max(self._nash_util, 0.9):
                        # print(f"Segment {idx+1} ignored (utility < Nash)")
                        selection_probabilities[idx] = 0
                else :
                    if max_segment_utility < min(self._nash_util, 0.8):
                        # print(f"Segment {idx+1} ignored (utility < Nash)")
                        selection_probabilities[idx] = 0  # Ignore segments with utility below Nash

            
            if highest_segment_index is not None:
                selection_probabilities[highest_segment_index] = max(selection_probabilities[highest_segment_index], 1.0)
        ### Add a verification


        
       
        # 归一化选择概率以确保其和为1
        selection_probabilities /= np.sum(selection_probabilities)

        # 打印用于验证
        # for idx, prob in enumerate(selection_probabilities):
        #     print(f"Segment {idx+1}: Probability = {prob}")

        return selection_probabilities


    def analyze_concession(self, current_offer):
        """
        Analyze whether the opponent has made a concession and the level of the concession.
        A concession is defined as an offer with lower utility for the opponent than their previous offer.
        
        Parameters:
            current_offer: The current offer made by the opponent.
        
        Returns:
            concession_type: "rejection", "small_concession", or "significant_concession"
            concession_level: The magnitude of the concession (None if rejection).
        """
        if len(self.opponent_utilities) < 2:
            # If less than two offers exist, assume no concession
            # print("[INFO] No prior offers to compare. No concession detected.")
            return "no_prior_offers", None
        
        # Get the opponent's utility of the current offer
        current_opponent_utility = float(self.opponent_ufun1(current_offer))
        
        # Find the opponent's last utility (the utility of the last offer)
        last_opponent_utility = self.opponent_utilities[-2]  # The second to last utility (the most recent completed offer)
        
        # Print utilities for verification
        # print(f"[DEBUG] Last opponent utility: {last_opponent_utility}")
        # print(f"[DEBUG] Current opponent utility: {current_opponent_utility}")
        # Check if the opponent made a concession (i.e., current offer is worse for them)
        if current_opponent_utility < last_opponent_utility:
            # Calculate the concession level
            concession_level = last_opponent_utility - current_opponent_utility
            
            # Classify the concession as small or significant
            if concession_level < 0.1:  # You can adjust this threshold
                concession_type = "small_concession"
            else:
                concession_type = "significant_concession"
            # print(f"[INFO] Opponent made a {concession_type}. Concession level: {concession_level}")
            return concession_type, concession_level
        else:
            # No concession was made, hence it's a rejection or holding firm
            # print("[INFO] No concession detected. The opponent is holding firm.")
            return "rejection", None



    def dynamic_adjustment(self, concession_type):
        """
        Dynamically adjust the penalty factors α and β based on the negotiation progress
        or the opponent's behavior.
        
        Parameters:
            concession_type: The type of concession made by the opponent.
        
        Returns:
            alpha: Adjusted penalty factor for rejections.
            beta: Adjusted penalty factor for concessions.
        """
        base_alpha = 0.05  # Starting α value
        base_beta_small_concession = 0.1  # Starting β value for small concession
        base_beta_significant_concession = -0.1  # Starting β value for significant concession
        k = 0.1  # Scaling factor for α growth
        max_round = 100  # Maximum expected number of rounds (基于run里的session调整)

        # Dynamically adjust α using a logarithmic function to limit its growth
        alpha = base_alpha + (k * math.log(1 + self.negotiation_round) / math.log(1 + max_round))
        # print(f"[DEBUG] Dynamic adjustment of α: {alpha} (Negotiation round: {self.negotiation_round})")

        # Adjust β based on concession type
        if concession_type == "small_concession":
            beta = base_beta_small_concession  # Positive β for small concessions
        elif concession_type == "significant_concession":
            beta = base_beta_significant_concession  # Negative β for significant concessions
        else:
            beta = 0  # No concession (rejection) should not use β
        # print(f"[DEBUG] Dynamic adjustment of β: {beta} (Concession type: {concession_type})")

        return alpha, beta

    def update_and_adjust_regret(self, concession_type):
        """
        Update and adjust the regret for the current segment based on the opponent's behavior.
        
        Parameters:
            concession_type: The type of concession made by the opponent ("rejection", "small_concession", "significant_concession").
        """
        # Set default values for α and β
        alpha, beta = self.dynamic_adjustment(concession_type)

        # Print the current segment index for verification
        # print("--------current_segment-----")
        # print(self.current_segment)

        # Print the last_generated_offer for verification
        # print("--------last_generated_offer-----")
        # print(self.last_generated_offer)

        if self.last_generated_offer is None:
            # print("The fisrt offer")
            return
        


        if self.current_segment is None:
            # print("[ERROR] No segment index recorded for the current offer.")
            return

        

        # Get expected and action utilities for the current segment
        U_expected = self.get_expected_utility(self.current_segment)[0]
        U_action = self.ufun(self.last_generated_offer)
        # print(f"[DEBUG] Expected utility: {U_expected}, Action utility: {U_action}")
        utility_diff = U_expected - U_action  # Difference between expected and action utility

        # Determine the adjustment factor based on the concession type
        if concession_type == "rejection":
            # Increase regret significantly based on α
            adjustment_factor = alpha * utility_diff
            # print(f"[DEBUG] Rejection detected. Applying α penalty: {adjustment_factor}")
        elif concession_type == "small_concession":
            # Increase regret slightly based on β for small concession
            adjustment_factor = beta * utility_diff
            # print(f"[DEBUG] Small concession detected. Applying β penalty: {adjustment_factor}")
        elif concession_type == "significant_concession":
            # Decrease regret based on β for significant concession
            adjustment_factor = beta * utility_diff
            # print(f"[DEBUG] Significant concession detected. Applying β reduction: {adjustment_factor}")
        else:
            # Handle unexpected concession types by defaulting to no adjustment
            adjustment_factor = 0
            # print(f"[WARNING] Unexpected concession type: {concession_type}. No adjustment applied.")


        
        # Update the regret for the current segment
        self.segment_regrets[self.current_segment_index] += adjustment_factor

        # Ensure regret values remain within reasonable bounds (>= 0)
        self.segment_regrets[self.current_segment_index] = max(0, self.segment_regrets[self.current_segment_index])

        # Print updated regret for verification
        # print(f"[DEBUG] Updated regret for segment {self.current_segment_index}: {self.segment_regrets[self.current_segment_index]}")

        #self.selection_probabilities = self.assign_selection_probabilities()


    def calculate_upper_bound(self, segment):
        """
        Calculate the upper bound of the opponent's utility at the intersection
        of the given segment and the Pareto frontier.
        """
        # Get the indices for the current segment
        segment_indices = segment  # This contains the indices of your utility values for the segment

        # Initialize the upper bound
        upper_bound = None

        # Iterate through the outcomes corresponding to the segment indices
        for idx in segment_indices:
            outcome = self.ufun.outcome_space.enumerate_or_sample()[idx]
            opp_util = self.opponent_ufun1(outcome)

            # Check if this is the highest opponent utility within the segment
            if upper_bound is None or opp_util > upper_bound:
                upper_bound = opp_util

        if upper_bound is None or upper_bound == 0:
            # Print an error message and raise an exception or return a default value
            # print(f"[ERROR] No valid upper bound found for segment {segment}. Upper bound is {upper_bound}.")
            raise ValueError("No valid upper bound found in the current segment.")
        
        return upper_bound

    def sample_offer_from_segment(self, segment):

        
        """
        Sample an offer from the given segment using Importance Monte Carlo Sampling based on utilities.
        All points are considered, but those within the utility bounds have higher importance.
        
        Parameters:
            segment: The segment from which to sample an offer (list of outcome indices).
            lower_bound: The lower bound of the opponent's utility in this segment.
            upper_bound: The upper bound of the opponent's utility in this segment.
        
        Returns:
            The sampled offer within the segment, giving higher importance to outcomes within the bounds.
        """
        # List to hold all outcomes and their utilities for weighting

        valid_outcomes = [self.enumerated_outcomes[idx] for idx in segment]
        opp_util_values = [self.opponent_ufun1(outcome) for outcome in valid_outcomes]

        
        if not valid_outcomes:
            # print(f"[ERROR] No valid outcomes found in segment {segment}.")
            raise ValueError("No valid outcomes found in the current segment.")
        sorted_indices = np.argsort(opp_util_values)
        sorted_outcomes = [valid_outcomes[i] for i in sorted_indices]
        sorted_opp_utils = [opp_util_values[i] for i in sorted_indices]
        # Calculate the index for the top 30% cutoff
        num_outcomes = len(sorted_outcomes)
        top_30_cutoff = int(np.ceil(num_outcomes * 0.3))  # Select the top 30%

        # # Select the top 30% of the sorted outcomes
        top_outcomes = sorted_outcomes[-top_30_cutoff:]  # Select last 30%
        top_opp_utils = sorted_opp_utils[-top_30_cutoff]

        # Assign weights based on opponent utility (higher utility -> higher weight)
        # Example: exponentially increasing importance based on utility rank
        num_top_outcomes = len(top_outcomes)
        weights = np.array([1.2 ** i for i in range(num_top_outcomes)])  # Adjust the 1.2 factor to control the importance increase


        # num_outcomes = len(sorted_outcomes)
        # top_30_cutoff = int(np.ceil(num_outcomes * 0.3))  # Select up to 40%
        # top_10_cutoff = int(np.ceil(num_outcomes * 0.1))  # Select up to 20%

        # # Select the outcomes in the top 20-40% range
        # mid_top_outcomes = sorted_outcomes[top_10_cutoff:top_30_cutoff]
        # mid_top_opp_utils = sorted_opp_utils[top_10_cutoff:top_30_cutoff]
        # num_mid_top_outcomes = len(mid_top_outcomes)
        # weights = np.array([1.4 ** i for i in range(num_mid_top_outcomes)])  # Adjust the 1.2 factor to control the importance increase
        
        
        # Normalize weights to sum to 1
        total_weight = np.sum(weights)
        probabilities = weights / total_weight

        # Use weighted sampling to pick an outcome from the top 30%
        sampled_outcome = random.choices(top_outcomes, weights=probabilities, k=1)[0]

        return sampled_outcome




    
    def __call__(self, state):
        if not self.negotiation_started:
            self.opponent_ufun1 = self.on_negotiation_start(state)
            self.negotiation_started = True



        
        # self.ufun = self.ufun.normalize()
        # print(type(self.ufun))
        # assert False
        
        # # 如果谈判尚未开始，则调用 on_negotiation_start 方法
        # if not self.negotiation_started:
        #     cnt_start += 1
        #     if cnt_start > 1:
        #         print(self)
        #         assert False
        #     self.opponent_ufun1 = self.on_negotiation_start(state)
        #     if self.opponent_ufun1 is None:
        #         print('fuck')
        #         assert False
        #     self.negotiation_started = True
            #self.action_abstraction(state, self.opponent_ufun1)
        self.negotiation_round += 1



        
        
        # print(self.opponent_ufun1.reserved_value)
        # assert False

    
        # update the opponent reserved value in self.opponent_ufun
        # 更新对对手保留值的估计
        self.update_reserved_value(state.current_offer, state.relative_time)
        # run the acceptance strategy and if the offer received is acceptable, accept it
        # 检查当前的提议是否应该被接受
        # print(f"[VERIFICATION] All opponent utilities: {self.opponent_utilities}")

        # Analyze whether the opponent made a concession
        concession_type, concession_level = self.analyze_concession(state.current_offer)
        # Update and adjust regret based on the concession type
         # Update and adjust regret based on the concession type and the current segment
        if self.current_segment is not None:
            self.update_and_adjust_regret(concession_type)
        else:
            print("[WARNING] current_segment is None; skipping regret update.")
        if self.is_acceptable(state.current_offer, state.relative_time):
            return SAOResponse(ResponseType.ACCEPT_OFFER, state.current_offer)
        # call the offering strategy
        # 如果当前的报价是不可接受的，我们调用投标策略generate_offer()来生成一个新的报价
        final_offer = self.generate_offer(state, state.relative_time)
        # print('final_offer',final_offer)
        return SAOResponse(ResponseType.REJECT_OFFER, final_offer)

    def is_opponent_tough(self):
        if not self.opponent_utilities:
            return False  # No data yet
        max_utility = max(self.opponent_utilities)
        min_utility = min(self.opponent_utilities)
        utility_difference = max_utility - min_utility
        toughness_threshold = 0.05
        return utility_difference < toughness_threshold


    # Bidding Strategy 出价策略 （每次让步的策略）
    def generate_offer(self, state, relative_time) -> Outcome:
        time_checkpoints = [0.5, 0.6, 0.7, 0.8, 0.9]
        tolerance = 0.001
        if not self.opponent_tough :
            if any(abs(relative_time - checkpoint) < tolerance for checkpoint in time_checkpoints):
                if relative_time > self.last_checked_time:  # Make sure we don't repeat the check
                    self.opponent_tough = self.is_opponent_tough()
                    self.last_checked_time = relative_time  # Update the last checked time
                    if self.opponent_tough:
                        print("Tough opponent detected!")
                        # input("Press any key to continue")
        # print(self.opponent_ufun.reserved_value)

        # Analyze the opponent's current offer for concessions
        # print("----concession_type----")
        concession_type, concession_level = self.analyze_concession(state.current_offer)
        # print("----concession_type finish----")

        if concession_type == "significant_concession":
            # upper_bound = self.calculate_upper_bound(self.current_segment) -0.05 # Calculate based on the current segment
            # lower_bound = upper_bound - 0.3  # or 0.2 based on your preference
            # print("----sampled_outcome----")
            sampled_outcome = self.sample_offer_from_segment(self.current_segment)
            # print("----sampled_outcome finish----")
            # print(f"Sampled Outcome Utility from Current Segment: {sampled_outcome}")
            self.last_generated_offer = sampled_outcome
            return sampled_outcome


        # print("----assign_selection_probabilities----")

        # Assign selection probabilities
        selection_probabilities = self.assign_selection_probabilities(relative_time)

        # print("----assign_selection_probabilities finish----")

        # Choose a segment based on these probabilities
        chosen_segment_index = np.random.choice(len(self.ufun_grid), p=selection_probabilities)
        chosen_segment = self.ufun_grid[chosen_segment_index]

        # Record the segment index for future reference
        self.current_segment = chosen_segment
        self.current_segment_index = chosen_segment_index

        # print(f"Chosen Segment Index: {chosen_segment_index + 1}")
        # Calculate a new segment based on opponent's offer if no significant concession
        # upper_bound = self.calculate_upper_bound(chosen_segment) - 0.05
        # lower_bound = upper_bound - 0.3
        sampled_outcome = self.sample_offer_from_segment(chosen_segment )

        # print(f"Sampled Outcome Utility from New Segment: {sampled_outcome}")

        # Additional logic for handling the offer
        # if self.current_segment_index < (self.total_segments // 2):
        #     print("出价太低，重新计算")
        #     return self.generate_offer(state, relative_time)
        self.last_generated_offer = sampled_outcome

        return sampled_outcome


    def is_acceptable(self, offer, relative_time) -> bool:
        
        """The acceptance strategy"""
        if offer is None:
            return False
        offer_utility = float(self.ufun(offer))
    
        if self.opponent_tough:
            # Adjust threshold more strictly if the opponent is tough
            if relative_time > 0.985:
                return offer_utility > min(self._nash_util, 0.6)
            return offer_utility >= self._nash_util * 1.2
            
        else:
            # Regular acceptance logic
            if relative_time > 0.99:
                return offer_utility >= 0.5
            if relative_time > 0.9:
                return offer_utility >= self._nash_util * 1.3
            elif relative_time < 0.8:
                return offer_utility >= 0.95
            else:
                return offer_utility >= 0.8

    # Opponent Modeling 对手建模 （估算保留值）
    def update_reserved_value(self, offer, relative_time):
        """Learns the reserved value of the partner"""
        # 如果我们没有对手的报价，我们就无能为力了。就返回
        if offer is None:
            # self.writer.write(f'{relative_time},update_reserved_value,None\n')
            return
        # save to the list of utilities received from the opponent and their times
        # 我们将时间和对手的效用附加到对手提供效用的运行列表中
        self.opponent_utilities.append(float(self.opponent_ufun(offer)))
        self.opponent_times.append(relative_time)
        # Use curve fitting to estimate the opponent reserved value 使用曲线拟合来估计对手保留值
        # We assume the following: 我们假设如下：
        # - The opponent is using a concession strategy with an exponent between 0.2, 5.0 - 对手正在使用指数在 0.2, 5.0 之间的让步策略 这是基于时间的策略通常使用的指数范围。
        # - The opponent never offers outcomes lower than their reserved value which means - 对手永远不会提供低于其保留值的结果，这意味着
        #   that their rv must be no higher than the worst outcome they offered for themselves. 他们的 rv 必须不高于他们为自己提供的最坏结果。
        # curve_fit参数：f函数，xdate自变量,ydata因变量,bounds 参数范围
        bounds = ((0.2, 0.0), (5.0, min(self.opponent_utilities)))
        try:
            optimal_vals, _ = curve_fit(
                lambda x, e, rv: aspiration_function(
                    x, self.opponent_utilities[0], rv, e
                ),
                self.opponent_times,
                self.opponent_utilities,
                bounds=bounds,
            )
            # 我们用新的估计值更新对手的保留值，为以后保留最新的值
            self._past_oppnent_rv = self.opponent_ufun.reserved_value
            # self.writer.write(f'{relative_time},update_reserved_value,{self._past_oppnent_rv}\n')
            self.opponent_ufun.reserved_value = optimal_vals[1]
            # print(optimal_vals)
        except Exception as e:
            pass

