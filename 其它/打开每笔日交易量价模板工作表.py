import win32com.client

# 创建Excel应用对象
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True  # 可视化界面

try:
    # 打开工作簿
    workbook = excel.Workbooks.Open(r'D:\图片\每笔日交易量价模板.xlsx')

    # 切换到指定工作表
    worksheet = workbook.Worksheets("30个股R1S1")
    worksheet.Activate()

    print("文件已打开并切换到目标工作表。")

except Exception as e:
    print(f"操作失败: {e}")
    excel.Quit()