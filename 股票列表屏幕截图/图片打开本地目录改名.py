import os
import sys
from datetime import datetime, timedelta

def get_valid_date():
    """
    获取用户输入的有效日期 (YYYYMMDD)。
    处理空输入、格式错误、无效日期及 Ctrl+C 退出。
    """
    while True:
        try:
            date_input = input("请输入日期（格式：YYYYMMDD，例如20250411），或按Ctrl+C退出）：")
            if not date_input:
                print("输入不能为空，请重新输入！")
                continue
            if len(date_input) != 8 or not date_input.isdigit():
                print("日期格式错误！请输入8位纯数字（YYYYMMDD格式），请重新输入！")
                continue
            try:
                input_date_obj = datetime.strptime(date_input, "%Y%m%d")
                return date_input, input_date_obj
            except ValueError:
                print("无效的日期！请确保输入正确的年月日（YYYYMMDD格式），请重新输入！")
        except KeyboardInterrupt:
            print("\n用户请求退出程序...")
            sys.exit(0)
        except EOFError:
            print("\n接收到输入结束信号，程序退出。")
            sys.exit(1)

def generate_bat_file():
    """
    获取日期，生成对应的 BAT 文件到当前用户的桌面。
    美股路径使用输入日期的前一天，其他市场使用输入日期。
    """
    try:
        date_input, input_date_obj = get_valid_date()
        if date_input is None or input_date_obj is None:
            print("未能获取有效日期，程序终止。")
            return

        year = date_input[0:4]
        date_str = input_date_obj.strftime("%Y年%m月%d日")
        month_str = input_date_obj.strftime("%Y年%m月")
        prev_day_obj = input_date_obj - timedelta(days=1)
        prev_day_date_str = prev_day_obj.strftime("%Y年%m月%d日")

        # BAT文件内容，匹配源文件结构
        bat_content = f"""@echo off

start "" "E:\\图片\\A股资金历史记录\\{year}A股资金历史记录\\{month_str}A股资金历史记录\\{date_str}A股资金历史记录"
start "" "Z:\\图片\\A股资金历史记录\\{year}A股资金历史记录\\{month_str}A股资金历史记录\\{date_str}A股资金历史记录"
start "" "\\\\192.168.1.17\\图片\\A股资金历史记录\\{year}A股资金历史记录\\{month_str}A股资金历史记录\\{date_str}A股资金历史记录"

start "" "E:\\图片\\港股资金历史记录\\{year}港股资金历史记录\\{month_str}港股资金历史记录\\{date_str}港股资金历史记录"
start "" "Z:\\图片\\港股资金历史记录\\{year}港股资金历史记录\\{month_str}港股资金历史记录\\{date_str}港股资金历史记录"
start "" "\\\\192.168.1.17\\图片\\港股资金历史记录\\{year}港股资金历史记录\\{month_str}港股资金历史记录\\{date_str}港股资金历史记录"

start "" "E:\\图片\\美股资金历史记录\\{year}美股资金历史记录\\{month_str}美股资金历史记录\\{prev_day_date_str}美股资金历史记录"
start "" "Z:\\图片\\美股资金历史记录\\{year}美股资金历史记录\\{month_str}美股资金历史记录\\{prev_day_date_str}美股资金历史记录"
start "" "\\\\192.168.1.17\\图片\\美股资金历史记录\\{year}美股资金历史记录\\{month_str}美股资金历史记录\\{prev_day_date_str}美股资金历史记录"

start "" "E:\\图片\\市值300资金历史记录\\{year}市值A股资金历史记录\\{month_str}市值300A股资金历史记录\\{date_str}市值300A股资金历史记录"
start "" "Z:\\图片\\市值300资金历史记录\\{year}市值A股资金历史记录\\{month_str}市值300A股资金历史记录\\{date_str}市值300A股资金历史记录"
start "" "\\\\192.168.1.17\\图片\\市值300资金历史记录\\{year}市值A股资金历史记录\\{month_str}市值300A股资金历史记录\\{date_str}市值300A股资金历史记录"

start "" "E:\\图片\\中特估69资金历史记录\\{year}中特估69资金历史记录\\{month_str}中特估69资金历史记录\\{date_str}中特估69A股资金历史记录"
start "" "Z:\\图片\\中特估69资金历史记录\\{year}中特估69资金历史记录\\{month_str}中特估69资金历史记录\\{date_str}中特估69A股资金历史记录"
start "" "\\\\192.168.1.17\\图片\\中特估69资金历史记录\\{year}中特估69资金历史记录\\{month_str}中特估69资金历史记录\\{date_str}中特估69A股资金历史记录"
"""

        # 获取桌面路径并创建目标文件夹
        desktop_path = os.path.expanduser("~\\Desktop")
        if not os.path.isdir(desktop_path):
            desktop_path = os.getcwd()  # 回退到当前工作目录

        sub_folder = "每日统计改名"
        target_dir = os.path.join(desktop_path, sub_folder)
        output_filename = "图片打开本地目录.bat"
        output_path = os.path.join(target_dir, output_filename)

        os.makedirs(target_dir, exist_ok=True)

        # 写入BAT文件，使用gbk编码
        with open(output_path, 'w', encoding='gbk') as f:
            f.write(bat_content)
        print(f"\n已成功生成BAT文件：'{output_filename}'")
        print(f"文件已保存在 '{target_dir}' 文件夹中。")
        print(f"完整路径：{output_path}")
        print(f"注意：美股路径已自动使用前一天 ({prev_day_date_str}) 的日期。")

    except PermissionError:
        print(f"\n错误：权限不足！无法在 '{target_dir}' 创建或写入文件。")
        print("请以管理员权限运行脚本或检查文件夹权限。")
    except OSError as e:
        print(f"\n错误：创建目录或写入文件时发生系统错误：{e}")
    except Exception as e:
        print(f"\n错误：生成BAT文件时发生未知错误：{e}")

if __name__ == "__main__":
    print("--- BAT 文件生成脚本 ---")
    print("提示：输入日期时请使用YYYYMMDD格式（如20250411）")
    print("      美股路径将自动使用输入日期的【前一天】。")
    print("      按Ctrl+C可随时退出程序")
    print("-" * 25)

    generate_bat_file()

    print("-" * 25)
    input("操作完成。按 Enter 键退出...")