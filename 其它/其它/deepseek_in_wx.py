import time
from wxauto import WeChat
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
import os

# DeepSeek API 配置
client = OpenAI(
    api_key="sk-cjicinjyfxpzmqyknbmjjuuhgtcndrxzcipmkogalqsogjao",  # 替换为你的 DeepSeek API 密钥
    base_url="https://api.siliconflow.cn"  # DeepSeek 的 API 地址
)

# 预设角色信息
SYSTEM_PROMPT = "你是fanfan"

# 全局对话历史记录
conversation_history = {}
wx = WeChat()  # 初始化微信自动化

# 需要对哪些人的消息进行监听
listen_list = ["范范","聆我"]

# 创建线程池
executor = ThreadPoolExecutor(max_workers=10)

# 处理消息并根据发送者进行回复
def process_messages(messages):
    # 使用 items() 解包字典的键值对
    for sender, content_list in messages.items():
        # 判断发送者是否在监听列表中
        if sender not in listen_list:
            print(f"{sender} 不在监听列表中，跳过处理")
            continue
         # 确保消息内容有效
        if content_list and isinstance(content_list, list):
            # 遍历发送者的所有消息内容
            for content in content_list:
                # 检查消息内容是否包含 "SYS" 或 "Self",如果消息类型是 "SYS" 或 "Self"，则跳过
                if content[0] == "SYS" or content[0] == "Self":
                    print(f"跳过 '{content[0]}' 消息")
                    continue
                # 处理非 "SYS" 和 非 "Self" 的消息
                message_content = content[1]  # 获取消息内容
                print(f"处理消息：'{message_content}'，发送者：{sender}")

                # 调用线程池异步回复
                executor.submit(reply_message, sender, message_content)


# 调用 API 获取回复
def get_ai_reply(sender, message):
    # 储存对话历史记录
    global conversation_history

    # 初始化发送者的对话历史（如果不存在）
    if sender not in conversation_history:
        conversation_history[sender] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # 将用户消息添加到对话历史
    conversation_history[sender].append({"role": "user", "content": message})

    try:
        # 调用 API
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # 使用的模型
            messages=conversation_history[sender]  # 使用发送者的完整对话历史
        )

        # 获取助手的回复
        assistant_reply = response.choices[0].message.content.strip()

        # 将助手的回复添加到对话历史
        conversation_history[sender].append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        print(f"调用 API 出错：{e}")
        # return "抱歉，我暂时无法处理您的请求，请稍后再试。"
        return ""

# 根据消息内容生成回复并发送
def reply_message(sender, message_content):
    reply_content = get_ai_reply(sender, message_content)
    if reply_content:
        send_reply(sender, reply_content)

# 发送回复
def send_reply(sender, content):
    wx.SendMsg(content, sender)
    print(f"已发送消息：'{content}' 给 {sender}")

# 主程序入口
if __name__ == "__main__":
    #wx = WeChat()

    while True:
        msgs = wx.GetAllNewMessage()  # 获取所有新消息
        if msgs:
            print("收到的新消息：", msgs)
            process_messages(msgs)  # 调用函数处理消息
        time.sleep(2)  # 延时，减少系统负担