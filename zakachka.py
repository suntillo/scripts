import time
import sys
import matplotlib.pyplot as plt
import pandas as pd
from binance import Client


# Проверка на наличие аргумента командной строки
if len(sys.argv) != 2:
    print("Использование: py zakachka.py <символ>")
    #sys.exit(1)

# Получение символа из аргумента командной строки
#sym = sys.argv[1]
bb=20
b=50
m=200
sym='ETHUSDT'

api_key = "SwO2TuUBmccphz25XzHsY82UKYz3JMuRlgAz55GPebE8NCy0w4yzLf5sJQLdNxgR"
api_secret = "NKSBZB8ZDVLy9LWGoNpNoRfBhJcEEb2dcKmDnMmOniws2okPje38PfkDWAcztPua"
client = Client(api_key, api_secret)
trades = client.futures_historical_trades(symbol=sym, limit=1)
target_id = trades[0]['id'] - 1000
time0 = int(trades[0]['time'] / 1000)
time1 = (time0 - 60 * 60 * 24) * 1000
print(time0)
print(time1)
print(target_id)
#print("\nИсторические сделки:")
#print(trades)

all_trades = []
last_trade_time = 0

while last_trade_time == 0 or last_trade_time >= time1:
    trades = client.futures_historical_trades(symbol=sym, fromId=target_id, limit=1000)

    if not trades:
        break

    all_trades.extend(trades)
    last_trade_time = trades[0]['time']

    # Увеличиваем target_id для следующего запроса
    target_id = trades[0]['id'] - 1000
    #print(f"Загружено {len(all_trades)} сделок.")
    # Небольшая пауза, чтобы не превышать лимиты API Binance
    time.sleep(0.5)

#print(f"Загружено {len(all_trades)} сделок.")
#all_trades = all_trades.sort_values(by='id', ascending=False)
# Создание словаря для агрегации данных
all_trades.sort(key=lambda x: x['qty'], reverse=True)
aggregated_data = {}

# Обработка данных и агрегация
for trade in all_trades:
    price_part = round(float(trade['price']) * 10/3)*3/10
    time_part = round(int(trade['time']) / 60000)*60000
    qty_part = float(trade['qty'])*-1
    if not trade['isBuyerMaker']:
        qty_part *= -1


    key = (price_part, time_part)
    if key in aggregated_data:
        aggregated_data[key]['zn'] += qty_part
    else:
        aggregated_data[key] = {'ax': time_part, 'ay': price_part, 'zn': qty_part}

# Преобразование aggregated_data в список словарей
aggregated_list = list(aggregated_data.values())

# Создание DataFrame
new_df = pd.DataFrame(aggregated_list)

# Вывод DataFrame
#print("\nDataFrame:")
print(new_df)

new_df = new_df.sort_values(by='zn', ascending=False)
bbp = new_df['zn'].iloc[bb]
bb1=bb*-1
bbm = new_df['zn'].iloc[bb1]
bp = new_df['zn'].iloc[b]
b1=b*-1
bm = new_df['zn'].iloc[b1]
mp = new_df['zn'].iloc[m]
m1=m*-1
mm = new_df['zn'].iloc[m1]
# Фильтрация строк по условию
dfbbp = new_df[(new_df['zn'] > bbp)]
dfbbm = new_df[(new_df['zn'] < bbm)]
dfbp = new_df[(new_df['zn'] > bp)]
dfbm = new_df[(new_df['zn'] < bm)]
dfmp = new_df[(new_df['zn'] > mp)]
dfmm = new_df[(new_df['zn'] < mm)]

#print(df3000)
# Преобразование данных для построения графика
x = new_df['ax']
y = new_df['ay']
#z = df3000['zn']
# Создание точечного графика
plt.figure(figsize=(48, 27))
spr = sym+' '+str(bbp)+' '+str(bp)+' '+str(mp)
plt.text(new_df['ax'].min(), new_df['ay'].max(), spr, color="r")
plt.gca().set_facecolor('k')
plt.scatter(x, y, s=5, c='grey', marker='s')  # s - размер маркера, c - цвет маркера, cmap - цветовая схема

x5 = dfmp['ax']
y5 = dfmp['ay']
plt.scatter(x5, y5, s=20, c='r', marker='s')  # s - размер маркера, c - цвет маркера, cmap - цветовая схемаx1 = df3000['ax']

x6 = dfmm['ax']
y6 = dfmm['ay']
plt.scatter(x6, y6, s=20, c='g', marker='s')  # s - размер маркера, c - цвет маркера, cmap - цветовая схемаx1 = df3000['ax']

x3 = dfbp['ax']
y3 = dfbp['ay']
plt.scatter(x3, y3, s=100, c='r', marker='s')  # s - размер маркера, c - цвет маркера, cmap - цветовая схемаx1 = df3000['ax']

x4 = dfbm['ax']
y4 = dfbm['ay']
plt.scatter(x4, y4, s=100, c='g', marker='s')  #

x1 = dfbbp['ax']
y1 = dfbbp['ay']
plt.scatter(x1, y1, s=200, c='y', marker='s')  # s - размер маркера, c - цвет маркера, cmap - цветовая схемаx1 = df3000['ax']

x2 = dfbbm['ax']
y2 = dfbbm['ay']
plt.scatter(x2, y2, s=200, c='m', marker='s')




plt.savefig(sym+'screen.png')

plt.show()


#print(df3000)

