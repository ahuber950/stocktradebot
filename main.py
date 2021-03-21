# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:47:20 2021

@author: ahube
"""

# https://aroussi.com/post/python-yahoo-finance site with helpful commands

import yfinance as yf
import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date

        

class Stock_Info:
    
    def __init__(self, ticker):
        self.ticker = ticker

    def get_data(self, date):
        stock_tick = yf.Ticker(self.ticker)
        stock_data = stock_tick.history(interval = "1m", start = date.replace(hour = 0), end = date.replace(hour = 23))
        stock_data.insert(0,"Times",stock_data.index.strftime("%H:%M"))

        mav_array = np.c_[np.array(stock_data["High"]), np.zeros((len(stock_data), 3))]

        for idx in range(len(stock_data)):
            if idx < 20:
                mav_array[idx][1] = np.nan
            elif idx == 20:
                mav_array[idx][1] = stat.mean(mav_array[:,0][:20])
            else:
                mav_array[idx][1] = mav_array[idx][0]*2/21+mav_array[idx-1][1]*(1-2/21)
        for idx in range(len(stock_data)):
            if idx < 50:
                mav_array[idx][2] = np.nan
            elif idx == 50:
                mav_array[idx][2] = stat.mean(mav_array[:,0][:50])
            else:
                mav_array[idx][2] = mav_array[idx][0]*2/51+mav_array[idx-1][2]*(1-2/51)
            mav_array[idx][3] = mav_array[idx][1] - mav_array[idx][2]
        stock_data["20 Min Moving Ave"] = mav_array[:,1]
        stock_data["50 Min Moving Ave"] = mav_array[:,2]
        # print(mav_array)
        return stock_data, mav_array
    
    
    def show_plot(self, datestring, numdays):
        date = datetime.strptime(datestring, "%Y/%m/%d") + timedelta(days = numdays)
        try:
            stock_data, buysell_array = self.get_data(date)
            plt.plot(stock_data["High"],
                     "k",
                     label = "Price")
            plt.plot(stock_data["20 Min Moving Ave"],
                      "b",
                      label = "20 Min Moving Ave")
            plt.plot(stock_data["50 Min Moving Ave"],
                      "m",
                      label = "50 Min Moving Ave")
            stock_bought = False
            balance = 0
            price_bought = np.nan
            for idx in range(50, len(buysell_array[:,3])):
                if buysell_array[:,3][idx] > 0 and buysell_array[:,3][idx - 1] < 0 and stock_bought == False:
                    plt.vlines(stock_data.index[idx],
                               ymin = min(stock_data["High"]),
                               ymax = max(stock_data["High"]),
                               colors = "g")
                    stock_bought = True
                    price_bought = stock_data["High"].iloc[idx]
                    # print("buy here at", str(stock_data.index[idx]), "for", str(price_bought))
                if (buysell_array[idx][0] > price_bought + 1.25 and stock_bought == True) or (buysell_array[idx][0] < price_bought - 1 and stock_bought == True):
                    plt.vlines(stock_data.index[idx],
                               ymin = min(stock_data["High"]),
                               ymax = max(stock_data["High"]),
                               colors = "r")
                    stock_bought = False
                    price_sold = stock_data["High"].iloc[idx]
                    # print("sell here at", str(stock_data.index[idx]), "for", str(price_sold), "for a profit of: ", str(price_sold - price_bought)) 
                    balance += price_sold - price_bought
                    # print("balance: ", str(balance), "\n")
            if stock_bought == True:
                plt.vlines(stock_data.index[idx],
                           ymin = min(stock_data["High"]),
                           ymax = max(stock_data["High"]),
                           colors = "r")
                stock_bought = False
                price_sold = stock_data["High"].iloc[-1]
                # print("sell here at", str(stock_data.index[-1]), "for", str(price_sold), "for a profit of: ", str(price_sold - price_bought)) 
                balance += price_sold - price_bought  
                # print("balance: ", str(balance), "\n")
            
            X_TICKS = round(len(stock_data)/11) # use every nth value; change this number until you like the result
            plt.xticks(stock_data.index[::X_TICKS], stock_data["Times"][::X_TICKS], rotation = 45)
            plt.xlabel(stock_data.index[0].strftime("%m/%d/%y"))
            plt.ylabel("Price")
            plt.title("Price of {ticker} on {date}".format(ticker = self.ticker, date = stock_data.index[0].strftime("%m/%d/%y")))
            plt.legend(bbox_to_anchor=(1, 1),
                       loc="upper left")
            plt.show()
            return balance
        except:
            pass
spy = Stock_Info("spy")
# daily_balance = spy.show_plot("2021/03/08")

# print(daily_balance)
total_balance = 0
startdate = "2021/02/23"
for numdays in range(30):
    daily_balance = spy.show_plot(startdate, numdays)
    try:
        total_balance += daily_balance
        print("on ", str(datetime.strptime(startdate, "%Y/%m/%d") + timedelta(days = numdays)), "daily balance was ", str(daily_balance), " and total balance was ", str(total_balance))
    except:
        pass
