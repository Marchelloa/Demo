from data_for_3dplot import get_data
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from class_ticker import DataTicker


def charts1(obj: DataTicker, _bin: int):
    ''' 
    График подсчёта количества в диапазоне значений отклонений, и ****************** в каждом дипазоне.
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
    plt.ylabel('Количество отлонений', fontsize=7, fontweight = 100, color='slateblue')
    
    #Построение второй диаграммы
    df_bar.plot(kind='bar', grid=True, figsize=(12,5))
    plt.title(f'{obj.ticker}, {type_deel}, MA{obj.ma_period}, hold time={obj.hold_time} day\n'
              f'максимальный минимальный % proff/loss в диапазоне {obj.hold_time} дней', fontsize=7)
    plt.xlabel('диапазон отклонений', fontsize=7, color='slateblue')
    plt.ylabel('Количество отлонений', fontsize=7, fontweight = 100, color='slateblue')  


def charts2(obj: DataTicker, coloumn_name: list[str] = [], _slice: tuple[int, ...] | None = None):
    '''
    Построение графиков по заданным колонкам:
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



def data3d_prepare(obj: DataTicker) -> tuple[str, int, list[float]]:
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

    return (name_deel, duration, res)

    

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

    name_deel, duration, res = data3d_prepare(obj)

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

    name_deel, duration, res = data3d_prepare(obj)

    fig = go.Figure(data=[go.Surface(z=np.array(res))])
    fig.update_layout(title=f'{obj.ticker} {name_deel} max duration {duration}', autosize=False,
                    width=1500, height=950,
                    margin=dict(l=150, r=150, b=20, t=90))
    fig.show()



    
