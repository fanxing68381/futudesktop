import math
import matplotlib.pyplot as plt
import numpy as np

# 设置 matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体，支持中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def horizon_distance(height_km):
    """
    计算飞行器在特定高度时能看到的最远水平距离
    参数:
    height_km - 飞行器高度（单位：公里）
    返回值:
    distance_km - 最远可见距离（单位：公里）
    """
    # 地球平均半径（单位：公里）
    earth_radius_km = 6371

    # 检查输入高度是否有效
    if height_km < 0:
        return "高度不能为负数"

    # 将高度转换为米计算
    height_m = height_km * 1000
    earth_radius_m = earth_radius_km * 1000

    # 计算最远距离（单位：米）
    distance_m = math.sqrt(2 * earth_radius_m * height_m + height_m ** 2)

    # 转换为公里
    distance_km = distance_m / 1000

    return distance_km


def plot_horizon_diagram(height_km, distance_km):
    """
    绘制地球曲率和视线范围的示意图
    参数:
    height_km - 飞行器高度（公里）
    distance_km - 最远可见距离（公里）
    """
    # 地球半径
    R = 6371

    # 创建角度数组用于绘制地球弧
    theta = np.linspace(-np.pi / 4, np.pi / 4, 100)
    x_earth = R * np.cos(theta)
    y_earth = R * np.sin(theta) + R

    # 飞行器位置
    x_aircraft = 0
    y_aircraft = R + height_km

    # 地平线两端点（简化表示）
    x_horizon1 = -distance_km
    x_horizon2 = distance_km
    y_horizon = R

    # 绘制图形
    plt.figure(figsize=(8, 8))
    plt.plot(x_earth, y_earth, 'b-', label='地球表面')
    plt.plot(x_aircraft, y_aircraft, 'ro', label='飞行器位置')
    plt.plot([x_aircraft, x_horizon1], [y_aircraft, y_horizon], 'g--', label='视线')
    plt.plot([x_aircraft, x_horizon2], [y_aircraft, y_horizon], 'g--')

    # 添加标注
    plt.text(x_aircraft, y_aircraft + 50, f'高度 = {height_km} km', ha='center')
    plt.text(x_horizon1, y_horizon - 100, f'距离 = {distance_km:.2f} km', ha='right')
    plt.text(x_horizon2, y_horizon - 100, f'距离 = {distance_km:.2f} km', ha='left')

    # 设置图形属性
    plt.title("飞行器高度与地平线距离示意图")
    plt.xlabel("水平距离 (km)")
    plt.ylabel("高度 (km)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # 保持比例
    plt.show()


def main():
    try:
        # 获取用户输入的高度（公里）
        height_km = float(input("请输入飞行器的高度（单位：公里）："))

        # 计算可见距离
        result = horizon_distance(height_km)

        if isinstance(result, str):
            print(result)
        else:
            print(f"在 {height_km} 公里高度时，最远可见距离约为 {result:.2f} 公里")
            # 绘制示意图
            plot_horizon_diagram(height_km, result)

    except ValueError:
        print("请输入有效的数字")


if __name__ == "__main__":
    main()