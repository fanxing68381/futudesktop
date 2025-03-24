import os
import re
from datetime import datetime
from glob import glob

# ============== 配置区 ==============
PYTHON_FILES_DIR = r""
BAT_FILES_DIR = r"C:\Users\Administrator\Desktop\每日统计改名"


# ===================================

class DateUpdater:
    def __init__(self):
        self.date_info = None
        self.modified_files = []

    def parse_date(self, input_str):
        """增强版日期解析，支持容错"""
        try:
            clean_str = re.sub(r"\D", "", input_str)  # 移除非数字字符
            if len(clean_str) != 8:
                raise ValueError("日期长度必须为8位数字")

            self.date_info = {
                "year": int(clean_str[:4]),
                "month": f"{int(clean_str[4:6]):02d}",
                "day": f"{int(clean_str[6:8]):02d}",
                "ymd": f"{clean_str[:4]}-{clean_str[4:6]}-{clean_str[6:8]}",
                "chs_date": f"{clean_str[:4]}年{clean_str[4:6]}月{clean_str[6:8]}日"
            }
            return True
        except Exception as e:
            print(f"日期解析失败: {str(e)}")
            return False

    def generate_python_path(self, stock_type):
        """动态生成Python文件保存路径"""
        path_templates = {
            "中特估69股": [
                r"D:\图片\中特估69资金历史记录",
                r"{year}中特估69资金历史记录",
                r"{year}年{month}月中特估69资金历史记录",
                r"{year}年{month}月{day}日中特估69A股资金历史记录"
            ],
            "港股": [
                r"D:\图片\港股资金历史记录",
                r"{year}港股资金历史记录",
                r"{year}年{month}月港股资金历史记录",
                r"{year}年{month}月{day}日港股资金历史记录"
            ],
            "A股": [
                r"D:\图片\A股资金历史记录",
                r"{year}A股资金历史记录",
                r"{year}年{month}月A股资金历史记录",
                r"{year}年{month}月{day}日A股资金历史记录"
            ],
            "302股": [
                r"D:\图片\市值300资金历史记录",
                r"{year}市值A股资金历史记录",
                r"{year}年{month}月市值300A股资金历史记录",
                r"{year}年{month}月{day}日市值300A股资金历史记录"
            ],
            "59个美股": [
                r"D:\图片\美股资金历史记录",
                r"{year}美股资金历史记录",
                r"{year}年{month}月美股资金历史记录",
                r"{year}年{month}月{day}日美股资金历史记录"
            ]
        }

        parts = [p.format(**self.date_info) for p in path_templates[stock_type]]
        return os.path.join(*parts)

    def update_python_file(self, file_path, stock_type):
        """深度处理Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 生成新旧路径
            new_save_dir = self.generate_python_path(stock_type)
            old_pattern = re.compile(
                r'SAVE_DIR\s*=\s*r["\'](.*?)["\']',
                re.DOTALL
            )
            match = old_pattern.search(content)

            if not match:
                print(f"未找到SAVE_DIR定义: {os.path.basename(file_path)}")
                return False

            old_save_dir = match.group(1)
            if old_save_dir == new_save_dir:
                print(f"[跳过] 路径未变化: {os.path.basename(file_path)}")
                return False

            # 执行替换
            new_content = content.replace(old_save_dir, new_save_dir)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # 记录修改并打印详情
            self.modified_files.append(file_path)
            print("\n" + "=" * 60)
            print(f"成功更新: {os.path.basename(file_path)}")
            print("旧路径结构:")
            print("\n".join(old_save_dir.split("\\")[-3:]))
            print("\n新路径结构:")
            print("\n".join(new_save_dir.split("\\")[-3:]))
            print("=" * 60)
            return True

        except Exception as e:
            print(f"处理失败 {os.path.basename(file_path)}: {str(e)}")

            return False

    def update_bat_files(self):
        """处理所有bat文件（包含新增需求）"""
        bat_files = glob(os.path.join(BAT_FILES_DIR, "*.bat"))
        for bat_path in bat_files:
            try:
                with open(bat_path, 'r', encoding='gbk') as f:
                    content = f.read()

                # 同时替换多种日期格式
                patterns = [
                    (r"\d{4}-\d{2}-\d{2}", self.date_info["ymd"]),  # 标准日期
                    (r"\d{4}年\d{2}月\d{2}日", self.date_info["chs_date"])  # 中文日期
                ]

                modified = False
                for pattern, replacement in patterns:
                    new_content, count = re.subn(pattern, replacement, content)
                    if count > 0:
                        content = new_content
                        modified = True

                if modified:
                    with open(bat_path, 'w', encoding='gbk') as f:
                        f.write(content)
                    self.modified_files.append(bat_path)
                    print(f"成功更新: {os.path.basename(bat_path)}")
                else:
                    print(f"[跳过] 未修改: {os.path.basename(bat_path)}")

            except Exception as e:
                print(f"处理失败 {os.path.basename(bat_path)}: {str(e)}")


def main():
    updater = DateUpdater()

    # 输入日期
    while True:
        input_date = input("请输入8位日期(例如20260201): ").strip()
        if updater.parse_date(input_date):
            break

    # 处理Python文件
    py_files = {
        "中特估69股": glob(os.path.join(PYTHON_FILES_DIR, "*中特估69股*.py"))[0],
        "港股": glob(os.path.join(PYTHON_FILES_DIR, "*港股*.py"))[0],
        "A股": glob(os.path.join(PYTHON_FILES_DIR, "*A股*.py"))[0],
        "302股": glob(os.path.join(PYTHON_FILES_DIR, "*302股*.py"))[0],
        "59个美股": glob(os.path.join(PYTHON_FILES_DIR, "*美股*.py"))[0]
    }

    for stock_type, path in py_files.items():
        updater.update_python_file(path, stock_type)

    # 处理bat文件
    updater.update_bat_files()

    # 生成报告
    print("\n" + "=" * 60)
    print(f"操作完成！共修改 {len(updater.modified_files)} 个文件")
    print("修改清单:")
    for i, f in enumerate(updater.modified_files, 1):
        print(f"{i}. {os.path.basename(f)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
