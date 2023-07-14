import pandas as pd
from collections import deque


from settings import DIR_FOR_LOAD as DIR

class Build:
    '''Дескриптор для вызова метода DT_Build.build при присвоении нового значения атрибуту
       в экземплярах класса DataTicker'''
    
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value
        
        if (hasattr(instance, 'ma_period'), 
            hasattr(instance, 'hold_time'), 
            hasattr(instance, 'type_deel')) == True:
            instance.build()

    

class DT_Build:
    '''Класс с методами для построения DataFrame c дополнительными колонками данных'''
    
    def build(self):
        self.__create_MA()
        self.__create_DELTA()
        self.__create_pl()  

    def __create_MA(self):
        '''метод добавление колонки значения скользящей средней'''

        ma_queue = deque([], maxlen=self.ma_period) #Очередь для значений средних за период
        self.data_cr = self.data.copy()
        for i in self.data.index:
            ma_i = self.data.loc[i][['OPEN', 'HIGH', 'LOW', 'CLOSE']].mean() #среднее за таймфрэйм
            ma_queue.append(ma_i)
            ma_n = sum(ma_queue)/len(ma_queue)
            self.data_cr.loc[i, f'MA{self.ma_period}'] = ma_n

    def __create_DELTA(self):
        '''метод добавления колонки со значениями отклоения в % от HIGH для шорта, или LOW для лонга, от скользящей средней MA'''
        
        extr = 'LOW' if self.type_deel else 'HIGH'
        self.data_cr[f'DELTA-{extr[0]}%'] = self.data_cr[f'{extr}']*100/self.data_cr[f'MA{self.ma_period}'] - 100

    def __create_pl(self):
        '''Метод добавления колонок с максимальным проффитом и убытком в % который можно получить при удержании в течение
        hold_time, так же количество дней после открытия когда происходит этот убыток/профит'''

        df = self.data_cr
        for index, row in df.iterrows():
            if index == df.shape[0] -1: break
            day_current = row['DATE']
            f_index = index + 1
            l_index = f_index + self.hold_time
            day_maxhigh, max_high = df.loc[df['HIGH'][f_index: l_index].idxmax()][['DATE','HIGH']]
            day_minlow, min_low = df.loc[df['LOW'][f_index: l_index].idxmin()][['DATE','LOW']]
            duration_maxhigh = pd.Timestamp(f'{day_maxhigh}') - pd.Timestamp(f'{day_current}')
            duration_minlow = pd.Timestamp(f'{day_minlow}') - pd.Timestamp(f'{day_current}')
            
            if self.type_deel:
                open_deal = row['LOW']
                prof_max = max_high * 100/ open_deal - 100
                loss_max = min_low * 100/ open_deal - 100                
                self.data_cr.loc[index, 'Day_maxprof'] = duration_maxhigh.days
                self.data_cr.loc[index, 'prof_max %'] = prof_max
                self.data_cr.loc[index, 'Day_maxloss'] = duration_minlow.days
                self.data_cr.loc[index, 'loss_max %'] = loss_max
                            
            else:
                open_deal = row['HIGH']
                prof_max =  100 - min_low * 100/ open_deal
                loss_max = 100 - max_high * 100/ open_deal           
                self.data_cr.loc[index, 'Day_maxprof'] = duration_minlow.days
                self.data_cr.loc[index, 'prof_max %'] = prof_max
                self.data_cr.loc[index, 'Day_maxloss'] = duration_maxhigh.days
                self.data_cr.loc[index, 'loss_max %'] = loss_max

                      
            
            
class DataTicker(DT_Build):
    '''
    Построение класса тиккера с заданными параметрами:\n
    ticker - имя тиккера,\n
    ma_period - период для построения скользящей средней, \n
    hold_period - период удержания позиции,\n
    type_deel - True -лонг, False -шорт.\n
    '''
    ma_period = Build()
    hold_time = Build()
    type_deel = Build()

    def __init__(self, ticker: str, ma_period: int, hold_time: int, type_deel: bool = True):
        self._ticker = ticker
        self.ma_period = ma_period
        self.hold_time = hold_time
        self.type_deel = type_deel
        self.data = self.__get_data()
        self.build()

    def __get_data(self):
        '''Метод загрузки данных из файла и конывртации в DataFrame'''

        file_name = f'{DIR}\{self.ticker}_day.txt'
        return pd.read_csv(file_name, index_col=None)
    
         
    @property
    def ticker(self):
        return self._ticker
    
    @ticker.setter
    def ticker(self, value):
        self._ticker = value
        self.data = self.__get_data()
        self.build()

 
    def __repr__(self):
        return f'DataTicker({self.ticker!r}, {self.ma_period}, {self.hold_time}, {self.type_deel!r})'
    
    