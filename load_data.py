
import requests
from datetime import date
import time
from tqdm import tqdm
from settings import DIR_FOR_LOAD, TICKER_FOR_LOAD, PERIOD, URL, MARKET_ID, TICKER_ID



start_date = ['01', '01', '1980']
current_date = str(date.today())
current_date_list = current_date.split('-')
year, month, day = current_date_list
period  = PERIOD
code_p = {'day': '8', 'week': '9'}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"}

session = requests.Session()

def req(name, market='Акции'): 
        """Функция запроса requests. В данной функции происходит запрос с сервера и сохранение в файл."""

        ticker = name
        t_id = TICKER_ID[ticker]
        m_id = MARKET_ID[market]
        data = {'market': m_id, 'em': t_id, 'code': ticker, 'apply': '0', 'df': start_date[0], 'mf': start_date[1], 'yf': start_date[2], 'dt': day,
                'mt': int(month)-1, 'yt': year, 'p': code_p[period], 'f': f'{ticker}_{start_date[2]}{start_date[1]}{start_date[0]}_{year[-2:]}{month}{day}', 'e': '.csv', 'cn': ticker, 'dtf': '1', 'tmf': '1', 'MSOR': '1', 'mstime': 'on',
                'mstimever': '1', 'sep': '1', 'sep2': '1', 'datf': '2', 'at': '1'}

        response = session.get(URL, params=data, headers=headers)
        
        text = response.text
        
        #Цикл очистки текста от ненужных символов
        for sign in ['<', '>']: 
                text = text.replace(sign, '')        
        
        #Сохранение в файл
        file = f'{ticker}_{period}.txt'
        with open(f'{DIR_FOR_LOAD}\{file}', 'w', newline='\n') as w: # Изменил адрес сохранения, но остальные модули будут искать по старому адресу, нужно исправить
                w.write(text)
        
def main():        
        '''Функция запуска цикла выполнения текущего скрипта.'''

        for elem in tqdm(TICKER_FOR_LOAD):
                req(elem)
                time.sleep(3)
        import daily_view_ref
        daily_view_ref.main()

if __name__ == '__main__':        
        main()
        

