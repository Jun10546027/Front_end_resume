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

#時間變數的轉換設置
def set_date(row):
    #藉由開發人員工具，發現到它會把時間變數乘1000
    #格式化時間變數
    time = (row['datetime']/1000)
    time = datetime.datetime.fromtimestamp(time)
    row['datetime'] = time
    return row

#將每一行傳進set_date進行時間變數的轉換
df = df.apply(lambda row:set_date(row), axis=1)
df1 = df1.apply(lambda row:set_date(row), axis=1)


df.set_index('datetime',inplace=True)
df1.set_index('datetime',inplace=True)

mvg30 = df['value'].rolling(window=30).mean()
mvg7 = df1['value'].rolling(window=7).mean()


#設定位置------------------df---------------------------------------
plt.subplot(2,1,1)

plt.plot(df,label = 'Bitcoin tendency')
plt.plot(mvg30,label = 'Bitcoin mvg')
print("由古至今的彼特幣標準差",df['value'].std())
print("由古至今的彼特幣各項描述",df['value'].describe())
print("樣本數",len(df['value']))
plt.legend()

plt.title("All of Bitcoin tendency / month",loc="right")
plt.ylabel('value')
plt.xlabel('time')
#設定位置------------------df---------------------------------------

#設定位置------------------df1---------------------------------------
plt.subplot(3,1,3)

plt.plot(df1,label = 'Bitcoin tendency of year')
plt.plot(mvg7,label = 'Bitcoin mvg of week')
print("================分隔線================")
print("單位為一年的彼特幣標準差",df1['value'].std())
print("單位為一年的彼特幣各項描述",df1['value'].describe())
print("樣本數",len(df1['value']))
plt.legend()

plt.title("Bitcoin tendency of year/ week",loc="right")
plt.ylabel('value')
plt.xlabel('time')
#設定位置------------------df1---------------------------------------

#-----------------df2(每月份平均圖)---------------------------------------
df2 = pd.DataFrame(jd_year['stats'])
df2.columns = ['datetime','value']

#時間變數的轉換設置(這裡改了時間的format，因為要以月來判斷時間)
def set_df2_time(row):
    #藉由開發人員工具，發現到它會把時間變數乘1000
    #格式化時間變數
    time = (row['datetime']/1000)
    time = datetime.datetime.fromtimestamp(time).strftime("%Y-%m")
    row['datetime'] = time
    return row

df2 = df2.apply(lambda row:set_df2_time(row), axis=1)


#最後要畫圖的資料
month_mvg = []
month_time = []

# print(df2.loc[0,'value'])
def month_total():
    total = 0
    day = 0
    for i in range(1,len(df2)-1):
        #     df.loc -> 可以藉由index和colunn，來找數據
        # df2.iloc[-1]['value'] ->最後一行的value，意即df[364]
        #  if 有順序性 如果將最後一天的判斷擺在elif，會被前面的if覆蓋掉，所以將最後一天的判斷放在if
        if int(df2.iloc[-1]['value']) == int(df2.loc[i, 'value']):
            #避免最後一天跨月
            if df2.loc[i, 'datetime'] == df2.loc[i - 1, 'datetime']:
                total = total + df2.loc[i - 1, 'value'] + df2.loc[i, 'value']
                # 因為要要加上 倒數第二天 和 倒數第一天的數值
                day = day + 2

                month_mvg.append(total / day)
                month_time.append(df2.loc[i-1, 'datetime'])

            else:
                total = total + df2.loc[i - 1, 'value']
                day = day + 1

                month_mvg.append(total / day)
                month_time.append(df2.loc[i - 1, 'datetime'])
                month_mvg.append(df2.loc[i, 'value'])
                month_time.append(df2.loc[i,'datetime'])

        #如果是同個月份的話，就累加
        elif df2.loc[i,'datetime'] == df2.loc[i-1,'datetime']:
            total = df2.loc[i-1, 'value'] + total
            day = day + 1

        #不是同個月分，就進行平均數
        else:
            total = total + df2.loc[i-1,'value']
            day = day + 1

            month_mvg.append(total/day)
            month_time.append(df2.loc[i-1,'datetime'])
            day=0
            total=0

month_total()

#新增一張圖
plt.figure(figsize=(12,4))

#畫圖並設定label
plt.bar(month_time,month_mvg,width=0.35,label = "mean(USD)",facecolor = 'lightgreen', edgecolor = 'white')
plt.legend()

#在長條圖上加上文字
for x,y in zip(month_time,month_mvg):
    #設定文字位置，%.2f為設定出現的值，這裡指到小數第二位
    plt.text(x, y+0.05, '%.2f ' % y, ha='center', va= 'bottom')

#設定圖片標題，X軸，Y軸
plt.xlabel("month")
plt.ylabel("value")
plt.title("monthly mean")
#------------------df2(每月份平均圖)---------------------------------------

#------------------df3(圓餅圖)---------------------------------------
plt.figure()
# print(month_time)
# print(month_mvg)
mvg_autopct = []
small_autopc=[]
time_set=[]
total_mvg = 0
other_total = 0

for i in month_mvg:
    total_mvg = total_mvg + i


#計算比例
for i in month_mvg:
    every_mvg_autopct = round((i / total_mvg)*100,2)
    mvg_autopct.append(every_mvg_autopct)

#計算比例小於平均值的月份
for t in range(len(month_time)):
    if mvg_autopct[t] <= 8.3:
        small_autopc.append(mvg_autopct[t])
        time_set.append(month_time[t])
    else:
        other_total= other_total+mvg_autopct[t]
small_autopc.append(other_total)
time_set.append("other time")

# small_autopc.append(other_total)

plt.pie(small_autopc,
        labels = time_set,
        autopct = "%1.1f%%",        # 將數值百分比並留到小數點一位
        pctdistance = 0.6,          # 數字距圓心的距離
        textprops = {"fontsize" : 8},#文字大小
        )

plt.axis('equal') # 使圓餅圖比例相等
plt.title("Price is lower than 8%", {"fontsize" : 12},loc="left")  # 設定標題及其文字大
plt.legend(loc = "best")

#------------------df3(圓餅圖)---------------------------------------
plt.show()