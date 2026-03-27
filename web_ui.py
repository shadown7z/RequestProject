import streamlit as st
import pandas as pd

# 1. 设置网页的标题和布局
st.set_page_config(page_title="设备监控大屏", layout="wide")
st.title("📊 设备智能监控中心")

# 2. 读取我们之前抓取保存的 CSV 日志数据
# 假设你的日志文件叫 device_logs.csv
try:
    df = pd.read_csv('device_logs.csv')
    
    # 3. 在网页上直接显示漂亮的原始数据表格
    st.subheader("📝 最新日志数据")
    st.dataframe(df.tail(5)) # 只看最新的 5 条
    
    # 4. 画一个交互式的折线图 (把时间和需要展示的列对应起来)
    st.subheader("📈 CPU 与温度趋势图")
    # 将 timestamp 设为索引，这样图表的横坐标就是时间了
    chart_data = df.set_index('timestamp')[['cpu_usage', 'temperature']]
    st.line_chart(chart_data)

except FileNotFoundError:
    st.error("❌ 找不到 device_logs.csv 文件，请先运行抓取脚本生成数据哦！")