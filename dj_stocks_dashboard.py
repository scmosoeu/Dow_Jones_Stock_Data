# DASH IMPORTS
import dash
import dash_daq as dq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

# PLOTLY IMPORTS
import plotly.graph_objs as go

# OTHER IMPORTS
import pandas as pd
import numpy as np
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

# STOCK DATA INFO
stock_names = pd.read_excel('dj_stock_names.xlsx')
stock_list = os.listdir('stocks')

app.layout = html.Div([
    dcc.Tabs(id='tabs',value='history',children=[
        dcc.Tab(label='Overview',value='history',
        className='tab',selected_className='tab-selected'),
        dcc.Tab(label='Dow Jones Stocks',value='dow_jones',
        className='tab',selected_className='tab-selected'),
        dcc.Tab(label='Stock Performance',value='perform',
        className='tab',selected_className='tab-selected'),
        dcc.Tab(label='Correlations',value='correlations',
        className='tab',selected_className='tab-selected')
    ]),
    html.Div(id='tab-content')
])

#########################_____Overview Tab______##################################################################################

overview = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                figure={
                    'data': [
                        go.Scatter(
                            x=stock_names['year_added'],
                            mode='markers + text',
                            text=stock_names['name'],
                            textposition='top center',
                            hoverinfo='x',
                            marker={'size':10}
                        )
                    ],
                    'layout': go.Layout(
                        hovermode='closest',
                        title='Year stock joined Dow Jones Index',
                        xaxis={'title':'Year'},
                        yaxis={'visible':False},
                        height=500
                    )
                },
                className='my_graphs'
            )
        ]),
        html.Div([
            dcc.Graph(
                figure={
                    'data': [
                        go.Bar(
                            x=stock_names['stock_market'].value_counts(),
                            y=stock_names['stock_market'].value_counts().index,
                            orientation='h',
                            marker={'color':'rgba(250,70,120,0.7)'}
                        )
                    ],
                    'layout': go.Layout(
                        hovermode='closest',
                        title='Number of Dow Jones stocks in each market',
                        height=330
                    )
                }
            )
        ],className='split_graph')
    ])
])

######################____Dow Jones Stocks Tab______#########################################

stock_names.set_index('ticker',inplace=True)
options = []
for tic in stock_names.index:
    options.append({'label':'{} {}'.format(tic,stock_names.loc[tic]['name']),'value':tic})

stocks = html.Div([
    html.Div([
        dcc.Dropdown(
            id='tickers',
            options=options,
            value='AAPL',
            className='dropmenu'
        )
    ]),
    html.Div([
        html.Div(id='line-graph',className='line_graph')
    ])
])

@app.callback(Output('line-graph','children'),
             [Input('tickers','value')]
)

def first_graph(ticker):

    df = pd.read_csv('stocks/'+str(ticker)+'.csv')
    data = [
        go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='closing price'
        ),
        go.Scatter(
            x=df['date'],
            y=df['close'].rolling(23).mean(),
            mode='lines',
            name='1 month MA'
        ),
        go.Scatter(
            x=df['date'],
            y=df['close'].rolling(138).mean(),
            mode='lines',
            name='6 months MA'
        )
    ]

    layout = go.Layout(
        hovermode='closest',
        title='{}'.format(stock_names.loc[ticker]['name']),
        yaxis={'title':'share price (USD)'},
        xaxis={
            'title':'Date',
            'rangeslider':{'visible':True}
        },
        legend=dict(x=0.9,y=1.1),
        height=800
    )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )


#######################_____Stock Performance Tab_____###########################################
#performance = html.Div([])

#######################_____Correlations Tab_____#################################################
#correlate = html.Div([])

@app.callback(Output('tab-content','children'),
             [Input('tabs','value')]
)

def display_content(selected_tab):

    if selected_tab == 'history':
        return overview
    elif selected_tab == 'dow_jones':
        return stocks
    elif selected_tab == 'perform':
        return performance
    else:
        return correlate

if __name__ == '__main__':
    app.run_server()
