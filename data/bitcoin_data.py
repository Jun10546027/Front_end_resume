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



