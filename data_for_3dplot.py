import pandas as pd


def get_data(open: list[float], extremum: list[float], duration: int, long: bool = True) -> list[list[int]]:
    '''Функция расчитывает *******************************************************************.
    open - список значений ***************************,
    extremum - список значений *************************,
    duration -  *********************************************,
    long - если *************** то True, если нет то False'''
    
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




