import tushare as ts
import pandas as pd
import datetime
import os
import xlwings as xw
import time
from tkinter import messagebox


pro = ts.pro_api('**')
os.chdir('/Users/**/Documents/03 Python/股票')



def timer(function):
    """
    装饰器函数timer
    :param function:想要计时的函数
    :return:
    """

    def wrapper(*args, **kwargs):
        time_start = time.time()
        res = function(*args, **kwargs)
        cost_time = time.time() - time_start
        print("【%s】运行时间：【%s】秒" % (function.__name__, cost_time))
        return res

    return wrapper


def gp_list():
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,market,list_date')
    data.to_excel('股票.xlsx')


def ts_date(ttoday=True):
    if ttoday:
        today = datetime.date.today()
    else:
        today = datetime.date.today() - datetime.timedelta(days=1)

    if today.isoweekday() > 5:
        today = today - datetime.timedelta(days=(today.isoweekday() % 5))
        ysday = today - datetime.timedelta(days=1)
        today = today.strftime('%Y%m%d')
        ysday = ysday.strftime('%Y%m%d')
    else:
        ysday = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')

    return today, ysday


def create_excel(bookname, sheetname, title, df, df_value):
    print("---Excel Started---")
    # app = xw.App(visible=True, add_book=False)
    # app.display_alerts = False
    # app.screen_updating = False
    wb = xw.Book(bookname)
    sheet = wb.sheets[sheetname]
    num_col = sheet.range('A1').end('right').column
    num_row = sheet.range('A1').end('down').row

    i = 2
    sheet.range((1, (num_col + 1))).value = title

    while i < (num_row + 1):
        try:
            sheet.range((i, (num_col + 1))).value = df.at[sheet.range('A' + str(i)).value, df_value]
        except:
            sheet.range((i, (num_col + 1))).value = "NULL"
        i += 1

    wb.save(bookname)
    # wb.close()
    print("---Excel Finished---")


def create_excel_new(bookname, sheetname, title, df):
    print("---Excel Started---")
    wb = xw.Book(bookname)
    sheet = wb.sheets[sheetname]
    num_col = sheet.range('A1').end('right').column
    num_row = sheet.range('A1').end('down').row

    sheet.range((1, (num_col + 1))).options(index=False).value = df
    sheet.range((1, (num_col + 1))).value = title
    sheet.range((1, num_col), (num_row, num_col)).copy()
    sheet.range((1, (num_col + 1)), (num_row, num_col+1)).paste("formats")
    sheet.range((1, (num_col + 1)), (num_row, num_col + 1)).autofit()
    
    wb.save(bookname)
    print("---Excel Finished---")


def daily_pct(date):
    daily = pro.daily(trade_date=date, fields="ts_code,pct_chg,close,amount")
    daily2 = daily.set_index('ts_code')
    create_excel("股票.xlsx", "股票", date+"-涨跌", daily2, "pct_chg")
    # create_excel("股票.xlsx", "股票", date+"-收盘", daily2, "close")
    # create_excel("股票.xlsx", "股票", date+"成交量", daily2, "amount")


# def daily_pct(date, bookname='股票.xlsx', sheetname='股票'):
#     daily = pro.daily(trade_date=date, fields="ts_code,pct_chg,close")
#     daily2 = daily.set_index('ts_code')

# xw.Book()
# wb = xw.Book(bookname)
# sheet = wb.sheets[sheetname]
# num_col = sheet.range('A1').end('right').column
# num_row = sheet.range('A1').end('down').row
#
# i = 2
# sheet.range((1, (num_col + 1))).value = date
#
# while i < (num_row + 1):
#     try:
#         sheet.range((i, (num_col + 1))).value = daily2.at[sheet.range('A' + str(i)).value, 'pct_chg']
#     except:
#         sheet.range((i, (num_col + 1))).value = "NULL"
#     i += 1
#
# wb.save(bookname)
# print('finished')

def daily_pct_new(date):
    daily = pro.daily(trade_date=date, fields="ts_code,pct_chg,close,amount")
    df_gp = pd.read_excel('股票.xlsx')
    df_merge = pd.merge(df_gp, daily, how='outer', on="ts_code")
    create_excel_new("股票.xlsx", "股票", date+"-涨跌", df_merge['pct_chg'])


def reven(year, Q):
    q = {"Q1": str(year) + "0331", "Q2": str(year) + "0630",
         "Q3": str(year) + "0930", "Q4": str(year) + "1231"}
    reven_value = pro.income_vip(period=q[Q], fields='ts_code,ann_date,f_ann_date,end_date,total_revenue,'
                                                     'n_income_attr_p')
    reven_value2 = reven_value.set_index('ts_code')
    # reven_value2 = reven_value.set_index('ts_code').drop_duplicates()
    # reven_value2.drop_duplicates(subset=['ts_code'], keep='last', inplace=True)
    reven_value2 = reven_value2[~reven_value2.index.duplicated(keep='last')]
    create_excel("股票.xlsx", "股票", str(year) + Q + "-收入", reven_value2, "total_revenue")
    create_excel("股票.xlsx", "股票", str(year) + Q + "-利润", reven_value2, "n_income_attr_p")


@timer
def main():
    # gp_list()
    # reven(2021, "Q3")

    ## PE和市值
    # s_pe = pro.daily_basic(ts_code='', trade_date='20211215', fields='ts_code,pe_ttm,total_mv')
    # s_pe = s_pe.set_index('ts_code')
    # create_excel("股票.xlsx", "股票", "PE", s_pe, "pe_ttm")
    # create_excel("股票.xlsx", "股票", "市值", s_pe, "total_mv")
    ## PE和市值

    # today, ysday = ts_date()
    # print("Today is", today)
    # daily_pct(today)
    # daily_pct("20211215")
    daily_pct_new("20211215")


if __name__ == "__main__":
    print("---Starting---")
    main()
    messagebox.showinfo('股票', '...完成任务...')
    print("---Finished---")
