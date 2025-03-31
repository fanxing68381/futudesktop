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
        options.add_argument("--start-maximized")  # 最大化窗口
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        print("浏览器已启动并打开目标网页")

        # 模拟人工操作
        actions = ActionChains(driver)

        # 步骤1：关闭可能的登录弹窗
        time.sleep(1)
        try:
            close_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//*[contains(@class, 'close') or contains(text(), '关闭') or contains(text(), '取消') or @aria-label='关闭']"))
            )
            close_button.click()
            print("已关闭手机号登录弹窗")
            time.sleep(1)
        except:
            print("未检测到登录弹窗，执行备用关闭方案")
            actions.send_keys(Keys.ESCAPE).perform()
            print("已发送 ESC 键")

        # 步骤2：点击"最新"按钮
        try:
            latest_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'orderby-last-publish'))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_btn)
            latest_btn.click()
            print("成功点击'最新'选项")
            time.sleep(2)
        except Exception as e:
            print(f"点击'最新'按钮失败: {e}")
            raise Exception("无法继续执行，因未能切换至最新内容")

        # 步骤3：优化滚动加载逻辑
        loaded_items = 0
        max_attempts = 8
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_failures = 0

        while loaded_items < max_attempts and consecutive_failures < 3:
            try:
                more_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.orderby-last-publish.add-more'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", more_btn)
                more_btn.click()
                print(f"第 {loaded_items + 1} 次加载更多内容")
                time.sleep(2)
                loaded_items += 1
                consecutive_failures = 0
            except:
                print("尝试滚动加载...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
                consecutive_failures += 1

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("页面高度未变化，停止加载")
                break
            last_height = new_height

        # 步骤4：解析页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        center_column = soup.find('ul', class_='orderby-last-publish')
        if not center_column:
            raise Exception("无法定位内容列")

        articles = []
        for item in center_column.find_all('li', class_='index-list-item'):
            author_tag = item.find('div', class_='user-main').find('h4').find('a') if item.find('div',
                                                                                                class_='user-main') else None
            author_name = author_tag.text.strip() if author_tag else '未知作者'

            article_tag = item.find('div', class_='list-item').find('h4').find('a') if item.find('div',
                                                                                                 class_='list-item') else None
            if article_tag:
                full_title = article_tag.text.strip()
                link = article_tag['href']
                if link.startswith('/'):
                    link = 'https://user.guancha.cn' + link

                content_tag = item.find('div', class_='item-content')
                content = content_tag.get_text(strip=True)[:250] if content_tag else '无摘要'

                articles.append({
                    'author_name': author_name,
                    'full_title': full_title,
                    'link': link,
                    'summary': content
                })

        if not articles:
            raise Exception("未找到任何文章")

        if len(articles) < 40:
            print(f"警告：仅加载到 {len(articles)} 条，不足40条")
        articles = articles[:40]

        # 生成带序列号的HTML表格
        current_date = datetime.now().strftime('%Y-%m-%d')
        table_rows = ''.join([f'''
            <tr>
                <td>第{idx}篇</td>
                <td><a href="{article['link']}" target="_blank">{article['author_name']}</a></td>
                <td>{article['full_title']}</td>
                <td>{article['summary']}</td>
            </tr>''' for idx, article in enumerate(articles, 1)])

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
        a {{ 
            color: #0066cc; 
            text-decoration: none; 
        }}
        a:hover {{ 
            text-decoration: underline; 
        }}
        /* 新增序列号列样式 */
        td:first-child {{
            font-weight: bold;
            color: #666;
            width: 80px;
        }}
    </style>
</head>
<body>
    <h1>风闻社区文章列表 - 抓取日期: {current_date}</h1>
    <table>
        <tr>
            <th>序列</th>
            <th>作者</th>
            <th>完整标题</th>
            <th>缩写内容（前250字符）</th>
        </tr>
        {table_rows}
    </table>
</body>
</html>"""

        # 保存HTML文件
        desktop_path = r'C:\Users\Administrator\Desktop'
        html_filename = f'fengwen_articles_{current_date}.html'
        html_path = os.path.join(desktop_path, html_filename)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"HTML文件已保存：{html_path}")

        # 保存链接到文本文件
        txt_filename = "观察者网40链接.txt"
        txt_path = os.path.join(desktop_path, txt_filename)

        try:
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                paragraph = "《依次先提取下列链接的主题，然后围绕各主题内的中文中文内容，分别详细总结各篇文章的中文内容（不少于600字），将之前600字完整版详细总结出中文内容，生成到一个html链接（html内的中文内容不要省略，将每篇文章600字的总结全部写进html里，下面有多少链接，就输出多少条链接的文章中文内容,如果遇到某些链接打不开或其它问题就跨越过去，但不能跨过可能打开的链接。每一篇增加一个序列，如“第12篇”。不要只输出部分文章中文内容，尽可能在一次对话中输出所有文章中文内容）（千万不要输出原文的链接）：》\n"
                txt_file.write(paragraph)
                for article in articles:
                    txt_file.write(f"{article['link']}\n")
            print(f"成功保存 {len(articles)} 条链接到：{txt_path}")
        except Exception as e:
            print(f"保存链接文件失败: {e}")
            raise

        # 自动打开文件
        webbrowser.open('file://' + os.path.realpath(html_path))
        webbrowser.open('file://' + os.path.realpath(txt_path))

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已安全关闭")


if __name__ == "__main__":
    target_url = "https://user.guancha.cn/?s=dhfengwen"
    fetch_and_save_webpage(target_url)