from flask import Flask, request, jsonify

app = Flask(__name__)

# 定义一个路由处理前端发送的 POST 请求
@app.route('/api/process', methods=['POST'])
def process_data():
    try:
        # 获取请求体中的 JSON 数据
        data = request.get_json()

        # 校验数据格式
        if 'CODE' not in data or 'data' not in data:
            return jsonify({'error': '缺少必要的字段 CODE 或 data'}), 400

        code = data['CODE']
        obj = data['data']

        # 校验 CODE 是否为正整数
        if not isinstance(code, int) or code <= 0:
            return jsonify({'error': 'CODE 必须是一个正整数'}), 400

        # 模拟处理逻辑，根据 CODE 执行不同操作
        if code == 1:
            result = {key: value.upper() for key, value in obj.items()}  # 示例操作：将字符串转为大写
        elif code == 2:
            result = {key: value[::-1] for key, value in obj.items()}  # 示例操作：反转字符串
        else:
            result = {'message': '未知的 CODE'}

        # 返回处理结果
        return jsonify({'status': 'success', 'result': result})

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
