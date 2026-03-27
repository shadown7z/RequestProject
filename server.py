from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# 定义一个 API 接口路径，比如 /api/data
@app.route('/api/data', methods=['GET'])
def get_device_data():
    # 模拟生成传感器数据
    mock_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage": round(random.uniform(10.0, 95.0), 2),     # 随机生成 10-95 的 CPU 占用率
        "temperature": round(random.uniform(20.0, 60.0), 1),   # 随机生成 20-60 的温度
        "humidity": round(random.uniform(30.0, 80.0), 1),      # 随机生成 30-80 的湿度
        "status": "normal"
    }
    # jsonify 会自动将 Python 字典转换成标准的 JSON 格式发给客户端
    return jsonify(mock_data)

if __name__ == '__main__':
    # 启动服务器，运行在本地的 5000 端口
    print("🚀 模拟设备数据 API 已启动！")
    print("👉 请在浏览器访问测试: http://127.0.0.1:5000/api/data")
    app.run(host='0.0.0.0', port=5000)