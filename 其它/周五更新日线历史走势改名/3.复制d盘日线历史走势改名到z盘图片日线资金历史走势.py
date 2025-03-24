import os
import shutil
from datetime import datetime
import time
import ctypes

# 配置路径
source_dir = r'E:\图片\日线资金历史走势'
target_dir = r'Z:\图片\日线资金历史走势'
record_file = 'copied_files.txt'

MAX_RETRIES = 3
DELAY_TIME = 5

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


def debug_log(msg):
    """带时间戳的调试日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {msg}")


def is_admin():
    """检查是否以管理员身份运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def validate_network_drive(path):
    """验证网络驱动器是否已连接"""
    if path.startswith(r"Z:"):
        if not os.path.exists(path):
            debug_log("尝试重新连接网络驱动器...")
            try:
                # 示例：使用net use命令连接网络驱动器（需替换实际参数）
                os.system(r'net use Z: \\192.168.1.100\share /user:username password')
                time.sleep(5)  # 等待驱动器连接
            except Exception as e:
                raise RuntimeError(f"网络驱动器连接失败: {str(e)}")
    return os.path.exists(path)


def validate_environment():
    """增强型环境验证"""
    debug_log("=== 开始环境验证 ===")

    # 检查管理员权限
    if not is_admin():
        debug_log("警告：未以管理员身份运行，可能影响网络驱动器操作")

    # 验证源目录
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"源目录不存在: {source_dir}")
    debug_log(f"源目录验证通过: {os.path.abspath(source_dir)}")

    # 验证目标目录（网络驱动器特殊处理）
    try:
        if not validate_network_drive(target_dir):
            raise FileNotFoundError(f"目标目录不可访问: {target_dir}")

        # 创建目标目录（如果不存在）
        os.makedirs(target_dir, exist_ok=True)
        debug_log(f"目标目录验证通过: {os.path.abspath(target_dir)}")

        # 写入测试文件
        test_file = os.path.join(target_dir, 'permission_test.tmp')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('权限测试文件，可安全删除')
        os.remove(test_file)
        debug_log("目标目录写入权限验证通过")
    except Exception as e:
        raise RuntimeError(f"目标目录验证失败: {str(e)}")


def get_valid_filename(filename):
    """处理可能存在的非法字符（防御性编程）"""
    return filename.replace('/', '_').replace('\\', '_')


def copy_files_with_report():
    """带详细日志的文件同步"""
    try:
        validate_environment()
    except Exception as e:
        debug_log(f"环境验证失败: {str(e)}")
        raise

    success_list = []
    fail_list = []
    copied_files = set()

    # 加载历史记录文件
    record_path = os.path.abspath(record_file)
    debug_log(f"历史记录文件路径: {record_path}")
    if os.path.exists(record_path):
        try:
            with open(record_path, 'r', encoding='utf-8') as f:
                copied_files = set(line.strip() for line in f)
            debug_log(f"已加载 {len(copied_files)} 条历史记录")
        except Exception as e:
            debug_log(f"读取历史记录失败: {str(e)}")

    start_time = datetime.now()
    debug_log(f"=== 开始文件同步，共 {len(stock_files)} 个文件 ===")

    for index, filename in enumerate(stock_files, 1):
        file_start = time.time()
        clean_name = get_valid_filename(filename)
        debug_log(f"正在处理 ({index}/{len(stock_files)})：{clean_name}")

        src_path = os.path.join(source_dir, clean_name)
        dst_path = os.path.join(target_dir, clean_name)

        # 跳过已记录文件（但验证实际存在）
        if clean_name in copied_files:
            if os.path.exists(dst_path):
                success_list.append(clean_name)
                debug_log(f"跳过已记录且存在的文件: {clean_name}")
                continue
            else:
                debug_log(f"记录存在但目标文件缺失: {clean_name}，重新复制")

        # 源文件验证
        if not os.path.exists(src_path):
            error = f"源文件不存在: {os.path.abspath(src_path)}"
            debug_log(error)
            fail_list.append((clean_name, error))
            continue

        # 复制操作
        retry = 0
        while retry < MAX_RETRIES:
            try:
                debug_log(f"尝试复制 ({retry + 1}/{MAX_RETRIES})")

                # 确保目标目录存在
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                # 执行复制
                shutil.copy2(src_path, dst_path)

                # 验证复制结果
                if not os.path.exists(dst_path):
                    raise FileNotFoundError("目标文件未创建")

                # 大小验证（考虑大文件情况）
                src_size = os.path.getsize(src_path)
                dst_size = os.path.getsize(dst_path)
                if abs(src_size - dst_size) > 1024:  # 允许1KB误差
                    raise ValueError(f"大小差异超过阈值 | 源: {src_size}字节 目标: {dst_size}字节")

                # 内容校验（简单首字节验证）
                with open(src_path, 'rb') as f_src, open(dst_path, 'rb') as f_dst:
                    if f_src.read(1) != f_dst.read(1):
                        raise ValueError("文件首字节不一致")

                # 更新记录
                with open(record_path, 'a', encoding='utf-8') as f:
                    f.write(f"{clean_name}\n")

                success_list.append(clean_name)
                debug_log(f"复制成功，耗时 {time.time() - file_start:.2f}s")
                break

            except Exception as e:
                retry += 1
                error_msg = str(e)
                debug_log(f"复制失败: {error_msg}")

                # 清理不完整文件
                if os.path.exists(dst_path):
                    try:
                        os.remove(dst_path)
                        debug_log("已清理不完整文件")
                    except Exception as clean_error:
                        debug_log(f"清理失败: {str(clean_error)}")

                if retry < MAX_RETRIES:
                    time.sleep(DELAY_TIME)
                else:
                    fail_list.append((clean_name, f"最终失败: {error_msg}"))
                    debug_log(f"文件同步失败，总耗时 {time.time() - file_start:.2f}s")

        # 增加操作间隔
        time.sleep(1)

    # 生成最终报告
    debug_log("=== 生成同步报告 ===")
    print(f"\n{'=' * 40} 文件同步报告 {'=' * 40}")
    print(f"执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {datetime.now() - start_time}")
    print(f"文件总数: {len(stock_files)}")
    print(f"成功数量: {len(success_list)}")
    print(f"失败数量: {len(fail_list)}")

    if fail_list:
        print("\n失败详情：")
        for i, (name, err) in enumerate(fail_list, 1):
            print(f"{i}. {name}")
            print(f"   {err}")

    # 验证目标目录内容
    try:
        copied_count = len([f for f in os.listdir(target_dir) if f.endswith('.xls')])
        print(f"\n目标目录实际文件数：{copied_count}个XLS文件")
    except Exception as e:
        print(f"\n目标目录验证失败：{str(e)}")


if __name__ == '__main__':
    try:
        if not is_admin():
            print("建议：请以管理员身份运行以确保网络驱动器访问权限")

        print("正在启动文件同步程序...")
        copy_files_with_report()

        # 保持窗口打开
        input("\n操作完成，按回车键查看目标目录...")
        os.startfile(target_dir)
    except Exception as e:
        print(f"\n发生关键错误：{str(e)}")
        input("按回车键退出...")