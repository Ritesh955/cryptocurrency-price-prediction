import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

import numpy as np  
import pandas as pd  
from pandas_datareader import data as wb 
import matplotlib.pyplot as plt  
from scipy.stats import norm
import plotly
import plotly.graph_objs as go
import plotly.plotly as py


server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df = pd.read_csv('coins.csv')

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Optimal Buy Time For Top 5 Cryptocurrencies'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'BTC-USD', 'value': 'BTC'},
            {'label': 'ETH-USD', 'value': 'ETH'},
            {'label': 'XRP-USD', 'value': 'XRP'},
            {'label': 'LTC-USD', 'value': 'LTC'},
            {'label': 'USDT-USD', 'value': 'USDT'}
        ],
        value='BTC'
    ),
    dcc.Graph(id='my-graph'),
    dcc.Graph(id='new-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = df.loc[:,selected_dropdown_value]
    a = dff.values.tolist()
    minimum = a.index(min(a))
    layout = go.Layout(
    showlegend=False,title = 'Price for coming 12 days',
    annotations=[
        dict(
            x=minimum,
            y=a[minimum],
            xref='x',
            yref='y',
            text='Best Day',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )],xaxis = dict(
      title = "Days",
    ),
    yaxis = dict(
      title = "Closing Price",
    ) )     
    data= [{
            'y': dff.values,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }]
    return {'data':data,'layout':layout}  


@app.callback(Output('new-graph', 'figure'),
        [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    ticker = selected_dropdown_value+"-USD"
    data = pd.DataFrame()
    data = wb.DataReader(ticker, data_source='yahoo', start='2012-01-01',end='2018-03-31')['Adj Close']
    log_returns = np.log(1 + data.pct_change())
    log_returns.tail()
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    Z = norm.ppf(np.random.rand(10,2))
    t_intervals = 30
    iterations = 500
    daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(t_intervals, iterations)))
    S0 = data.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0]=S0
    for t in range(1, t_intervals):
        price_list[t] = price_list[t - 1] * daily_returns[t]
    price_list = price_list.transpose()

    layout = dict(title = 'Monte Carlo Simulation',
              xaxis = dict(title = 'Days'),
              yaxis = dict(title = 'Closing Price'),
              showlegend=False # set the background colour
             )
    data = []
    for i in range(500):
       data.append(go.Scatter(y=price_list[i]))

    return {
        'data': data,
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server()
