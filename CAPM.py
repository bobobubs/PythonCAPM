# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:27:02 2022

@author: macwr
"""

import numpy as np 
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#market interest rate
RISK_FREE_RATE = 0.05
#considering monthly returns, want annual returns
MONTHS_IN_YEAR = 12
class CAPM:
    
    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        
    def download_data(self):
        self.data = {}
        for stock in self.stocks:
            ticker = yf.download(stock, self.start_date, self.end_date)
            self.data[stock] = ticker['Adj Close']
        
        return pd.DataFrame(self.data)
    
    def initialize(self):
        stock_data = self.download_data()
        
        #change to month instead of day data
        stock_data = stock_data.resample('M').last()
        self.data = pd.DataFrame({'s_adjclose':stock_data[self.stocks[0]],
                                  'm_adjclose':stock_data[self.stocks[1]]})
        #determine log monthly returns
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']]/
                                                self.data[['s_adjclose', 'm_adjclose']].shift(1))
        #remove Nan's
        self.data = self.data[1:]
        print(self.data)
        
    
    def calculate_beta(self):
        #beta defined as:
        #covariance between instrument and market divided my market volatility
        #beta = cov(a, M)/var(M)
        covariance_matrix = np.cov(self.data['s_returns'], self.data['m_returns'])
        beta = covariance_matrix[0, 1]/covariance_matrix[1,1]
        print("Beta from formula: ", beta)
    
    
    def regression(self):
        #performs a linear regression betwween expected market returns and 
        #expected stock returns
        beta, alpha = np.polyfit(self.data['m_returns'], self.data['s_returns'], deg = 1)
        print("Beta from regression: ", beta)
        print("Alpha from regression: ", alpha)
        
        #determining expected return using the CAPM formula
        expected_return = RISK_FREE_RATE + beta *(self.data['m_returns'].mean() * MONTHS_IN_YEAR
                                                  - RISK_FREE_RATE)
        print("Expected return: ", expected_return)
        self.plot_regression(alpha, beta)
        
    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize = (20, 10))
        axis.scatter(self.data['m_returns'], self.data['s_returns'], label = 'Data Points')
        axis.plot(self.data['m_returns'], beta * self.data['m_returns'] + alpha, color = 'red', label = "CAPM Line")
        plt.title('Capital Asset Pricing Model')
        plt.xlabel('Market return $R_m$', fontsize = 18)
        plt.ylabel('Stock return $R_a$')        
        plt.legend()
        plt.grid(True)
        plt.show()
        
if __name__ == '__main__':
    capm = CAPM(['IBM', '^GSPC'], '2010-01-01', '2017-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()
    
        