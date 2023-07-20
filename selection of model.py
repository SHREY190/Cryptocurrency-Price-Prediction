import pandas as pd

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,7)

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

from scipy import stats
import statsmodels.api as sm
from itertools import product

import warnings 
warnings.filterwarnings('ignore')
dateparse = lambda dates:pd.datetime.strptime(dates,'%Y-%m-%d')

df = pd.read_csv('crypto-markets.csv',parse_dates=['date'],index_col='date',date_parser=dateparse)
print(df.head())

print(df.tail())


# Extracting bitcoin data
btc=df[df['symbol']=='BTC']
btc.drop(['slug','volume','symbol','name','ranknow','market','close_ratio','spread'],axis=1,inplace=True)
print(btc.head())

#Monthly forcasting
btc_month = btc.resample('M').mean()

btc_month['close_box'], lmbda = stats.boxcox(btc_month.close)
print("Dickey–Fuller test: p=%f" % adfuller(btc_month.close_box)[1])


#Initial approximation of parameters

qs = range(0,3)
ps = range(0,3)
d=1
parameters = product(ps,qs)
parameters_list = list(parameters)
len(parameters_list)

# model selection 
results = []
best_aic = float("inf")
warnings.filterwarnings('ignore')
for param in parameters_list:
    try:
        model = SARIMAX (btc_month.close_box, order=(param[0],d,param[1])).fit(disp=-1)
    except ValueError:
        print('bad parameter combination:',param)
        continue
    aic = model.aic 
    if aic < best_aic:
        bestodel = model
        best_aic = aic
        best_param = param

    results.append([param,model.aic])

# Best model 
results_table = pd.DataFrame(results)
results_table.columns = ['parameters','aic']
print(results_table.sort_values(by = 'aic', ascending = True).head())

best_model = SARIMAX(btc_month.close_box, order=(1, d, 0)).fit(disp=-1)
print(best_model.summary())