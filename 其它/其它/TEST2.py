import time
from datetime import datetime  # 新增导入模块
from futu import *


class RTDataTest(RTDataHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("RTDataTest: error, msg: %s" % data)
            return RET_ERROR, data

        # 新增时间过滤逻辑：仅处理15:00:00前的数据
        current_time = data.get('time', '')
        if current_time >= "15:00:00":
            return RET_OK, data  # 超过时间直接返回不打印

        print("RTDataTest ", data)
        return RET_OK, data


# 创建连接（保持原样）
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
handler = RTDataTest()
quote_ctx.set_handler(handler)

# 订阅目标股票（保持原样）
ret, data = quote_ctx.subscribe([
    "SZ.300127",  # 创业板股票（300开头）
    "SZ.300003",  # 乐普医疗
    "SH.688151",  # 科创板股票（688开头）
    "SH.688981"  # 中芯国际
], [SubType.RT_DATA])

if ret == RET_OK:
    print("订阅成功:", data)
else:
    print('订阅失败:', data)

# 动态计算到15:00:00的等待时间（核心修改）
now = datetime.now().time()
target_time = datetime.strptime("15:00:00", "%H:%M:%S").time()

# 计算剩余秒数（处理跨天情况）
if now <= target_time:
    wait_seconds = (datetime.combine(datetime.today(), target_time) -
                    datetime.combine(datetime.today(), now)).seconds
else:
    wait_seconds = 1 # 如果当前时间已过15点，立即关闭

time.sleep(wait_seconds + 1)  # 多等1秒确保覆盖边界
quote_ctx.close()
print("连接已在15:00:00准时关闭")