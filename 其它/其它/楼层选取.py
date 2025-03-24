import matplotlib.pyplot as plt

# 设置中文字体（确保系统支持中文字体，例如 SimHei）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 字体支持中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 定义楼层总数和状态
total_floors = 10
sold_floors = {1, 3, 5, 9}  # 已售楼层
recommended_floor = 7        # 推荐楼层

# 生成所有楼层列表
all_floors = list(range(1, total_floors + 1))

# 定义颜色
colors = []
for floor in all_floors:
    if floor in sold_floors:
        colors.append('red')    # 已售楼层为红色
    elif floor == recommended_floor:
        colors.append('green')  # 推荐楼层为绿色
    else:
        colors.append('blue')   # 待选楼层为蓝色

# 创建图形
plt.figure(figsize=(6, 8))  # 设置图形大小

# 绘制每层楼的矩形
for i, floor in enumerate(all_floors):
    plt.barh(i + 1, 1, height=0.8, left=0, color=colors[i], edgecolor='black')
    plt.text(0.5, i + 1, f'第 {floor} 层', ha='center', va='center', color='white', fontsize=12, fontweight='bold')

# 设置图形属性
plt.xlim(0, 1.5)
plt.ylim(0.5, total_floors + 0.5)
plt.xlabel('楼房')
plt.ylabel('楼层')
plt.title('10层楼房：楼层选择', fontsize=14)

# 移除 x 轴刻度（不需要宽度刻度）
plt.xticks([])

# 添加图例
plt.legend(handles=[
    plt.Rectangle((0, 0), 1, 1, color='red', label='已售楼层'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='可选楼层'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='推荐楼层')
], loc='upper right')

# 显示图形
plt.grid(False)  # 关闭网格
plt.tight_layout()
plt.show()

# 输出推荐楼层
print(f"推荐购买的楼层是：第 {recommended_floor} 层")