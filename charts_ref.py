import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
from matplotlib.colors import LightSource

from class_ticker_descriptor import DataTicker
from data_prepare import obj_params, get_data, get_data_for_broken_barh


def charts1(obj: DataTicker, _bin: int):
    '''Построение диаграммы

    График подсчёта количества в диапазоне значений отклонений, и maxmin profloss в каждом дипазоне.
    Строится две диаграммы.
    '''
    #Логика для построения первой диаграммы
    df = obj.data_cr.round(2)
    value_counts = df.iloc[:, 9].value_counts(sort=False, bins=_bin, normalize=False)
    type_deel = 'long' if obj.type_deel else 'short'

    #Логика для построения второй диаграммы
    index_range = [(elem.left, elem.right) for elem in value_counts.index]
    data_pl = {'prof_max': [], 'prof_min': [], 'loss_max': [], 'loss_min': []}
    for _range in index_range:
        df_range = df[(df.iloc[:, 9] > _range[0]) & (df.iloc[:, 9] < _range[1])]
        data_pl['prof_max'].append(df_range['prof_max %'].max())
        data_pl['prof_min'].append(df_range['prof_max %'].min())
        data_pl['loss_max'].append(df_range['loss_max %'].min())
        data_pl['loss_min'].append(df_range['loss_max %'].max())
   
    #Построение первой диаграммы
    df_bar = pd.DataFrame(data_pl, index=value_counts.index)
    value_counts.plot(kind='bar', grid=True, figsize=(12,7))
    plt.title(f'{obj.ticker}, {type_deel}, MA{obj.ma_period}, hold time={obj.hold_time} day', fontsize=7)
    plt.xlabel('Диапазон отклонений', labelpad = 5, fontsize=7, fontweight = 100, color='slateblue')
    plt.ylabel('Количество отклонений', fontsize=7, fontweight = 100, color='slateblue')
    
    #Построение второй диаграммы
    df_bar.plot(kind='bar', grid=True, figsize=(12,5))
    plt.title(f'{obj.ticker}, {type_deel}, MA{obj.ma_period}, hold time={obj.hold_time} day\n'
              f'максимальный минимальный % proff/loss в диапазоне {obj.hold_time} дней', fontsize=7)
    plt.xlabel('диапазон отклонений', fontsize=7, color='slateblue')
    plt.ylabel('Количество отклонений', fontsize=7, fontweight = 100, color='slateblue')  


def charts2(obj: DataTicker, coloumn_name: list[str] = [], _slice: tuple[int, ...] | None = None):
    '''Построение графиков по заданным колонкам:

    coloumn_name - имена колонок,
    _slice - значения для среза
    '''
    
    type_deel = 'long' if obj.type_deel else 'short'
    
    if _slice:
        start, end = _slice[0], _slice[1]
        slice_obj = slice(start, end)
    else:
        slice_obj = slice(_slice)

    df = obj.data_cr[slice_obj]
    df[coloumn_name].plot(figsize=(12, 8), grid=True, linewidth=1, color=['tab:orange', 'tab:blue', 'crimson'])
    plt.axvline(df.index[-obj.hold_time], ymin = -1, ymax = 1, color='violet')
    plt.title(f'{coloumn_name}, {obj.ticker}, {type_deel}, MA{obj.ma_period}, hold time={obj.hold_time} day\n', fontsize=7)



