from collections import namedtuple
from typing import NamedTuple
from class_ticker_descriptor import DataTicker
import pandas as pd
from concurrent import futures
from time import perf_counter

from settings import TICKER_FOR_LOAD, PARAMS


KEY = TICKER_FOR_LOAD
MA_PERIOD: tuple[int, int, int] = (24, 50, 100)
WORKERS = None

total_daily = []


def single_calc(ticker: str) -> NamedTuple:
    global MA_PERIOD
    ma1, ma2, ma3 = MA_PERIOD
    obj = (DataTicker(ticker, ma1, 1))
    ma_period_gen = ((DataTicker(ticker, ma, 1)).data_cr.iloc[-1, 8] for ma in MA_PERIOD[1:]) 
    ticker_ma = namedtuple('Ticker_ma', ['TICKER', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 
                                         f'MA{ma1}', f'MA{ma2}', f'MA{ma3}'])
    OPEN, HIGH, LOW, CLOSE = obj.data.iloc[-1][4:8]
    ma1_value, ma2_value, ma3_value = obj.data_cr.iloc[-1, 8], next(ma_period_gen), next(ma_period_gen)
    obj_MA = ticker_ma(ticker, OPEN, HIGH, LOW, CLOSE, ma1_value, ma2_value, ma3_value)
    return obj_MA._asdict()

def extr_delta(MA, extr):
    delta_extr = extr- MA
    extr_ma = delta_extr*100/MA
    return extr_ma

def save_toexcel(frame, file = r'Load_data\dayly.xlsx'):
    frame.to_excel(file, index=False)

def main() -> None:
    global total_daily
    if WORKERS: 
        workers = WORKERS
    else:
        workers = None
    
    t0 = perf_counter()
    # print(f'Calculation with {executor._max_workers} processes')
    
    with futures.ProcessPoolExecutor(workers) as executor:
        print(f'Calculation with {executor._max_workers} processes')
        for result in executor.map(single_calc, KEY):
            total_daily.append(result)
        
        
    daily_frame = pd.DataFrame(total_daily)

    number_column = 6 #Номер колокни за которой будут вставлены две новые колонки.
    for i in MA_PERIOD:
        name_column = 'MA{}'.format(i)
        exd = extr_delta(daily_frame[name_column], daily_frame['HIGH'])
        daily_frame.insert(number_column, f'%HIGH-{name_column}', exd)
        exd = extr_delta(daily_frame[name_column], daily_frame['LOW'])
        daily_frame.insert(number_column +1, f'%LOW-{name_column}', exd)
        number_column += 3
    
    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')
    save_toexcel(daily_frame)




if __name__ == '__main__':
    main()

