import os
import sys
import zipfile
import ebooklib
import time
from datetime import datetime
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd
from mobi import Mobi


def count_chinese_words(text):
    """统计中文字符（包括中文标点）"""
    return sum(1 for char in text if '\u4e00' <= char <= '\u9fff')


def extract_epub_text(epub_path):
    """从EPUB文件中提取文本"""
    try:
        book = epub.read_epub(epub_path)
        full_text = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text().strip()
                full_text.append(text)
        return ' '.join(full_text), None
    except Exception as e:
        return None, str(e)


def extract_mobi_text(mobi_path):
    """从MOBI文件中提取文本"""
    try:
        with open(mobi_path, 'rb') as f:
            mobi_file = Mobi(f)
            parsed = mobi_file.parse()
            text = BeautifulSoup(parsed['html'], 'html.parser').get_text().strip()
            return text, None
    except Exception as e:
        return None, str(e)


def process_file(file_path):
    """处理单个文件"""
    if file_path.lower().endswith('.epub'):
        text, error = extract_epub_text(file_path)
        if text:
            return '成功', count_chinese_words(text), os.path.getsize(file_path)
        return '失败', 0, os.path.getsize(file_path)
    elif file_path.lower().endswith('.mobi'):
        text, error = extract_mobi_text(file_path)
        if text:
            return '成功', count_chinese_words(text), os.path.getsize(file_path)
        return '失败', 0, os.path.getsize(file_path)
    return '跳过', 0, os.path.getsize(file_path)


def process_folder(folder_path):
    """处理整个文件夹"""
    data = []
    total_files = 0
    processed_files = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            total_files += 1

    start_time = time.time()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            status, word_count, file_size = process_file(file_path)
            data.append({
                '文件名': file,
                '文件路径': file_path,
                '文件大小（字节）': file_size,
                '状态': status,
                '中文字数': word_count
            })
            processed_files += 1

            # 显示进度
            elapsed = time.time() - start_time
            progress = processed_files / total_files
            print(f"\r进度: {processed_files}/{total_files} [{progress:.1%}] 已用时间: {elapsed:.1f}s", end='')

    print()
    df = pd.DataFrame(data)
    # 按中文字数降序排序
    df = df.sort_values(by='中文字数', ascending=False)
    return df


def save_excel(df, output_path):
    """保存到Excel文件"""
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        return True
    except Exception as e:
        print(f"保存失败: {str(e)}")
        return False


def validate_directory(path):
    """验证目录有效性"""
    while True:
        if os.path.isdir(path):
            return os.path.normpath(path)
        print(f"目录不存在: {path}")
        path = input("请输入有效目录路径：").strip('"')


def validate_file_path(path):
    """验证文件路径有效性"""
    while True:
        dir_part = os.path.dirname(path)
        if os.path.isdir(dir_part):
            return os.path.normpath(path)
        print(f"路径不存在: {dir_part}")
        path = input("请输入有效文件路径：").strip('"')


if __name__ == "__main__":
    print("=== EPUB和MOBI电子书中文字数统计工具 ===")
    print("本程序将遍历指定目录下的所有EPUB和MOBI文件并统计中文字数\n")
    default_dir = r"D:\BOOK1\EPUB"
    # 获取输入目录
    input_dir = input(f"请输入要扫描的目录路径（可直接拖拽文件夹到这里，默认: {default_dir}）：").strip('"')
    if not input_dir:
        input_dir = default_dir
    input_dir = validate_directory(input_dir)

    # 获取输出路径
    default_output_file = os.path.join(default_dir, "统计结果.xlsx")
    output_file = input(f"\n请输入结果文件保存路径（示例：D:\\统计结果.xlsx，默认: {default_output_file}）：").strip('"')
    if not output_file:
        output_file = default_output_file
    output_file = validate_file_path(output_file)

    print("\n开始处理...（处理时间视文件数量而定）")
    start_time = time.time()

    try:
        df = process_folder(input_dir)
        success = save_excel(df, output_file)

        if success:
            print(f"\n完成！结果已保存至：{os.path.abspath(output_file)}")
            print(f"总耗时：{time.time() - start_time:.1f}秒")
            print("\n统计摘要：")
            print(f"扫描文件总数：{len(df)}")
            print(f"成功处理文件数：{len(df[df['状态'] == '成功'])}")
            print(f"总中文字数：{df['中文字数'].sum():n}")

            if not df[df['状态'] == '失败'].empty:
                print("\n以下文件处理失败：")
                for row in df[df['状态'] == '失败'].itertuples():
                    print(f"- {row.文件路径}")
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"发生错误：{str(e)}")
    finally:
        input("\n按回车键退出程序...")
