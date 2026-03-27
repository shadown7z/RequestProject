import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import requests
import csv
import os
import datetime
import webbrowser

# === 专家规则库 (原封不动搬过来) ===
def analyze_cpu(cpu_val):
    if cpu_val >= 85.0: return f"🔴 异常告警：CPU高达 <b>{cpu_val}%</b>，请检查进程！"
    elif cpu_val >= 60.0: return f"🟡 关注提示：CPU达到 <b>{cpu_val}%</b>，负载偏高。"
    else: return f"🟢 运行良好：CPU <b>{cpu_val}%</b>，资源充裕。"

def analyze_temp(temp_val):
    if temp_val > 45.0: return f"🔥 高温危险：温度 <b>{temp_val}℃</b>，请检查散热！"
    else: return f"❄️ 温度正常：温度 <b>{temp_val}℃</b>，散热良好。"

def analyze_hum(hum_val):
    if hum_val > 60.0: return f"💧 湿度过高：湿度 <b>{hum_val}%</b>，注意防潮。"
    elif hum_val < 30.0: return f"🏜️ 湿度过低：湿度 <b>{hum_val}%</b>，注意防静电。"
    else: return f"✅ 湿度适宜：湿度 <b>{hum_val}%</b>，范围正常。"


# === 主窗口初始化 ===
root = tk.Tk()
root.title("💻 设备本地监控工作站 (全能版)")
root.geometry("700x550")
root.configure(bg="#f0f0f0")

cpu_var = tk.StringVar(value="-- %")
temp_var = tk.StringVar(value="-- ℃")
time_var = tk.StringVar(value="等待读取...")

# === 核心功能 1：读取本地数据刷新界面 ===
def refresh_data():
    if not os.path.exists('device_logs.csv'):
        return
    df = pd.read_csv('device_logs.csv')
    if df.empty: return
        
    latest = df.iloc[-1]
    cpu_var.set(f"{latest['cpu_usage']} %")
    temp_var.set(f"{latest['temperature']} ℃")
    time_var.set(f"最后更新: {latest['timestamp']}")
    
    for row in tree.get_children(): tree.delete(row)
    for index, row in df.tail(8).iterrows():
        tree.insert("", "end", values=(row['timestamp'], row['cpu_usage'], row['temperature'], row['humidity']))

# === 核心功能 2：一键采集数据 (相当于之前的 fetch_data.py) ===
def auto_fetch():
    api_url = 'http://127.0.0.1:5000/api/data'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        file_exists = os.path.isfile('device_logs.csv')
        with open('device_logs.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'cpu_usage', 'temperature', 'humidity', 'status'])
            if not file_exists: writer.writeheader()
            writer.writerow(data)
        
        refresh_data() # 采集完立刻刷新界面
        messagebox.showinfo("成功", "✅ 数据采集成功！")
    except Exception as e:
        messagebox.showerror("错误", f"❌ 采集失败！请确保你的 Flask 模拟服务器正在运行。\n报错信息: {e}")

# === 核心功能 3：一键生成报告 (相当于之前的 generate_report.py) ===
def generate_report_action():
    if not os.path.exists('device_logs.csv'):
        messagebox.showwarning("警告", "没有数据可供生成报告，请先点击采集！")
        return
        
    df = pd.read_csv('device_logs.csv')
    latest = df.iloc[-1]
    
    # 组合 HTML (去掉了长篇 CSS，保持核心结构，保留了下载 PDF 按钮)
    html_content = f"""
    <!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>诊断报告</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>body{{font-family:sans-serif; background:#f4f4f4; padding:20px;}} #report{{background:#fff; padding:30px; border-radius:8px; max-width:800px; margin:auto;}}</style>
    </head><body>
    <div style="text-align:center; margin-bottom:20px;">
        <button onclick="html2pdf().from(document.getElementById('report')).save('设备诊断报告.pdf')" style="padding:10px 20px; background:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer;">📥 下载为 PDF</button>
    </div>
    <div id="report">
        <h1 style="text-align:center; border-bottom:2px solid #333; padding-bottom:10px;">📊 设备智能巡检诊断报告</h1>
        <p style="text-align:right; color:red;">报告生成时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p style="text-align:right;">数据采样时间：{latest['timestamp']}</p>
        <div style="background:#f9f9f9; padding:15px; margin-top:20px; border-left:4px solid #2980b9;">
            <h3>💻 1. CPU 分析</h3><p>{analyze_cpu(float(latest['cpu_usage']))}</p>
        </div>
        <div style="background:#f9f9f9; padding:15px; margin-top:20px; border-left:4px solid #e67e22;">
            <h3>🌡️ 2. 温度分析</h3><p>{analyze_temp(float(latest['temperature']))}</p>
        </div>
        <div style="background:#f9f9f9; padding:15px; margin-top:20px; border-left:4px solid #3498db;">
            <h3>💧 3. 湿度分析</h3><p>{analyze_hum(float(latest['humidity']))}</p>
        </div>
    </div>
    </body></html>
    """
    
    report_path = os.path.abspath('一键诊断报告.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 用默认浏览器自动打开生成的报告
    webbrowser.open(f"file://{report_path}")
    messagebox.showinfo("成功", "🎉 报告生成成功，已在浏览器中为您打开！")


# === 界面排版 ===
header_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
header_frame.pack(fill="x")
tk.Label(header_frame, text="最新数据时间:", bg="#f0f0f0").pack(side="left", padx=10)
tk.Label(header_frame, textvariable=time_var, fg="blue", bg="#f0f0f0").pack(side="left")

# --- 这里是新增的两个核心操作按钮 ---
action_frame = tk.Frame(root, bg="#f0f0f0", pady=5)
action_frame.pack(fill="x")
tk.Button(action_frame, text="⚡ 一键采集最新数据", command=auto_fetch, bg="#3498db", fg="white", font=("Arial", 11, "bold"), width=20, pady=5).pack(side="left", padx=20)
tk.Button(action_frame, text="📄 生成并查看诊断报告", command=generate_report_action, bg="#e67e22", fg="white", font=("Arial", 11, "bold"), width=20, pady=5).pack(side="right", padx=20)

card_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
card_frame.pack(fill="x")
cpu_card = tk.LabelFrame(card_frame, text="🖥️ CPU 占用率", font=("Arial", 10, "bold"), bg="white", padx=20, pady=10)
cpu_card.pack(side="left", padx=20, expand=True, fill="both")
tk.Label(cpu_card, textvariable=cpu_var, font=("Arial", 28, "bold"), fg="#e74c3c", bg="white").pack()
temp_card = tk.LabelFrame(card_frame, text="🌡️ 环境温度", font=("Arial", 10, "bold"), bg="white", padx=20, pady=10)
temp_card.pack(side="right", padx=20, expand=True, fill="both")
tk.Label(temp_card, textvariable=temp_var, font=("Arial", 28, "bold"), fg="#e67e22", bg="white").pack()

table_frame = tk.Frame(root, padx=20, pady=10, bg="#f0f0f0")
table_frame.pack(fill="both", expand=True)
columns = ("时间", "CPU(%)", "温度(℃)", "湿度(%)")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
for col in columns: tree.heading(col, text=col); tree.column(col, anchor="center", width=120)
tree.pack(fill="both", expand=True)

# 启动程序
refresh_data()
root.mainloop()