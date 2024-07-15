import sys
import threading
import spider
import analyse
import wash
import emotion
import draw
import guigui


# 定义线程的目标函数
def thread_target(url):
    try:
        print(f"Thread {threading.current_thread().name} is fetching {url}")
        spider.create_csv(url)
        source_file = f"{url.split(',')[1]}.csv"
        analyse.process_comments(source_file)
        final_file = wash.clean_data(source_file)
        emotion.create_emotion(final_file)
    except Exception as e:
        # 打印异常信息
        print(f"An error occurred: {e}")

# 主程序
def main():
    # URL列表
    urls = [
        'https://guba.eastmoney.com/list,002654',
        'https://guba.eastmoney.com/list,300364'
    ]

    # 创建线程列表
    threads = []

    # 创建并启动线程
    for url in urls:
        thread = threading.Thread(target=thread_target, args=(url,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print("All threads have completed.")
    

if __name__ == '__main__':
    try:
        main()
        draw.paint()
        guigui.guigui()
    except Exception as e:
        # 打印异常信息
        print(f"An error occurred: {e}")
        # 退出程序，退出码非0表示发生错误
        sys.exit(1)
