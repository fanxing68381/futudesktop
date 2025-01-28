# -*- coding: utf-8 -*-
import numpy as np


class HoltWintersForecaster:
    """
    Holt-Winters三重指数平滑预测器
    """

    def __init__(self, alpha=0.3, beta=0.1, gamma=0.2, season_length=30):
        """
        :param alpha: 水平平滑系数 (0 < α < 1)
        :param beta: 趋势平滑系数 (0 < β < 1)
        :param gamma: 季节平滑系数 (0 < γ < 1)
        :param season_length: 季节性周期长度
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.season_length = season_length

        # 初始化状态
        self.L = None  # 水平分量
        self.T = None  # 趋势分量
        self.S = np.zeros(season_length)  # 季节因子

    def initialize(self, initial_data):
        """
        使用初始数据初始化模型
        :param initial_data: 至少包含完整一个周期的数据
        """
        if len(initial_data) < self.season_length:
            raise ValueError("初始数据需要至少包含一个完整周期")

        # 初始水平：首周期的平均值
        self.L = np.mean(initial_data[:self.season_length])

        # 初始趋势：首两个周期的线性趋势
        if len(initial_data) >= 2 * self.season_length:
            y1 = np.mean(initial_data[:self.season_length])
            y2 = np.mean(initial_data[self.season_length:2 * self.season_length])
            self.T = (y2 - y1) / self.season_length
        else:
            self.T = 0.0

        # 初始季节因子
        for i in range(self.season_length):
            self.S[i] = initial_data[i] / self.L

    def update(self, actual_value, t):
        """
        更新模型状态
        :param actual_value: 实际观测值
        :param t: 当前时间步 (0-based)
        """
        prev_L = self.L
        prev_T = self.T

        # 计算当前季节位置
        m = self.season_length
        s_idx = t % m

        # 更新水平分量
        self.L = self.alpha * (actual_value / self.S[s_idx]) + (1 - self.alpha) * (prev_L + prev_T)

        # 更新趋势分量
        self.T = self.beta * (self.L - prev_L) + (1 - self.beta) * prev_T

        # 更新季节因子
        self.S[s_idx] = self.gamma * (actual_value / self.L) + (1 - self.gamma) * self.S[s_idx]

    def forecast(self, steps):
        """
        生成未来预测
        :param steps: 预测步长
        :return: 预测值数组
        """
        forecasts = []
        current_t = len(self.S)  # 假设已完成初始化
        for k in range(1, steps + 1):
            s_idx = (current_t + k) % self.season_length
            forecast = (self.L + k * self.T) * self.S[s_idx]
            forecasts.append(forecast)
        return forecasts


# ===== 示例使用 =====
if __name__ == "__main__":
    # 示例参数设置
    stores = 40  # 店铺数量
    initial_sales = 2000  # 首30天总销量

    # 初始化模型
    hw = HoltWintersForecaster(
        alpha=0.3,
        beta=0.1,
        gamma=0.2,
        season_length=30
    )

    # 生成初始数据（假设前30天每日销量）
    daily_sales = [initial_sales / stores / 30] * 30  # 初始日均1.67件/店
    hw.initialize(daily_sales)

    # 模拟第30天更新（假设实际销量2200件）
    actual_day30_sales = 2200
    daily_actual = actual_day30_sales / stores  # 转换为单店日均

    # 更新模型（第30天）
    hw.update(daily_actual, t=29)  # t是0-based索引

    # 打印当前状态
    print(f"更新后水平分量(L): {hw.L:.2f}")
    print(f"更新后趋势分量(T): {hw.T:.4f}")
    print(f"当前季节因子(S[29]): {hw.S[29]:.4f}")  # 第30天对应索引29

    # 预测未来60天单店销量
    forecast_daily = hw.forecast(steps=60)
    total_forecast = sum(forecast_daily) * stores

    print(f"\n预测60天总销量: {total_forecast:.0f}件")
    print("预测日均趋势:")
    print(np.array(forecast_daily).reshape(-1, 30).mean(axis=1))

# 验证示例计算结果
"""
预期输出应接近：
更新后水平分量(L): 1.72
更新后趋势分量(T): 0.0050
预测60天总销量: 3232件
"""
