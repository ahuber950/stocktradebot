# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 08:16:10 2021

@author: ahube
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date

ticker = "SPY"
date = datetime.now().replace(hour = 9, minute = 45)
time_int_mins = 390

prev_date = date.replace(hour = 9,minute = 29)
stock_tick = yf.Ticker(ticker)
stock_data = stock_tick.history(interval = "1m", start = prev_date, end = date)
stats = {
    "last" : np.mean(stock_data["High"].tail(1)),
    "hourly avg" : np.mean(stock_data["High"].tail(60)),
    "2 hr avg" : np.mean(stock_data["High"].tail(120))
    }


stock_data.insert(0,"Time",stock_data.index.strftime("%H:%M"))
print(stock_data, type(stock_data))

x = stock_data["Time"]
y = stock_data["High"]

plt.plot(x,y,label = "High")
X_TICKS = 60
plt.xlabel(stock_data.index[0].strftime("%m/%d/%Y"))
plt.xticks(stock_data.index, labels = stock_data.index.strftime("%H:%M"), rotation = 45)
# plt.xaxis.set_major_locator(ticker.LinearLocator(10))
plt.ylabel("Price")
plt.legend(bbox_to_anchor=(1, 1),
            loc="upper left")

plt.show()

# plt.plot(stock_data["Close"],
#          "b",
#          label = "Price")
# plt.hlines(stats["last"],
#             xmin = stock_data.index[0],
#             xmax = stock_data.index[-1],
#             colors = "r",
#             linestyles = "--",
#             label = "current price")
# plt.hlines(stats["hourly avg"],
#             xmin = stock_data.index[0],
#             xmax = stock_data.index[-1],
#             colors = "m",
#             linestyles = "--",
#             label = "hourly avg")
# plt.hlines(stats["2 hr avg"],
#             xmin = stock_data.index[0],
#             xmax = stock_data.index[-1],
#             colors = "g",
#             linestyles = "--",
#             label = "2 hour avg")
# plt.xlabel("Date")
# plt.xticks(stock_data["Time"], rotation = 45)
# plt.ylabel("Price")
# plt.legend(bbox_to_anchor=(1, 1),
#            loc="upper left")
# plt.show()

