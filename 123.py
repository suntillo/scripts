import binance
import time
from datetime import datetime, timedelta

# API ключи Binance
api_key = "SwO2TuUBmccphz25XzHsY82UKYz3JMuRlgAz55GPebE8NCy0w4yzLf5sJQLdNxgR"
api_secret = "NKSBZB8ZDVLy9LWGoNpNoRfBhJcEEb2dcKmDnMmOniws2okPje38PfkDWAcztPua"

# Символ фьючерса эфира
symbol = "ETHUSDT"

# Время начала (2 дня назад)
start_time = int((datetime.now() - timedelta(days=2)).timestamp() * 1000)

# Создание пустого массива для хранения данных
tick_data = {}

# Функция для обработки тиковых данных
def handle_ticks(msg):
    if msg['e'] == 'kline':
        # Преобразование времени в timestamp
        timestamp = int(msg['k']['t'] / 1000)
        # Сохранение цены, объема в массив с timestamp как ключом
        if timestamp not in tick_data:
            tick_data[timestamp] = []
        tick_data[timestamp].append({'price': msg['k']['c'], 'volume': msg['k']['v']})

# Инициализация клиента Binance
client = binance.Client(api_key, api_secret)

# Получение исторических данных
historical_klines = client.aggregate_trade_iter(symbol=symbol, start_str=start_time)

# Заполнение массива историческими данными
for kline in historical_klines:
    timestamp = int(kline['T'] / 1000)  # Исправлено: получение времени из 'T'
    if timestamp not in tick_data:
        tick_data[timestamp] = []
    tick_data[timestamp].append({'price': kline['p'], 'volume': kline['q']})  # Исправлено: получение цены и объема

# Инициализация и запуск менеджера websocket
twm = binance.ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()

# Подписка на поток тиковых данных
twm.start_kline_socket(callback=handle_ticks, symbol=symbol, interval=binance.Client.KLINE_INTERVAL_1MINUTE)

# Бесконечный цикл для поддержания соединения

    # Остановка менеджера websocket и закрытие соединения
twm.stop()
client.close_connection()

# Вывод массива с данными (для проверки)
print(tick_data)
