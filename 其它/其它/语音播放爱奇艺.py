import speech_recognition as sr
import os
import platform

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        audio = r.listen(source)

    try:
        # 使用 Google 语音识别将语音转换为文本
        text = r.recognize_google(audio, language='zh-CN')
        print(f"你说的是: {text}")
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
    except sr.RequestError as e:
        print(f"请求错误; {e}")
    return None

def open_iqiyi():
    system_platform = platform.system()
    if system_platform == "Windows":
        try:
            # 尝试打开爱奇艺应用程序
            os.startfile("C:\Program Files\IQIYI Video\LStyle\QyClient.exe")
            print("已打开爱奇艺")
        except FileNotFoundError:
            print("未找到爱奇艺应用程序，请检查安装路径。")
    elif system_platform == "Linux":
        try:
            import subprocess
            # 在 Linux 系统上尝试打开爱奇艺
            subprocess.Popen(["xdg-open", "/usr/share/applications/iqiyi.desktop"])
            print("已打开爱奇艺")
        except FileNotFoundError:
            print("未找到爱奇艺应用程序，请检查安装路径。")
    elif system_platform == "Darwin":
        try:
            import subprocess
            # 在 macOS 系统上尝试打开爱奇艺
            subprocess.Popen(["open", "-a", "爱奇艺"])
            print("已打开爱奇艺")
        except FileNotFoundError:
            print("未找到爱奇艺应用程序，请检查安装路径。")
    else:
        print("不支持的操作系统")

if __name__ == "__main__":
    speech_text = recognize_speech()
    if speech_text and "打开爱奇艺" in speech_text:
        open_iqiyi()