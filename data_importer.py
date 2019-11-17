# We need to install pandas_datareader package before running this file i.e run pip install pandas-datareader

import requests 
from datetime import datetime 
import pandas as pd  
from pandas_datareader import data as wb 
import matplotlib.pyplot as plt  
import lxml.html 
from lxml.html.soupparser import fromstring


r = requests.get('http://coinmarketcap.com/')

file = open('./coinmarketcap.txt', "w+")
file.write(r.text)
file.close()

file = open('./coinmarketcap.txt','r')
tree = fromstring(file.read())

data = tree.xpath("//td[@class='no-wrap currency-name']//text()") 
coin_symbols =[]

for coin_symbol in data:
    if(coin_symbol != '\n'):
            coin_symbols.append(coin_symbol)

coin_symbol_map ={}
for ind,symbol in enumerate(coin_symbols):
    if(ind%2 ==0):
        coin_symbol_map[coin_symbols[ind]] = coin_symbols[ind+1]
        
coin_symbol_map


#creating marketname to get data
markets =[]
for symbol in coin_symbol_map.keys():
    markets.append(symbol+"-USD")
    
print(markets)


data = pd.DataFrame()
start_date = '2012-01-01'
end_date = '2019-04-05'

for ind,market in enumerate(markets):
        try:
            data = wb.DataReader(market, data_source='yahoo', start=start_date,end=end_date)
            data['coin_name'] = coin_symbol_map[list(coin_symbol_map.keys())[ind]]
            data['coin_symbol'] = list(coin_symbol_map.keys())[ind]
            data.to_csv('./data/'+market+".csv")
        except:
            pass

