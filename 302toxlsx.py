from futu import *
import time
import pandas as pd
import os
import subprocess
from openpyxl import load_workbook

# 定义股票列表
stock_codes = ["SH.600519","SH.601398","SH.600941","SH.601939","SH.601628","SH.601288",
               "SZ.300750","SH.600036","SH.601988","SH.601857","SH.601318","SZ.002594",
               "SH.600938","SZ.000858","SH.601088","SH.600028","SH.600900","SH.601888",
               "SH.601658","SZ.300760","SH.601728","SH.603288","SH.601166","SZ.000333",
               "SH.601328","SH.600809","SH.688981","SH.601012","SZ.002415","SZ.000568",
               "SH.600030","SH.600309","SZ.002352","SZ.002714","SH.601899","SH.601633",
               "SZ.300059","SZ.000001","SH.600276","SH.601998","SZ.002304","SH.603259",
               "SH.601816","SZ.300999","SH.600690","SH.601601","SZ.002475","SH.601319",
               "SH.601668","SZ.300015","SZ.002142","SH.600000","SZ.000002","SH.600887",
               "SZ.300124","SH.601995","SH.601066","SZ.300014","SH.688235","SZ.000651",
               "SH.601138","SH.600048","SH.601225","SH.600438","SH.600436","SH.600406",
               "SH.600188","SH.600104","SH.601818","SH.601919","SH.600905","SZ.300274",
               "SH.601111","SZ.001289","SH.600016","SH.688271","SH.688223","SH.600600",
               "SH.600585","SH.601766","SZ.002460","SH.600050","SH.600009","SZ.000596",
               "SZ.300122","SZ.002459","SH.688599","SH.601390","SH.600029","SZ.003816",
               "SH.600031","SZ.002466","SH.601800","SZ.000725","SH.600019","SZ.300498",
               "SZ.002493","SZ.000792","SH.688111","SH.600018","SZ.300896","SZ.002129",
               "SZ.000625","SZ.000063","SH.601211","SZ.002371","SZ.002812","SH.600025",
               "SZ.000776","SH.600011","SH.603392","SH.601688","SH.600999","SH.601238",
               "SH.600760","SH.601898","SZ.002049","SH.601985",            "SH.600893",
               "SH.600346","SH.600919","SH.601009","SH.601669","SH.601186","SH.600115",
               "SH.688303","SH.600150","SZ.002311","SZ.000166","SH.603993","SZ.001979",
               "SH.601006","SZ.000538","SZ.002027","SH.600196","SH.688041","SH.601881",
               "SH.601868","SZ.002179","SH.603501","SZ.300347","SH.600111","SH.600660",
               "SH.601169","SH.601336","SH.603260","SH.603799","SH.603806","SZ.002709",
               "SZ.000338","SZ.000895","SH.600010","SH.600989","SZ.000301","SZ.000708",
               "SH.600703","SZ.002736","SH.600547","SZ.300316","SH.601229","SH.603195",
               "SH.600015","SZ.000963","SH.601100","SZ.002271","SH.600588","SH.600845",
               "SZ.300759","SH.601989","SH.600886","SH.600221","SH.605117","SH.601808",
               "SZ.002230","SH.688187","SH.600570","SH.601600","SH.600926","SZ.002050",
               "SH.600089","SH.603659","SH.600958","SZ.002180","SH.603833","SH.600795",
               "SZ.000877","SZ.300751","SH.688008","SH.601865","SZ.000617","SZ.002410",
               "SH.600426","SH.605499","SH.688396","SZ.000768","SH.600233","SH.603986",
               "SH.600039","SH.601018","SH.601788","SZ.000661","SH.601607","SZ.300763",
               "SZ.300979","SH.600875","SH.600745","SH.601618","SH.688363","SH.601689",
               "SZ.300450","SZ.300142","SH.603369","SZ.300957","SZ.002938","SZ.000100",
               "SZ.300661","SH.600754","SH.688036","SH.601916","SH.601021","SZ.300782",
               "SH.600132","SH.688012","SH.601727","SH.600085","SH.688180","SH.600362",
               "SZ.000733","SZ.002920","SH.601127","SZ.300408","SH.601877","SZ.000425",
               "SH.600256","SH.601615","SH.688385","SZ.000876","SZ.002001","SZ.002241",
               "SH.600026","SH.600515","SH.600027","SH.601825","SZ.300413","SH.603290",
               "SH.601838","SZ.000938","SZ.002821","SZ.300628","SH.600522","SH.600176",
               "SH.600741","SZ.300033","SH.600674","SH.600702","SZ.300433","SZ.002074",
               "SH.601901","SZ.002648","SZ.002603","SH.688032","SH.603899","SH.601991",
               "SH.688009","SH.601699","SH.600803","SH.603198","SH.601377","SH.600332",
               "SZ.301269","SH.603688","SH.601117","SH.600763","SH.601698","SH.688126",
               "SZ.000983","SH.603605","SH.603345","SH.688063","SZ.300454","SZ.001965",
               "SZ.300496","SZ.000157","SH.600460","SH.601360","SZ.002202","SZ.000999",
               "SH.601155","SH.600383","SH.603939","SH.688777","SH.603606","SH.601872",
               "SH.600765","SH.600023","SZ.002601","SZ.300919","SH.688114","SH.688122",
               "SH.600372","SZ.300003"]

# 指定输出路径
output_dir = r"D:\30269"
output_file = os.path.join(output_dir, "302.xlsx")

# 创建目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化数据列表
results = []

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 获取所有股票的基本信息，包括名称
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

    if ret == RET_OK:
        if not data.empty:
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
df = df[['股票代码', '股票名称', '时间', '整体净流入(万元)']]
df.to_excel(output_file, index=False)

# 调整列宽
wb = load_workbook(output_file)
ws = wb.active
column_widths = {'A': 15, 'B': 20, 'C': 20, 'D': 18}
for col, width in column_widths.items():
    ws.column_dimensions[col].width = width
wb.save(output_file)

# 文件打开新顺序
try:
    # 优先打开统计文件
    existing_file = r'E:\图片\市值300每日统计.xlsm'
    subprocess.Popen(f'start excel "{existing_file}"', shell=True)
    print(f"已打开基准文件: {existing_file}")

    # 延迟0.5秒确保顺序
    time.sleep(0.5)

    # 打开新生成文件
    subprocess.Popen(f'start excel "{output_file}"', shell=True)
    print(f"已生成新文件: {output_file}")

    # 打开输出目录
    subprocess.Popen(f'explorer "{output_dir}"')

except Exception as e:
    print(f"文件打开异常: {str(e)}")

print(f"数据处理完成，保存路径: {output_file}")