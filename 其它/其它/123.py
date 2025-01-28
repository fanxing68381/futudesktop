import os
import pandas as pd


def convert_excel_to_xls(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.xlsx', '.xls')):
            file_path = os.path.join(directory, filename)
            try:
                # 指定使用 xlrd 引擎读取 .xls 文件
                if filename.endswith('.xls'):
                    df = pd.read_excel(file_path, engine='xlrd')
                else:
                    df = pd.read_excel(file_path)
                new_filename = os.path.splitext(filename)[0] + '.xls'
                new_file_path = os.path.join(directory, new_filename)
                df.to_excel(new_file_path, index=False)
                print(f"已将 {filename} 转换为 {new_filename}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")


if __name__ == "__main__":
    # 使用原始字符串，避免转义问题
    directory = r'C:\Users\Administrator\Desktop\日线历史走势改名'
    convert_excel_to_xls(directory)