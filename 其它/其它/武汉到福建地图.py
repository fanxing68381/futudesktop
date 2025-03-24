import folium
import requests
from geopy.geocoders import Nominatim

# 坐标点配置（纬度,经度）
locations = [
    {"name": "武汉", "pos": [30.5928, 114.3055], "day": "Day0", "cost": "出发地"},
    {"name": "庐山风景区", "pos": [29.5555, 115.9953], "day": "Day1", "cost": "700元"},
    {"name": "武夷山景区", "pos": [27.7566, 118.0264], "day": "Day2-3", "cost": "1890元"},
    {"name": "奇达村", "pos": [26.3684, 119.6812], "day": "Day4", "cost": "345元"},
    {"name": "平潭岛", "pos": [25.5031, 119.7833], "day": "Day5", "cost": "1405元"}
]


def get_osrm_route(start, end):
    """获取两点之间的驾驶路径（增强错误处理）"""
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full"
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            print(f"请求失败：HTTP状态码 {res.status_code}")
            return None, None
        data = res.json()
        if not isinstance(data, dict):
            print("响应数据格式错误：预期字典类型")
            return None, None
        if data.get('code') != 'Ok':
            print(f"路径规划失败：{data.get('message', '未知错误')}")
            return None, None
        # 检查路径数据是否可用
        if 'routes' not in data or len(data['routes']) < 1 or 'geometry' not in data['routes'][0]:
            print("路径数据不完整")
            return None, None
        route_coords = [
            [coord[1], coord[0]]  # 转换为(纬度,经度)
            for coord in data['routes'][0]['geometry']['coordinates']
        ]
        distance = round(data['routes'][0]['distance'] / 1000, 1)
        return route_coords, distance
    except Exception as e:
        print(f"网络请求或数据解析异常：{str(e)}")
        return None, None


# 创建地图（改用OpenStreetMap确保路径可见）
m = folium.Map(location=[28.15, 117.0], zoom_start=5, tiles='openstreetmap')

# 添加路径图层（添加颜色循环）
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
for i in range(len(locations) - 1):
    start = locations[i]["pos"]
    end = locations[i + 1]["pos"]
    route_coords, distance = get_osrm_route(start, end)

    if route_coords:
        # 绘制带箭头路径
        folium.PolyLine(
            locations=route_coords,
            color=colors[i % 4],
            weight=3,
            popup=f"<b>{locations[i]['name']} → {locations[i + 1]['name']}</b><br>\
                   里程：{distance}公里<br>\
                   日期：{locations[i + 1]['day']}",
            opacity=0.8
        ).add_to(m)
        print(f"已生成路径：{locations[i]['name']}→{locations[i + 1]['name']} ({distance}km)")  # 调试输出

# 添加标记点（表格化弹窗）
for loc in locations:
    html_table = f"""
    <table style="width:200px">
        <tr><th colspan="2">{loc['name']}</th></tr>
        <tr><td>📅日期</td><td>{loc['day']}</td></tr>
        <tr><td>💰消费</td><td>{loc['cost']}</td></tr>
    </table>
    """
    folium.Marker(
        location=loc["pos"],
        popup=folium.Popup(html_table, max_width=250),
        icon=folium.Icon(color='red' if loc['day'] == 'Day0' else 'cadetblue', icon='info-sign')
    ).add_to(m)

# 保存地图
m.save('fixed_fujian_roadtrip.html')
print("修复版地图已生成，请用浏览器打开 fixed_fujian_roadtrip.html")
