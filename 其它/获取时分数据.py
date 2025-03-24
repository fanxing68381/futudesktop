# 导入必要模块：time用于控制程序休眠，futu用于富途证券API操作
import time
from futu import *

# 自定义实时分时数据处理类，继承自富途的RTDataHandlerBase基类
class RTDataTest(RTDataHandlerBase):
    # 重写响应接收方法，当收到服务器推送时会自动调用此方法
    def on_recv_rsp(self, rsp_pb):
        # 调用父类方法解析响应数据，返回状态码和数据内容
        ret_code, data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        # 错误处理：当返回码不为成功时打印错误信息
        if ret_code != RET_OK:
            print("RTDataTest: error, msg: %s" % data)
            return RET_ERROR, data
        # 成功时打印实时分时数据（可在此处添加自定义处理逻辑）
        print("RTDataTest ", data)
        return RET_OK, data

# 创建行情上下文对象，连接本地运行的OpenD服务（需提前启动富途客户端）
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 实例化自定义的实时数据处理对象
handler = RTDataTest()

# 将自定义处理器绑定到行情上下文，用于接收分时数据推送
quote_ctx.set_handler(handler)

# 订阅股票列表的实时分时数据（SubType.RT_DATA 表示分时数据类型）
ret, data = quote_ctx.subscribe([
    "SH.600737",  # 沪市股票代码（600737）
    "SZ.000876",  # 深市主板股票（000876）
    "SH.600372",  # 沪市股票
    "SZ.000617",  # 深市股票
    "SZ.002594",  # 深市中小板股票（002开头）
    "SH.601899",  # 沪市股票
    "SH.600406",
    "SH.600938",
    "SH.600019",
    "SH.600027",
    "SH.600547",
    "SH.601318",  # 中国平安
    "SH.600031",  # 三一重工
    "SZ.002352",  # 顺丰控股
    "SH.600690",  # 青岛海尔
    "SZ.000338",  # 潍柴动力
    "SH.600808",  # 马钢股份
    "SH.601633",  # 长城汽车
    "SH.601688",  # 华泰证券
    "SH.601995",  # 中金公司
    "SH.600030",  # 中信证券
    "SH.600941",  # 中国移动
    "SH.600150",  # 中国船舶
    "SZ.300127",  # 创业板股票（300开头）
    "SZ.300003",  # 乐普医疗
    "SH.688151",  # 科创板股票（688开头）
    "SH.688981"   # 中芯国际
], [SubType.RT_DATA])  # 订阅分时数据类型

# 检查订阅结果
if ret == RET_OK:
    print(data)  # 打印订阅成功信息
else:
    print('error:', data)  # 打印错误信息

# 保持连接15秒以接收实时数据（可根据需要调整时长）
time.sleep(15)

# 关闭行情连接（OpenD会在1分钟后自动取消订阅）
quote_ctx.close()