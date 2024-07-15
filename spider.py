import requests
import re
import csv
from time import sleep


# 设置请求头，添加User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472\
    .124 Safari/537.36'
}

csv_columns = ['user_nickname', 'reply_time', 'reply_text']


def create_csv(base_url):
    try:
        # 当模块作为主程序运行时，下面的代码将被执行
        with open(f"{base_url.split(',')[1]}.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()

            # 爬取前25页
            for page_num in range(1, 25):
                if page_num == 1:
                    url = f"{base_url}.html"
                else:
                    url = f"{base_url}_{page_num}.html"

                try:
                    # 发送HTTP GET请求获取页面内容
                    response = requests.get(url, headers=headers)
                    response.encoding = 'utf-8'  # 设置正确的编码
                    html_content = response.text
                except requests.exceptions.RequestException as e:
                    print(f"Request failed on page {page_num}: {e}")
                    continue  # 跳过当前页，继续处理下一页

                # 清除变量缓存
                user_nicknames = []
                reply_times = []
                reply_texts = []

                if page_num == 1:
                    # 提取用户昵称、回复时间和回复内容
                    user_nicknames = re.findall(r'"user_nickname":"(.*?)"', html_content)
                    reply_times = re.findall(r'"reply_time":"(.*?)"', html_content)
                    reply_texts = re.findall(r'"reply_text":"(.*?)"', html_content)
                else:
                    user_nicknames = re.findall(r'"user_nickname":"(.*?)"', html_content)
                    reply_times = re.findall(r'"post_publish_time":"(.*?)"', html_content)
                    reply_texts = re.findall(r'"post_title":"(.*?)"', html_content)

                # 将提取的信息写入CSV文件
                for idx in range(min(len(user_nicknames), len(reply_times), len(reply_texts))):
                    writer.writerow({
                        'user_nickname': user_nicknames[idx],
                        'reply_time': reply_times[idx],
                        'reply_text': reply_texts[idx]
                    })
                if page_num % 5 == 0:
                    print(f"Page {page_num} processed and written to CSV.")

                # 延时以避免触发反爬机制
                sleep(1)
    except IOError as e:
        print(f"File operation failed: {e}")
    except csv.Error as e:
        print(f"CSV writing failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


