import pandas as pd
import numpy as np
import requests
import datetime
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


for symbol in ['BTC','ETH','XRP','EOS','LTC','BCH','BNB','ADA','XLM','USDT']:
    timestamps = [1538888400,1531688400,1524488400,1553295562]
    close_url = "https://min-api.cryptocompare.com/data/histohour?fsym="+symbol+"&tsym=USD&limit=2000&aggregate=1&toTs=1524488400"
    close_response = requests.get(close_url)
    close_prices = close_response.json()
    close_df = pd.DataFrame(close_prices['Data'])
    close_df['time_original'] = close_df['time'].apply(lambda x:datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    for t in timestamps:
         close_url = "https://min-api.cryptocompare.com/data/histohour?fsym="+symbol+"&tsym=USD&limit=2000&aggregate=1&toTs="+str(t)
         close_response = requests.get(close_url)
         close_prices = close_response.json()
         close_df1 = pd.DataFrame(close_prices['Data'])
         close_df1['time_original'] = close_df1['time'].apply(lambda x:datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
         close_df = pd.concat([close_df, close_df1])
         close_df.to_csv("data_"+symbol+".csv")

