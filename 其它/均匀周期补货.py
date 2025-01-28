# 参数设定
initial_trend_factor = 2000 / (40 * 30)  # 1.67件/店/天
seasonal_cycle = 30  # 季节性周期 30天
alpha = 0.3  # 平滑系数
beta = 0.1   # 平滑系数
gamma = 0.2  # 季节性平滑系数（未在示例中直接用到）

# 预测步骤：
def calculate_forecast(actual_sales_day_30, initial_trend_factor, alpha, beta):
    # 计算基线水平L₃₀
    L_30 = alpha * (actual_sales_day_30 / 40) + (1 - alpha) * (initial_trend_factor + 0)  # 初始趋势项T₀ = 0
    # 更新趋势项T₃₀
    T_30 = beta * (L_30 - initial_trend_factor) + (1 - beta) * 0  # 初始趋势项T₀ = 0
    # 计算季节性因子S₃₀
    S_30 = 1  # 假设季节性因子为1，具体计算可能需要更多的数据

    # 预测未来60天销量
    forecast = 40 * ((L_30 + 60 * T_30) * S_30)
    return forecast

# 第30天实际销量 = 2200件（即日均1.83件/店）
actual_sales_day_30 = 2200  # 实际销量

# 计算预测销量
forecast_60_days = calculate_forecast(actual_sales_day_30, initial_trend_factor, alpha, beta)

# 输出预测销量
print(f"预测未来60天的销量为：{forecast_60_days:.2f}件")
