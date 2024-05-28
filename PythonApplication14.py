# -*- coding: cp1251 -*-

import requests
import json
import datetime
import pandas as pd
import numpy as np
import openpyxl

# Задаем URL-адрес API Binance для получения списка торговых пар по рейтингу
symbol_url = 'https://api.binance.com/api/v3/exchangeInfo'

# Отправляем GET-запрос к API для получения списка торговых пар
symbol_response = requests.get(symbol_url)

# Проверяем статус код ответа
if symbol_response.status_code != 200:
    print('NO SYMBOL')
    exit()

# Получаем данные из ответа в формате JSON
symbol_data = symbol_response.json()
# Извлекаем символы первых десяти торговых пар
symbols = [symbol['symbol'] for symbol in symbol_data['symbols'] if symbol['symbol'].endswith('USDT')][:1000]

# Задайте параметры запроса
#symbols = ['BTCUSDT','ETHUSDT','BNBUSDT','LTCUSDT','ETCUSDT','LINKUSDT','WAVESUSDT','XMRUSDT','THETAUSDT','MATICUSDT','ATOMUSDT','DUSKUSDT','MTLUSDT','TOMOUSDT','KEYUSDT','CHZUSDT','BANDUSDT','HBARUSDT','NKNUSDT','RLCUSDT','BCHUSDT','SOLUSDT','MDTUSDT','KNCUSDT']  # Символы торговых пар
interval = '4h'    # Интервал времени (4 часа)
limit = 400        # Количество записей (неделя = 6 записей)
z_values = []
dfx = pd.DataFrame()
x = 1
syms = [] # Список для хранения временных меток начала суток
for symbol in symbols:
    candle_ranges = []  # Список для хранения значений candle_range
    body_ranges = []    # Список для хранения значений body_range
    timestamps = [] # Список для хранения временных меток начала суток
    closes = [] # Список для хранения временных меток начала суток
    highes = [] # Список для хранения временных меток начала суток
    lowes = [] # Список для хранения временных меток начала суток
    x_values = []
# Переводим текущую дату и время в миллисекунды (timestamp)
    end_timestamp = int(datetime.datetime.now().timestamp() * 1000)

    # Вычисляем начальную дату и время (1 неделя назад)
    start_timestamp = end_timestamp - (400 * 4 * 60 * 60 * 1000)

    # Задаем URL-адрес API Binance для получения кандловых данных
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}&startTime={start_timestamp}&endTime={end_timestamp}'

    # Отправляем GET-запрос к API
    response = requests.get(url)
    # Проверяем статус код ответа
    if response.status_code != 200:
        print(f'NO SYMBOL {symbol}')
        continue

    # Получаем данные из ответа в формате JSON
    data = response.json()
    if len (data)==0:
            continue
    print(f'{x} Symbol: {symbol}')
    x=x+1
    #syms.append(symbol)
    # Итерируемся по данным и выводим каждую запись
    syms=''
    syms = ('https://ru.tradingview.com/chart/5EOV4Q5y/?symbol=BINANCE:'+symbol)

    min_price=''
    price_step=''
    url1 = f'https://api.binance.com/api/v3/exchangeInfo?symbol={symbol}'
    response1 = requests.get(url1)
    if response1.status_code == 200:
        data1 = response1.json()
        filters1 = data1['symbols']
        filters2 = filters1[0]
        filters = filters2['filters']
    for filter in filters:
        if filter['filterType'] == 'PRICE_FILTER':
            min_price = float(filter['minPrice'])
            price_step = float(filter['tickSize'])
            #print(f"Шаг цены: {price_step}, Минимальная цена: {min_price}")
            
    

    for candle in data:
        open_time = datetime.datetime.utcfromtimestamp((int(candle[0])/1000)+25200).strftime('%Y-%m-%d %H:%M:%S')
        close_time = datetime.datetime.utcfromtimestamp(int(candle[6])/1000).strftime('%Y-%m-%d %H:%M:%S')
        open_price = float(candle[1])
        high_price = float(candle[2])
        low_price = float(candle[3])
        close_price = float(candle[4])
        volume = float(candle[5])
        candle_range = high_price - low_price
        body_range = abs(open_price - close_price)
        XDATA = datetime.datetime.utcfromtimestamp((int(candle[0])/1000)+25200)

        # Добавляем значения candle_range и body_range в соответствующие списки
        candle_ranges.append(candle_range)
        body_ranges.append(body_range)
        x_values.append(XDATA)
        closes.append(close_price)
        highes.append(high_price)
        lowes.append(low_price)


        # Получаем временную метку начала суток
        timestamp = int(candle[0])  # Временная метка в миллисекундах
        dt = datetime.datetime.utcfromtimestamp(timestamp / 1000)  # Преобразование в datetime
        start_of_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)  # Начало текущих суток   
        timestamps.append(start_of_day.timestamp() * 1000)  # Временная метка в миллисекундах
            
    df = pd.DataFrame({
        f'{symbol}': body_ranges,
    })
    cf = pd.DataFrame({
        f'cl': closes,
    })
    hf = pd.DataFrame({
        f'hi': highes,
    })
    lf = pd.DataFrame({
        f'lo': lowes,
    })






