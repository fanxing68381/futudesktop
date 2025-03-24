import baostock as bs
import pandas as pd
import os
import sys
import subprocess
from datetime import datetime
import xlwt

# 股票名称与代码映射
stock_code_map = {
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

# 手动上市日期补充
manual_listed_dates = {
    "600737": "1996-12-09",
    "000617": "1996-06-26",
    "600027": "2005-02-03",
    "600547": "2003-08-28",
    "600938": "2022-04-21",
    "601318": "2004-06-24",
    "600031": "2003-07-03",
    "002352": "2017-02-24",
    "000876": "1998-03-11",
    "000338": "2007-04-30",
    "600690": "1993-11-19",
    "600406": "2003-10-16",
    "601688": "2010-02-26",
    "601633": "2011-09-28",
    "600808": "1994-01-06",
    "688981": "2020-07-16",
    "300427": "2022-06-30",
    "300127": "2010-03-26",
    "600372": "1997-06-26",
    "601995": "2019-11-01",
    "600030": "2003-01-06",
    "600150": "1998-05-20",
    "600941": "2022-01-05",
    "300003": "2009-10-30",
    "600019": "2000-12-12",
    "601899": "2008-04-25",
    "002594": "2011-06-30"
}

# 输出完整股票列表
print("\n当前股票列表:")
for name, code in stock_code_map.items():
    print(f"{name}: {code}")

# 保存路径设置
save_dir = r"C:\Users\Administrator\Desktop\日线历史走势改名"
os.makedirs(save_dir, exist_ok=True)

print(f"数据将保存到目录: {save_dir}")


def check_dependencies():
    """检查并安装必要依赖库"""
    # 只检查 baostock 和 xlwt
    required = {'baostock', 'xlwt'}
    installed = {pkg for pkg in required if pkg in sys.modules}
    missing = required - installed
    if missing:
        print(f"检测到缺少必要库 {missing}，正在尝试自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + list(missing))
            print("依赖安装成功")
        except subprocess.CalledProcessError as e:
            print(f"自动安装失败，请手动执行：pip install {' '.join(missing)}\n错误信息: {str(e)}")
            sys.exit(1)


def get_full_code(stock_code):
    """生成带交易所前缀的完整股票代码"""
    if stock_code.startswith(("6", "5", "9")):
        return f"sh.{stock_code}"
    elif stock_code.startswith(("0", "2", "3")):
        return f"sz.{stock_code}"
    else:
        raise ValueError(f"未知的股票代码格式: {stock_code}")


def process_data(df):
    """数据清洗处理"""
    df = df.replace('', pd.NA).dropna(how='all')

    column_mapping = {
        'date': '时间',
        'open': '开盘',
        'high': '最高',
        'low': '最低',
        'close': '收盘',
        'pctChg': '涨幅',
        'turn': '换手%',
        'volume': '总手',
        'amount': '金额'
    }
    df = df.rename(columns=column_mapping)

    try:
        price_cols = ['开盘', '最高', '最低', '收盘']
        for col in price_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

        df['总手'] = pd.to_numeric(df['总手'], errors='coerce').mul(1).fillna(0).astype(int)
        df['金额'] = pd.to_numeric(df['金额'], errors='coerce').mul(1).round(0)

        prev_close = df['收盘'].shift(1).replace(0, pd.NA)
        df['振幅'] = ((df['最高'] - df['最低']) / prev_close).fillna(0)

        df['涨幅'] = pd.to_numeric(df['涨幅'], errors='coerce').fillna(0) / 100
        df['换手%'] = pd.to_numeric(df['换手%'], errors='coerce').fillna(0).round(2)

    except Exception as e:
        print(f"数据处理异常: {str(e)}")

    df['时间'] = df['时间'].apply(convert_weekday)
    # 过滤掉总手为 0 的行
    df = df[df['总手'] != 0]
    return df[['时间', '开盘', '最高', '最低', '收盘', '涨幅', '振幅', '总手', '金额', '换手%']]


def convert_weekday(date_str):
    """添加中文星期"""
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
        chinese_weekday = ['一', '二', '三', '四', '五', '六', '日']
        return f"{date_str},{chinese_weekday[date_obj.weekday()]}"
    except:
        return date_str


def save_to_excel(df, save_path, sheet_name):
    """保存数据到Excel（完整覆盖）"""
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)

    percent_style = xlwt.XFStyle()
    percent_style.num_format_str = '0.00%'
    decimal_style = xlwt.XFStyle()
    decimal_style.num_format_str = '0.00'

    headers = df.columns.tolist()
    for col, header in enumerate(headers):
        sheet.write(0, col, header)

    for row_idx, row_data in enumerate(df.values, 1):
        for col_idx, value in enumerate(row_data):
            if headers[col_idx] in ['涨幅', '振幅']:
                sheet.write(row_idx, col_idx, value, percent_style)
            elif headers[col_idx] == '换手%':
                sheet.write(row_idx, col_idx, value, decimal_style)
            else:
                sheet.write(row_idx, col_idx, value)

    col_widths = {
        0: 5000, 1: 3000, 2: 3000, 3: 3000,
        4: 3000, 5: 3000, 6: 3000, 7: 5000,
        8: 5000, 9: 3000
    }
    for col, width in col_widths.items():
        sheet.col(col).width = width

    workbook.save(save_path)


def get_listed_date(full_code):
    """获取股票的上市日期"""
    stock_code = full_code.split('.')[1]
    if stock_code in manual_listed_dates:
        return manual_listed_dates[stock_code]
    try:
        rs = bs.query_stock_basic(code=full_code)
        if rs.error_code == '0':
            data_list = []
            while rs.next():
                data_list.append(rs.get_row_data())
            if data_list:
                return data_list[0][3]
        else:
            print(f"获取 {stock_code} 上市日期时出错，错误代码: {rs.error_code}，错误信息: {rs.error_msg}")
    except Exception as e:
        print(f"获取 {stock_code} 上市日期时发生异常: {str(e)}")
    return None


def main():
    check_dependencies()

    bs.login()

    # 让用户输入结束日期
    while True:
        end_date = input("请输入结束日期（格式：YYYY-MM-DD）：")
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            break
        except ValueError:
            print("日期格式不正确，请重新输入。")

    print(f"最终选择的日期为: {end_date}")

    total = len(stock_code_map)
    for idx, (stock_name, stock_code) in enumerate(stock_code_map.items(), 1):
        try:
            print(f"\n处理进度 ({idx}/{total}): {stock_name}")
            full_code = get_full_code(stock_code)
            filename = f"{stock_name}日线历史走势.xls"
            file_path = os.path.join(save_dir, filename)

            # 获取上市日期
            start_date = get_listed_date(full_code)
            if not start_date:
                print(f"|-- 无法获取 {stock_name} 的上市日期，跳过")
                continue

            # 获取新数据
            rs = bs.query_history_k_data_plus(
                code=full_code,
                fields="date,open,high,low,close,volume,amount,turn,pctChg",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                # 修改为除权数据
                adjustflag="3"
            )

            new_data = []
            while (rs.error_code == '0') & rs.next():
                new_data.append(rs.get_row_data())

            if not new_data:
                print(f"|-- 无新数据")
                continue

            # 处理新数据
            new_df = process_data(pd.DataFrame(new_data, columns=rs.fields))
            print(f"|-- 获取到{len(new_df)}条新数据")

            # 读取现有数据
            existing_df = pd.DataFrame()
            if os.path.exists(file_path):
                try:
                    existing_df = pd.read_excel(file_path, engine='xlrd')
                    existing_df = existing_df[new_df.columns]  # 对齐列顺序
                except Exception as e:
                    print(f"|-- 读取失败，将覆盖文件: {str(e)}")

            # 合并数据（直接追加）
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)

            # 保存数据
            save_to_excel(combined_df, file_path, f"{stock_name}日线历史走势")
            print(f"|-- 成功保存，总数据量：{len(combined_df)}条")

        except Exception as e:
            print(f"|-- 处理失败: {str(e)}")
            continue

    bs.logout()
    print("\n处理完成！")
    input("按回车键退出...")


if __name__ == "__main__":
    main()
