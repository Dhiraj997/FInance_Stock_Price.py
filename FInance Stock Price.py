# Finance Data Project

from pandas_datareader import data, wb
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
sns.set_style('whitegrid')

## Data

# We need to get data using pandas datareader.We will get stock information for the following banks:
# Bank of America
# CitiGroup
# Goldman Sachs
# JPMorgan Chase
# Morgan Stanley
# Wells Fargo


# 1.Use datetime to set start and end datetime objects.
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

# 2.Figure out the ticker symbol for each bank.
# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)

# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)

# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)

# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)

# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)

# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

# 3. Figure out how to use datareader to grab info on the stock.
# Could also do this for a Panel Object

df = data.DataReader(['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC'], 'yahoo', start, end)
print(df.head())

# ** Create a list of the ticker symbols( as strings) in alphabetical order.Call this list: tickers **

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

##** Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks.Set the keys
#    argument equal to the tickers list.Also pay attention to what axis you concatenate on. **

bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], axis=1, keys=tickers)
print(bank_stocks)

##** Set the column name levels(this is filled out for you):**

bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']

##** Check the head of the bank_stocks dataframe. **

print(bank_stocks.head())

# EDA

##** What is the max Close price for each bank's stock throughout the time period?**

max_close_price = bank_stocks.xs(key='Close', axis=1, level='Stock Info').max()
print(max_close_price)

##** Create a new empty DataFrame called returns.

returns = pd.DataFrame()

##** We can use pandas pct_change() method on the Close column to create a column representing this return value.Create
# a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the
# returns DataFrame.**

for tick in tickers:
    returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()
print(returns.head())

##** Create a pairplot using seaborn of the returns dataframe.What stock stands out to you? Can you figure out why? **
#CitiGroup

sns.pairplot(returns[1:])
plt.show()

##** Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single dayreturns.You
# should notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day? **

# Worst Drop (4 of them on Inauguration day)

print(returns.idxmin())

##** You should have noticed that Citigroup's largest drop and biggest gain were very close to one another, did anything
# significant happen in that time frame? **


print(returns.idxmax())

##** Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire
# time period? Which would you classify as the riskiest for the year 2015? **

print(returns.std())

# Very similar risk profiles, but Morgan Stanley or BofA

print(returns.loc['2015-01-01':'2015-12-31'].std())

##** Create a distplot using seaborn of the 2015 returns for Morgan Stanley **

sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color='green', bins=100)
plt.show()

##** Create a distplot using seaborn of the 2008 returns for CitiGroup **

sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color='red', bins=100)
plt.show()


##** Create a line plot showing Close price for each bank for the entire index of time.

bank_stocks.xs(key='Close', axis=1, level='Stock Info').plot(figsize=(12, 4), label='tick')
plt.show()

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12, 4), label=tick)
plt.legend()
plt.show()

## Moving Averages

#Let's analyze the moving averages for these stocks in the year 2008.

##** Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

plt.figure(figsize=(12, 6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()
plt.show()

##** Create a heatmap of the correlation between the stocks Close Price. **

sns.heatmap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)
plt.show()

##Use seaborn's clustermap to cluster the correlations together:**

sns.clustermap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True, cmap='coolwarm')
plt.show()
