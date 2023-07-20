import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
df = pd.read_csv('crypto-markets.csv')
#print(df.head())


# Transforming  date to date object 
df['date'] = pd.to_datetime(df['date'], format ='%Y-%m-%d')

# Getting data frame containing the latest date's data for each currency
print("Latest Crypto data")
latest_df = df[df['date'] == max(df['date'])]
latest_df.head() # print to check latest data

# total number of crypto currencies available in the dataset
print("Number of crypto currencies listed: ")
latest_df['symbol'].nunique() # print to see the number of currencies

# getting the starting date of all currencies
start_date_df = pd.DataFrame({'start_date':df.groupby(["name","ranknow"])['date'].min()}).reset_index()

# List of the oldest cryptocurrencies
print("Oldest Cryptocurrencies")
start_date_df.sort_values(['start_date']).head(n=10)# print to get the first 10 cryptocurrencies

# List of the latest cryptocurrencies
print("New Cryptocurrencies")
start_date_df.sort_values(['start_date']).tail(n=10)# print to get the latest cryptocurrencies name

# Top cryptocurrencies in the current market
latest_df[latest_df['ranknow']<=10].groupby('ranknow').name.unique()# print to get the names of top currencies

# Plotting the top 10 currencies according to market valuation
name = latest_df['name'].unique()
currency = []
marketval = []
x_currencies =name[:10]
for i, cn in enumerate(x_currencies):
    filtered = latest_df[(latest_df['name']==str(cn))]
    currency.append(str(cn))
    marketval.append(filtered['market'].values[0])

f, ax = plt.subplots(figsize=(20,8))
g = sns.barplot( y = currency, x = marketval, palette=sns.cubehelix_palette(10, reverse=True))
plt.title("Top 10 Cryptocurrencies Marketval")
ax.set_xticklabels(ax.get_xticks())
fig = plt.gcf() #get current figure
plt.show() #remove comment to get the barplot
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)


# plotting top currencies by volume 
volume = []
for i, cn in enumerate(x_currencies):
    filtered = latest_df[(latest_df['name']==str(cn))]
    volume.append(filtered['volume'].values[0])

f, ax = plt.subplots(figsize=(20,8))
g = sns.barplot( y = currency, x = volume, palette=sns.cubehelix_palette(10, reverse=True))
plt.title("Top 10 Cryptocurrencies Volume")
ax.set_xticklabels(ax.get_xticks())
fig = plt.gcf() #get current figure
plt.show() #remove comment to get the barplot
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)


# Candlestick chart for Bitcoin
rank = 1
months = 6

name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]
OHLCfiltered_df = filtered_df[['date','open','high','low','close']]
OHLCfiltered_df['date'] = mdates.date2num(OHLCfiltered_df['date'].dt.date)

f,ax=plt.subplots(figsize=(15,11))
ax.xaxis_date()
candlestick_ohlc(ax, OHLCfiltered_df.values, width=0.5, colorup='g', colordown='r',alpha=0.75)

plt.xlabel("Date")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.title(name + " price")
plt.ylabel("Price")
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)

# Candlestick chart for Etherium
rank = 2
months = 6

name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]
OHLCfiltered_df = filtered_df[['date','open','high','low','close']]
OHLCfiltered_df['date'] = mdates.date2num(OHLCfiltered_df['date'].dt.date)

f,ax=plt.subplots(figsize=(15,11))
ax.xaxis_date()
candlestick_ohlc(ax, OHLCfiltered_df.values, width=0.5, colorup='g', colordown='r',alpha=0.75)

plt.xlabel("Date")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.title(name + " price")
plt.ylabel("Price")
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)

# Moving average chart for bitcoin
rank = 1
months = 6
name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]

filtered_df.set_index('date', inplace=True)

f, ax = plt.subplots(figsize=(15,11))
filtered_df.close.plot(label='Raw', ax=ax)
filtered_df.close.rolling(20).mean().plot(label='20D MA', ax=ax)
filtered_df.close.ewm(alpha=0.03).mean().plot(label='EWMA(alpha=.03)', ax=ax)

plt.title(name + " price with Moving Averages")
plt.legend()
plt.xlabel("Date")
plt.gcf().autofmt_xdate()
plt.ylabel("Close ($)")
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)

# Moving average chart for Etherium
rank = 2
months = 6
name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]

filtered_df.set_index('date', inplace=True)

f, ax = plt.subplots(figsize=(15,11))
filtered_df.close.plot(label='Raw', ax=ax)
filtered_df.close.rolling(20).mean().plot(label='20D MA', ax=ax)
filtered_df.close.ewm(alpha=0.03).mean().plot(label='EWMA(alpha=.03)', ax=ax)

plt.title(name + " price with Moving Averages")
plt.legend()
plt.xlabel("Date")
plt.gcf().autofmt_xdate()
plt.ylabel("Close ($)")
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)


# Moving average chart for BTC
rank = 1
months = 10
name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]
filtered_df.set_index('date', inplace=True)
sma20 = filtered_df.close.rolling(20).mean()
sma50 = filtered_df.close.rolling(50).mean()
sma200 = filtered_df.close.rolling(200).mean()
smaplot =pd.DataFrame({'Raw': filtered_df.close, 'SMA 20': sma20, 'SMA 50': sma50, 'SMA 200': sma200})
smaplot.plot(figsize=(9,5), legend=True, title="Bitcoin price with Moving Averages")
plt.gcf().autofmt_xdate()
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)

# Moving average chart for ETH
rank = 2
months = 10
name = df[df.ranknow == rank].iloc[-1]['name']
filtered_df = df[(df['ranknow'] == rank) & (df['date'] > (max(df['date']) - timedelta(days=30*months)))]

filtered_df.set_index('date', inplace=True)

# simple moving averages
sma20 = filtered_df.close.rolling(20).mean()
sma50 = filtered_df.close.rolling(50).mean()
sma200 = filtered_df.close.rolling(200).mean()
 
smaplot = pd.DataFrame({'Raw': filtered_df.close, 'SMA 20': sma20, 'SMA 50': sma50, 'SMA 200': sma200})
smaplot.plot(figsize=(9,5), legend=True, title="Etherium price with Moving Averages")

plt.gcf().autofmt_xdate()
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)