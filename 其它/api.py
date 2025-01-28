from futu import *
import pandas as pd
import time
import os
from datetime import datetime

# 股票列表
stocks = {
    "中粮糖业": "600737",
    "中油资本": "000617",
    "华电国际": "600027",
    "山东黄金": "600547",
    "中国海油": "600938",
    "中国平安": "601318",
    "三一重工": "600031",
    "顺丰控股": "002352",
    "新希望": "000876",
    "潍柴动力": "000338",
    "海尔智家": "600690",
    "国电南瑞": "600406",
    "华泰证券": "601688",
    "长城汽车": "601633",
    "马钢股份": "600808",
    "中芯国际": "688981",
    "华强科技": "300427",
    "银河磁体": "300127",
    "中航电子": "600372",
    "中金公司": "601995",
    "中信证券": "600030",
    "中国船舶": "600150",
    "中国移动": "600941",
    "乐普医疗": "300003",
    "宝钢股份": "600019",
    "紫金矿业": "601899",
    "比亚迪": "002594"
}


def convert_stock_code(code):
    """精确转换股票代码"""
    if code.startswith(('6', '9', '688')):  # 沪市及科创板
        return f'SH.{code}'
    elif code.startswith(('0', '2', '3', '002', '300')):  # 深市、中小板、创业板
        return f'SZ.{code}'
    elif code.startswith('4'):  # 北交所
        return f'BJ.{code}'
    return None


def convert_data(data):
    # 转换时间格式
    data['时间'] = pd.to_datetime(data['time']).dt.strftime('%H:%M:%S')
    # 重命名列
    data = data.rename(columns={'price': '成交', 'volume': '现手'})
    # 根据交易方向添加箭头
    data['现手'] = data.apply(
        lambda row: f"{row['现手']}↑" if row['交易方向'] == '买入' else f"{row['现手']}↓" if row[
                                                                                                 '交易方向'] == '卖出' else f"{row['现手']}--",
        axis=1)
    # 增加笔数列，值为 1
    data['笔数'] = 1
    return data[['时间', '成交', '现手', '笔数']]


def test_stock_ticker_data(quote_ctx, stock_name, stock_code):
    futu_code = convert_stock_code(stock_code)
    if not futu_code:
        print(f"代码转换失败：{stock_code}")
        return 0

    try:
        print(f"尝试订阅 {futu_code} 的分笔数据...")
        # 订阅分笔数据
        ret_sub = quote_ctx.subscribe(futu_code, SubType.TICKER)
        print(f"订阅返回结果类型: {type(ret_sub)}, 返回结果: {ret_sub}")

        # 根据订阅状态判断是否订阅成功
        sub_status = quote_ctx.query_subscription()
        if sub_status[0] == RET_OK and futu_code in sub_status[1]['sub_list'].get(SubType.TICKER, []):
            print(f"成功订阅 {futu_code} 的分笔数据")
            # 等待数据推送
            print("等待 5 秒，让数据有足够时间推送...")
            time.sleep(5)
            # 获取分笔数据
            print(f"尝试获取 {futu_code} 的分笔数据...")
            ret, data = quote_ctx.get_rt_ticker(futu_code, 10)
            print(f"获取分笔数据返回结果类型: {type(ret)}, 返回结果: {ret}, 数据: {data}")
            if ret == RET_OK:
                if not data.empty:
                    # 打印数据的列名
                    print("分笔数据的列名：", data.columns)
                    # 添加交易方向列
                    data['交易方向'] = data['ticker_direction'].apply(
                        lambda x: '买入' if x == 'B' else '卖出' if x == 'S' else '未知')
                    # 转换数据格式
                    converted_data = convert_data(data)
                    print("成功获取到分笔数据，转换后数据如下：")
                    print(converted_data)

                    # 保存文件
                    output_dir = r"C:\Users\Administrator\Desktop\每日统计改名"
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    filename = f"资金{stock_name}_10_{date_str}.xlsx"
                    filepath = os.path.join(output_dir, filename)
                    converted_data.to_excel(filepath, index=False)
                    print(f"成功保存文件：{filepath}")
                    return 1
                else:
                    print("未获取到有效的分笔数据。")
            else:
                print(f"获取 {futu_code} 的分笔数据失败，错误信息：{data}")
        else:
            print(f"订阅 {futu_code} 的分笔数据失败，错误码: {ret_sub[0]}，错误信息: {ret_sub[1]}")
            print(f"当前订阅状态: {sub_status}")
    except Exception as e:
        print(f"处理 {futu_code} 时发生异常：{e}")
    finally:
        # 取消订阅
        print(f"取消订阅 {futu_code} 的分笔数据...")
        quote_ctx.unsubscribe(futu_code, SubType.TICKER)
    return 0


def get_stock_basic_info(quote_ctx, market, security_type):
    try:
        # 获取股票基本信息
        ret, data = quote_ctx.get_stock_basicinfo(market, security_type)
        if ret == RET_OK:
            print(f"成功获取 {market} 市场 {security_type} 类型的基本信息：{data}")
        else:
            print(f"获取 {market} 市场 {security_type} 类型的基本信息失败，错误信息：{data}")
    except Exception as e:
        print(f"发生异常：{e}")


if __name__ == "__main__":
    # 创建行情上下文对象
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    file_count = 0
    try:
        # 获取股票基本信息
        get_stock_basic_info(quote_ctx, Market.SZ, SecurityType.STOCK)

        for stock_name, stock_code in stocks.items():
            file_count += test_stock_ticker_data(quote_ctx, stock_name, stock_code)
    except Exception as e:
        print(f"发生全局异常：{e}")
    finally:
        # 关闭上下文
        print("关闭行情上下文...")
        quote_ctx.close()
        print(f"一共生成了 {file_count} 个 .xlsx 文件。")
