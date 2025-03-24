import time
from futu import *



class RTDataHandler(RTDataHandlerBase):
    def __init__(self):
        self.target_time = "15:00:00"  # 指定目标时间
        self.data_received = False  # 标记是否已捕获数据

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super().on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print(f"RTData 错误: {data}")
            return RET_ERROR, data

        # 遍历实时数据条目
        for item in data:
            # 获取当前数据时间（假设字段名为 'time'，需根据实际响应字段调整）
            current_time = datetime.now().strftime("%H:%M:%S")
            # 或者从 item 中直接获取时间（例如 item.update_time）

            # 检查是否到达目标时间
            if current_time >= self.target_time and not self.data_received:
                print(f"捕获到目标时间 {self.target_time} 的成交额:")
                print(f"股票代码: {item.code}, 成交额: {item.amount}")
                self.data_received = True  # 标记已捕获

        return RET_OK, data


# 连接富途行情服务
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# 订阅股票列表
symbols = ["SZ.688981"]

# 设置回调处理器
handler = RTDataHandler()
quote_ctx.set_handler(handler)

# 订阅实时分时数据
ret, err_msg = quote_ctx.subscribe(symbols, [SubType.RT_DATA])
if ret != RET_OK:
    print(f"订阅失败: {err_msg}")
    quote_ctx.close()
    exit()

# 持续运行直到捕获目标时间或超时
start_time = time.time()
timeout = 3600  # 最长等待1小时（根据需要调整）

while not handler.data_received and (time.time() - start_time) < timeout:
    now = datetime.now().strftime("%H:%M:%S")
    if now >= handler.target_time:
        # 主动查询一次确保捕获（可选）
        ret, snapshot = quote_ctx.get_market_snapshot(symbols)
        if ret == RET_OK:
            for stock in snapshot:
                print(f"主动查询 {stock.code} 成交额: {stock.amount}")
        break
    time.sleep(1)  # 每秒检查一次

# 关闭连接
quote_ctx.close()
print("连接已关闭")