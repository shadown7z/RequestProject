import csv
import os

LOG_FILE = 'device_logs.csv'
REPORT_FILE = '系统诊断报告.html'

# === 第一步：编写“专家规则库”（保持不变） ===
def analyze_cpu(cpu_val):
    if cpu_val >= 85.0:
        return f"🔴 **异常告警**：当前 CPU 占用率高达 <b>{cpu_val}%</b>，处于极高负载状态！<br>💡 <b>建议行动</b>：请立即检查是否有死循环进程或异常流量攻击，考虑进行扩容或重启占用过高的服务。"
    elif cpu_val >= 60.0:
        return f"🟡 **关注提示**：当前 CPU 占用率为 <b>{cpu_val}%</b>，负载偏高。<br>💡 <b>建议行动</b>：建议排查当前运行的大型任务，观察是否有持续上涨的趋势。"
    else:
        return f"🟢 **运行良好**：当前 CPU 占用率为 <b>{cpu_val}%</b>，资源充裕。<br>💡 <b>建议行动</b>：系统健康，无需干预。"

def analyze_humidity(hum_val):
    if hum_val > 60.0:
        return f"💧 **湿度过高**：当前环境湿度为 <b>{hum_val}%</b>。<br>💡 <b>建议行动</b>：机房湿度过高可能导致设备主板凝露结水，引发短路！请立即检查机房精密空调的除湿功能是否正常运行。"
    elif hum_val < 30.0:
        return f"🏜️ **湿度过低**：当前环境湿度为 <b>{hum_val}%</b>。<br>💡 <b>建议行动</b>：环境过于干燥极易产生静电，增加击穿精密电子元器件的风险！建议开启加湿器或调整空调参数。"
    else:
        return f"✅ **湿度适宜**：当前环境湿度为 <b>{hum_val}%</b>，在标准范围(30%-60%)内。<br>💡 <b>建议行动</b>：继续保持当前环境监控。"

def analyze_temperature(temp_val):
    if temp_val > 45.0:
        return f"🔥 **高温危险**：当前温度达到 <b>{temp_val}℃</b>！<br>💡 <b>建议行动</b>：温度过高会导致服务器宕机或硬件寿命缩短。请立即检查散热系统、风扇转速及机房空调状态。"
    else:
        return f"❄️ **温度正常**：当前温度为 <b>{temp_val}℃</b>，散热状况良好。<br>💡 <b>建议行动</b>：保持现状。"


# === 第二步：读取数据并生成带动态交互的 HTML ===
def generate():
    if not os.path.exists(LOG_FILE):
        print("❌ 找不到日志文件，请先运行抓取脚本。")
        return

    with open(LOG_FILE, mode='r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        if not reader:
            print("❌ 日志文件为空。")
            return
        latest_data = reader[-1]

    cpu = float(latest_data['cpu_usage'])
    hum = float(latest_data['humidity'])
    temp = float(latest_data['temperature'])

    # 注意：Python 的 f-string 中，CSS 和 JS 的大括号需要写两遍 {{ }} 来转义
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>设备巡检诊断报告</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
        
        <style>
            body {{ font-family: 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333; background-color: #f0f2f5; margin: 0; padding: 20px; }}
            /* 报告的主体容器 */
            #report-container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .time-stamp {{ text-align: right; color: #e74c3c; font-weight: bold; font-size: 1em; }}
            .module {{ margin-top: 25px; padding: 15px; background-color: #f8fcfd; border-left: 5px solid #3498db; border-radius: 5px; }}
            h3 {{ margin-top: 0; color: #2980b9; }}
            
            /* 按钮的样式 */
            .btn-container {{ text-align: center; margin-bottom: 20px; }}
            #download-btn {{ background-color: #27ae60; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; transition: 0.3s; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
            #download-btn:hover {{ background-color: #2ecc71; transform: translateY(-2px); }}
        </style>
    </head>
    <body>
        
        <div class="btn-container">
            <button id="download-btn" onclick="downloadPDF()">📥 下载为 PDF 报告</button>
        </div>

        <div id="report-container">
            <h1>📊 设备智能巡检诊断报告</h1>
            <p class="time-stamp" id="live-time">报告生成时间：加载中...</p>

            <div class="module">
                <h3>💻 1. 计算资源分析 (CPU)</h3>
                <p>{analyze_cpu(cpu)}</p>
            </div>

            <div class="module">
                <h3>🌡️ 2. 环境温度分析</h3>
                <p>{analyze_temperature(temp)}</p>
            </div>

            <div class="module">
                <h3>💧 3. 环境湿度分析</h3>
                <p>{analyze_humidity(hum)}</p>
            </div>
            
            <p style="text-align: center; margin-top: 40px; color: #bdc3c7; font-size: 0.8em;">-- 本报告由系统规则引擎自动生成 --</p>
        </div>

        <script>
            // --- 功能 1：动态时间时钟 ---
            function updateTime() {{
                const now = new Date();
                const year = now.getFullYear();
                const month = String(now.getMonth() + 1).padStart(2, '0');
                const day = String(now.getDate()).padStart(2, '0');
                const hours = String(now.getHours()).padStart(2, '0');
                const minutes = String(now.getMinutes()).padStart(2, '0');
                const seconds = String(now.getSeconds()).padStart(2, '0');
                
                const timeString = `${{year}}-${{month}}-${{day}} ${{hours}}:${{minutes}}:${{seconds}}`;
                document.getElementById('live-time').innerText = '当前系统时间：' + timeString;
            }}
            
            // 每 1000 毫秒 (1秒) 执行一次 updateTime 函数
            setInterval(updateTime, 1000);
            updateTime(); // 网页刚打开时立刻执行一次

            // --- 功能 2：生成并下载 PDF ---
            function downloadPDF() {{
                const element = document.getElementById('report-container'); // 选中要生成 PDF 的区域
                const btn = document.getElementById('download-btn');
                
                // 改变按钮文字提示用户正在处理
                btn.innerText = "⏳ 正在生成 PDF...";
                btn.style.backgroundColor = "#95a5a6";
                btn.disabled = true;

                // 配置 PDF 参数
                const opt = {{
                    margin:       10,
                    filename:     '智能诊断报告.pdf',
                    image:        {{ type: 'jpeg', quality: 0.98 }},
                    html2canvas:  {{ scale: 2 }}, // 提高 PDF 清晰度
                    jsPDF:        {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
                }};

                // 调用库生成 PDF
                html2pdf().set(opt).from(element).save().then(() => {{
                    // 下载完成后恢复按钮状态
                    btn.innerText = "📥 下载为 PDF 报告";
                    btn.style.backgroundColor = "#27ae60";
                    btn.disabled = false;
                }});
            }}
        </script>
    </body>
    </html>
    """

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"🎉 动态交互报告已生成！请在浏览器双击打开：{REPORT_FILE}")

if __name__ == '__main__':
    generate()