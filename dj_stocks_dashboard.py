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

overview = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='date_joined',
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
                        title='Year stock joined Dow Jones',
                        xaxis={'title':'Year'},
                        yaxis={'visible':False}
                    )
                },
                className='my_graphs'
            )
        ]),
        html.Div()
    ])
])

@app.callback(Output('tab-content','children'),
             [Input('tabs','value')]
)

def display_content(selected_tab):

    if selected_tab == 'history':
        return overview

if __name__ == '__main__':
    app.run_server(debug=True)
