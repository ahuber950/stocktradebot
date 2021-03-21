# https://aroussi.com/post/python-yahoo-finance site with helpful commands

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date


# class Stock_Info:
    
#     def __init__(self, ticker):
#         self.ticker = ticker
        
#     def get_data(self)
    
#     def show_plot(self, date):
#         pass
    
    
def create_plot(stock_data, stats, ticker):
    plt.plot(stock_data["High"],
             "b",
             label = "Price")
    X_TICKS = round(len(stock_data)/11) # use every nth value; change this number until you like the result
    plt.xticks(stock_data.index[::X_TICKS], stock_data["Times"][::X_TICKS], rotation = 45)
    plt.xlabel(stock_data.index[0].strftime("%m/%d/%y"))
    plt.ylabel("Price")
    plt.title("Price of {ticker} on {date}".format(ticker = ticker, date = stock_data.index[0].strftime("%m/%d/%y")))
    plt.legend(bbox_to_anchor=(1, 1),
               loc="upper left")
    plt.show()

def get_stats(ticker, date = datetime.now(), time_int_mins = 390):
    prev_date = date.replace(hour = 9,minute = 29)
    stock_tick = yf.Ticker(ticker)
    stock_data = stock_tick.history(interval = "1m", start = prev_date, end = date)
    stats = {
        "last" : np.mean(stock_data["High"].tail(1)),
        "hourly avg" : np.mean(stock_data["High"].tail(60)),
        "2 hr avg" : np.mean(stock_data["High"].tail(120))
        }
    stock_data.insert(0,"Times",stock_data.index.strftime("%H:%M"))
    create_plot(stock_data.tail(time_int_mins), stats, ticker)
    print(stock_data, type(stock_data))
    return stats, stock_data

get_stats("SPY", datetime.now().replace(day = 15))
print(datetime.now())
print(type(datetime.now()))


# spy = yf.Ticker("SPY")
# spy_stock_data = spy.history(interval = "1d", start = "2020-10-14", end = "2020-12-15")
# print(spy_stock_data)
# spy_highs = np.array(spy_stock_data["High"])
# print(spy_highs)
# get_stats(spy, "2020-12-14", 10)
# plt.plot(spy_stock_data)

# account = 10000
# shares = 0
# for idx, val in enumerate(spy_highs):
#     try:
#         if val > spy_highs[idx -1] and shares == 0:
#             shares += 1
#             account -= val
#             print("\nTime: {}, 1 share was bought for {}, leaving {} remaining in the account".format(spy_stock_data.index[idx],val,account))
#         if val < spy_highs[idx - 1] and shares == 1:
#             print("\nTime: {}, all {} shares were sold for {}, leaving {} remaining in the account".format(spy_stock_data.index[idx], shares, val, account))
#             account += shares * val
#             shares = 0
#     except:
#         print("passed for idx {}".format(idx))

        
            
        

# _______________________________________________________________________________________

# print("What ticker would you like to view?")
# ticker = input()
# while True:
#     try:
#         yf.Ticker(ticker).info
#         break
#     except:
#         print("\nThat ticker is not valid. Please enter a valid ticker.")
#         ticker = input()

        
# print("\nWhat time interval would you like to look at?\nValid intervals are: \
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo.")
# interval = input()

# while interval not in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]:
#     print("\nThat interval is not valid. Please enter a valid interval.\
# \nValid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo.")
#     interval = input()

# get_stats(ticker, date.today(), 100)

# print("\nWhat start date would you like to use? Please name date in .")
# interval = input()

# _________________________________________________________________________________________














