# 导入 win32com.client 模块，该模块允许 Python 程序与 Windows 系统上的 COM（Component Object Model）组件进行交互
# COM 是一种微软的技术，用于实现软件组件之间的通信和交互，这里主要用于与 Excel 等 Office 应用程序进行交互
import win32com.client
# 导入 shutil 模块，它提供了许多高级的文件和目录操作功能，这里主要使用其中的 rmtree 函数来删除整个目录树
import shutil

# 获取 gen_py 缓存路径
# win32com.client.gencache 是 win32com 库中用于管理 COM 类型库缓存的模块
# GetGeneratePath() 方法用于获取存储生成的 Python 包装器（用于与 COM 对象交互）的目录路径
# 这些生成的包装器会被缓存起来，以便后续快速访问 COM 对象
gen_py_path = win32com.client.gencache.GetGeneratePath()

# 删除整个 gen_py 目录
try:
    # shutil.rmtree() 函数用于递归地删除指定目录及其所有子目录和文件
    # 这里将之前获取的 gen_py 缓存目录删除，目的是清除可能存在的旧的或损坏的 COM 类型库缓存
    shutil.rmtree(gen_py_path)
    # 如果删除成功，打印提示信息，告知用户缓存目录已被清除
    print(f"已清除缓存目录: {gen_py_path}")
except Exception as e:
    # 如果在删除过程中出现异常（例如目录不存在、权限不足等）
    # 捕获该异常并打印错误信息，告知用户清除缓存失败以及具体的错误原因
    print(f"清除缓存失败: {e}")

# 重新初始化 COM 对象
# win32com.client.Dispatch() 方法用于创建一个指定的 COM 对象实例
# 这里创建了一个 Excel 应用程序的 COM 对象实例，后续可以使用该对象来操作 Excel 软件，如打开、创建、编辑 Excel 文件等
excel = win32com.client.Dispatch("Excel.Application")