import os
import win32com.client
import tkinter as tk
from tkinter import messagebox
import pythoncom

# VBA 组件类型常量
vbext_ct_StdModule = 1  # 标准模块
vbext_ct_ClassModule = 2  # 类模块
vbext_ct_MSForm = 3  # 用户窗体
vbext_ct_Document = 100  # 文档模块（如 ThisWorkbook、Sheet1）


def extract_vba_code(source_file, vba_password=None):
    """提取源文件中的VBA代码"""
    try:
        print(f"尝试打开源文件: {source_file}")
        if not os.path.exists(source_file):
            raise FileNotFoundError("源文件不存在")

        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        print("Excel应用程序已启动")

        if vba_password:
            wb = excel.Workbooks.Open(source_file, Password=vba_password)
        else:
            wb = excel.Workbooks.Open(source_file)
        print("工作簿已打开")

        vba_project = wb.VBProject
        print("VBA项目已访问")

        component_count = vba_project.VBComponents.Count
        print(f"VBA 项目包含 {component_count} 个组件")

        vba_components = {}
        for component in vba_project.VBComponents:
            print(f"组件名称: {component.Name}, 类型: {component.Type}")
            code_module = component.CodeModule
            line_count = code_module.CountOfLines
            print(f"模块 {component.Name} 包含 {line_count} 行代码")
            if line_count > 0:
                code = code_module.Lines(1, line_count)
                vba_components[component.Name] = {'code': code, 'type': component.Type}
                print(f"成功提取模块: {component.Name}")
            else:
                print(f"模块 {component.Name} 为空")

        wb.Close()
        excel.Quit()
        return vba_components if vba_components else None
    except Exception as e:
        print(f"提取VBA代码时出错: {str(e)}")
        return None
    finally:
        pythoncom.CoUninitialize()


def copy_vba_code(target_file, vba_components):
    """将VBA代码复制到目标文件"""
    try:
        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        wb = excel.Workbooks.Open(target_file, UpdateLinks=0, ReadOnly=False)
        print(f"目标文件 {target_file} 已打开")

        vba_project = wb.VBProject
        print(f"访问目标文件的 VBA 项目，现有组件数: {vba_project.VBComponents.Count}")

        # 只移除标准模块
        existing_components = list(vba_project.VBComponents)
        for component in existing_components:
            if component.Type == vbext_ct_StdModule:
                try:
                    vba_project.VBComponents.Remove(component)
                    print(f"移除标准模块: {component.Name}")
                except Exception as e:
                    print(f"移除模块 {component.Name} 失败: {str(e)}")
            else:
                print(f"跳过非标准模块: {component.Name} (类型: {component.Type})")

        # 添加或覆盖 VBA 代码
        for component_name, component_data in vba_components.items():
            code = component_data['code']
            component_type = component_data['type']

            # 只处理标准模块
            if component_type == vbext_ct_StdModule:
                try:
                    print(f"尝试添加标准模块: {component_name}")
                    new_module = vba_project.VBComponents.Add(vbext_ct_StdModule)
                    new_module.Name = component_name
                    print(f"模块 {component_name} 已创建")
                    new_module.CodeModule.AddFromString(code)
                    print(f"代码已添加到模块 {component_name}")
                except Exception as e:
                    print(f"添加模块 {component_name} 失败: {str(e)}")
                    raise
            else:
                print(f"跳过非标准模块: {component_name} (类型: {component_type})")

        wb.Save()
        print(f"文件 {target_file} 已保存")
        wb.Close()
        excel.Quit()
        return True
    except Exception as e:
        print(f"复制VBA代码到 {target_file} 时出错: {str(e)}")
        return False
    finally:
        pythoncom.CoUninitialize()


def convert_to_xlsm(file_path):
    """将文件转换为xlsm格式"""
    try:
        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        wb = excel.Workbooks.Open(file_path)

        new_path = os.path.splitext(file_path)[0] + ".xlsm"
        wb.SaveAs(new_path, FileFormat=52)
        wb.Close()
        excel.Quit()

        os.remove(file_path)
        return new_path
    except Exception as e:
        print(f"转换文件 {file_path} 时出错: {str(e)}")
        return None
    finally:
        pythoncom.CoUninitialize()


def process_files():
    source_file = r"C:\Users\Administrator\Desktop\每日统计改名\转化成xlsm.xlsm"
    target_dir = r"D:\30269\批量修改文件格式并复制vba宏"

    print(f"检查源文件路径: {source_file}, 是否存在: {os.path.exists(source_file)}")
    if not os.path.exists(source_file):
        print("源文件不存在！程序终止")
        return

    if not os.path.exists(target_dir):
        print(f"目标目录 {target_dir} 不存在！程序终止")
        return

    vba_components = extract_vba_code(source_file)
    if not vba_components:
        print("无法提取VBA代码，程序终止")
        return

    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    non_xlsm_files = [f for f in files if f.lower().endswith(('.xls', '.xlsx'))]

    if non_xlsm_files:
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno(
            "文件格式检查",
            f"检测到以下文件不是xlsm格式：\n{', '.join(non_xlsm_files)}\n是否将目录下的.xls和.xlsx文件转换为xlsm格式？"
        )

        if response:
            for file in files:
                file_path = os.path.join(target_dir, file)
                if file.lower().endswith(('.xls', '.xlsx')):
                    print(f"正在转换: {file}")
                    new_file = convert_to_xlsm(file_path)
                    if new_file:
                        print(f"成功转换为: {os.path.basename(new_file)}")
                    else:
                        print(f"转换失败: {file}")
        root.destroy()

    xlsm_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.xlsm')]
    for file in xlsm_files:
        target_file = os.path.join(target_dir, file)
        print(f"正在处理: {file}")
        if copy_vba_code(target_file, vba_components):
            print(f"成功复制VBA代码到: {file}")
        else:
            print(f"处理失败: {file}")


if __name__ == "__main__":
    process_files()
    print("处理完成！")