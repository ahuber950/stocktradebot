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

# creating a class for stock info 
class Stock_Info:
    
    # object defined by its stock ticker
    def __init__(self, ticker):
        self.ticker = ticker
    
    # scrapes data from yahoofin
    def get_data(self, date):
        # stock_tick defines object containing info on stock data
        stock_tick = yf.Ticker(self.ticker)

        # retreiving all data from 0:00 to 23:00 for a specific day (trading hours are well within these limits)
        stock_data = stock_tick.history(interval = "1m", start = date.replace(hour = 0), end = date.replace(hour = 23))
        
        # creating Times column in pandas dataframe to reference on x axis
        stock_data.insert(0,"Times",stock_data.index.strftime("%H:%M"))

        # creating a buy/sell array which will allow us to determine when to buy/sell based on moving averages
        # col 0 will be price at every minute
        # col 1 will be 20 min moving average
        # col 2 will be 50 min moving average
        # col 3 will be 20 min moving average - 50 min moving average, indicating trend shifts
        buysell_array = np.c_[np.array(stock_data["High"]), np.zeros((len(stock_data), 3))]

        for idx in range(len(stock_data)):
            if idx < 20:
                buysell_array[idx][1] = np.nan
            elif idx == 20:
                buysell_array[idx][1] = stat.mean(buysell_array[:,0][:20])
            else:
                buysell_array[idx][1] = buysell_array[idx][0]*2/21+buysell_array[idx-1][1]*(1-2/21)
        for idx in range(len(stock_data)):
            if idx < 50:
                buysell_array[idx][2] = np.nan
            elif idx == 50:
                buysell_array[idx][2] = stat.mean(buysell_array[:,0][:50])
            else:
                buysell_array[idx][2] = buysell_array[idx][0]*2/51+buysell_array[idx-1][2]*(1-2/51)
            buysell_array[idx][3] = buysell_array[idx][1] - buysell_array[idx][2]
        
        # adding moving averages to stock_data dataframe to more easily plot them alongside time
        stock_data["20 Min Moving Ave"] = buysell_array[:,1]
        stock_data["50 Min Moving Ave"] = buysell_array[:,2]
        return stock_data, buysell_array
    
    
    def show_plot(self, datestring, numdays):
        
        # converting datestring into datetime object
        date = datetime.strptime(datestring, "%Y/%m/%d") + timedelta(days = numdays)
        
        # using try/except for cases when we pass data when stock market never opens. if there is no data, pass
        try:
            
            # getting data arrays from get_data function
            stock_data, buysell_array = self.get_data(date)
            
            # plotting stock price
            plt.plot(stock_data["High"],
                     "k",
                     label = "Price")
            
            # plotting 20 min moving average
            plt.plot(stock_data["20 Min Moving Ave"],
                      "b",
                      label = "20 Min Moving Ave")
            
            # plotting 50 min moving average
            plt.plot(stock_data["50 Min Moving Ave"],
                      "m",
                      label = "50 Min Moving Ave")
            
            # initializing each day as no stock bought today.
            # for this simulation, only 1 stock will be traded/bought at a time
            stock_bought = False
            
            # initializing daily balance
            balance = 0
            
            # initializing price_bought
            price_bought = np.nan
            
            # setting up a loop with conditions on when to buy and sell a stock
            
            for idx in range(50, len(buysell_array[:,3])):
                
                # if 50mMAV rises above 20mMAV and no stock is bought, then buy
                if buysell_array[:,3][idx] > 0 and buysell_array[:,3][idx - 1] < 0 and stock_bought == False:
                    
                    # plot vline where stock bought
                    plt.vlines(stock_data.index[idx],
                               ymin = min(stock_data["High"]),
                               ymax = max(stock_data["High"]),
                               colors = "g")
                    
                    # change status of stock_bought so we cannot buy more than 1 at a time
                    stock_bought = True
                    
                    # record what price we bought stock at
                    price_bought = stock_data["High"].iloc[idx]
                    
                # if price of stock rises above a gain threshold or falls below a loss threshold and stock_bought == True: sell
                if (buysell_array[idx][0] > price_bought + 1.5 and stock_bought == True) or (buysell_array[idx][0] < price_bought - 1 and stock_bought == True):
                    
                    # plot vline where stock sold
                    plt.vlines(stock_data.index[idx],
                               ymin = min(stock_data["High"]),
                               ymax = max(stock_data["High"]),
                               colors = "r")
                    
                    # change status of stock_bought so we can buy again
                    stock_bought = False
                    
                    # record price of stock sold
                    price_sold = stock_data["High"].iloc[idx]
                    
                    # add profit/loss from trade to daily balance
                    balance += price_sold - price_bought
                    
            # if we still have stock at end of day: sell
            if stock_bought == True:
                
                # plot vline where stock sold
                plt.vlines(stock_data.index[idx],
                           ymin = min(stock_data["High"]),
                           ymax = max(stock_data["High"]),
                           colors = "r")
                
                # change status of stock_bought so we can buy again
                stock_bought = False
                
                # record price of stock sold
                price_sold = stock_data["High"].iloc[-1]
                
                # add profit/loss from trade to daily balance
                balance += price_sold - price_bought
            
            # make x axis read Time column in stock_data dataframe for legibility. 
            # no_ticks will be the number of ticks on your x axis
            no_ticks = 11
            X_TICKS = round(len(stock_data)/no_ticks) # use every nth value; change this number until you like the result
            plt.xticks(stock_data.index[::X_TICKS], stock_data["Times"][::X_TICKS], rotation = 45)
            plt.xlabel(stock_data.index[0].strftime("%m/%d/%y"))
            
            # y axis reads price
            plt.ylabel("Price")
            
            # title
            plt.title("Price of {ticker} on {date}".format(ticker = self.ticker, date = stock_data.index[0].strftime("%m/%d/%y")))
            
            # placing legend
            plt.legend(bbox_to_anchor=(1, 1),
                       loc="upper left")
            plt.show()
            return balance
        except:
            pass

#creating spy object
spy = Stock_Info("spy")

# initiating total balance over number of days
total_balance = 0

# initializing start date as 30 days ago
startdate = str((datetime.today() - timedelta(days = 30)).strftime("%Y/%m/%d"))

# forloop runs for 30 days because that is the window that yfin stores minute to minute data
for numdays in range(30):
    
    # daily balance = output from any given day
    daily_balance = spy.show_plot(startdate, numdays)
    
    # try/except for days that do not contain trading data
    try:
        
        # add daily balance to total balance for x days
        total_balance += daily_balance
        
        # print how much the trades made on a given day and total for date range
        print("on ", str(datetime.strptime(startdate, "%Y/%m/%d") + timedelta(days = numdays)), "daily balance was ", str(daily_balance), " and total balance was ", str(total_balance))
    except:
        pass






