import pandas as pd
from class_ticker_descriptor import DataTicker

def obj_params(obj: DataTicker) -> tuple[str, int, list[list[int]]]:
    '''Функция для '''
    if obj.type_deel == True: #Тип сделки.
        name_deel = 'Long'
        open = obj.data['LOW']
        extremum = obj.data['HIGH']
    else:
        name_deel = 'Short'
        open = obj.data['HIGH']
        extremum = obj.data['LOW']

    long = obj.type_deel
    duration = obj.hold_time
    res = get_data(open, extremum, duration, long)
    return (name_deel, duration, res)


def get_data(open: list[float]|pd.Series, extremum: list[float]|pd.Series, 
             duration: int, long: bool = True) -> list[list[int]]:
    '''Функция расчитывает максимальный возможный проффит в процентах на срок удержания от 1го до duration дней
    на каждый торговый день.
    open - список значений открытия сделки,
    extremum - список значений HIGH или LOW,
    duration -  максимальный срок удержания позиции,
    long - если сделка лонг то True, если нет то False'''
    
    total_prof_list: list[list[int]] = []
    for i in range(len(open)):
        open_deal = open[i]
        prof_list: list[int] = []
        
        for n in range(1, duration + 1):
            if long:
                prof = max(extremum[i:(i + n)])
                prof_percent = prof * 100 / open_deal - 100
            else:
                prof = min(extremum[i:(i +n)])
                prof_percent = 100 - prof * 100 / open_deal
            prof_list.append(int(prof_percent))
        
        total_prof_list.append(prof_list)
    
    return total_prof_list



def get_data_for_broken_barh(list_data: list[float]) -> tuple[list[tuple[int, int]], list[bool]]:
    '''Функция расчитывает диапазоны индексов когда происходит смена тренда в изменении ряда чисел.
    list_data - список значений
    Возвращает кортеж из списка с кортежами индексов значений, и списка булинговых значений.
    '''
    
    #этот блок строит список data из булинговых значений, True если текущее значение выше предыдущего,
    #False если текущее значение ниже предыдущегою
    data = []
    prev_data = list_data[0]
    for value in list_data[1:]:
        if value >= prev_data:
            data.append(True)
        else:
            data.append(False)
        prev_data = value

    #этот блок строит список count_change из индексов значений списка data на которых происходит 
    # смена булинговых значений. 
    count = 0
    count_change = []
    prev_bool = data[0]
    for i in data[1:]:
        if i == prev_bool:
            count += 1
            continue
        else:
            prev_bool = i
            count += 1
            count_change.append(count)
    count_change.append(count)

    
    #этот блок готовит данные для return на основе предыдущих расчётов
    data_for_broken_barh = []
    prev_index = 0
    for i in count_change:
        data_range = prev_index, i - prev_index
        data_for_broken_barh.append(data_range)
        prev_index = i
    data_for_return = (data_for_broken_barh, data)
    return data_for_return

