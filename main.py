# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:27:02 2022

@author: macwr
"""

import numpy as np 
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class CAPM:
    
    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        
    def download_data(self):
        data = {}
        for stock in self.stocks:
            ticker = yf.download(stock, self.start_date, self.end_date)
            data[stock] = ticker['Adj Close']
            return pd.DataFrame(data)