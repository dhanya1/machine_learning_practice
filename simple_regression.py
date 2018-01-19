import pandas as pd
import quandl
import math

#To get a dataset from Quandl.com
#Goto-financial data => Select a data set => click Python tab => Get the code and paste here for import
quandl.ApiConfig.api_key = 'HNfUQYQsVHBKBzJmMH2Q'
df = quandl.get_table('WIKI/PRICES')

#Cleaning data
#Remove the columns that are explaining the same variation, Like Low and Adj Low
#We will keep only the below features
df = df[['adj_open','adj_high','adj_low','adj_close','adj_volume']]

#Add some meaningful features
#In our case it will be we add %change = high-low/100
df['HL_PCT'] = (df['adj_high'] - df['adj_low'])/df['adj_low']* 100.0
df['PCT_change'] = (df['adj_close'] - df['adj_open'])/df['adj_open'] * 100.0

#Remove all the unnecessary columns nw
df = df[['adj_close','HL_PCT','PCT_change','adj_volume']]
print(df.head())

#We want to forecast future closing price
forecast_col = 'adj_close'

#Replace non-data with a certain value. It will be treated as an outlier
df.fillna(-9999, inplace = True)

#Using only 10 percent of data
forecast_out = int(math.ceil(0.01*len(df)))

#Features are input columns, labels are output columns.
#We are shifing the data in forecast column by 10 rows to the top and assigning it to label. Now each value in the
# adj_close column has a corresponding value in label column which is nothing but adjusted_close value from future.(1% coz 0.01)
df['label'] = df[forecast_col].shift(-forecast_out)
