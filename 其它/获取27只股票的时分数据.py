from futu import *
import pandas as pd
import os
from datetime import datetime

# 股票列表
stocks = {
    "中粮糖业": "600737"
}


def convert_stock_code(code):
    """精确转换股票代码（增加北交所支持）"""
    if code.startswith(('6', '9', '688')):  # 沪市
        return f'SH.{code}'
    elif code.startswith(('0', '2', '3', '002', '300')):  # 深市、创业板
        return f'SZ.{code}'
    elif code.startswith(('4', '8')):  # 北交所
        return f'BJ.{code}'
    return None


def convert_ticker_data(data):
    """转换分笔数据格式"""
    if data.empty:
        return pd.DataFrame()

    # 处理含毫秒的时间戳
    data['时间'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d %H:%M:%S')

    # 重命名字段
    data = data.rename(columns={
        'price': '成交价',
        'volume': '成交量',
        'turnover': '成交额'
    })

    # 添加买卖方向标记
    data['方向'] = data['ticker_direction'].apply(
        lambda x: '↑' if x == 'B' else '↓' if x == 'S' else '-'
    )

    # 按需筛选字段
    return data[['时间', '成交价', '成交量', '方向', 'sequence']]


def get_history_tickers(quote_ctx, stock_code, date_str):
    """
    获取历史分笔数据（正确的方法调用）
    参数说明：
    - date_str: 格式为'YYYY-MM-DD'的交易日
    - max_count: 单次最大获取数量（建议不超过100000）
    """
    try:
        # 验证日期有效性（不能超过当前日期）
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if target_date > datetime.now().date():
            print("错误：不能获取未来日期的数据")
            return None

        # 实际接口方法名称是get_history_ticker（注意复数形式）
        ret, data = quote_ctx.get_history_ticker(
            code=stock_code,
            start=date_str,
            end=date_str,
            max_count=100000  # 根据实际需要调整
        )

        if ret == RET_OK:
            return data
        print(f"获取数据失败：{data}")
        return None
    except Exception as e:
        print(f"日期处理错误：{str(e)}")
        return None


def main():
    # 创建行情上下文
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    try:
        # 配置参数
        stock_name = "中粮糖业"
        stock_code = stocks[stock_name]
        target_date = "2023-03-18"  # 修改为实际需要的日期

        # 转换股票代码
        futu_code = convert_stock_code(stock_code)
        if not futu_code:
            print(f"股票代码转换失败：{stock_code}")
            return

        # 获取历史分笔数据
        print(f"正在获取 {stock_name} 的历史分笔数据...")
        raw_data = get_history_tickers(quote_ctx, futu_code, target_date)

        if raw_data is not None and not raw_data.empty:
            # 转换数据格式
            converted_data = convert_ticker_data(raw_data)

            # 输出示例数据
            print(f"\n前10条数据样本：")
            print(converted_data.head(10))
            print(f"\n最后10条数据样本：")
            print(converted_data.tail(10))

            # 保存文件
            output_dir = r"C:\Users\Administrator\Desktop\每日统计改名"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{stock_name}_{target_date.replace('-', '')}_分笔数据.xlsx"
            filepath = os.path.join(output_dir, filename)
            converted_data.to_excel(filepath, index=False)
            print(f"\n数据已保存至：{filepath}")
        else:
            print("未获取到有效数据，可能原因：")
            print("1. 目标日期非交易日")
            print("2. 账户无历史分笔数据权限")
            print("3. 股票代码有误")

    except Exception as e:
        print(f"主程序异常：{str(e)}")
    finally:
        quote_ctx.close()
        print("行情连接已关闭")


if __name__ == "__main__":
    main()