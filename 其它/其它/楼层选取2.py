import matplotlib.pyplot as plt

# 设置中文字体（确保支持中文显示）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 第一步：输入总楼层数
while True:
    try:
        total_floors = int(input("请输入总楼层数（例如10）："))
        if total_floors > 0:
            break
        else:
            print("楼层数必须大于0，请重新输入！")
    except ValueError:
        print("请输入有效的整数！")

# 第二步：输入已售楼层
sold_floors = set()
print("请输入已售出的楼层（输入完成后输入'结束'）：")
while True:
    floor_input = input("已售楼层（例如1、3等）：")
    if floor_input.lower() == '结束':
        break
    try:
        floor = int(floor_input)
        if 1 <= floor <= total_floors:
            sold_floors.add(floor)
        else:
            print(f"楼层必须在1到{total_floors}之间，请重新输入！")
    except ValueError:
        print("请输入有效的整数！")

# 第三步：输入风水避免的楼层
fengshui_avoid = set()
print("请输入风水上需要避免的楼层（输入完成后输入'结束'）：")
while True:
    floor_input = input("避免的楼层（例如4）：")
    if floor_input.lower() == '结束':
        break
    try:
        floor = int(floor_input)
        if 1 <= floor <= total_floors:
            fengshui_avoid.add(floor)
        else:
            print(f"楼层必须在1到{total_floors}之间，请重新输入！")
    except ValueError:
        print("请输入有效的整数！")

# 第四步：输入最低接受楼层
while True:
    try:
        min_floor = int(input("请输入最低接受的楼层（例如4）："))
        if 1 <= min_floor <= total_floors:
            break
        else:
            print(f"最低楼层必须在1到{total_floors}之间，请重新输入！")
    except ValueError:
        print("请输入有效的整数！")

# 第五步：确认是否排除顶层
exclude_top = input("是否排除顶层？（是/否）：").lower() == '是'
top_floor = total_floors if exclude_top else None

# 计算可选楼层
all_floors = set(range(1, total_floors + 1))
low_floors = set(range(1, min_floor))  # 低于最低楼层的集合
unavailable = sold_floors | fengshui_avoid | low_floors
if top_floor:
    unavailable.add(top_floor)
available_floors = all_floors - unavailable

# 第六步：筛选楼上楼下未售的楼层
suitable_floors = []
for floor in available_floors:
    downstairs = floor - 1
    upstairs = floor + 1
    if (downstairs <= 0 or downstairs not in sold_floors) and (upstairs > total_floors or upstairs not in sold_floors):
        suitable_floors.append(floor)

# 确定推荐楼层（默认选第一个符合条件的）
recommended_floor = suitable_floors[0] if suitable_floors else None

# 生成楼层列表用于绘图
floor_list = list(range(1, total_floors + 1))
colors = []
for floor in floor_list:
    if floor in sold_floors:
        colors.append('red')    # 已售楼层为红色
    elif floor == recommended_floor:
        colors.append('green')  # 推荐楼层为绿色
    else:
        colors.append('blue')   # 待选楼层为蓝色

# 绘制图形
plt.figure(figsize=(6, 8))
for i, floor in enumerate(floor_list):
    plt.barh(i + 1, 1, height=0.8, left=0, color=colors[i], edgecolor='black')
    plt.text(0.5, i + 1, f'第 {floor} 层', ha='center', va='center', color='white', fontsize=12, fontweight='bold')

# 设置图形属性
plt.xlim(0, 1.5)
plt.ylim(0.5, total_floors + 0.5)
plt.xlabel('楼房')
plt.ylabel('楼层')
plt.title(f'{total_floors}层楼房：楼层选择', fontsize=14)
plt.xticks([])

# 添加图例
plt.legend(handles=[
    plt.Rectangle((0, 0), 1, 1, color='red', label='已售楼层'),
    plt.Rectangle((0, 0), 1, 1, color='blue', label='可选楼层'),
    plt.Rectangle((0, 0), 1, 1, color='green', label='推荐楼层')
], loc='upper right')

# 显示图形
plt.grid(False)
plt.tight_layout()
plt.show()

# 输出结果
if recommended_floor:
    print(f"推荐购买的楼层是：第 {recommended_floor} 层")
else:
    print("没有符合条件的楼层！")