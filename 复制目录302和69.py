import shutil
import os


def copy_file_with_retry(src_path, dst_path):
    while True:
        try:
            # 复制文件并验证完整性
            shutil.copy2(src_path, dst_path)

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


def main():
    src_dir = r"D:\30269"
    dst_dir = r"Z:\30269"
    files = ["302.xlsx", "69.xlsx"]

    # 创建目标目录（如果不存在）
    os.makedirs(dst_dir, exist_ok=True)

    for file in files:
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)

        if not os.path.exists(src_path):
            print(f"源文件不存在: {src_path}")
            continue

        print(f"正在复制: {file}")
        if copy_file_with_retry(src_path, dst_path):
            print(f"成功复制: {file}")
        else:
            print(f"放弃复制: {file}")


if __name__ == "__main__":
    main()