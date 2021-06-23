# -*- coding:utf-8 -*-
from functions.fund_functions_cmd import *
from functions.fund_para import *
import datetime


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


if __name__ == "__main__":
    start_date = '2021-01-01'
    start_date2 = '2021-03-23'
    start_date3 = '2021-04-26'
    today = datetime.date.today()
    HighVal_start_date = '2021-04-26'
    # {'name': 'QS', 'code': '007531', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}
    funds_1 = [{'name': 'BJ', 'code': '161725', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'YL', 'code': '009163', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'XNY', 'code': '009645', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]
    funds_2 = [{'name': 'KJ', 'code': '007872', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'C50', 'code': '160424', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]
    funds_3 = [{'name': 'GF', 'code': '011103', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]
    funds_4 = [{'name': 'k50', 'code': '011609', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]
    funds_5 = [{'name': 'ZGHL', 'code': '006328', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'N100', 'code': '006479', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'YN', 'code': '008764', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]

    show_rows = 5
    funds_1_table = show_table(funds_1, start_date, today, HighVal_start_date, show_rows=show_rows)
    print(funds_1_table)
    funds_2_table = show_table(funds_2, start_date, today, HighVal_start_date, show_rows=show_rows)
    print(funds_2_table)
    funds_3_table = show_table(funds_3, start_date2, today, HighVal_start_date, show_rows=show_rows)
    print(funds_3_table)
    funds_4_table = show_table(funds_4, start_date3, today, HighVal_start_date, show_rows=show_rows)
    print(funds_4_table)
    yesterday = getYesterday()
    funds_5_table = show_table(funds_5, start_date, yesterday, HighVal_start_date, show_rows=show_rows)
    print(funds_5_table)
