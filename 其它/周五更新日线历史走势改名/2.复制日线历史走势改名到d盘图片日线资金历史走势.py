import os
import shutil
from datetime import datetime

# 配置路径
source_dir = r'C:\Users\Administrator\Desktop\日线历史走势改名'
target_dir = r'E:\图片\日线资金历史走势'

# 股票文件列表
stock_files = [
    '国电南瑞日线历史走势.xls', '华电国际日线历史走势.xls', '海尔智家日线历史走势.xls',
    '乐普医疗日线历史走势.xls', '华强科技日线历史走势.xls', '山东黄金日线历史走势.xls',
    '顺丰控股日线历史走势.xls', '中国海油日线历史走势.xls', '三一重工日线历史走势.xls',
    '潍柴动力日线历史走势.xls', '新希望日线历史走势.xls', '银河磁体日线历史走势.xls',
    '中国平安日线历史走势.xls', '中粮糖业日线历史走势.xls', '中芯国际日线历史走势.xls',
    '中油资本日线历史走势.xls', '华泰证券日线历史走势.xls', '长城汽车日线历史走势.xls',
    '马钢股份日线历史走势.xls', '中航电子日线历史走势.xls', '中金公司日线历史走势.xls',
    '中信证券日线历史走势.xls', '中国船舶日线历史走势.xls', '中国移动日线历史走势.xls',
    '宝钢股份日线历史走势.xls', '紫金矿业日线历史走势.xls', '比亚迪日线历史走势.xls'
]


def copy_files_with_report():
    # 创建目标目录（如果不存在）
    os.makedirs(target_dir, exist_ok=True)

    success_list = []
    fail_list = []

    start_time = datetime.now()
    print(f"\n{'=' * 30} 开始文件复制 {'=' * 30}")

    for filename in stock_files:
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(target_dir, filename)

        try:
            # 执行文件复制（自动覆盖）
            shutil.copy2(src_path, dst_path)
            success_list.append(filename)
            print(f"[✓] 成功复制: {filename}")
        except Exception as e:
            fail_list.append((filename, str(e)))
            print(f"[×] 失败文件: {filename} | 错误信息: {str(e)}")

    # 生成统计报告
    print(f"\n{'=' * 30} 执行结果报告 {'=' * 30}")
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {datetime.now() - start_time}")
    print(f"文件总数: {len(stock_files)}")
    print(f"成功数量: {len(success_list)}")
    print(f"失败数量: {len(fail_list)}")

    if success_list:
        print("\n成功文件列表:")
        for i, name in enumerate(success_list, 1):
            print(f"{i}. {name}")

    if fail_list:
        print("\n失败文件明细:")
        for i, (name, err) in enumerate(fail_list, 1):
            print(f"{i}. {name}")
            print(f"   错误类型: {err}")


if __name__ == '__main__':
    copy_files_with_report()
    print(f"\n{'=' * 30} 操作执行完成 {'=' * 30}")