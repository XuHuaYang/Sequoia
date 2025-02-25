# -*- encoding: UTF-8 -*-
import logging
import talib as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
lookback_period = 5

def check(code_name, data, end_date=None, threshold=180):
    # print(len(data))
    data = data.tail(n=threshold)

    # print(data.iloc[0])
    df_selected = data[['日期', '收盘']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # 计算布林带
    period = 20  # 布林带的周期
    data['upper'], data['middle'], data['lower'] = ta.BBANDS(
        data['收盘'],
        timeperiod=period,
        nbdevup=2,  # 上轨的标准差倍数
        nbdevdn=2,  # 下轨的标准差倍数
        matype=ta.MA_Type.SMA  # 使用简单移动平均线
    )

    # 判断买入和卖出时机
    data.loc[:,'signal'] = 0  # 初始化信号列
    data.loc[data['收盘'] < data['lower'], 'signal'] = 1  # 买入信号
    data.loc[data['收盘'] > data['upper'], 'signal'] = -1  # 卖出信号

    # 输出结果
    recent_signals = data['signal'].tail(lookback_period)
    last_five_days_buy_signal = (recent_signals == 1).any()
    return last_five_days_buy_signal


def check_sell(code_name, data, end_date=None, threshold=180):
    # print(len(data))
    data = data.tail(n=threshold)

    # print(data.iloc[0])
    df_selected = data[['日期', '收盘']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # 计算布林带
    period = 20  # 布林带的周期
    data['upper'], data['middle'], data['lower'] = ta.BBANDS(
        data['收盘'],
        timeperiod=period,
        nbdevup=2,  # 上轨的标准差倍数
        nbdevdn=2,  # 下轨的标准差倍数
        matype=ta.MA_Type.SMA  # 使用简单移动平均线
    )

    # 判断买入和卖出时机
    data.loc[:,'signal'] = 0  # 初始化信号列
    data.loc[data['收盘'] < data['lower'], 'signal'] = 1  # 买入信号
    data.loc[data['收盘'] > data['upper'], 'signal'] = -1  # 卖出信号

    # 输出结果
    recent_signals = data['signal'].tail(lookback_period)
    last_five_days_sell_signal = (recent_signals == -1).any()
    return last_five_days_sell_signal
