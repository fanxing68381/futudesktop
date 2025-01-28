import shutil
import os

local_appdata = os.getenv('LOCALAPPDATA')
gen_py_path = os.path.join(local_appdata, 'Temp', 'gen_py')

if os.path.exists(gen_py_path):
    try:
        shutil.rmtree(gen_py_path)
        print("成功清除 win32com 缓存")
    except Exception as e:
        print(f"清除缓存时出现错误: {e}")
else:
    print("未找到 win32com 缓存目录")