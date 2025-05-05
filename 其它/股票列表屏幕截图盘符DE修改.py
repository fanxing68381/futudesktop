import os
import sys
import re
import ctypes


def find_target_directory():
    """定位目标文件夹"""
    base_path = r'D:\富途牛牛'
    target_name = '股票列表屏幕截图'

    if not os.path.exists(base_path):
        print(f"错误：基础目录不存在 {base_path}")
        sys.exit(1)

    # 优先检查直接子目录
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            check_path = os.path.join(full_path, target_name)
            if os.path.exists(check_path):
                return check_path

    # 深度搜索
    for root, dirs, _ in os.walk(base_path):
        if target_name in dirs:
            return os.path.join(root, target_name)
        dirs[:] = [d for d in dirs if 'futu' in d.lower() or '富途' in d]

    print(f"未找到目标目录：{target_name}")
    sys.exit(1)


def detect_current_path(target_dir):
    """智能检测当前路径"""
    sample_files = [
        '59个美股(批量截取富途牛牛股票列表).py',
        'A股(批量截取富途牛牛股票列表).py'
    ]

    # 修正后的正则表达式，匹配单反斜杠
    path_pattern = re.compile(r'["\']([D-E]:\\图片)["\']')

    for filename in sample_files:
        file_path = os.path.join(target_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                match = path_pattern.search(content)
                if match:
                    return match.group(1) + '\\'  # 保证结尾有单个反斜杠
            except:
                continue
    return None


def modify_files(target_dir, old_path, new_path):
    """执行智能替换"""
    files = [
        '59个美股(批量截取富途牛牛股票列表).py',
        '302股(批量截取富途牛牛股票列表).py',
        'A股(批量截取富途牛牛股票列表).py',
        '港股(批量截取富途牛牛股票列表).py',
        '中特估69股(批量截取富途牛牛股票列表).py'
    ]

    modified_count = 0
    # 修正路径匹配模式
    path_regex = re.compile(r'([D-E]):\\图片\\?', re.IGNORECASE)

    for filename in files:
        file_path = os.path.join(target_dir, filename)
        print(f"\n处理文件：{filename}")

        if not os.path.exists(file_path):
            print("文件不存在，跳过处理")
            continue

        try:
            # 自动检测编码
            encodings = ['utf-8', 'gbk', 'gb2312']
            content = None
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue

            if not content:
                print("无法识别文件编码")
                continue

            # 智能替换逻辑
            if old_path:
                # 精确替换已检测到的路径（使用原始字符串）
                old_pattern = re.compile(re.escape(old_path.replace('\\', '\\\\')), re.IGNORECASE)
                new_content = old_pattern.sub(new_path.replace('\\', '\\\\'), content)
            else:
                # 通配替换所有可能路径
                new_content = path_regex.sub(new_path + '\\', content)

            if new_content == content:
                print("未找到需要替换的内容")
                continue

            # 统一使用单反斜杠保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content.replace('\\\\', '\\'))

            modified_count += 1
            print("修改成功")

        except PermissionError:
            print("权限不足，请用管理员身份运行")
        except Exception as e:
            print(f"处理失败：{str(e)}")

    return modified_count


def main():
    # 提权提示
    if sys.platform == 'win32' and not ctypes.windll.shell32.IsUserAnAdmin():
        print("建议：请右键使用管理员身份运行")

    # 查找目录
    target_dir = find_target_directory()
    print(f"找到目标目录：{target_dir}")

    # 路径检测
    current_path = detect_current_path(target_dir)
    path_status = current_path if current_path else "未检测到有效路径"
    print(f"\n当前路径状态：{path_status}")

    # 用户确认
    choice = input("是否修改路径？(y-改为D盘/n-改为E盘)：").lower().strip()
    while choice not in ['y', 'n']:
        choice = input("请输入 y 或 n：").lower().strip()

    new_path = r'D:\图片' if choice == 'y' else r'E:\图片'
    old_path = current_path if current_path else None

    # 执行修改
    total = modify_files(target_dir, old_path, new_path + '\\')  # 保证路径结尾有单个反斜杠
    print(f"\n操作完成，成功修改 {total} 个文件")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
