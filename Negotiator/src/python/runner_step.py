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
        self.signal_handlers = {
            3: self.handle_recommendation_and_history,
            4: self.handle_offer_submission,
            5: self.handle_offer_acceptance,
            6: self.handle_termination,
            7: self.handle_timeout,
            8: self.handle_opponent_acceptance,
            9: self.handle_opponent_termination,
            10: self.run_automation_process,
        }

    def initialize_session(self):
        """初始化谈判会话和效用函数。"""
        domain_path = Path(self.base_path) / self.domain_name
        profile_a_path = domain_path / 'profileA.json'
        profile_b_path = domain_path / 'profileB.json'

        with open(profile_a_path, 'r') as f:
            profile_a_data = json.load(f)['LinearAdditiveUtilitySpace']
        with open(profile_b_path, 'r') as f:
            profile_b_data = json.load(f)['LinearAdditiveUtilitySpace']

        issues = [negmas.make_issue(name=k, values=v['values']) for k, v in profile_a_data['domain']['issuesValues'].items()]
        ufun_a_values = {k: v['DiscreteValueSetUtilities']['valueUtilities'] for k, v in profile_a_data['issueUtilities'].items()}
        ufun_b_values = {k: v['DiscreteValueSetUtilities']['valueUtilities'] for k, v in profile_b_data['issueUtilities'].items()}

        self.ufun_a = negmas.LinearUtilityAggregationFunction(values=ufun_a_values, weights=profile_a_data['issueWeights'], issues=issues)
        self.ufun_b = negmas.LinearUtilityAggregationFunction(values=ufun_b_values, weights=profile_b_data['issueWeights'], issues=issues)
        
        self.session = negmas.SAOMechanism(issues=issues, time_limit=self.time_limit, n_steps=self.n_steps)

        # 添加代理
        self.add_agents()
        return self.session

    def add_agents(self):
        """添加谈判代理到会话。"""
        if self.our_agent == 'AANegotiatior':
            our_agent_instance = AANegotiatior(name=self.our_name, private_info={'opponent_ufun': self.ufun_b})
            # our_agent_instance = None
        else:
            raise NotImplementedError(f"Agent {self.our_agent} not implemented")

        if self.opp_agent == 'MiCRO':
            opp_agent_instance = MiCRO(name=self.opp_name, private_info={'opponent_ufun': self.ufun_a})
            # opp_agent_instance = None
        else:
            raise NotImplementedError(f"Agent {self.opp_agent} not implemented")

        self.session.add(our_agent_instance, preferences=self.ufun_a)
        self.session.add(opp_agent_instance, preferences=self.ufun_b)
    
    

    def calculate_pareto_distance(agreement_utility, pareto_frontier, ufuns):
        """
        Calculate the minimum Euclidean distance between the agreement utility
        and the Pareto frontier.
        """
        pareto_distance = float("inf")
        cu = agreement_utility

        for pu in pareto_frontier:
            dist = math.sqrt(sum((pu_val - cu_val) ** 2 for pu_val, cu_val in zip(pu, cu)))
            pareto_distance = min(pareto_distance, dist)

        return pareto_distance


    def calculate_nash_distance(agreement_utility, nash_point, ufuns):
        """
        Calculate the Euclidean distance between the agreement utility
        and the Nash point, ensuring correct structure.
        """
        # 解包 nash_point 并提取实际的效用值
        if isinstance(nash_point, list) or isinstance(nash_point, tuple):
            # 提取 Nash 点中实际的效用值（假设为元组的第一个元素）
            nash_point_values = nash_point[0][0] if isinstance(nash_point[0], tuple) else nash_point[0]
        else:
            raise ValueError(f"无法解析 nash_point 的结构: {nash_point}")

        # 检查结构是否匹配
        if not isinstance(nash_point_values, (tuple, list)) or len(nash_point_values) != len(agreement_utility):
            raise ValueError(f"nash_point 和 agreement_utility 结构不匹配: nash_point={nash_point}, agreement_utility={agreement_utility}")

        # 计算欧几里得距离
        dist = math.sqrt(sum((np_val - cu_val) ** 2 for np_val, cu_val in zip(nash_point_values, agreement_utility)))
        return dist
    def calculate_distances(self,session, agreement, ufun_a, ufun_b):
        """
        Calculate Pareto and Nash distances for a negotiation session.
        """
        # 确保 agreement 不为 None
        if agreement is None:
            return float("inf"), float("inf")

        # 获取 agreement 的效用值
        agreement_utility = [ufun_a(agreement), ufun_b(agreement)]

        # 计算 Pareto 距离
        pareto_frontier = session.pareto_frontier(max_cardinality=float('inf'), sort_by_welfare=True)
        # pareto_distance = calculate_pareto_distance(agreement_utility, pareto_frontier[0], [ufun_a, ufun_b])
        pareto_distance = None

        # 计算 Nash 距离
        nash_point = session.nash_points(max_cardinality=float('inf'))
        if nash_point:
            # nash_distance = calculate_nash_distance(agreement_utility, nash_point, [ufun_a, ufun_b])
            nash_distance = None
        else:
            nash_distance = float("inf")

        return pareto_distance, nash_distance

    def handle_signal(self, signal_id, **kwargs):
        """
        主信号处理器，带调试信息
        """
        print(f"[DEBUG] 收到信号 ID: {signal_id}")
        try:
            if signal_id not in self.signal_handlers:
                raise ValueError(f"未知信号 ID: {signal_id}")
            
            # 获取当前会话状态
            state = self.session.state
            print(f"[DEBUG] 当前状态: {state}")

            # 调用信号处理器
            return self.signal_handlers[signal_id](state=state, **kwargs)  # 显式传递 state
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


    def handle_offer_submission(self, session, user_offer, **kwargs):
        if not isinstance(session, negmas.SAOMechanism):
            raise ValueError("[ERROR] session 必须是 SAOMechanism 的实例")

        # 将用户提议作为当前的 action 提交
        action = {self.our_name: negmas.SAOResponse(ResponseType.REJECT_OFFER, user_offer)}

        # 调用 session.step() 执行当前轮次
        step_result = session.step(action)
        print(step_result)
        print("---")

        # # 从 step_result 中提取 state
        # if hasattr(step_result, "state"):
        #     current_state = step_result.state  # 提取 negotiation state
        # else:
        #     raise ValueError("[ERROR] step_result 中缺少 state 属性")

        # 调用对手的 response
        opponent_response = session.step()  # 对手的响应
        print(opponent_response)
        print("---")
        next_offer = opponent_response.current_offer


        # 返回完整结果
        return {
            
            "next_offer": next_offer,
            
            "full_trace": session.full_trace,
        }

    
    def handle_offer_acceptance(self):
        """处理信号5：接受提议。"""
        agreement = self.session.state.agreement
        if not agreement:
            raise ValueError("No agreement reached yet.")
        return {
            'status': 'accepted',
            'agreement': agreement,
            'self_utility': self.ufun_a(agreement),
            'opponent_utility': self.ufun_b(agreement)
        }

    def handle_termination(self):
        """处理信号6：用户终止谈判。"""
        self.session.abort()
        return {'status': 'terminated'}

    def handle_timeout(self):
        """处理信号7：超时结束。"""
        return {'status': 'timeout', 'final_offer': self.session.state.current_offer}

    def handle_opponent_acceptance(self):
        """处理信号8：对方接受提议。"""
        agreement = self.session.state.agreement
        if not agreement:
            raise ValueError("No agreement reached yet.")
        return {'status': 'accepted_by_opponent', 'agreement': agreement}

    def handle_opponent_termination(self):
        """处理信号9：对方终止谈判。"""
        return {'status': 'terminated_by_opponent', 'final_offer': self.session.state.current_offer}

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

        return result, trace_file


if __name__ == "__main__":
    base_path = "/root/AANegotiator/Abstraction/scenarios/scenarios/specials"
    domain_name = "thompson_employment_mOlD"
    our_name = "AgentA"
    opp_name = "AgentB"
    our_agent = "AANegotiatior"
    opp_agent = "MiCRO"
    output_folder = "/root/AANegotiator/Abstraction/Results1213_test"

    runner = NegotiationRunner(base_path, domain_name, our_name, opp_name, our_agent, opp_agent, output_folder)
    session = runner.initialize_session()

    # # 处理信号示例
    print(runner.handle_signal(3))  # 推荐报价和历史
    print(runner.handle_signal(3))  # 推荐报价和历史

    runner.handle_signal(4, session=session, user_offer=('10%', 'Division D', '100%', '100%', '$38,000'))


    # result = runner.handle_signal(10)
    # print("Automation Process Result:", result)