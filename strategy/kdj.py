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
    df_selected = data[['日期', '收盘','最高','最低']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # 计算 KDJ 指标
    slowk, slowd = ta.STOCH(data['最高'], data['最低'], data['收盘'],
                               fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    slowj = 3 * slowk - 2 * slowd

    # 将 KDJ 指标添加到数据框中
    data.loc[:, 'slowk'] = slowk
    data.loc[:, 'slowd'] = slowd
    data.loc[:, 'slowj'] = slowj

    # 判断买入和卖出时机
    data['buy_signal'] = (data['slowk'] > data['slowd']) & (data['slowj'] < 20)
    last_five_days_buy_signal = data['buy_signal'].tail(5).any()
    # print(data[['slowk', 'slowd', 'slowj', 'buy_signal']].tail(20))

    return last_five_days_buy_signal


def check_sell(code_name, data, end_date=None, threshold=180):
    # print(len(data))
    data = data.tail(n=threshold)

    # print(data.iloc[0])
    df_selected = data[['日期', '收盘','最高','最低']]

    df = pd.DataFrame(df_selected)
    df.set_index('日期', inplace=True)

    # 计算 KDJ 指标
    slowk, slowd = ta.STOCH(data['最高'], data['最低'], data['收盘'],
                               fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    slowj = 3 * slowk - 2 * slowd

    # 将 KDJ 指标添加到数据框中
    data.loc[:,'slowk'] = slowk
    data.loc[:,'slowd'] = slowd
    data.loc[:,'slowj'] = slowj

    # 判断买入和卖出时机
    data['sell_signal'] = (data['slowk'] < data['slowd']) & (data['slowj'] > 80)
    last_five_days_sell_signal = data['sell_signal'].tail(5).any()
    # print(data[[ 'slowk', 'slowd', 'slowj', 'sell_signal']].tail(20))
    return last_five_days_sell_signal
