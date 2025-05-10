import os
import time
import pyautogui
from pygetwindow import getWindowsWithTitle

# ============= 必须配置的坐标参数 =============
# 通过坐标校准工具获取以下关键坐标：
SEARCH_BOX_POS = (2500, 20)  # 搜索框点击坐标（需手动校准）
CLEAR_ICON_POS = (2500, 20)  # 搜索框清除按钮坐标（小叉图标）
STOCK_PAGE_CHECK_POS = (600, 400)  # 页面加载标识坐标（如600027区域）
# =============================================

# ============= 运行时参数 ================
STOCK_LIST =["688575","600737","600703","600027","300127","300003","600161","600051",
             "000768","600519","000717","600569","000069","600031","601158","002460",
             "300035","600970","600195","600808","600600","000876","000031","000930",
             "300121","000830","000559","603787","002337","300054","600309","603160",
             "000725","300613","601939","600036","601988","002230","601857","600028",
             "002415","002594","600050","601398","000333","000952","600372","600879",
             "000901","000738","600893","002179","300397","002389","600184","300722",
             "600038","600210","601318","600030","300496","601225","600498","601003",
             "600598","600547","600760","600795","600938","600511","601728","002352",
             "688981","510050","510300","159841","688151","000338","600690","600406",
             "000617","601688","601633","601995","600150","600941","600019","601899"]

FUTU_WINDOW_TITLE = "富途牛牛"
SCREENSHOT_REGION = (0, 0, 3840, 2160)  # (x,y,width,height)
SAVE_DIR = r"E:\图片\A股资金历史记录\2025A股资金历史记录\2025年05月A股资金历史记录\2025年05月12日A股资金历史记录"  # ← 新增路径定义


# ========================================

def get_futu_window():
    """精确获取窗口对象"""
    wins = [w for w in getWindowsWithTitle(FUTU_WINDOW_TITLE) if w.visible]
    if not wins:
        raise Exception("窗口未找到，请：1.保持窗口可见 2.标题包含'富途牛牛'")
    window = wins[0]
    if window.isMinimized:
        window.restore()
    return window


def force_click(pos, clicks=1):
    """强制执行鼠标点击"""
    x, y = pos
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click(clicks=clicks, interval=0.2)


def capture_stock_screenshots():
    # 初始化环境
    os.makedirs(SAVE_DIR, exist_ok=True)
    futu_win = get_futu_window()
    current_date = time.strftime("%Y-%m-%d")  # 获取当前日期

    for idx, stock in enumerate(STOCK_LIST, start=1):  # 使用enumerate生成序号
        try:
            # ==== 阶段1：准备搜索环境 ====
            futu_win.activate()
            time.sleep(0.4)

            # 物理点击搜索框（比快捷键更可靠）
            force_click(SEARCH_BOX_POS)
            time.sleep(0.4)

            # 清空历史记录（通过点击清除按钮）
            force_click(CLEAR_ICON_POS)
            time.sleep(0.4)

            # ==== 阶段2：输入股票代码 ====
            pyautogui.write(stock)
            time.sleep(0.4)
            pyautogui.press("enter")
            print(f"已输入 {stock} 等待加载...")

            # ==== 阶段3：智能等待 ====
            # 方式一：颜色轮询检测（检测价格区域刷新）
            for _ in range(20):  # 最多等待10秒
                r, g, b = pyautogui.pixel(*STOCK_PAGE_CHECK_POS)
                # 如果颜色不是灰色底色（假设加载完成区域变白）
                if (r, g, b) != (240, 240, 240):
                    break
                time.sleep(0.4)
            else:
                raise Exception("页面加载超时")

            # ==== 阶段4：精确截图 ====
            # 偏移截图范围（需配合窗口位置）
            win_left, win_top = futu_win.left, futu_win.top
            region = (
                win_left + SCREENSHOT_REGION[0],
                win_top + SCREENSHOT_REGION[1],
                SCREENSHOT_REGION[2],
                SCREENSHOT_REGION[3]
            )

            # 生成带日期和序号的文件名
            filename = os.path.join(SAVE_DIR, f"{current_date}_${idx}.png")  # 修改此行
            pyautogui.screenshot(filename, region=region)
            print(f"√ 成功截图：{filename}")

        except Exception as e:
            print(f"! {stock} 处理失败：{str(e)}")
            continue


if __name__ == "__main__":
    pyautogui.PAUSE = 0.5  # 降低操作速率为人类可识别
    capture_stock_screenshots()
 # 新增打开Z盘目录指令（在原有E盘目录基础上修改盘符）
    #z_save_dir = SAVE_DIR.replace("E:", "Z:", 1)
    os.startfile(SAVE_DIR)    # 原始E盘目录
    #os.startfile(z_save_dir)  # 新增Z盘目录