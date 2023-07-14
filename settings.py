# адрес получения котировок
URL = ''

# директория для загрузки и сохранения данных
DIR_FOR_LOAD = 'Load_data' 

# период 'day' или 'week'
PERIOD = 'day'

# список тиккеров для загрузки данных с сервера с котировками
TICKER_FOR_LOAD = ['SBER', 'FIVE', 'YNDX', 'GMKN', 'PLZL', 'GAZP', 'NVTK', 'LKOH', 'MGNT',
                   'OZON', 'RUAL', 'MAGN', 'ROSN', 'NLMK', 'CHMF', 'GOLD', 'BRENT']        

# пока не использовано
PARAMS = {'NVTK': ['NVTK', 24, 'high', 60, 'sell'], 'GMKN': ['GMKN', 24, 'low', 60, 'buy'],
          'GAZP': ['GAZP', 24, 'low', 60, 'buy'],   'PLZL': ['PLZL', 24, 'low', 60, 'buy'],
          'FIVE': ['FIVE', 24, 'high', 60, 'sell'], 'NLMK': ['NLMK', 24, 'low', 60, 'buy'],
          'YNDX': ['YNDX', 24, 'high', 60, 'sell'], 'LKOH': ['LKOH', 24, 'high', 60, 'sell'],
          'MGNT': ['MGNT', 24, 'high', 60, 'sell'], 'GOLD': ['GOLD', 24, 'low', 180, 'buy'],
          'RSTI': ['RSTI', 24, 'high', 60, 'sell'], 'OZON': ['OZON', 24, 'high', 60, 'sell'],
          'MAGN': ['MAGN', 24, 'low', 60, 'buy'],   'RUAL': ['RUAL', 24, 'high', 60, 'sell'],
          'OKEY': ['OKEY', 24, 'high', 60, 'sell'], 'TCS':  ['TCS', 24, 'high', 60, 'sell'],
          'ROSN': ['ROSN', 24, 'high', 60, 'sell'], 'CHMF': ['CHMF', 24, 'high', 60, 'sell'],
          'SBER': ['SBER', 24, 'high', 60, 'sell'], 'BRENT': ['BRENT', 100, 'low', 60, 'buy']}  

MARKET_ID = {'Акции': '1', 'Товарка': '24'}

TICKER_ID = {'GAZP': '16842', 'GMKN': '795', 'PLZL': '17123', 'NVTK': '17370',
            'FIVE': '491944', 'NLMK': '17046', 'YNDX': '388383', 'LKOH': '8',
            'MGNT': '17086', 'RSTI': '20971', 'OZON': '2179435', 'MAGN': '16782',
            'RUAL': '414279', 'OKEY': '2216507', 'TCS': '913710', 'GOLD': '18953',
            'ROSN': '17273', 'CHMF': '16136', 'SBER': '23', 'BRENT': '19473'}