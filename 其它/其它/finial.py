from futu import *
import time  # 添加延时避免请求频率过高

# 定义股票列表
stock_codes = ["SH.688575", "SZ.000333","SZ.301269","SZ.300496"]

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

for code in stock_codes:
    ret, data = quote_ctx.get_capital_flow(code, period_type=PeriodType.INTRADAY)

    if ret == RET_OK:
        if not data.empty:
            last_record = data.iloc[-1]
            print(f'\n {code} ')
            print(f"时间：{last_record['capital_flow_item_time']}")
            print(f"整体净流入：{round(last_record['in_flow']/10000,2)} ")

        else:
            print(f"股票 {code} 无有效数据")
    else:
        print(f"获取 {code} 数据失败，错误信息:", data)

    time.sleep(1)  # 每次请求间隔1秒，避免触发API限制

quote_ctx.close()