# -*- coding:utf-8 -*-
from functions.fund_functions import *
from functions.fund_para import *

if __name__ == "__main__":
    start_date = '2021-01-01'
    today = datetime.date.today()
    HighVal_start_date = '2021-04-26'

    funds_1 = [{'name': 'BJ', 'code': '161725', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'XBY', 'code': '009645', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]
    funds_2 = [{'name': 'BDT', 'code': '008282', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0},
               {'name': 'QS', 'code': '007531', 'single': 10, 'threshold': -0.03, 'buy': 0, 'max': 0}]

    show_rows = 10
    funds_1_table = show_table(funds_1, start_date, today, HighVal_start_date, show_rows=show_rows)
    print(funds_1_table)
    funds_2_table = show_table(funds_2, start_date, today, HighVal_start_date, show_rows=show_rows)
    print(funds_2_table)
