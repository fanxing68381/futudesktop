import shutil
import os


def get_folder_stats(folder):
    """
    获取文件夹的文件数量和总大小。
    """
    file_count = 0
    total_size = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_count += 1
            total_size += os.path.getsize(file_path)
    return file_count, total_size


def get_file_dict(folder):
    """
    获取文件夹中所有文件的相对路径和大小的字典。
    """
    files_dict = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder)
            size = os.path.getsize(file_path)
            files_dict[relative_path] = size
    return files_dict


def copy_file_with_error_handling(src_path, dst_path):
    """
    复制单个文件，处理可能的错误。
    """
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    try:
        shutil.copy2(src_path, dst_path)
        return True
    except Exception as e:
        print(f"复制文件失败 {src_path} 到 {dst_path}: {str(e)}")
        return False


def copy_folder_with_retry(source, destination):
    """
    复制文件夹，失败时仅重试未复制的文件。
    """
    # 确保目标文件夹存在
    if not os.path.exists(destination):
        os.makedirs(destination)

    while True:
        try:
            # 获取源文件夹统计信息
            source_file_count, source_total_size = get_folder_stats(source)
            print(f"源文件夹 '{source}' 有 {source_file_count} 个文件，总大小 {source_total_size} 字节。")

            # 获取源和目标文件的字典
            source_files = get_file_dict(source)
            destination_files = get_file_dict(destination)

            # 找到需要复制的文件（源中有但目标中没有，或大小不匹配）
            files_to_copy = []
            for rel_path, src_size in source_files.items():
                dst_path = os.path.join(destination, rel_path)
                if rel_path not in destination_files or destination_files.get(rel_path, 0) != src_size:
                    files_to_copy.append(rel_path)

            if not files_to_copy:
                print("所有文件已成功复制，无需进一步操作。")
                dest_file_count, dest_total_size = get_folder_stats(destination)
                print(f"目标文件夹 '{destination}' 有 {dest_file_count} 个文件，总大小 {dest_total_size} 字节。")
                return True

            print(f"需要复制的文件：{files_to_copy}")

            # 尝试复制每个需要复制的文件
            all_successful = True
            for rel_path in files_to_copy:
                src_path = os.path.join(source, rel_path)
                dst_path = os.path.join(destination, rel_path)
                if not copy_file_with_error_handling(src_path, dst_path):
                    all_successful = False

            # 验证复制结果
            if compare_folders(source, destination):
                dest_file_count, dest_total_size = get_folder_stats(destination)
                print(f"目标文件夹 '{destination}' 有 {dest_file_count} 个文件，总大小 {dest_total_size} 字节。")
                print("复制验证成功。")
                return True
            else:
                print("验证失败。文件夹不匹配。")
                all_successful = False

            if all_successful:
                return True

        except Exception as e:
            print(f"复制过程出错: {str(e)}")

        # 询问是否重试
        retry = input("是否重新尝试复制？(y/n): ").strip().lower()
        if retry != 'y':
            return False


def compare_folders(source, destination):
    """
    比较两个文件夹的内容，确保文件路径和大小一致。
    """
    return get_file_dict(source) == get_file_dict(destination)


def main():
    """
    主函数，处理多个文件夹对的复制。
    """
    # 定义文件夹对
    folder_pairs = [
        (
            r"E:\图片\A股资金历史记录\2025A股资金历史记录\2025年03月A股资金历史记录\2025年03月11日A股资金历史记录",
            r"Z:\图片\A股资金历史记录\2025A股资金历史记录\2025年03月A股资金历史记录\2025年03月11日A股资金历史记录"),
        (
            r"E:\图片\港股资金历史记录\2025港股资金历史记录\2025年03月港股资金历史记录\2025年03月11日港股资金历史记录",
            r"Z:\图片\港股资金历史记录\2025港股资金历史记录\2025年03月港股资金历史记录\2025年03月11日港股资金历史记录"),
        (
            r"E:\图片\美股资金历史记录\2025美股资金历史记录\2025年03月美股资金历史记录\2025年03月11日美股资金历史记录",
            r"Z:\图片\美股资金历史记录\2025美股资金历史记录\2025年03月美股资金历史记录\2025年03月11日美股资金历史记录"),
        (
            r"E:\图片\市值300资金历史记录\2025市值A股资金历史记录\2025年03月市值300A股资金历史记录\2025年03月11日市值300A股资金历史记录",
            r"Z:\图片\市值300资金历史记录\2025市值A股资金历史记录\2025年03月市值300A股资金历史记录\2025年03月11日市值300A股资金历史记录"),
        (
            r"E:\图片\中特估69资金历史记录\2025中特估69资金历史记录\2025年03月中特估69资金历史记录\2025年03月11日中特估69A股资金历史记录",
            r"Z:\图片\中特估69资金历史记录\2025中特估69资金历史记录\2025年03月中特估69资金历史记录\2025年03月11日中特估69A股资金历史记录")
    ]

    # 处理每个文件夹对
    for source, destination in folder_pairs:
        if not os.path.exists(source):
            print(f"源文件夹不存在: {source}")
            continue
        print(f"正在复制文件夹对: {source} 到 {destination}")
        if copy_folder_with_retry(source, destination):
            print(f"成功复制: {source} 到 {destination}")
        else:
            print(f"放弃复制: {source} 到 {destination}")


if __name__ == "__main__":
    main()