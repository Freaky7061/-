import pandas as pd
import matplotlib.pyplot as plt
import ast


def paint():
    csv_files = ['300364_washed.csv', '002654_washed.csv']
    for csv_file in csv_files:
        create_fig(csv_file)


def create_fig(csv_file):
    # 读取带有情感分析结果的CSV文件
    df = pd.read_csv(csv_file)

    # 提取日期部分
    df['date'] = pd.to_datetime(df['reply_time']).dt.date

    # 初始化每日情感计数器
    daily_emotion_counts = {}

    # 遍历每条评论的情感分析结果
    for index, row in df.iterrows():
        date = row['date']
        try:
            result = ast.literal_eval(row['sentiment_analysis'])  # 将字符串转换为字典
        except (ValueError, SyntaxError):
            continue

        if date not in daily_emotion_counts:
            daily_emotion_counts[date] = {'positive': 0, 'negative': 0, 'neutral': 0}

        if result.get('pos', 0) > result.get('neg', 0):
            daily_emotion_counts[date]['positive'] += 1
        elif result.get('neg', 0) > result.get('pos', 0):
            daily_emotion_counts[date]['negative'] += 1
        else:
            daily_emotion_counts[date]['neutral'] += 1

    # 转换为DataFrame以便于绘图
    daily_emotion_df = pd.DataFrame.from_dict(daily_emotion_counts, orient='index')
    daily_emotion_df = daily_emotion_df.sort_index()

    # 计算每天正面评论占总评论的百分比
    daily_emotion_df['total'] = daily_emotion_df.sum(axis=1)

    try:
        # 计算每天正面评论占总评论的百分比，增加异常处理
        if daily_emotion_df['total'].any():  # 检查总评论数是否全为0
            daily_emotion_df['positive_pct'] = daily_emotion_df['positive'] / daily_emotion_df['total'] * 100
        else:
            print("数据为空，已被反爬，稍后重试")
            # 可以在这里处理数据为空的情况，例如直接返回或跳过绘图
            return
    except Exception as e:
        print(f"An error occurred while calculating positive percentages: {e}")
        # 可以选择在这里处理异常，例如跳过当前的CSV文件

    # 初始化图表
    fig, ax = plt.subplots(figsize=(12, 8))
    # plt.subplots_adjust(bottom=0.8)  # 为按钮腾出空间

    switch_to_bar(ax, daily_emotion_df, fig, csv_file)   
    switch_to_line(ax, daily_emotion_df, fig, csv_file)
    switch_to_pie(ax, daily_emotion_df, fig, csv_file)


# 画条形图
def switch_to_bar(ax, daily_emotion_df, fig, csv_file):
    ax.clear()
    daily_emotion_df[['positive', 'negative', 'neutral']].plot(kind='bar', stacked=True, color=['#66b3ff', '#ff9999', '#99ff99'], ax=ax)
    ax.set_title('Daily Positive, Negative, and Neutral Comments')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Comments')
    ax.legend(['Positive', 'Negative', 'Neutral'])
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.draw()
    plt.savefig(f'{csv_file[:6]}_bar.jpg')


# 画饼图
def switch_to_pie(ax, daily_emotion_df, fig, csv_file):
    ax.clear()
    emotion_counts = {'positive': daily_emotion_df['positive'].sum(),
                      'negative': daily_emotion_df['negative'].sum(),
                      'neutral': daily_emotion_df['neutral'].sum()}
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [emotion_counts['positive'], emotion_counts['negative'], emotion_counts['neutral']]
    colors = ['#66b3ff', '#ff9999', '#99ff99']
    explode = (0.1, 0, 0)  # 仅“Positive”分离出来

    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140)
    ax.axis('equal')  # 使饼图圆形
    plt.title('Sentiment Analysis of Comments')
    fig.tight_layout()
    plt.savefig(f'{csv_file[:6]}_pie.jpg')


# 画折线图
def switch_to_line(ax,daily_emotion_df, fig, csv_file):
    ax.clear()
    daily_emotion_df['positive_pct'].plot(kind='line', color='#66b3ff', ax=ax)
    ax.set_title('Daily Positive Comments Percentage')
    ax.set_xlabel('Date')
    ax.set_ylabel('Percentage of Positive Comments')
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.savefig(f'{csv_file[:6]}_line.jpg')



