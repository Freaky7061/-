import os
import pandas as pd
import jieba
import re

# 假设你的停用词表文件名为 "stopwords.txt"，每行一个停用词
stopwords_file = 'hit_stopwords.txt'

# 读取停用词表文件，创建停用词集合
with open(stopwords_file, 'r', encoding='utf-8') as file:
    stopwords = set([line.strip() for line in file])


# 清洗和分词函数
def preprocess(text):
    # 去除噪音
    text = re.sub(r'[^\w\s]', '', text)
    # 去除英文标点
    text = re.sub(r'[A-Za-z0-9]', '', text)
    # 分词
    words = jieba.cut(text)
    # 去除停用词
    words = [word for word in words if word not in stopwords]
    # 返回分词结果
    return ' '.join(words)


# 主处理函数
def process_comments(input_file):
    # 读取CSV文件
    df = pd.read_csv(input_file, encoding='utf-8')

    # 假设评论在名为 'comment_column' 的列中
    comment_column = 'reply_text'

    # 应用预处理函数
    df['processed_comments'] = df[comment_column].apply(preprocess)

    # 使用os.path.splitext分离文件名和扩展名
    file_base, file_ext = os.path.splitext(input_file)
    # 增加新的后缀
    new_suffix = '_split'
    output_file = f"{file_base}{new_suffix}{file_ext}"
    # 将预处理后的评论保存到新的CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8')

