import tushare as ts
import pandas as pd
import datetime
import os
import xlwings as xw

pro = ts.pro_api('**')
os.chdir('/Users/**/Documents/03_Python/股票')


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


def daily_pct(date):
    daily = pro.daily(trade_date=date, fields="ts_code,pct_chg,close,amount")
    daily2 = daily.set_index('ts_code')
    create_excel("股票.xlsx", "股票", date, daily2, "pct_chg")
    # create_excel("股票.xlsx", "股票", date, daily2, "close")
    # create_excel("股票.xlsx", "股票", date, daily2, "amount")


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


def reven(Q):
    q = {"Q1": "20210331", "Q2": "20210630", "Q3": "20210930", "Q4": "20211231"}
    reven_value = pro.income_vip(period=q[Q], fields='ts_code,ann_date,f_ann_date,end_date,total_revenue,'
                                                     'n_income_attr_p')
    reven_value2 = reven_value.set_index('ts_code')
    # reven_value2 = reven_value.set_index('ts_code').drop_duplicates()
    # reven_value2.drop_duplicates(subset=['ts_code'], keep='last', inplace=True)
    reven_value2 = reven_value2[~reven_value2.index.duplicated(keep='last')]
    create_excel("股票.xlsx", "股票", "收入", reven_value2, "total_revenue")
    create_excel("股票.xlsx", "股票", "利润", reven_value2, "n_income_attr_p")


if __name__ == "__main__":
    print("---Starting---")
    today, ysday = ts_date()
    print("Today is", today)
    # daily_pct(today)
    daily_pct("20211104")
    # s_pe = pro.daily_basic(ts_code='', trade_date=today, fields='ts_code,pe_ttm,total_mv')
    # s_pe = s_pe.set_index('ts_code')
    # create_excel("股票.xlsx", "股票", str(today)+"-PE", s_pe, "pe_ttm")
    # create_excel("股票.xlsx", "股票", str(today)+"-市值", s_pe, "total_mv")
    # reven("Q3")
    # reven("Q2")

    print("---Finished---")
