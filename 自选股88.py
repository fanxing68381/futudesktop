from futu import *
import time
import pandas as pd
import os
import subprocess
from openpyxl import load_workbook

# 定义股票列表
stock_codes = [
    "SH.688575", "SH.600737", "SH.600703", "SH.600027", "SZ.300127", "SZ.300003",
    "SH.600161", "SH.600051", "SZ.000768", "SH.600519", "SZ.000717", "SH.600569",
    "SZ.000069", "SH.600031", "SH.601158", "SZ.002460", "SZ.300035", "SH.600970",
    "SH.600195", "SH.600808", "SH.600600", "SZ.000876", "SZ.000031", "SZ.000930",
    "SZ.300121", "SZ.000830", "SZ.000559", "SH.603787", "SZ.002337", "SZ.300054",
    "SH.600309", "SH.603160", "SZ.000725", "SZ.300613", "SH.601939", "SH.600036",
    "SH.601988", "SZ.002230", "SH.601857", "SH.600028", "SZ.002415", "SZ.002594",
    "SH.600050", "SH.601398", "SZ.000333", "SZ.000952", "SH.600372", "SH.600879",
    "SZ.000901", "SZ.000738", "SH.600893", "SZ.002179", "SZ.300397", "SZ.002389",
    "SH.600184", "SZ.300722", "SH.600038", "SH.600210", "SH.601318", "SH.600030",
    "SZ.300496", "SH.601225", "SH.600498", "SH.601003", "SH.600598", "SH.600547",
    "SH.600760", "SH.600795", "SH.600938", "SH.600511", "SH.601728", "SZ.002352",
    "SH.688981", "SH.510050", "SH.510300", "SZ.159841", "SH.688151", "SZ.000338",
    "SH.600690", "SH.600406", "SZ.000617", "SH.601688", "SH.601633", "SH.601995",
    "SH.600150", "SH.600941", "SH.600019", "SH.601899"
]

# 指定输出路径
output_dir = r"D:\30269\每日统计改名"
output_file = os.path.join(output_dir, "自选股88.xlsx")

# 创建目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化数据列表
results = []

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 获取所有股票的基本信息，包括名称
ret, basic_info = quote_ctx.get_stock_basicinfo(Market.SH)  # 上海市场
ret2, basic_info2 = quote_ctx.get_stock_basicinfo(Market.SZ)  # 深圳市场
if ret == RET_OK and ret2 == RET_OK:
    all_basic_info = pd.concat([basic_info, basic_info2])
    stock_name_dict = dict(zip(all_basic_info['code'], all_basic_info['name']))
else:
    stock_name_dict = {}
    print("获取股票基本信息失败，将不显示股票名称")

for code in stock_codes:
    ret, data = quote_ctx.get_capital_flow(code, period_type=PeriodType.INTRADAY)

    if ret == RET_OK:
        if not data.empty:
            last_record = data.iloc[-1]
            result = {
                '股票代码': code,
                '股票名称': stock_name_dict.get(code, '未知'),  # 添加股票名称，找不到时显示'未知'
                '时间': last_record['capital_flow_item_time'],
                '整体净流入(万元)': round(last_record['in_flow'] / 10000, 2)
            }
        else:
            result = {
                '股票代码': code,
                '股票名称': stock_name_dict.get(code, '未知'),
                '时间': 'N/A',
                '整体净流入(万元)': 0
            }
    else:
        result = {
            '股票代码': code,
            '股票名称': stock_name_dict.get(code, '未知'),
            '时间': 'N/A',
            '整体净流入(万元)': '获取失败: ' + str(data)
        }

    results.append(result)
    print(f"处理 {code} 完成")
    time.sleep(1)

quote_ctx.close()

# 创建DataFrame并保存到Excel
df = pd.DataFrame(results)
df = df[['股票代码', '股票名称', '时间', '整体净流入(万元)']]  # 调整列顺序
df.to_excel(output_file, index=False)

# 调整列宽使用openpyxl
wb = load_workbook(output_file)
ws = wb.active

# 设置特定列宽（单位为Excel字符宽度）
column_widths = {
    'A': 15,  # 股票代码
    'B': 20,  # 股票名称
    'C': 20,  # 时间
    'D': 18   # 整体净流入(万元)
}

for col, width in column_widths.items():
    ws.column_dimensions[col].width = width

wb.save(output_file)

# 打开目录和文件
subprocess.Popen(f'explorer "{output_dir}"')
subprocess.Popen(f'start excel "{output_file}"', shell=True)

print(f"数据已保存到 {output_file}")