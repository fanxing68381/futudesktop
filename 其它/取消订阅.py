from futu import *
import time
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

print('current subscription status :', quote_ctx.query_subscription())  # 查询初始订阅状态
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE, SubType.TICKER], subscribe_push=False)
# 先订阅了 QUOTE 和 TICKER 两个类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    print('subscribe successfully！current subscription status :', quote_ctx.query_subscription())  # 订阅成功后查询订阅状态
    time.sleep(60)  # 订阅之后至少1分钟才能取消订阅
    ret_unsub, err_message_unsub = quote_ctx.unsubscribe_all()  # 取消所有订阅
    if ret_unsub == RET_OK:
        print('unsubscribe all successfully！current subscription status:', quote_ctx.query_subscription())  # 取消订阅后查询订阅状态
    else:
        print('Failed to cancel all subscriptions！', err_message_unsub)
else:
    print('subscription failed', err_message)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
