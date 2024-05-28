
import pandas as pd
from time import mktime, strptime
import openpyxl as xl
import matplotlib.pyplot as plt

df_data = {}
new_df = pd.DataFrame(columns=['ax', 'ay', 'zn'])
new_df = new_df.dropna(axis=1, how='all')
sym='eth'
# Список файлов для загрузки
files = [

    r"C:\SBProData\local_cachedata\v1.6\ticks\ETH-USDT-FUT\Auto\60\0.3\UTC\0.0\2024-05-22.locchache",
    r"C:\SBProData\local_cachedata\v1.6\ticks\ETH-USDT-FUT\Auto\60\0.3\UTC\0.0\2024-05-23.locchache",
    r"C:\SBProData\local_cachedata\v1.6\ticks\ETH-USDT-FUT\Auto\60\0.3\UTC\0.0\2024-05-24.locchache"
]

for file_path in files:
    with open(file_path, "r") as file:
        for line in file:
            row_name, *row_data = line.strip().split("*")
            row_name, *temp = row_name.split(":")
            row_name = row_name.replace(" ", "").replace(".000", "").replace("2024", "24")
            dtime = strptime(row_name, '%d%m%y%H%M%S')
            row_name = int(mktime(dtime))
            row_data = row_data[0].split("|")
            split_data = [item.split(":") for item in row_data]

            for i in range(len(split_data)):
                column_name = float(split_data[i][0])  # Название столбца
                data = float(split_data[i][2])  # Данные в столбце
            #if column_name not in df_data:
            #    df_data[column_name] = {}  # Создаем столбец, если его нет
            #df_data[column_name][row_name] = data  # Добавляем данные в столбец
                temp_df = pd.DataFrame({
                                    'ax': [row_name],
                                    'ay': [column_name],
                                    'zn': [data]},
                                    index = range(1))  # Добавляем индекс

                new_df = pd.concat([new_df, temp_df], ignore_index=True)
new_df = new_df.sort_values(by='zn', ascending=False)
bbp = new_df['zn'].iloc[9]
bbm = new_df['zn'].iloc[-10]
bp = new_df['zn'].iloc[49]
bm = new_df['zn'].iloc[-50]
mp = new_df['zn'].iloc[199]
mm = new_df['zn'].iloc[-200]
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


