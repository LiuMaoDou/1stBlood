def chi_chang(code):
    df = pro.fund_portfolio(ts_code=code)
    df_latest = df[df['end_date']=="20210930"]
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
    data.rename(columns={'ts_code':'symbol'},inplace=True)
    result = pd.merge(df_latest,data, on = "symbol")
    result.sort_values("mkv",ascending=False,inplace=True)
    return result
  

  
df1 = pro.fund_basic(market='O',status='L')
df2 = pro.fund_basic(market='O',status='I')
df3 = pro.fund_basic(market='E',status='L')
df4 = pro.fund_basic(market='E',status='I')
df = df1.append(df2).append(df3).append(df4)