# Размер группы и смещение
    group_size = 5
    offset = 1

# Нахождение максимальных значений по группам с заданным смещением
    max_values = []
    for i in range(0, group_size + group_size - 1, offset):
        max_values.append(0)
    for i in range(group_size+group_size-1, len(hf) , offset):
        max = 0
        j = i - group_size * 2+1
        while j < i:
            hfhf=float(hf.iat[j,0])              
     
            if hfhf > max:
                max = hfhf
            else:
                ty=1
            j+=1
        mf=float(hf.iat[j-group_size,0])
        if mf == max:
            max_values.append (max)
        else:
            max_values.append (max_values[i - 1])
    
    min_values = []
    for i in range(0, group_size + group_size - 1, offset):
        min_values.append(0)
    for i in range(group_size+group_size-1, len(lf) , offset):
        min = 10000000000
        j = i - group_size * 2+1
        while j < i:
            lflf=float(lf.iat[j,0])              
     
            if lflf < min:
                min = lflf
            else:
                ty=1
            j+=1
        ml=float(lf.iat[j-group_size,0])
        if ml == min:
            min_values.append (min)
        else:
            min_values.append (min_values[i - 1])
    
            
    hm = pd.DataFrame({
        f'hm': max_values,
    })
    lm = pd.DataFrame({
        f'lm': min_values,
    })
    #cf.append(hf)
    #cf.append(lf)
    #cf.append(hm)
    #cf.append(lm)
    #dataframe3 = cf.append(hf, ignore_index=True, sort=False)
    #print(sm)
    #print(hf)
    #print(lf) 
    #print(hm)
    #print(lm)
        
        
        
        
        
    ma2=max_values[len(max_values)-1]
    ma3=max_values[len(max_values)-2]
    ma4=max_values[len(max_values)-3]
    ma5=max_values[len(max_values)-4]
    ma6=max_values[len(max_values)-5]
    ma7=max_values[len(max_values)-6]
    mi2=min_values[len(min_values)-1]
    mi3=min_values[len(min_values)-2]
    mi4=min_values[len(min_values)-3]
    mi5=min_values[len(min_values)-4]
    mi6=min_values[len(min_values)-5]
    mi7=min_values[len(min_values)-6]
    cl2=float(cf.iat[len(cf.index)-1, 0])
    cl3=float(cf.iat[len(cf.index)-2, 0])
    cl4=float(cf.iat[len(cf.index)-3, 0])
    cl5=float(cf.iat[len(cf.index)-4, 0])
    cl6=float(cf.iat[len(cf.index)-5, 0])
    cl7=float(cf.iat[len(cf.index)-6, 0])
    stop=cl2*0.0015

    if cl2>ma2:
        da2=1
    else:
        ty=1
    if cl2<mi2:
        da2=-1
    else:
        ty=1
    if cl2<ma2 and cl2>mi2:
        da2=0
    else:
        ty=1
    if cl3>ma3:
        da3=1
    else:
        ty=1
    if cl3<mi3:
        da3=-1
    else:
        ty=1
    if cl3<ma3 and cl3>mi3:
        da3=0
    else:
        ty=1
    if cl4>ma4:
        da4=1
    else:
        ty=1
    if cl4<mi4:
        da4=-1
    else:
        ty=1
    if cl4<ma4 and cl4>mi4:
        da4=0
    else:
        ty=1
    if cl5>ma5:
        da5=1
    else:
        ty=1
    if cl5<mi5:
        da5=-1
    else:
        ty=1
    if cl5<ma5 and cl5>mi5:
        da5=0
    else:
        ty=1
    if cl6>ma6:
        da6=1
    else:
        ty=1
    if cl6<mi6:
        da6=-1
    else:
        ty=1
    if cl6<ma6 and cl6>mi6:
        da6=0
    else:
        ty=1
    if cl7>ma7:
        da7=1
    else:
        ty=1
    if cl7<mi7:
        da7=-1
    else:
        ty = 1
    if cl7<ma7 and cl7>mi7:
        da7 = 0
    else:
        ty = 1
    
    di2 = ma2-mi2


    a2 = df.iat[len(df.index)-2, 0]
    a3 = df.iat[len(df.index)-3, 0]
    a4 = df.iat[len(df.index)-4, 0]
    a5 = df.iat[len(df.index)-5, 0]
    a6 = df.iat[len(df.index)-6, 0]
    a7 = df.iat[len(df.index)-7, 0]
    mean = df.mean()
    m = mean.iloc[0]


    r1=(a2-m)/m
    if r1>0: r1+=1
    r2=(a3-m)/m
    if r2>0: r2+=1
    r3=(a4-m)/m
    if r3>0: r3+=1
    r4=(a5-m)/m
    if r4>0: r4+=1
    r5=(a6-m)/m
    if r5>0: r5+=1
    r6=(a7-m)/m
    if r6>0: r6+=1
    d1=df.iat[len(df.index)-2, 0]
    d2=df.iat[len(df.index)-3, 0]
    if d2!=0:
        d11 = d1/d2

    else:
        d11=0

    d2 = df.iat[len(df.index)-3, 0]
    d3 = df.iat[len(df.index)-4, 0]
    if d3 != 0:
        d12 = d2/d3
    else:
        d12=0
    d3=df.iat[len(df.index)-4, 0]
    d4=df.iat[len(df.index)-5, 0]
    if d4!=0:
        d13=d3/d4
    else:
        d13=0
    d4=df.iat[len(df.index)-5, 0]
    d5=df.iat[len(df.index)-6, 0]
    if d5!=0:
        d14=d4/d5
    else:
        d14=0
    d5=df.iat[len(df.index)-6, 0]
    d6=df.iat[len(df.index)-7, 0]
    if d6!=0:
        d15=d5/d6
    else:
        d15=0
    d6=df.iat[len(df.index)-7, 0]
    d7=df.iat[len(df.index)-8, 0]
    if d7!=0:
        d16=d6/d7
    else:
        d16 = 0
        
    cd2 = di2/cl2*100
    if di2 > 0:
        pc = price_step/di2*100
    
    if pc > 0:
        #if da2!=0:
            df.loc['стоп'] = [stop]
            df.loc['средн'] = [m]
            df.loc['выш.ср2'] = [r1]
            df.loc['выш.ср3'] = [r2]
            #df.loc[len(df.index)] = [r3]
            #df.loc[len(df.index)] = [r4]
            #df.loc[len(df.index)] = [r5]
            #df.loc[len(df.index)] = [r6]
            df.loc['выш.пр2'] = [d11]
            df.loc['выш.пр3'] = [d12]
            #df.loc[len(df.index)] = [d13]
            #df.loc[len(df.index)] = [d14]
            #df.loc[len(df.index)] = [d15]
            #df.loc[len(df.index)] = [d16]
            df.loc['цен'] = [cl2]
            df.loc['диап$'] = [di2]
            df.loc['%ди'] = [cd2]
            df.loc['п2'] = [da2]
            df.loc['п3'] = [da3]
            df.loc['п4'] = [da4]
            df.loc['п5'] = [da5]
            df.loc['п6'] = [da6]
            df.loc['п7'] = [da7]
            #df.loc[len(df.index),'средн'] = [min_price]
            df.loc['шаг'] = [price_step]
            df.loc['%д'] = [pc]
            df.loc['ссыл'] = [syms]


    df = df[::-1]
    df_transposed = df.T
    dfx = pd.concat([dfx, df_transposed])

#df.rename(columns = {' 400 ':' средн', '401 ':' выш.ср2 '}, inplace = True )
now = datetime.datetime.now()    
file = now.strftime("%d-%m-%Y-%H")+'.xlsx'  
dfx.to_excel(file)