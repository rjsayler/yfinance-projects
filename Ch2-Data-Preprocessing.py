#directory : cd excel-python
#virtual environment : source virt/bin/activate
#Run Program = python3 Ch2-Data-Preprocessing.py
#To Get Nasdaq data = pip install nasdaq-data-link

#Ch2 - Data Preprocessing 

'''
Many of the models and approaches used for time series modeling require 
the time series to be stationary. 

Stationary assumes that the statistics 
of a process, such as the series mean and variance, do not change ove time. 
Using that assumption, we can build models that aim to forecast the future 
values of the process. 

Asset prices are not stationary, to get them stationary we use returns.
There are two types of return
- simple returns : they aggregate over assets - the simple return of a portfolio is the 
	weighted sum of the returns of the individual assets in the portfolio. 
- Log returns (inflation adjusted returns)- The aggregate over time. It is easier to 
	understadn with the help of an example - the log return for a give month is the sum 
	of the log returns of the days within that month. 

The best practice while working with stock prices is to use adjusted values 
as they account for possible actions, such as stock splits.	Pg26 
When you are pulling data using the yf.download function you will multiple datasets 
to pull from. - Open, High, Low, Close, Adjusted Close, Volumn. 


Topics Covered in Chapter 2
- Converting prices to returns
- Adjusting the returns for inflation 
- Changing the frequency of time series data 
- Different Ways of imputing missing data 
- Changing currencies 
- Different ways of aggregatign trade data

'''

import pandas as pd 
import numpy as np 
import yfinance as yf
from openpyxl.workbook import workbook
from openpyxl import load_workbook
import nasdaqdatalink
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


nasdaqdatalink.ApiConfig.api_key = YOUR KEY HERE 

#Symbols as of 11/28/23 : 
# SPAXX**
# ARR
# FXAIX
# IRM
# JPM
# MAA
# MSFT
# O
# SBUX
# SCHD
# STAG
# T
# TSLA
# XOM

#yfiance methods to keep track of: 
# .actions .dividends .splits .get_shares_full .history
#Financials - .income_stmt .balance_sheet .cashflow 
#Holder - .major_holders .institutional_holders .mutualfund_holders
# .earnings_dates 

df = yf.download("AAPL",
				start="2000-12-01",
				end="2020-12-31",
				progress=False)

df = df.loc[:,["Adj Close"]]
#There are multiple columns but the book just has you call "Adj Close"
#Other Columns = Open, High, Low, Close, Adj Close, Volumn for the day
#loc[] allows you to just grab the column you need. Seems to be useful when the 
#dataframe has multiple columns that aren't providing much value. 


df = df.resample("M").last()

#Had to use the FRED data set and pull the consumer price index for 
#All Urban Consumers  
df_cpi = (
    nasdaqdatalink.get(dataset="FRED/CPIAUCSL", 
                       start_date="2000-12-01", 
                       end_date="2020-12-31",
                       collasp="monthly")
    .rename(columns={"Value": "cpi"})
)
df_cpi = df_cpi.resample("M").last()
print(df_cpi.head())
#print(df_cpi)
#The book uses the following table to get CPI - RATEINF/CPI_USA


#Join inflation data to prices 
df = df.join(df_cpi, how="left")
df["inflation_rate"] = df["cpi"].pct_change()
df["Simple_rtn"] = df["Adj Close"].pct_change()
df["log_rtn"] = np.log(df["Adj Close"]/df["Adj Close"].shift(1))
df["real_rtn"] = ((df["Simple_rtn"]+1) / (df["inflation_rate"] + 1) - 1)
print(df.head())
#print(df)
#df.to_excel("APPL_Plus_Inflation.xlsx")

def realized_volatility(x):
	return np.sqrt(np.sum(x**2))

df_rv =(
	df.groupby(pd.Grouper(freq="M"))
	.apply(realized_volatility)
	.rename(columns={"log_rtn" : "rv"})
	)
df_rv.rv = df_rv["rv"] * np.sqrt(12)
print("--------------------------------------------")
print(df_rv)

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(df["log_rtn"])
ax[0].set_title("Apple's Log Returns (2000-2020)")
ax[1].plot(df_rv["rv"])
ax[1].set_title("Annualized realized volatility")

########### - 
plt.show()


#Line 39 and 40 you are creating new columns in the data frame by doing some basic 
#Math to calculate "Simple return" and "Log Return"
#------------------------------------------------------------------
#yfiance methods to keep track of: 
# .actions .dividends .splits .get_shares_full .history
#Financials - .income_stmt .balance_sheet .cashflow 
#Holder - .major_holders .institutional_holders .mutualfund_holders
# .earnings_dates 

#Define which stock you want to pull information for. 
tickers = ['O']

end_date = datetime.today() 
print(end_date)

#Basically pulling data from two today to two years ago. 
start_date = end_date - timedelta(days =2*365)
print(start_date)

#Creates a table that the data can be loaded into. 
close_df = pd.DataFrame()

O_Data = yf.Ticker("O")

#print(O_Data.dividends)

#for tickers in tickers:
	#data = yf.download(tickers, start = start_date, end = end_date)
	#close_df[tickers] = data['Close']

#print(close_df)





#print(df)








