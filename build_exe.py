import os

print("🚀 开始准备打包环境...")

# 定义你要打包的主程序文件名
main_script = "gui_app.py"

if not os.path.exists(main_script):
    print(f"❌ 找不到 {main_script} 文件，请确保文件名正确并在当前目录下！")
else:
    # 构建 PyInstaller 的命令
    # -F (--onefile): 把所有依赖打包成一个独立的 .exe 文件
    # -w (--noconsole): 运行软件时，隐藏背后的黑色命令行窗口（只显示 GUI 界面）
    # -i icon.ico: (可选) 如果你有图标文件，可以加上这个参数替换默认图标
    
    command = f"pyinstaller -F -w {main_script}"
    
    print(f"📦 正在执行打包命令: {command}")
    print("⏳ 这个过程可能需要 1-3 分钟，请耐心等待，期间会输出很多编译日志...")
    
    # 执行终端命令
    os.system(command)
    
    print("\n🎉 打包流程结束！")
    print("👉 请在当前目录下的 'dist' 文件夹中寻找你的 .exe 应用程序！")