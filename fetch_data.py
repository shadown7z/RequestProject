import requests
import csv
import os

# 1. 目标 API 的地址（这里填你本地的地址）
API_URL = 'http://127.0.0.1:5000/api/data'
LOG_FILE = 'device_logs.csv'

def fetch_and_save():
    try:
        # 发送 GET 请求抓取数据
        print(f"正在从 {API_URL} 获取数据...")
        response = requests.get(API_URL)
        
        # 确保请求成功 (状态码 200)
        response.raise_for_status()
        
        # 将返回的 JSON 文本直接转换为 Python 字典
        data = response.json()
        print("✅ 成功抓取数据:", data)

        # 2. 将数据保存为 CSV 日志
        file_exists = os.path.isfile(LOG_FILE)
        
        # 以追加模式 ('a') 打开文件
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            # 定义 CSV 的表头（列名），要和抓取到的字典的键对应
            fieldnames = ['timestamp', 'cpu_usage', 'temperature', 'humidity', 'status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # 如果文件是新建的，先写一行表头
            if not file_exists:
                writer.writeheader()
            
            # 写入抓取到的数据
            writer.writerow(data)
            print(f"📁 数据已成功保存到日志文件 {LOG_FILE}\n")

    except Exception as e:
        print(f"❌ 抓取失败: {e}")

# 运行一次抓取测试
if __name__ == '__main__':
    fetch_and_save()