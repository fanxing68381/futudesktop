from futu import *
import time
import pandas as pd
import os
import subprocess
from openpyxl import load_workbook

# 定义股票列表
stock_codes = ["SH.601857", "SH.600938", "SH.600028", "SH.600339", "SH.600941", "SH.601728",
               "SH.600050", "SH.600498", "SH.601398", "SH.601939", "SH.601288", "SH.601988",
               "SH.601658", "SH.601328", "SH.601998", "SH.601818", "SH.601088", "SH.601898",
               "SZ.002128", "SZ.002415", "SZ.002230", "SH.600845", "SH.603019", "SZ.000066",
               "SH.600271", "SZ.002368", "SH.600131", "SH.601668", "SH.601390", "SH.601800",
               "SH.601186", "SH.601669", "SH.601868", "SH.601618", "SH.601117", "SZ.000032",
               "SH.600970", "SH.601611", "SH.601816", "SH.601919", "SH.601006", "SZ.001965",
               "SZ.001872", "SH.601866", "SH.601598", "SH.601319", "SH.601881", "SZ.000617",
               "SH.600406", "SH.601179", "SZ.003816", "SH.600011", "SH.601985", "SH.600025",
               "SH.600886", "SH.600019", "SZ.000898", "SZ.000778", "SZ.000761", "SH.600150",
               "SH.601698", "SH.601989", "SH.600685", "SH.600118", "SH.601600", "SH.600489",
               "SZ.000999", "SH.600511", "SZ.000028"]

# 指定输出路径
output_dir = r"D:\30269"
output_file = os.path.join(output_dir, "69.xlsx")

# 创建目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化数据列表
results = []

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 获取股票基本信息
ret, basic_info = quote_ctx.get_stock_basicinfo(Market.SH)
ret2, basic_info2 = quote_ctx.get_stock_basicinfo(Market.SZ)
if ret == RET_OK and ret2 == RET_OK:
    all_basic_info = pd.concat([basic_info, basic_info2])
    stock_name_dict = dict(zip(all_basic_info['code'], all_basic_info['name']))
else:
    stock_name_dict = {}
    print("获取股票基本信息失败，将不显示股票名称")

# 获取资金流数据
for code in stock_codes:
    ret, data = quote_ctx.get_capital_flow(code, period_type=PeriodType.INTRADAY)

    if ret == RET_OK and not data.empty:
        last_record = data.iloc[-1]
        result = {
            '股票代码': code,
            '股票名称': stock_name_dict.get(code, '未知'),
            '时间': last_record['capital_flow_item_time'],
            '整体净流入(万元)': round(last_record['in_flow'] / 10000, 2)
        }
    else:
        result = {
            '股票代码': code,
            '股票名称': stock_name_dict.get(code, '未知'),
            '时间': 'N/A',
            '整体净流入(万元)': 0 if ret == RET_OK else '获取失败'
        }

    results.append(result)
    print(f"处理 {code} 完成")
    time.sleep(1)

quote_ctx.close()

# 创建DataFrame并保存
df = pd.DataFrame(results)[['股票代码', '股票名称', '时间', '整体净流入(万元)']]
df.to_excel(output_file, index=False)

# 调整列宽
wb = load_workbook(output_file)
ws = wb.active
column_widths = {'A': 15, 'B': 20, 'C': 20, 'D': 18}
for col, width in column_widths.items():
    ws.column_dimensions[col].width = width
wb.save(output_file)

# 打开文件（按新顺序）
try:
    # 先打开现有统计文件
    existing_file = r'E:\图片\中特估69每日统计.xlsm'
    subprocess.Popen(f'start excel "{existing_file}"', shell=True)
    print(f"已优先打开：{existing_file}")

    # 短暂延迟确保顺序
    time.sleep(0.5)

    # 再打开新生成文件
    subprocess.Popen(f'start excel "{output_file}"', shell=True)
    print(f"已打开新文件：{output_file}")

    # 打开目录
    subprocess.Popen(f'explorer "{output_dir}"')

except Exception as e:
    print(f"文件打开异常：{str(e)}")

print(f"数据处理完成，保存路径：{output_file}")