import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#添加自定義感應器，參考網址:https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.plotting.register_matplotlib_converters.html
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#資料來源
res_max = requests.get('https://www.coingecko.com/price_charts/1/usd/max.json')
jd_max = res_max.json()

res_year = requests.get('https://www.coingecko.com/price_charts/1/usd/365_days.json')
jd_year = res_year.json()

#look for index
# print(jd)
df = pd.DataFrame(jd_max['stats'])
df.columns = ['datetime','value']

df1 = pd.DataFrame(jd_year['stats'])
df1.columns = ['datetime','value']

# removing null values to avoid errors
df.dropna(inplace = True)
df1.dropna(inplace = True)


#時間變數的轉換設置
def set_date(row):
    #藉由開發人員工具，發現到它會把時間變數乘1000
    #格式化時間變數
    time = (row['datetime']/1000)
    time = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d")
    row['datetime'] = time
    return row


#將每一行傳進set_date進行時間變數的轉換
df = df.apply(lambda row:set_date(row), axis=1)
df1 = df1.apply(lambda row:set_date(row), axis=1)


#---------------Bar Data-----------------------------------------
df2 = pd.DataFrame(jd_year['stats'])
df2.columns = ['datetime','value']

def set_month_time(row):
    #藉由開發人員工具，發現到它會把時間變數乘1000
    #格式化時間變數
    time = (row['datetime']/1000)
    time = datetime.datetime.fromtimestamp(time).strftime("%Y-%m")
    row['datetime'] = time
    return row

df2 = df2.apply(lambda row:set_month_time(row), axis=1)

def month_total(df,lvalue,ltime):
    total = 0
    day = 0
    for i in range(1,len(df)-1):
        #     df.loc -> 可以藉由index和colunn，來找數據
        # df.iloc[-1]['value'] ->最後一行的value，意即df[364]
        #  if 有順序性 如果將最後一天的判斷擺在elif，會被前面的if覆蓋掉，所以將最後一天的判斷放在if
        if int(df.iloc[-1]['value']) == int(df.loc[i, 'value']):
            #避免最後一天跨月
            if df.loc[i, 'datetime'] == df.loc[i - 1, 'datetime']:
                total = total + df.loc[i - 1, 'value'] + df.loc[i, 'value']
                # 因為要要加上 倒數第二天 和 倒數第一天的數值
                day = day + 2

                lvalue.append(total / day)
                ltime.append(df.loc[i-1, 'datetime'])

            else:
                total = total + df.loc[i - 1, 'value']
                day = day + 1

                lvalue.append(total / day)
                ltime.append(df.loc[i - 1, 'datetime'])
                lvalue.append(df.loc[i, 'value'])
                ltime.append(df.loc[i,'datetime'])

        #如果是同個月份的話，就累加
        elif df.loc[i,'datetime'] == df.loc[i-1,'datetime']:
            total = df.loc[i-1, 'value'] + total
            day = day + 1

        #不是同個月分，就進行平均數
        else:
            total = total + df.loc[i-1,'value']
            day = day + 1

            lvalue.append(total / day)
            ltime.append(df.loc[i-1,'datetime'])
            day=0
            total=0

#最後要畫圖的資料
bar_data = []
bar_time = []

month_total(df2,bar_data,bar_time)

#---------------Bar Data-----------------------------------------


#--------------------Line Data------------------------------------------

df.set_index('datetime',inplace=True)
df1.set_index('datetime',inplace=True)

overall_data = df["value"].to_list()
overall_day = df.index.tolist()

year_data = df1["value"].to_list()
year_day = df1.index.tolist()

mvg7 = df1['value'].rolling(window=7).mean()
mvg7.dropna(inplace = True)


year_mvg7_data = mvg7.to_list()
year_mvg7_day = mvg7.index.to_list()
#--------------------Line Data------------------------------------------







