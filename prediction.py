import pandas as pd
from pandas import DataFrame
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,7)

import seaborn as sns 
from datetime import datetime

from statsmodels.tsa.statespace.sarimax import SARIMAX

from scipy import stats

import warnings 
warnings.filterwarnings('ignore')
dateparse = lambda dates:pd.datetime.strptime(dates,'%Y-%m-%d')

# Inverse Box-Cox Transformation Function
def invboxcox(y,lmbda):
   if lmbda == 0:
      return(np.exp(y))
   else:
      return(np.exp(np.log(lmbda*y+1)/lmbda))

df = pd.read_csv('crypto-markets.csv',parse_dates=['date'],index_col='date',date_parser=dateparse)

# Extracting bitcoin data
btc=df[df['symbol']=='BTC']
btc.drop(['slug','volume','symbol','name','ranknow','market','close_ratio','spread'],axis=1,inplace=True)
print(btc.head())

#Monthly forcasting
btc_month = btc.resample('M').mean()

# Perform Box-Cox Transformation
btc_month['close_box'], lmbda = stats.boxcox(btc_month['close'])

best_model = SARIMAX(btc_month.close_box, order=(1, 1, 0),seasonal_order=(1,1,1,4)).fit(disp=-1)

btc_month_prediction = btc_month[['close']]
date_list = [datetime(2018,6,30),datetime(2018,5,31),datetime(2018,3,31),datetime(2018,4,30)]
future = pd.DataFrame(index=date_list, columns = btc_month.columns)
btc_prediction = pd.concat([btc_month_prediction,future])
btc_prediction['forecast']= invboxcox(best_model.predict(start=datetime(2014,1,31),end=datetime(2018,6,30)),lmbda)


plt.figure(figsize=(15,7))
btc_prediction['close'].plot()
btc_prediction['forecast'].plot(color='r', ls='--', label='Predicted Close')
plt.legend()
plt.title('Bitcoin monthly forecast')
plt.ylabel('USD')
plt.show()
#########################plt.savefig('img1',dpi=200,bbox_inches='tight',facecolor='red',transparent=True)

y_forecasted = btc_prediction['forecast']
y_truth = btc_month['2015-01-01':'2017-01-01']['close']

# Compute the root mean square error
rmse = np.sqrt(((y_forecasted - y_truth) ** 2).mean())
print('Mean Squared Error: {}'.format(round(rmse, 2)))