def charts3(obj: DataTicker):
    '''Построение 3D графика (изометрия) из 3х мерной матрицы.'''

    if obj.type_deel == True: #Тип сделки.
        name_deel = "Long"
        open = obj.data['LOW']
        extremum = obj.data['HIGH']
    else:
        name_deel = 'Short'
        open = obj.data['HIGH']
        extremum = obj.data['LOW']
    
    long = obj.type_deel
    duration = obj.hold_time

    res = get_data(open, extremum, duration, long)

    #Код построения графика.
    z = np.array(res)
    xmin, xmax = 1, duration
    ymin, ymax = 1, len(open)

    nrows, ncols = z.shape
    x = np.linspace(xmin, xmax, ncols)
    y = np.linspace(ymin, ymax, nrows)
    x, y = np.meshgrid(x, y)

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'), figsize=(15, 15))

    plt.title(f'{obj.ticker}, {name_deel}, MA{obj.ma_period}, duration={obj.hold_time} day', fontsize=14)
    plt.xlabel('duration', labelpad = 5, fontsize=12, fontweight = 100, color='slateblue')
    plt.ylabel('номер торговой сессии', fontsize=12, fontweight = 100, color='slateblue')

    ls = LightSource(270, 45)    
    rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=True, shade=False)

    plt.show()

def charts4(obj: DataTicker):
    '''Построение спектрокраммы из 3х мерной матрицы.'''

    name_deel, duration, res = obj_params(obj)

    z = np.array(res)
    z = z.transpose()

    fig, ax = plt.subplots(figsize=(20, 7))
    im = ax.imshow(z)
    plt.gca().invert_yaxis()

    ax.set_title(f"Цветовая карта значений proffit\n"
                 f"{obj.ticker}, duration = {duration}, {name_deel}")
    fig.colorbar(im, ax=ax, label='max % proffit')

    plt.show()


def charts5(obj: DataTicker):
    '''Построение 3D модели графика из 3х мерной матрицы'''

    name_deel, duration, res = obj_params(obj)

    fig = go.Figure(data=[go.Surface(z=np.array(res))])
    fig.update_layout(title=f'{obj.ticker} {name_deel} max duration {duration}', autosize=False,
                    width=1500, height=950,
                    margin=dict(l=150, r=150, b=20, t=90))
    fig.show()

def charts6(obj: DataTicker, column_name: str ='CLOSE', _slice: tuple[int, ...]|None = None):
    '''Построение графика в виде ленты 
    
    Cмена тренда числового ряда меняет цвет ленты. 
    Удобен для оценки пропорций периодов роста и снижения.
    '''
    
    if _slice:
        start, end = _slice[0], _slice[1]
        slice_obj = slice(start, end)
    else:
        slice_obj = slice(_slice)    
    
    
    df_list = obj.data_cr[column_name][slice_obj].to_list()
    # df.shape()
    data = get_data_for_broken_barh(df_list)   
    facecolors = ('tab:blue', 'tab:red') if data[1][0] else ('tab:red', 'tab:blue')
    
    # Horizontal bar plot with gaps
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.broken_barh(data[0], (-10, 20), facecolors=facecolors)
    ax.set_title(f'{obj.ticker}, {column_name}', fontsize=14)
    ax.set_yticks([])
    
    #задание параметров легенды в ручную
    red_patch = mpatches.Patch(color='tab:red', label=f'down trend {column_name}')
    blue_patch = mpatches.Patch(color='tab:blue', label=f'up trend {column_name}')
    ax.legend(handles=[red_patch, blue_patch])
    
    ax.set_xlabel('номер торговой сессии')
    ax.grid(axis='x')                                       # Make grid lines visible
  

    plt.show()
      
def charts7(obj: DataTicker, y_ax: list[str] = ['CLOSE', 'DELTA-H%', 'prof_max %', 'loss_max %'], size: tuple[int, int] = (1200, 850)):
    ''' 
    Построение линейного графика в plotly.
    y_ax - имена колонок для построения графика.
    size - размер графика (ширина, высота)
    '''

    if obj.type_deel: 
        type_deal = 'Long'
    else:    
        type_deal = 'Short'

    fig = px.line(df, y = y_ax, title = '{}, {}, MA{}day, hold period {} day'.format(obj.ticker, type_deal, obj.ma_period, obj.hold_time), width=size[0], height=size[1])
    fig.add_vline(x = df.index[-obj.hold_time], color='red')
    fig.show()