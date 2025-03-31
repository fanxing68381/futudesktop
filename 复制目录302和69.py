import shutil
import os
import time


def copy_file_with_retry(src_path, dst_path):
    while True:
        try:
            source_size = os.path.getsize(src_path)
            copied_size = 0
            buffer_size = 1024 * 1024

            with open(src_path, 'rb') as src, open(dst_path, 'wb') as dst:
                while True:
                    data = src.read(buffer_size)
                    if not data:
                        break
                    dst.write(data)
                    copied_size += len(data)
                    progress = (copied_size / source_size) * 100
                    print(f"已拷贝 {copied_size} 字节，进度: {progress:.2f}%")

            # 检查文件是否完整复制
            if os.path.getsize(src_path) == os.path.getsize(dst_path):
                return True

            # 如果大小不一致则主动抛出异常
            os.remove(dst_path)
            raise RuntimeError("文件大小不一致，可能未完整复制")

        except Exception as e:
            print(f"复制出错: {str(e)}")

            # 清理可能残留的不完整文件
            if os.path.exists(dst_path):
                try:
                    os.remove(dst_path)
                except:
                    pass

            # 用户选择是否重试
            retry = input("是否重新尝试复制？(y/n): ").strip().lower()
            if retry != 'y':
                return False


def load_copied_files(record_file):
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            return set(line.strip() for line in f)
    return set()


def save_copied_file(record_file, file):
    with open(record_file, 'a') as f:
        f.write(file + '\n')


def get_file_time(path):
    try:
        mtime = os.path.getmtime(path)
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    except Exception:
        return "未知"


def main():
    src_dir = r"D:\30269"
    dst_dir = r"Z:\30269"
    files = ["302.xlsx", "69.xlsx"]
    record_file = 'copied_files.txt'

    # 每次运行自动删除记录文件
    if os.path.exists(record_file):
        os.remove(record_file)

    # 创建目标目录（如果不存在）
    os.makedirs(dst_dir, exist_ok=True)

    copied_files = load_copied_files(record_file)

    for file in files:
        if file in copied_files:
            print(f"跳过已复制的文件: {file}")
            continue

        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)

        if not os.path.exists(src_path):
            print(f"源文件不存在: {src_path}")
            continue

        src_time = get_file_time(src_path)
        print(f"源文件 {src_path} 创建/修改时间: {src_time}")

        if os.path.exists(dst_path):
            dst_time = get_file_time(dst_path)
            print(f"目标文件 {dst_path} 创建/修改时间: {dst_time}")
            overwrite = input("目标文件已存在，是否覆盖复制？(y/n): ").strip().lower()
            if overwrite != 'y':
                print(f"放弃复制: {file}")
                continue

        print(f"正在复制: {file}")
        if copy_file_with_retry(src_path, dst_path):
            print(f"成功复制: {file}")
            save_copied_file(record_file, file)
        else:
            print(f"放弃复制: {file}")


if __name__ == "__main__":
    main()
    