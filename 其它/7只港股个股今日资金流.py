from futu import *
import time
import pandas as pd
import os
import platform
import re  # 添加到文件开头
from openpyxl import load_workbook

stock_code_to_name = {
"HK.02318":"中国平安","HK.01787":"山东黄金","HK.00981":"中芯国际","HK.01071":"华电国际",
    "HK.03968":"招商银行","HK.06862":"海底捞","HK.00883":"中国海洋石油",
}

stock_codes = list(stock_code_to_name.keys())
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 创建一个空列表用于存储数据
data_list = []

for code in stock_codes:
    ret, data = quote_ctx.get_capital_flow(code, period_type=PeriodType.INTRADAY)
    company_name = stock_code_to_name[code]

    if ret == RET_OK:
        if not data.empty:
            last_record = data.iloc[-1]
            # 将数据添加到列表
            data_list.append({
                "股票代码": code,
                "公司名称": company_name,
                "时间": last_record['capital_flow_item_time'],
                "整体净流入（万元）": round(last_record['in_flow'] / 10000, 2)
            })
            # 保留原有的打印逻辑（可选）
            print(f'\n {company_name} ')
            #print(f"时间：{last_record['capital_flow_item_time']}")
            print(f"{round(last_record['in_flow']/10000, 2)}万净流入")
        else:
            print(f"公司 {company_name} 无有效数据")
    else:
        print(f"获取 {company_name} 数据失败，错误信息:", data)
    time.sleep(1)

quote_ctx.close()

# 将数据转换为DataFrame并保存为Excel
if data_list:  # 如果列表不为空
    df = pd.DataFrame(data_list)
    # 修改保存路径
    file_path = r"D:\30269\7只港股资金流向数据.xlsx"
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)
    print(f"\n数据已保存至 {file_path}")

    # 其他代码保持不变...

    # 加载工作簿
    wb = load_workbook(file_path)
    ws = wb.active

    # 新增：自适应列宽函数（考虑中文字符）
    import re  # 需要添加到文件开头


    def auto_column_width(worksheet):
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter

            for cell in col:
                cell_value = str(cell.value) if cell.value else ""

                # 计算中文字符数（每个占2单位）
                chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', cell_value))
                # 计算其他字符数（每个占1单位）
                other_chars = len(cell_value) - chinese_chars
                # 总宽度计算
                total_width = chinese_chars * 2 + other_chars

                if total_width > max_length:
                    max_length = total_width

            # 设置列宽（基础宽度 + 缓冲值）
            adjusted_width = (max_length + 3) * 1.3  # 可根据实际显示效果调整系数
            worksheet.column_dimensions[col_letter].width = adjusted_width


    # 应用自适应列宽
    auto_column_width(ws)

    # 保存修改后的工作簿
    wb.save(file_path)

    # 自动打开文件代码保持不变...

    # 自动打开文件
    current_platform = platform.system()
    if current_platform == "Windows":
        os.startfile(file_path)
    elif current_platform == "Darwin":  # macOS
        import subprocess
        subprocess.call(('open', file_path))
    elif current_platform == "Linux":
        import subprocess
        subprocess.call(('xdg-open', file_path))
else:
    print("\n无有效数据可保存")