# -*- encoding: UTF-8 -*-
import itertools
from logging.handlers import TimedRotatingFileHandler

import data_fetcher
import settings
import strategy.enter as enter
from strategy import turtle_trade, climax_limitdown
from strategy import backtrace_ma250
from strategy import breakthrough_platform
from strategy import parking_apron
from strategy import low_backtrace_increase
from strategy import keep_increasing
from strategy import high_tight_flag
import akshare as ak
import push
import logging
import time
import datetime


totalMap={}

# 配置日志记录器1
logger1 = logging.getLogger("Logger1")
logger1.setLevel(logging.INFO)

date_suffix=datetime.datetime.now().strftime("%Y-%m-%d")
log_filename=f"combinations_{date_suffix}.log"
file_handler1 = logging.FileHandler(log_filename)
file_handler1.suffix="%Y-%m-%d"
formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler1.setFormatter(formatter1)
logger1.addHandler(file_handler1)

def prepare():
    logging.info("************************ process start ***************************************")
    all_data = ak.stock_zh_a_spot_em()
    subset = all_data[['代码', '名称']]
    stocks = [tuple(x) for x in subset.values]
    statistics(all_data, stocks)

    strategies = {
        '放量上涨': enter.check_volume,
        '均线多头': keep_increasing.check,
        # '停机坪': parking_apron.check,
        # '回踩年线': backtrace_ma250.check,
         '突破平台': breakthrough_platform.check,
        '无大幅回撤': low_backtrace_increase.check,
        '海龟交易法则': turtle_trade.check_enter,
        # '高而窄的旗形': high_tight_flag.check,
        # '放量跌停': climax_limitdown.check,
    }

    if datetime.datetime.now().weekday() == 0:
        strategies['均线多头'] = keep_increasing.check

    process(stocks, strategies)

    for r in range(2, len(totalMap) + 1):  # 从2个键到最大长度的组合
        for combo in itertools.combinations(totalMap.keys(), r):
            # 求键对应值的交集
            intersection = set.intersection(*(totalMap[key] for key in combo))
            # 打印组合名称和交集内容
            combo_name = "+".join(combo)
            logger1.info(f"{combo_name}:\n {intersection}")
            if len(intersection) > 0:
                push.strategy(
                    '**************"{0}"**************\n{1}\n**************"{0}"**************\n'.format(combo_name, list(intersection)))
    logging.info("************************ process   end ***************************************")

def process(stocks, strategies):
    stocks_data = data_fetcher.run(stocks)
    for strategy, strategy_func in strategies.items():
        check(stocks_data, strategy, strategy_func)
        time.sleep(2)

def check(stocks_data, strategy, strategy_func):
    end = settings.config['end_date']
    m_filter = check_enter(end_date=end, strategy_fun=strategy_func)
    results = dict(filter(m_filter, stocks_data.items()))
    totalMap[strategy]=set(list(results.keys()))
    # if len(results) > 0:
        # push.strategy('**************"{0}"**************\n{1}\n**************"{0}"**************\n'.format(strategy, list(results.keys())))


def check_enter(end_date=None, strategy_fun=enter.check_volume):
    def end_date_filter(stock_data):
        if end_date is not None:
            if end_date < stock_data[1].iloc[0].日期:  # 该股票在end_date时还未上市
                logging.debug("{}在{}时还未上市".format(stock_data[0], end_date))
                return False
        return strategy_fun(stock_data[0], stock_data[1], end_date=end_date)


    return end_date_filter


# 统计数据
def statistics(all_data, stocks):
    limitup = len(all_data.loc[(all_data['涨跌幅'] >= 9.5)])
    limitdown = len(all_data.loc[(all_data['涨跌幅'] <= -9.5)])

    up5 = len(all_data.loc[(all_data['涨跌幅'] >= 5)])
    down5 = len(all_data.loc[(all_data['涨跌幅'] <= -5)])

    msg = "涨停数：{}   跌停数：{}\n涨幅大于5%数：{}  跌幅大于5%数：{}".format(limitup, limitdown, up5, down5)
    push.statistics(msg)


