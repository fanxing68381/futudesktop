import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import webbrowser

def fetch_and_save_webpage(url):
    driver = None
    try:
        # 初始化浏览器配置
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")  # 禁用信息栏
        options.add_argument("--start-maximized")   # 最大化窗口
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        print("浏览器已启动并打开目标网页")

        # 模拟人工操作
        actions = ActionChains(driver)

        # 步骤1：打开页面后暂停并尝试关闭可能的登录弹窗
        time.sleep(1)
        try:
            # 尝试定位并点击关闭按钮（假设弹窗有常见的关闭标识）
            close_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'close') or contains(text(), '关闭') or contains(text(), '取消') or @aria-label='关闭']"))
            )
            close_button.click()
            print("已关闭手机号登录弹窗")
            time.sleep(1)  # 等待弹窗关闭
        except:
            print("未检测到手机号登录弹窗或无法关闭，继续执行后续步骤")
            actions.send_keys(Keys.ESCAPE).perform()  # 备用方案：发送 ESC 键
            print("已发送 ESC 键作为备用关闭操作")

        # 步骤2：点击“最新”按钮
        try:
            latest_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'orderby-last-publish'))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_btn)
            latest_btn.click()
            print("成功点击'最新'选项")
            time.sleep(2)  # 等待页面加载
        except Exception as e:
            print(f"点击'最新'按钮失败: {e}")
            raise Exception("无法继续执行，因未能切换至最新内容")

        # 步骤3：滚动并加载更多内容
        loaded_items = 0
        max_attempts = 5  # 最大加载次数
        last_height = driver.execute_script("return document.body.scrollHeight")

        while loaded_items < max_attempts:
            try:
                # 尝试点击“查看更多内容”按钮
                more_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.orderby-last-publish.add-more'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", more_btn)
                more_btn.click()
                print(f"第 {loaded_items + 1} 次加载更多内容")
                time.sleep(2)  # 等待内容加载
                loaded_items += 1
            except:
                print("未找到'查看更多内容'按钮或已加载所有内容，尝试滚动加载")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)

            # 检查页面高度是否变化
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("页面高度未变化，停止加载")
                break
            last_height = new_height

        # 步骤4：解析页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        center_column = soup.find('ul', class_='orderby-last-publish')
        if not center_column:
            raise Exception("无法定位最新发布的内容列")

        articles = []
        for item in center_column.find_all('li', class_='index-list-item'):
            # 获取作者名
            author_tag = item.find('div', class_='user-main').find('h4').find('a') if item.find('div', class_='user-main') else None
            author_name = author_tag.text.strip() if author_tag else '未知作者'

            # 获取标题和链接
            article_tag = item.find('div', class_='list-item').find('h4').find('a') if item.find('div', class_='list-item') else None
            if article_tag:
                full_title = article_tag.text.strip()
                link = article_tag['href']
                if link.startswith('/'):
                    link = 'https://user.guancha.cn' + link

                # 获取摘要
                content_tag = item.find('div', class_='item-content')
                content = content_tag.get_text(strip=True)[:250] if content_tag else '无摘要'

                articles.append({
                    'author_name': author_name,
                    'full_title': full_title,
                    'link': link,
                    'summary': content
                })

        if not articles:
            raise Exception("未找到任何文章标题和内容")

        # 限制为40条
        if len(articles) < 40:
            print(f"警告：仅加载到 {len(articles)} 条新闻，不足40条，可能已达页面最大内容")
        articles = articles[:40]

        # 步骤5：生成HTML文件
        current_date = datetime.now().strftime('%Y-%m-%d')
        table_rows = ''.join([f'''
            <tr>
                <td><a href="{article['link']}" target="_blank">{article['author_name']}</a></td>
                <td>{article['full_title']}</td>
                <td>{article['summary']}</td>
            </tr>''' for article in articles])

        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>风闻社区文章列表 - {current_date}</title>
    <style>
        table {{
            width: 90%;
            border-collapse: collapse;
            margin: 20px auto;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>风闻社区文章列表 - 抓取日期: {current_date}</h1>
    <table>
        <tr>
            <th>作者</th>
            <th>完整标题</th>
            <th>缩写内容（前250字符）</th>
        </tr>
        {table_rows}
    </table>
</body>
</html>"""

        # 保存文件到桌面
        desktop_path = r'C:\Users\Administrator\Desktop\每日统计改名'
        filename = f'fengwen_articles_{current_date}.html'
        full_path = os.path.join(desktop_path, filename)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html_template)

        print(f"文件已成功保存至：{full_path}")
        print(f"共生成 {len(articles)} 条新闻。")

        # 步骤6：自动打开文件
        webbrowser.open('file://' + os.path.realpath(full_path))

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    target_url = "https://user.guancha.cn/?s=dhfengwen"
    fetch_and_save_webpage(target_url)