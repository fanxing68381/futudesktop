import os

def replace_string_in_files(directory, old_str, new_str):
    # 遍历目录及子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 替换字符串
                new_content = content.replace(old_str, new_str)
                # 如果内容有变化则写入文件
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'已修改文件：{file_path}')

# 使用示例
directory = r'D:\富途牛牛\futu(backup)\股票列表屏幕截图'
old_str = r'D:\图片'
new_str = r'E:\图片'

replace_string_in_files(directory, old_str, new_str)