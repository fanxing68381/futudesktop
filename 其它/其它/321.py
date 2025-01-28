import pandas as pd
import os
from datetime import datetime, timedelta


def excel_num_to_date(n):
    """将Excel序列号转换为日期（处理Excel 1900闰年错误）"""
    if pd.isna(n):
        return None
    try:
        n = int(n)
        if n > 60:
            n -= 1  # 修正Excel的闰年错误
        return (datetime(1899, 12, 30) + timedelta(days=n)).strftime("%Y-%m-%d")
    except:
        return None


def process_sheet(sheet_name, df, base_path):
    """处理单个工作表"""
    month = f"{int(sheet_name):02d}"
    for row_idx, row in df.iloc[:, 20:43].iterrows():  # U列到AQ列
        dates = [excel_num_to_date(x) for x in row if not pd.isna(x)]

        # 获取股票信息（根据实际数据结构调整索引）
        stock_info = df.iloc[row_idx, 0:5].dropna().values

        if len(dates) == 0 or len(stock_info) < 3:
            continue

        for date_str in dates:
            if not date_str or len(date_str) != 10:
                continue

            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                if dt.year != 2028:
                    continue
            except:
                continue

            # 构建路径（使用os.path处理路径兼容性）
    save_path = os.path.join(
        base_path,
        "2028A股资金历史记录",
        f"2028年{month}月A股资金历史记录",
        f"2028年{month}月{dt.day:02d}日A股资金历史记录"
    )

    os.makedirs(save_path, exist_ok=True)

    # 构建bat内容（使用GBK编码保证中文兼容性）
    bat_content = [
        "@echo off",
        f"ren _{stock_info[0]}.png {stock_info[1]}_{stock_info[2]}.png",
        "exit"
    ]

    try:
        with open(os.path.join(save_path, "change name.bat"), "w", encoding="gbk") as f:
            f.write("\n".join(bat_content))
    except Exception as e:
        print(f"文件写入失败：{str(e)}")


if __name__ == "__main__":
    # 使用原始字符串处理Windows路径
    base_dir = r"C:\Users\Administrator\Desktop\日线历史走势改名"
    excel_path = os.path.join(base_dir, "2028A股资金历史记录(删除周末) - 副本.xlsx")

    try:
        xls = pd.ExcelFile(excel_path)

        # 处理所有01-12的工作表
        valid_sheets = [s for s in xls.sheet_names if s.isdigit() and 1 <= int(s) <= 12]

        for sheet in valid_sheets:
            df = pd.read_excel(xls, sheet_name=sheet, header=None)
            process_sheet(sheet, df, base_dir)

        print("处理完成！生成目录结构：")
        print(f"请检查：{base_dir}\\2028A股资金历史记录\\...")

    except FileNotFoundError:
        print(f"错误：文件不存在 {excel_path}")
        print("请确认：")
        print("1. 文件名称是否与代码中的完全一致（包括空格和符号）")
        print("2. 文件是否存在于桌面目录：C:\\Users\\Administrator\\Desktop\\日线历史走势改名")
    except Exception as e:
        print(f"运行时错误：{str(e)}")
