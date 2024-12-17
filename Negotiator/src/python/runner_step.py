import json
import time  # Import the time module
import math
import numpy as np
from pathlib import Path
from negmas.gb.negotiators.timebased import (
    BoulwareTBNegotiator,
    ConcederTBNegotiator,
    LinearTBNegotiator,
)
import pandas as pd
# from Abstraction.action_abstraction_1006 import AANegotiatior
# from Abstraction.micro import MiCRO
# from Abstraction.nash_seeker import NashSeeker
import negmas
import matplotlib.pyplot as plt
import os, sys
import csv

from action_abstraction_1006 import AANegotiatior
from micro import MiCRO
from nash_seeker import NashSeeker



# from Abstraction.em import *
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)
# os.chdir("..")
# print(currentdir)
# assert False

import negmas
from pathlib import Path
import json
from multiprocessing import Pool
import re
# from negmas.genius.gnegotiators import Atlas3, AgentK , AgentGG, MetaAgent , CUHKAgent
from negmas.sao.negotiators import AspirationNegotiator
from negmas.genius.gnegotiators import BoulwareNegotiationParty
from negmas.genius.gnegotiators import GeniusNegotiator
from negmas import Outcome, ResponseType


import multiprocessing



class NegotiationRunner:
    def __init__(self, base_path, domain_name, our_name, opp_name, our_agent, opp_agent, output_folder, time_limit=10, n_steps=1000):
        self.base_path = base_path
        self.domain_name = domain_name
        self.output_folder = output_folder
        self.our_name = our_name
        self.opp_name = opp_name
        self.our_agent = our_agent
        self.opp_agent = opp_agent
        self.time_limit = time_limit
        self.n_steps = n_steps
        self.session = None
        self.ufun_a = None
        self.ufun_b = None

        # 信号处理函数映射
        # 信号处理函数映射
        self.signal_handlers = {
            1: self.initialize_session,  # 信号 1: 初始化谈判
            2: self.reset_session,  # 信号 2: 重置谈判
            3: self.handle_recommendation_and_history,  # 信号 3: 推荐报价和历史
            4: self.handle_offer_submission,  # 信号 4: 用户提交提议
            5: self.handle_offer_acceptance,  # 信号 5: 接受提议
            6: self.handle_termination,  # 信号 6: 用户终止谈判
            7: self.handle_timeout,  # 信号 7: 超时处理
            10: self.run_automation_process,  # 信号 10: 自动化谈判流程
        }



    def initialize_session(self, profile_a, profile_b, weight_a, weight_b):
        """
        初始化会话，并根据用户和对手配置完成设置。
        """
        print(f"[DEBUG] 初始化谈判会话: {self.domain_name}, 用户: {self.our_name}, 对手: {self.opp_name}")

        # 获取对手类型映射
        json_file_path = Path(__file__).parent / 'opponents_genius.json'
        if not json_file_path.exists():
            raise FileNotFoundError(f"[ERROR] 对手映射文件 {json_file_path} 不存在。")

        with json_file_path.open(mode='r') as file:
            opponents_list = json.load(file)
        opponents_mapping = {item[0]: item[1] for item in opponents_list}

        # 计算策略
        bid_strategy, acceptance_strategy, opponent_agent = self.get_negotiation_strategies(profile_a, profile_b)

        # 配置领域路径和效用函数
        domain_path = Path(self.base_path) / self.domain_name
        profile_a_path = domain_path / "profileA.json"
        profile_b_path = domain_path / "profileB.json"

        with open(profile_a_path, "r") as f:
            profile_a_data = json.load(f)["LinearAdditiveUtilitySpace"]
        with open(profile_b_path, "r") as f:
            profile_b_data = json.load(f)["LinearAdditiveUtilitySpace"]

        issues = [negmas.make_issue(name=k, values=v["values"]) for k, v in profile_a_data["domain"]["issuesValues"].items()]
        ufun_a_values = {k: v["DiscreteValueSetUtilities"]["valueUtilities"] for k, v in profile_a_data["issueUtilities"].items()}
        ufun_b_values = {k: v["DiscreteValueSetUtilities"]["valueUtilities"] for k, v in profile_b_data["issueUtilities"].items()}

        self.ufun_a = negmas.LinearUtilityAggregationFunction(values=ufun_a_values, weights=weight_a, issues=issues)
        self.ufun_b = negmas.LinearUtilityAggregationFunction(values=ufun_b_values, weights=weight_b, issues=issues)
        print("-----------------++++++++++++++++------------------")
        print(self.ufun_a)
        print("-----------------++++++++++++++++------------------")
        print(self.ufun_b)



        # 初始化会话
        self.session = negmas.SAOMechanism(issues=issues, n_steps=self.n_steps)
        # self.session = negmas.SAOMechanism(issues=issues, time_limit=self.time_limit, n_steps=self.n_steps)

        # 配置我们的智能体
        our_agent_instance = AANegotiatior(name=self.our_name, private_info={"opponent_ufun": self.ufun_b})

        # 配置对手智能体
        if opponent_agent in ["AANegotiator", "MiCRO"]:
            if opponent_agent == "AANegotiator":
                opp_agent_instance = AANegotiatior(name=self.opp_name, private_info={"opponent_ufun": self.ufun_a})
            elif opponent_agent == "MiCRO":
                opp_agent_instance = MiCRO(name=self.opp_name, private_info={"opponent_ufun": self.ufun_a})
        else:
            # 从映射中获取对手的 Java 类
            java_class_name = opponents_mapping.get(opponent_agent)
            if not java_class_name:
                raise ValueError(f"[ERROR] 对手类型 {opponent_agent} 未在映射文件中找到。")
            print(opponent_agent)
            print(java_class_name)
            opp_agent_instance = negmas.genius.GeniusNegotiator(name=self.opp_name, java_class_name=java_class_name)
            

        # 添加智能体到会话
        self.session.add(our_agent_instance, preferences=self.ufun_a)
        self.session.add(opp_agent_instance, preferences=self.ufun_b)

        print("[DEBUG] 谈判设置完成，智能体已加入会话。")

    def reset_session(self):
        """
        重置谈判会话。
        """
        print("[DEBUG] 重置谈判会话。")
        self.session = None
        self.ufun_a = None
        self.ufun_b = None

    def get_negotiation_strategies(self, profile_a, profile_b):
        """
        根据用户和对手配置计算策略。
        """
        # 出价策略类型
        if profile_a[0] >= 1 and profile_a[1] <= 0 and profile_a[2] >= 0 and profile_a[3] >= 0:
            bid_strategy = [1, "优化个人效用值 (Personal Utility Value)"]
        elif profile_a[0] >= 1 and profile_a[1] >= 0 and profile_a[2] >= -1 and profile_a[3] >= -1:
            bid_strategy = [2, "趋近纳什均衡点 (Nash Equilibrium Point)"]
        elif profile_a[0] <= 0 and profile_a[1] >= 1:
            bid_strategy = [3, "趋近双赢 (Social Welfare)"]
        else:
            bid_strategy = [3, "趋近双赢 (Social Welfare)"]

        # 接受策略类型
        if profile_a[1] > 0 and profile_a[4] > 0:
            acceptance_strategy = [1, "保守型 (Conservative)"]
        else:
            acceptance_strategy = [2, "强硬型 (Hardline)"]


        # opponent_agent = "MiCRO"
        # # 对手智能体类型
        if profile_b[0] >= 1 and profile_b[1] <= 0:
            opponent_agent = "Atlas3"
        elif profile_b[0] >= 1:
            opponent_agent = "PonPokoAgent"
        elif profile_b[1] >= 1 and profile_b[2] >= 1:
            opponent_agent = "AgreeableAgent2018"
        elif profile_b[3] >= 1:
            opponent_agent = "Caduceus"
        elif profile_b[4] >= 1:
            opponent_agent = "KakeSoba"
        else:
            opponent_agent = "Atlas3"

        return bid_strategy, acceptance_strategy, opponent_agent

    def add_agents(self):
        """添加谈判代理到会话。"""
        if self.our_agent == 'AANegotiatior':
            our_agent_instance = AANegotiatior(name=self.our_name, private_info={'opponent_ufun': self.ufun_b})
        else:
            raise NotImplementedError(f"Agent {self.our_agent} not implemented")

        if self.opp_agent == 'MiCRO':
            opp_agent_instance = MiCRO(name=self.opp_name, private_info={'opponent_ufun': self.ufun_a})
        else:
            raise NotImplementedError(f"Agent {self.opp_agent} not implemented")

        self.session.add(our_agent_instance, preferences=self.ufun_a)
        self.session.add(opp_agent_instance, preferences=self.ufun_b)
    
    

    def calculate_pareto_distance(self, agreement_utility, pareto_frontier):
        """
        Calculate the minimum Euclidean distance between the agreement utility
        and the Pareto frontier.
        """
        pareto_distance = float("inf")
        for pareto_point in pareto_frontier:
            dist = math.sqrt((pareto_point[0] - agreement_utility[0]) ** 2 +
                            (pareto_point[1] - agreement_utility[1]) ** 2)
            if dist < pareto_distance:
                pareto_distance = dist
        return pareto_distance



    def calculate_nash_distance(self, agreement_utility, nash_point):
        """
        Calculate the Euclidean distance between the agreement utility
        and the Nash point. Handles nested structures in nash_point.
        """
        # 提取 nash_point 的实际数值（去除嵌套结构）
        if isinstance(nash_point, (list, tuple)) and isinstance(nash_point[0], (list, tuple)):
            nash_point = nash_point[0]  # 取出嵌套的第一层
        elif isinstance(nash_point, (list, tuple)) and len(nash_point) == 2:
            pass  # 正常的 (x, y) 结构
        else:
            raise ValueError(f"Unexpected Nash point structure: {nash_point}")

        # 计算欧几里得距离
        nash_distance = math.sqrt((nash_point[0] - agreement_utility[0]) ** 2 +
                                (nash_point[1] - agreement_utility[1]) ** 2)
        return nash_distance






    def calculate_distances(self, session, agreement, ufun_a, ufun_b):
        """
        Calculate Pareto and Nash distances for a negotiation session.
        If no agreement is reached, distances are calculated from (0,0).
        """
        # If agreement exists, calculate utilities; otherwise default to (0, 0)
        if agreement:
            agreement_utility = [ufun_a(agreement), ufun_b(agreement)]
        else:
            agreement_utility = [0, 0]

        # Calculate Pareto distance
        pareto_frontier = session.pareto_frontier(max_cardinality=float('inf'), sort_by_welfare=True)[0]
        pareto_distance = self.calculate_pareto_distance(agreement_utility, pareto_frontier)

        # Calculate Nash distance
        nash_points = session.nash_points(max_cardinality=float('inf'))
        nash_point = nash_points[0] if nash_points else [0, 0]
        nash_distance = self.calculate_nash_distance(agreement_utility, nash_point)

        return pareto_distance, nash_distance


    # def handle_signal(self, signal_id, **kwargs):
    #     """
    #     主信号处理器，带调试信息
    #     """
    #     print(f"[DEBUG] 收到信号 ID: {signal_id}")
    #     try:
    #         if signal_id not in self.signal_handlers:
    #             raise ValueError(f"未知信号 ID: {signal_id}")
            
    #         # 获取当前会话状态
    #         state = self.session.state
    #         print(f"[DEBUG] 当前状态: {state}")

    #         # 调用信号处理器
    #         return self.signal_handlers[signal_id](state=state, **kwargs)  # 显式传递 state
    #     except Exception as e:
    #         print(f"[ERROR] 处理信号时出错: {e}")
    #         raise

    def handle_signal(self, signal_id, **kwargs):
        """
        主信号处理器，带调试信息
        """
        print(f"[DEBUG] 收到信号 ID: {signal_id}")
        try:
            if signal_id not in self.signal_handlers:
                raise ValueError(f"未知信号 ID: {signal_id}")

            # 初始化信号不需要检查 session
            if signal_id == 1:
                return self.signal_handlers[signal_id](**kwargs)

            # 其他信号需要检查 session 是否已初始化
            if not self.session:
                raise ValueError("[ERROR] 谈判会话未初始化。请先发送信号 1 初始化谈判会话。")

            # 获取当前会话状态
            state = self.session.state

            # 获取信号处理函数
            handler = self.signal_handlers[signal_id]

            # 动态解析函数参数需求
            handler_params = handler.__code__.co_varnames
            call_args = {}

            # 如果需要 state 参数
            if 'state' in handler_params:
                call_args['state'] = state

            # 如果需要 session 参数
            if 'session' in handler_params:
                call_args['session'] = self.session

            # 添加额外的 kwargs
            call_args.update(kwargs)

            # 调用信号处理函数
            return handler(**call_args)
        except Exception as e:
            print(f"[ERROR] 处理信号时出错: {e}")
            raise





    def handle_recommendation_and_history(self, state, **kwargs):
        """
        Signal 3: 推荐报价和历史分析
        """
        print(f"[DEBUG] 正在处理推荐报价和历史 (Signal 3)...")
        
        # 获取我方智能体实例
        our_agent = next(
            (neg for neg in self.session.negotiators if neg.name == self.our_name),
            None
        )
        if not our_agent:
            raise ValueError(f"无法找到我方智能体: {self.our_name}")
        
        # 调用智能体的 __call__ 方法
        response = our_agent(state)
        if response.response == ResponseType.ACCEPT_OFFER:
            print("[INFO] 推荐接受当前报价")
        elif response.response == ResponseType.REJECT_OFFER:
            print(f"[INFO] 推荐的报价: {response.outcome}")
        elif response.response == ResponseType.END_NEGOTIATION:
            print("[INFO] 推荐结束谈判")
        
        history = self.session.trace  # 获取谈判历史

        print(f"[DEBUG] 历史记录长度: {len(history)}")
        
        return {
            "response": response,
            "history": history
        }



    # def handle_offer_submission(self, session, user_offer, **kwargs):
    #     """
    #     Signal 4: 用户提交新的提议，触发对手的响应
    #     输入:
    #     - session: 当前谈判的 session 对象
    #     - user_offer: 用户提出的具体提议，格式与 response.outcome 相同
    #     返回:
    #     - response: 对手的反馈（如 accept/reject/counter）
    #     - next_offer: 对手的反提议（如有）
    #     - session_state: 当前谈判的状态，包括当前提议和轮次
    #     - full_trace: 更新后的完整历史
    #     """
    #     print(f"[DEBUG] Signal 4: 用户提交提议 -> {user_offer}")

    #     # Step 1: 将用户的提议作为输入传递到 session 的 step 方法
    #     action = {self.our_name: negmas.SAOResponse(ResponseType.REJECT_OFFER, user_offer)}
    #     print(session)
    #     print("---")
    #     step_result = session.step(action)  # 执行当前轮次
        
    #     # Step 2: 提取对手的响应和反提议
    #     current_state = step_result.state
    #     response_type = step_result.state.responses.get(self.opp_name, None)
    #     next_offer = current_state.current_offer if response_type == ResponseType.COUNTER_OFFER else None

    #     # Step 3: 获取完整历史记录
    #     full_trace = session.full_trace

    #     # Step 4: 返回结构化数据
    #     return {
    #         "response": response_type.name.lower() if response_type else "no_response",
    #         "next_offer": next_offer,
    #         "session_state": {
    #             "step": current_state.step,
    #             "current_offer": current_state.current_offer,
    #             "current_proposer": current_state.current_proposer,
    #         },
    #         "full_trace": full_trace,
    #     }


    # def handle_offer_submission(self, session, user_offer, **kwargs):
    #     if not isinstance(session, negmas.SAOMechanism):
    #         raise ValueError("[ERROR] session 必须是 SAOMechanism 的实例")

    #     # 将用户提议作为当前的 action 提交
    #     action = {self.our_name: negmas.SAOResponse(ResponseType.REJECT_OFFER, user_offer)}
    #     # action = {
    #     #     self.our_name: negmas.SAOResponse(
    #     #         response=ResponseType.REJECT_OFFER,
    #     #         outcome= ('Hospitality', 'Nightlife and entertainment', 'International cuisine', 'Small boutiques', 'Music hall', 'Hiking', 'Parks and Gardens')
    #     #     )
    #     # }
    #     # 调用 session.step() 执行当前轮次
    #     print('kingking----')
    #     print(session.state)
        
    #     # assert False
        
        
    #     step_result = session.step(action)
    #     print(step_result)
    #     print("****413---")

    #     # 调用对手的 response
    #     opponent_response = session.step()  # 对手的响应
    #     print(opponent_response)
    #     print("---")
    #     next_offer = opponent_response.current_offer


    #     # 返回完整结果
    #     return {
            
    #         "next_offer": next_offer,
            
    #         "full_trace": session.full_trace,
    #     }

    def handle_offer_submission(self, session, user_offer, **kwargs):
        if not isinstance(session, negmas.SAOMechanism):
            raise ValueError("[ERROR] session 必须是 SAOMechanism 的实例")

        # 将用户提议作为当前的 action 提交
        action = {
            self.our_name: negmas.SAOResponse(
                response=ResponseType.REJECT_OFFER,
                outcome=user_offer
            )
        }

        # 调用 session.step() 执行当前轮次
        print("[DEBUG] 提交用户提议...")
        step_result = session.step(action)

        # 获取当前的谈判状态
        current_state = session.state
        print("[DEBUG] 对手响应: ", current_state)

        # 提取对手的最新提议
        next_offer = current_state.current_offer

        # 判断对手的响应状态
        if current_state.broken:
            response_type = ResponseType.END_NEGOTIATION
            print("[INFO] 对手选择终止谈判。")
        elif current_state.timedout:
            response_type = ResponseType.NO_RESPONSE
            print("[INFO] 谈判超时。")
        elif current_state.agreement:
            response_type = ResponseType.ACCEPT_OFFER
            print("[INFO] 双方达成一致，谈判结束。")
        else:
            response_type = ResponseType.REJECT_OFFER
            print("[INFO] 对手拒绝了提议，并提出新提议。", next_offer)

        # 返回完整结果
        return {
            "response": response_type,
            "next_offer": next_offer,
            "full_trace": session.full_trace,
        }

    
    def handle_offer_acceptance(self, session, **kwargs):
        """
        Signal 5: 用户接受当前提议
        """
        print("[DEBUG] 用户接受当前提议 (Signal 5)...")

        # 生成 ACCEPT_OFFER 的 action
        agreement = self.session.state.current_offer
        self.session.state.running = False  # 结束谈判
        session.state.agreement = agreement
        
        self_ufun_agreement = self.ufun_a(agreement) if agreement else 0
        opp_ufun_agreement = self.ufun_b(agreement) if agreement else 0

        pareto_distance, nash_distance = self.calculate_distances(
            self.session, agreement, self.ufun_a, self.ufun_b
        )

        result = {
            'self_agent': self.our_name,
            'opp_agent': self.opp_name,
            'agreement': agreement,
            'self_ufun_agreement': self_ufun_agreement,
            'opp_ufun_agreement': opp_ufun_agreement,
            'number_of_steps': len(self.session.trace),
            'total_social_welfare': self_ufun_agreement + opp_ufun_agreement,
            'pareto_distance': pareto_distance,
            'nash_distance': nash_distance,
        }

        # 保存结果、谈判历史和图表
        return self.save_results_to_csv(self.session, result)

    def handle_termination(self):
        """
        Signal 6: 用户终止谈判
        """
        print("[DEBUG] 用户终止谈判 (Signal 6)...")
        self.session.state.running = False  # 设置谈判为非运行状态
        self.session.state.broken = True  # 标记谈判被中断

        # 没有达成协议时设置默认值
        agreement = None
        self_ufun_agreement = 0
        opp_ufun_agreement = 0

        result = {
            'self_agent': self.our_name,
            'opp_agent': self.opp_name,
            'agreement': agreement,
            'self_ufun_agreement': self_ufun_agreement,
            'opp_ufun_agreement': opp_ufun_agreement,
            'number_of_steps': len(self.session.trace),
        }

        # 保存结果
        return self.save_results_to_csv(self.session, result)



    def handle_timeout(self):
        """处理信号7：超时结束。"""
        return {'status': 'timeout', 'final_offer': self.session.state.current_offer}

    import csv

    def save_results_to_csv(self, session, result):
        """
        保存谈判结果到CSV文件，并计算Pareto和Nash距离。
        """
        # 获取Pareto前沿和Nash点
        pareto_frontier = session.pareto_frontier(max_cardinality=float('inf'), sort_by_welfare=True)[0]
        nash_point_raw = session.nash_points(max_cardinality=float('inf'))
        nash_point = nash_point_raw[0] if nash_point_raw else [0, 0]

        # 获取效用值
        agreement_utility = [result['self_ufun_agreement'], result['opp_ufun_agreement']]

        # 计算距离
        pareto_distance = self.calculate_pareto_distance(agreement_utility, pareto_frontier)
        nash_distance = self.calculate_nash_distance(agreement_utility, nash_point)

        # 更新结果
        result.update({
            'pareto_distance': pareto_distance,
            'nash_distance': nash_distance
        })

        # 输出CSV文件
        csv_file = Path(self.output_folder) / f"{self.domain_name}_{self.our_name}_vs_{self.opp_name}_results.csv"
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=result.keys())
            writer.writeheader()
            writer.writerow(result)

        # 保存图表
        figures_folder = Path(self.output_folder) / "figures"
        figures_folder.mkdir(parents=True, exist_ok=True)
        figure_path = figures_folder / f'bidding_history_{self.domain_name}_{self.our_name}_vs_{self.opp_name}.png'
        session.plot(ylimits=(0.0, 1.01), show_agreement=True)
        plt.savefig(figure_path)
        plt.close()

        print(f"[INFO] 结果和图表已保存到: {csv_file}, {figure_path}")
        return result






    def run_automation_process(self):
        """处理信号10：自动运行整个谈判流程，并计算关键结果指标。"""
        self.session.run()

        agreement = self.session.state.agreement
        self_ufun_agreement = self.ufun_a(agreement) if agreement else 0
        opp_ufun_agreement = self.ufun_b(agreement) if agreement else 0

        pareto_distance, nash_distance = self.calculate_distances(self.session, agreement, self.ufun_a, self.ufun_b)

        result = {
            'self_agent': self.our_name,
            'opp_agent': self.opp_name,
            'agreement': agreement,
            'self_ufun_agreement': self_ufun_agreement,
            'opp_ufun_agreement': opp_ufun_agreement,
            'number_of_steps': len(self.session.trace),
            'total_social_welfare': self_ufun_agreement + opp_ufun_agreement,
            'pareto_distance': pareto_distance,
            'nash_distance': nash_distance,
        }

            # 将 `trace` 直接保存到文件
        trace_data = self.session.trace

        # 创建输出文件夹
        output_path = Path(self.output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存结果到 CSV 文件
        result_file = output_path / f'{self.domain_name}_{self.our_name}_vs_{self.opp_name}_final_result.csv'
        pd.DataFrame([result]).to_csv(result_file, index=False)

        # 保存谈判过程到 JSON 文件
        trace_file = output_path / f'{self.domain_name}_{self.our_name}_vs_{self.opp_name}_trace.json'
        with trace_file.open(mode='w', encoding='utf-8') as f:
            json.dump(trace_data, f, ensure_ascii=False, indent=4)
        # 生成谈判历史图表
        figures_folder = output_path / "figures"
        figures_folder.mkdir(parents=True, exist_ok=True)

        figure_path = figures_folder / f'bidding_history_{self.domain_name}_{self.our_name}_vs_{self.opp_name}.png'
        self.session.plot(
            ylimits=(0.0, 1.01),
            show_reserved=False,
            mark_max_welfare_points=False,
            show_agreement=True
        )
        plt.savefig(figure_path)
        plt.close()  # 关闭图表以释放内存

        print(f"[INFO] 图表已保存到: {figure_path}")

        return result, trace_file


if __name__ == "__main__":
    base_path = "/root/AANegotiator/Abstraction/scenarios/scenarios/specials"
    domain_name = "travel_domain_hOhD"
    output_folder = "/root/AANegotiator/Abstraction/Results1213_test"
    our_name = "AgentA"
    opp_name = "AgentB"
    time_limit = 180
    n_steps = 1000
    profile_a = [1, 0, 1, -1, 0]
    profile_b = [-1,2,-2,-2,-2]
    weight_a = [0.1, 0.1, 0.1, 0.1,0.2,0.2,0.2]
    weight_b = [0.1, 0.1, 0.1, 0.1,0.2,0.2,0.2]

    # 实例化 NegotiationRunner
    runner = NegotiationRunner(base_path, domain_name, our_name, opp_name, "AANegotiatior", "MiCRO", output_folder, time_limit, n_steps)

    # 初始化会话
    runner.handle_signal(1, profile_a=profile_a, profile_b=profile_b, weight_a=weight_a, weight_b=weight_b)
    
    # 处理其他信号
    print(runner.handle_signal(3))  # 推荐报价和历史
    # runner.handle_signal(4, user_offer=('10%', 'Division D', '100%', '100%', '$38,000'))

    runner.handle_signal(4, user_offer=('Political stability', 'Nightlife and entertainment', 'International cuisine', 'Shopping malls', 'Theater', 'Bike tours', 'Palace'))

    # runner.handle_signal(5)
    runner.handle_signal(6)

