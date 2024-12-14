from flask import Flask, request, jsonify
from pathlib import Path
import json,os
from runner_step import NegotiationRunner 

from flask_cors import CORS

import traceback
import logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG) 
# 创建StreamHandler并添加到logger
console_handler = logging.StreamHandler()

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 将Handler添加到logger
logger.addHandler(console_handler)



from pathlib import Path
# current_directory = Path.cwd()
# files_and_dirs = [item.name for item in current_directory.iterdir()]
# print(files_and_dirs)



# 相对路径
PREFIX_PATH=Path(r"D:\\Negotiator\\Negotiator\\src\\python")
DEFINED_PROFILES_PATH=PREFIX_PATH / "defined_profiles"
OUTPUT_DIR=PREFIX_PATH / "output_dir"

# 选什么模型
NEGO_SUFFIX="mOlD"

DICTIONARY_CN_EN={
    "杂货店":"Supermarket_domain_",
    "买车":"adg_",
    "旅行":"travel_domain_",
    "找工作":"Supermarket_domain_",
    "买卖自行车零件":"ItexvsCypress_domain_"
}

DICTIONARY_EN_CN={value: key for key, value in DICTIONARY_CN_EN.items()}

# 人物的映射关系
ROLES_DICTIONARY_FUNCTION={
    "A":["Sam","买家","旅行者A","应聘者"],
    "B":["Mary","卖家","旅行者B","雇主"]
}

def translation(domain,my):
    # 中文名称：谈判域 我方角色 对手角色
    domain_EN=DICTIONARY_CN_EN[domain]
    domain_EN=domain_EN+NEGO_SUFFIX
    
    my_EN,op_EN='',''
    
    if my in ROLES_DICTIONARY_FUNCTION["A"] :
        my_EN="AgentA"
        op_EN="AgentB"
    elif my in ROLES_DICTIONARY_FUNCTION["B"] :
        my_EN="AgentB"
        op_EN="AgentA"
    else:
        raise ValueError(f"双方角色不匹配！")
    
    return domain_EN,my_EN,op_EN




# Global runner instance
runner = None



app = Flask(__name__)
CORS(app)

@app.route('/api/negotiation', methods=['POST'])
def negotiation_handler():
    global runner

    # Get the JSON payload from the request
    # data = request.get_json()
    
    response=None
    
    data = request.json
    print('收到的数据:', data)

    if not data or 'signal' not in data:
        return jsonify({"error": "Invalid request. 'signal' is required."}), 400

    signal = data['signal']
    payload = data['data']
    
    # print(signal)
    # print(payload)

    try:
        if signal == 1:
            # Initialize the runner instance
            base_path = DEFINED_PROFILES_PATH
            domain_name = payload.get('Domain')
            
            our_name = payload["Role"]
            
            my_first=payload.get('First')
                        
            # our_agent = payload.get('our_agent')
            # opp_agent = payload.get('opp_agent')
            
            # 不知道选agent的逻辑在哪
            our_agent = "AANegotiatior"
            opp_agent = "MiCRO"
            
            our_agent_profile_values=payload["Profile"]["my"]
            opp_agent_profile_values=payload["Profile"]["op"]            
            
            time_limit=payload.get('Times')
            n_steps=payload.get('Rounds')
            
            output_folder = OUTPUT_DIR

            # interests，一维数组
            my_interest_arr=payload['MyInterests']
            op_interest_arr=payload['OpInterests']
            
            # issues，二维数组
            my_issues_arr=payload['MyIssues']
            op_issues_arr=payload['OpIssues']
            
            
            
            domain_name,our_name,opp_name=translation(domain_name,our_name)
            
            logger.info("Before initializing negotiation runner ---------------------")
            logger.info(f"domain_name: {domain_name}")
            logger.info(f"our_name: {our_name}")
            logger.info(f"opp_name: {opp_name}")
            logger.info(f"our_agent_profile_values: {our_agent_profile_values}")
            logger.info(f"opp_agent_profile_values: {opp_agent_profile_values}")
            logger.info(f"time_limit: {time_limit}")
            logger.info(f"n_steps: {n_steps}")
            logger.info(f"my_first: {my_first}")
            
            logger.info(f"my_interest_arr: {my_interest_arr}")
            logger.info(f"op_interest_arr: {op_interest_arr}")
            logger.info(f"my_issues_arr: {my_issues_arr}")
            logger.info(f"op_issues_arr: {op_issues_arr}")
            

            
            

            runner = NegotiationRunner(
                base_path=base_path,
                domain_name=domain_name,
                our_name=our_name,
                opp_name=opp_name,
                our_agent=our_agent,
                opp_agent=opp_agent,
                output_folder=output_folder,
                time_limit=time_limit,
                n_steps=n_steps
            )

            runner.initialize_session()
            response={
                "message":"成功初始化谈判！"
            }

        elif signal in range(3, 11):
            if not runner:
                return jsonify({"error": "Runner not initialized. Please send signal 1 first."}), 400

            if signal == 4:
                # Handle user offer submission (signal 4)
                user_offer = payload.get('user_offer')
                if not user_offer:
                    return jsonify({"error": "'user_offer' is required for signal 4."}), 400
                
                result = runner.handle_signal(signal, session=runner.session, user_offer=user_offer)
                return jsonify(result)

            else:
                # Handle other signals
                result = runner.handle_signal(signal)
                return jsonify(result)

        
        
        
        
        
        else:
            return jsonify({"error": f"Unknown signal: {signal}"}), 400
        
        
        return jsonify(response)

    except Exception as e:
        print(e.with_traceback())
        # print(e.with_traceback(e.__traceback__))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True


    app.run(debug=True, port=5000)
