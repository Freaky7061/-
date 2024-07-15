import os
import sys

import pandas as pd


def clean_data(input_csv_file):
    # 使用os.path.splitext分离文件名和扩展名
    file_base, file_ext = os.path.splitext(input_csv_file)
    # 增加新的后缀
    new_suffix = '_washed'
    output_csv_file = f"{file_base}{new_suffix}{file_ext}"

    # 读取CSV文件到DataFrame
    df = pd.read_csv(input_csv_file)

    # 删除评论内容相同的条目
    df.drop_duplicates(subset='reply_text', inplace=True)

    # 将'reply_time'列转换为datetime对象
    df['reply_time'] = pd.to_datetime(df['reply_time'], format='%Y-%m-%d %H:%M:%S')

    try:
        # 只保留6月份的评论数据
        df_june = df[df['reply_time'].dt.month == 6]
        # 检查是否有6月份的数据
        if df_june.index.empty:
            raise ValueError(
                "No data available for June. Possible anti-crawling mechanism triggered or no June data found.")
        # 将清洗后的数据写入新的CSV文件
        df_june.to_csv(output_csv_file, index=False)

        print(f"Data has been successfully cleaned and written to {output_csv_file}")

        return output_csv_file
    except ValueError as ve:
        # 处理特定错误，例如没有6月份的数据
        print("当前已被反爬，请稍后再试")
        sys.exit(1)  # 退出程序
    except Exception as e:
        # 处理其他所有未预料到的异常
        print(f"An unexpected error occurred: {e}")
