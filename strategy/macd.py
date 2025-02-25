# -*- encoding: UTF-8 -*-
import logging
import talib as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def check(code_name, data, end_date=None, threshold=180):
    # print(len(data))
    data = data.tail(n=threshold)

    # print(data.iloc[0])
    df_selected = data[['日期', '收盘']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # print(df['收盘'])
    df['MACD'], df['Signal'], df['Histogram'] = ta.MACD(
    df['收盘'].astype(float), fastperiod=12, slowperiod=26, signalperiod=9)
    df['买入信号'] = (df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))
    # df['卖出信号'] = (df['MACD'] < df['Signal']) & (df['MACD'].shift(1) >= df['Signal'].shift(1))
    # print(df[df['买入信号']])
    last_five_days_buy_signal = df['买入信号'].tail(5).any()
    # print(last_five_days_buy_signal)
    return last_five_days_buy_signal
    # print(df)
    # print(df[df['卖出信号']])
    # # 绘制 MACD 图
    # plt.figure(figsize=(14, 8))
    #
    # # 绘制收盘价
    # plt.subplot(2, 1, 1)
    # plt.plot(df.index, df['收盘'], label='收盘价', color='blue')
    # plt.title('收盘价与MACD', fontsize=16)
    # plt.xlabel('日期', fontsize=12)
    # plt.ylabel('价格', fontsize=12)
    # plt.legend()
    #
    # # 绘制 MACD、Signal 和 Histogram
    # plt.subplot(2, 1, 2)
    # plt.plot(df.index, df['MACD'], label='MACD', color='red')
    # plt.plot(df.index, df['Signal'], label='Signal', color='green')
    # plt.bar(df.index, df['Histogram'], label='Histogram', color='gray', alpha=0.5)
    # plt.xlabel('日期', fontsize=12)
    # plt.ylabel('MACD', fontsize=12)
    # plt.legend()
    #
    # # 显示图形
    # plt.tight_layout()
    # plt.show()

    # 计算买卖信号


    # 绘制 MACD 图
    # plt.figure(figsize=(14, 10))
    #
    # # 绘制收盘价
    # plt.subplot(2, 1, 1)
    # plt.plot(df.index, df['收盘'], label='收盘价', color='blue')
    # plt.title('收盘价与MACD买卖信号', fontsize=16)
    # plt.xlabel('日期', fontsize=12)
    # plt.ylabel('价格', fontsize=12)
    #
    # # 标注买入信号
    # buy_signals = df[df['买入信号']]
    # plt.scatter(buy_signals.index, buy_signals['收盘'], color='green', marker='^', label='买入信号', alpha=1)
    #
    # # 标注卖出信号
    # sell_signals = df[df['卖出信号']]
    # plt.scatter(sell_signals.index, sell_signals['收盘'], color='red', marker='v', label='卖出信号', alpha=1)
    #
    # plt.legend()
    #
    # # 绘制 MACD、Signal 和 Histogram
    # plt.subplot(2, 1, 2)
    # plt.plot(df.index, df['MACD'], label='MACD', color='red')
    # plt.plot(df.index, df['Signal'], label='Signal', color='green')
    # plt.bar(df.index, df['Histogram'], label='Histogram', color='gray', alpha=0.5)
    # plt.xlabel('日期', fontsize=12)
    # plt.ylabel('MACD', fontsize=12)
    # plt.legend()
    #
    # # 显示图形
    # plt.tight_layout()
    # plt.show()

    # breakpoint()
def check_sell(code_name, data, end_date=None, threshold=180):
    # print(len(data))
    data = data.tail(n=threshold)

    # print(data.iloc[0])
    df_selected = data[['日期', '收盘']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # print(df['收盘'])
    df['MACD'], df['Signal'], df['Histogram'] = ta.MACD(
    df['收盘'].astype(float), fastperiod=12, slowperiod=26, signalperiod=9)
    #df['买入信号'] = (df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))
    df['卖出信号'] = (df['MACD'] < df['Signal']) & (df['MACD'].shift(1) >= df['Signal'].shift(1))
    # print(df[df['买入信号']])
    last_five_days_sell_signal = df['卖出信号'].tail(5).any()
    # print(last_five_days_buy_signal)
    return last_five_days_sell_signal
