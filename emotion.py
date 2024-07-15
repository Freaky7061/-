import pandas as pd
from cnsenti import Sentiment
from pprint import pprint


def create_emotion(file_path):
    # 读取处理好的CSV文件
    df = pd.read_csv(file_path)

    # 初始化情感分析对象
    senti = Sentiment()

    # 对每条评论进行情感分析并将结果存储在列表中
    analysis_results = []
    for reply_text in df['reply_text']:
        result = senti.sentiment_count(reply_text)
        analysis_results.append(result)

    # 将情感分析结果添加到数据框中
    df['sentiment_analysis'] = analysis_results

    # 打印前几条记录以查看结果
    pprint(df.head())

    # 将带有情感分析结果的数据保存回CSV文件
    df.to_csv(file_path, index=False)
