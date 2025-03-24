import os
import win32com.client as win32
import subprocess
import send2trash


def convert_xls_to_xlsx(directory):
    # 修改这里，使用 Dispatch 替代 EnsureDispatch
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False  # 不显示Excel界面
    successful_conversions = []

    try:
        # 遍历目录中的所有.xls文件
        for filename in os.listdir(directory):
            if filename.endswith('.xls'):
                # 构造完整文件路径
                old_path = os.path.join(directory, filename)

                # 新文件名（替换扩展名）
                new_name = os.path.splitext(filename)[0] + '.xlsx'
                new_path = os.path.join(directory, new_name)

                try:
                    # 打开工作簿并另存为xlsx格式
                    workbook = excel.Workbooks.Open(old_path)
                    workbook.SaveAs(new_path, FileFormat=51)  # 51表示xlsx格式
                    workbook.Close()
                    successful_conversions.append(old_path)
                    print(f"转换成功: {filename} -> {new_name}")
                except Exception as e:
                    print(f"转换 {filename} 时出现错误: {str(e)}")

    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
    finally:
        # 确保退出Excel应用
        excel.Quit()

    # 将转换成功的 .xls 文件移至回收站
    for file in successful_conversions:
        try:
            send2trash.send2trash(file)
            print(f"已将 {os.path.basename(file)} 移至回收站")
        except Exception as e:
            print(f"将 {os.path.basename(file)} 移至回收站时出错: {str(e)}")

    return successful_conversions


def run_bat_file(directory):
    bat_file_path = os.path.join(directory, "change name 港股.bat")
    renamed_files = []
    if os.path.exists(bat_file_path):
        try:
            # 运行批处理文件，捕获输出和错误信息
            result = subprocess.run([bat_file_path], cwd=directory, shell=True, check=True, capture_output=True,
                                    text=True)
            print("批处理文件执行成功！")
            print("批处理文件输出信息：")
            print(result.stdout)
            # 解析批处理文件中的重命名操作
            try:
                with open(bat_file_path, 'r') as f:
                    batch_content = f.readlines()
                for line in batch_content:
                    if line.startswith('ren'):
                        _, old_name, new_name = line.split()
                        old_file_path = os.path.join(directory, old_name)
                        new_file_path = os.path.join(directory, new_name)
                        if os.path.exists(old_file_path) and os.path.exists(new_file_path):
                            renamed_files.append(old_file_path)
            except Exception as read_error:
                print(f"读取批处理文件时出现错误: {read_error}")
        except subprocess.CalledProcessError as e:
            print(f"批处理文件执行失败: {e}")
            print("批处理文件错误信息：")
            print(e.stderr)
            try:
                # 尝试使用系统默认编码读取批处理文件
                with open(bat_file_path, 'r') as f:
                    batch_content = f.readlines()
                for line in batch_content:
                    if line.startswith('ren'):
                        _, old_name, _ = line.split()
                        old_file_path = os.path.join(directory, old_name)
                        if not os.path.exists(old_file_path):
                            print(f"文件 {old_name} 不存在，可能导致重命名失败。")
            except Exception as read_error:
                print(f"读取批处理文件时出现错误: {read_error}")
    else:
        print("未找到change name 港股.bat文件。")

    return renamed_files


if __name__ == "__main__":
    target_dir = r'C:\Users\Administrator\Desktop\每日统计改名'
    # 转换文件
    converted_files = convert_xls_to_xlsx(target_dir)
    print("所有文件转换完成！")
    # 运行批处理文件
    renamed_files = run_bat_file(target_dir)

    # 统计处理的文件
    all_processed_files = converted_files + renamed_files
    num_processed_files = len(all_processed_files)

    print(f"\n总共处理了 {num_processed_files} 个文件，它们是：")
    if num_processed_files > 5:
        for file in all_processed_files[:3]:
            print(os.path.basename(file))
        print("...")
        for file in all_processed_files[-2:]:
            print(os.path.basename(file))
    else:
        for file in all_processed_files:
            print(os.path.basename(file))