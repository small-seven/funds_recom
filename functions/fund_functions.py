import requests
from bs4 import BeautifulSoup
from prettytable import *
import sys
import re
import json
from datetime import datetime
import baostock as bs


def accumulate(integer):
    sum_tmp = 0
    for i in range(0, integer + 1):
        sum_tmp += i
    return sum_tmp


def red_green_show(string):
    if '-' in string:
        return '\033[0;32m' + string + '\033[0m'
    else:
        return '\033[0;31m' + string + '\033[0m'


def safe_pe_green_show(string):
    return '\033[0;32m' + str(string) + '\033[0m'


def risk_pe_red_show(string):
    return '\033[0;31m' + str(string) + '\033[0m'


def yellow_show(string):
    return '\033[0;33m' + string + '\033[0m'


def estimate_show(string):
    if '-' in string:
        return '\033[4;32m' + string + '\033[0m'
    else:
        return '\033[4;31m' + string + '\033[0m'


def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def query_stock_info(code):
    if code[0] == '0':
        code = 'sz.' + code
    elif code[0] == '6':
        code = 'sh.' + code
    rs = bs.query_history_k_data_plus(code, "date,code,close,pctChg,peTTM,pbMRQ", start_date='2021-05-01',
                                      frequency="d", adjustflag="3")
    data_list = []
    data_dict = {}
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())

    data_list = data_list[len(data_list) - 1]

    data_dict['date'] = data_list[0]
    data_dict['code'] = data_list[1]
    data_dict['close'] = format(float(data_list[2]), '.2f')
    data_dict['pctChg'] = format(float(data_list[3]), '.2f') + '%'
    data_dict['peTTM'] = format(float(data_list[4]), '.2f')
    data_dict['pbMRQ'] = format(float(data_list[5]), '.2f')

    return data_dict


def get_fund_data(code, name, start='', end=''):
    record = {}
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': code, 'per': 65535, 'sdate': start, 'edate': end}
    html = get_url(url, params)
    pages = int((html.split(',')[2]).split(':')[1])
    records = []
    for i in range(1, pages + 1):
        params = {'type': 'lsjz', 'code': code, 'page': i, 'per': 65535, 'sdate': start, 'edate': end}
        html = get_url(url, params)
        soup = BeautifulSoup(html, 'html.parser')
        tab = soup.findAll('tbody')[0]
        for tr in tab.findAll('tr'):
            if tr.findAll('td') and len((tr.findAll('td'))) == 7:
                record['date'] = str(tr.select('td:nth-of-type(1)')[0].getText().strip())
                record[name] = str(tr.select('td:nth-of-type(2)')[0].getText().strip())
                ChangePercent = name + '_CP'
                record[ChangePercent] = str(tr.select('td:nth-of-type(4)')[0].getText().strip())
                record[name + '_HF'] = ''
                record[name + '_BM'] = ''
                records.append(record.copy())
    return records


def get_current_netestimate(code):
    url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
    content = get_url(url)
    pattern = r'^jsonpgz\((.*)\)'
    search = re.findall(pattern, content)
    estimate = {}
    for i in search:
        data = json.loads(i)
        # print("{}%, {}, {}".format(data['gszzl'], data['gsz'], data['gztime']))
        estimate['date'] = str(data['gztime']).split(' ')[0]
        estimate['net'] = data['gsz']
        estimate['net_CP'] = data['gszzl'] + '%'
        return estimate


def get_records_of_one_fund(start_date, end_date, fund, HighVal_start_date):
    dayOfWeek = datetime.now().weekday()
    code = fund['code']
    name = fund['name']
    records = get_fund_data(code, name, start_date, end_date)
    max_value = 0
    # estimate the netvalue
    est_record = {}
    if records[0]['date'] < str(end_date) and dayOfWeek < 5:
        estimate = get_current_netestimate(code)
        if estimate['date'] != records[0]['date']:
            est_record['date'] = estimate['date']
            est_record[name] = estimate['net']
            est_record[name + '_CP'] = estimate_show(estimate['net_CP'])
            est_record[name + '_HF'] = ''
            est_record[name + '_BM'] = ''
            records.insert(0, est_record.copy())
    records = records[::-1]
    for i in range(0, len(records)):
        records[i][name + '_CP'] = red_green_show(records[i][name + '_CP'])
        max_value = records[i][name] if float(max_value) < float(records[i][name]) else max_value
        if records[i]['date'] == HighVal_start_date:
            HighVal = records[i].copy()
        elif records[i]['date'] > HighVal_start_date:
            if float(records[i][name]) > float(HighVal[name]):
                HighVal[name] = records[i][name]
                fund['buy'] = 0
            else:
                HighFall = float(records[i][name]) / float(HighVal[name]) - 1.0
                multiple_HF = int(HighFall // fund['threshold'])
                if multiple_HF > fund['buy']:
                    records[i][name + '_BM'] = (accumulate(multiple_HF) - accumulate(fund['buy'])) * fund['single']
                    fund['buy'] = multiple_HF
                str_HF = str(format(HighFall * 100, '.2f')) + '%'
                records[i][name + '_HF'] = str_HF
                records[i][name + '_HF'] = yellow_show(str_HF) if records[i][name + '_BM'] != '' else records[i][
                    name + '_HF']
    records = records[::-1]
    # print(max_value)
    return records, max_value


def show_table(funds, start_date, end_date, HighVal_start_date, show_rows=0):
    header = []
    records_set = []
    max_str = ''
    for i in range(0, len(funds)):
        records, max_value = get_records_of_one_fund(start_date, end_date, funds[i], HighVal_start_date)
        max_HF = format((float(records[0][funds[i]['name']]) / float(max_value) - 1.0) * 100, '.2f') + '%'
        max_str += funds[i]['name'] + ': ' + str(max_value) + ' (HF: ' + red_green_show(max_HF) + ')\t'
        for key, value in records[0].items():
            header.append(key)
        records_set.append(records)
    # if show_rows == 0:
    #     show_rows = len(records)
    show_rows = len(records) if show_rows == 0 else show_rows
    header = sorted(set(header), key=header.index)
    table = PrettyTable(header, encoding=sys.stdout.encoding)
    table.align = 'r'
    rows = []
    for i in range(0, len(records_set)):
        records = records_set[i]
        for j in range(0, show_rows):
            row = []
            if i == 0:
                for key, value in records[j].items():
                    row.append(value)
                rows.append(row)
            else:
                for key, value in records[j].items():
                    if key != 'date':
                        rows[j].append(value)
    table.add_rows(rows)
    print(max_str)
    return table
