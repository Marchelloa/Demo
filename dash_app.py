from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from functools import cache
from class_ticker_descriptor import DataTicker
from settings import TICKER_FOR_LOAD

TICKERS = TICKER_FOR_LOAD
# ticker = DataTicker('FIVE', 100, 180, False)
# df = ticker.data_cr
columns_index = {'DELTA-H%': 9, 'DELTA-L%': 9, 'CLOSE': 7, 'prof_max %': 11 , 'loss_max %': 13}
columns = ['DELTA-H%', 'DELTA-L%', 'CLOSE', 'prof_max %', 'loss_max %']

#кэширование данных чтобы постоянно не проводить расчёт при обновлении графика
@cache
def factory_DataTicker(*args, **kwargs):
    return DataTicker(*args, **kwargs)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Select ticker'),
            dcc.Dropdown(TICKERS, 'FIVE', id='dropdown-selection'),
            # html.Br(),
            html.Label('MA period(day)'), html.Br(),
            dcc.Input(id="input-1", type="number", debounce=True, placeholder="MA period(day)", value=100),
            html.Br(),
            html.Label('Hold period(day)'), html.Br(),
            dcc.Input(id="input-2", type="number", debounce=True, placeholder="hold period(day)", value=180)
        ], style={'padding': 10, 'flex': 1}),
        html.Div([  
            # html.Br(),html.Br(),
            html.Label('Type deal'),
            dcc.RadioItems(
                options=['Short', 'Long'],
                value='Long',
                id='type_deal-radio',
                inline=True
                ),
            # html.Br(),
            html.Label('Select charts'),
            dcc.Checklist(
                inline=False,
                id='checklist'
                )        
        ], style={'padding': 10, 'flex': 10})
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div(children=[
        dcc.Graph(id='graph-content')
    ])
])


@callback(
    Output('checklist', 'options'),
    Input('type_deal-radio', 'value')
)
def set_deal_options(radio_value):
    if radio_value == 'Long':
        col_name = columns.copy()
        col_name.remove('DELTA-H%') 
        return col_name
    else:
        col_name = columns.copy()
        col_name.remove('DELTA-L%') 
        return col_name
    
@callback(
        Output('checklist', 'value'),
        Input('checklist', 'options')
)
def set_checklist_value(available_options):
    return [available_options[0]]
       
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('type_deal-radio', 'value'),
    Input('checklist', 'value'),
    Input("input-1", "value"),
    Input("input-2", "value")
)
def update_graph(d_value, deal_value, ch_value, inp_1_value, inp_2_value):
    if deal_value == 'Long': 
        type_deal = True
    else:    
        type_deal = False
    obj_ticker = factory_DataTicker(d_value, inp_1_value, inp_2_value, type_deal)
    df = obj_ticker.data_cr
    title, obj_MA, obj_hold_time = obj_ticker.ticker, obj_ticker.ma_period, obj_ticker.hold_time
    fig1 = px.line(df, y=ch_value, height=800, title='{}, {}, MA{}day, hold period {} day'.format(title, deal_value, obj_MA, obj_hold_time))
    fig1.add_vline(x = df.index[-inp_2_value])
    print(factory_DataTicker.cache_info())
    return fig1

if __name__ == "__main__":
    app.run_server(debug=True)