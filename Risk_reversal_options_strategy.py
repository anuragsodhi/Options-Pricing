# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 16:02:35 2018

@author: Anurag
"""
from datetime import datetime as dt
from scipy import stats
from math import log, sqrt, exp
import numpy as np
import matplotlib.pyplot as plt

class risk_reversal:
    
    def __init__(self, S0, K1, K2, t, M, r, sigma, div):
        
        '''
        Attributes:
        ------------------------------------------------------------------------------------------
        S0 (initial underlying level),     ## Risk reversal startegy: K1 < S0 < K2
        K1 (option strike price),          ## Selling an out of the money put with strike K1
        K2 (option strike price),          ## Buying an out of the money call with strike K2
        t (pricing date),                  ## Can enter in datetime format or str ('dd/mm/yyyy') or years (float)
        M (maturity date),                 ## Same as t
        r (constant risk-free short rate), ## For 5%, enter 0.05
        sigma (volatility),                ## For 5%, enter 0.05
        div (constant dividend rate),    ## For 5%, enter 0.05
        ------------------------------------------------------------------------------------------
        
        Methods:
        ------------------------------------------------------------------------------------------
        value (return present value of the risk reversal strategy),
        plot_payoff (plots net payoff diagram and present value for the range of underlying prices
                     [0.9 * K1, 1.1 * K2]).
        
        ------------------------------------------------------------------------------------------
        '''
        
        self.S0 = S0
        self.K1 = K1
        self.K2 = K2
        self.t = t
        self.M = M
        self.r = r
        self.sigma = sigma
        self.div = div
        
        self.refresh()
    
    def refresh(self):
        
        if self.K1 < self.K2:
            pass
        else:
            raise ValueError("For risk reversal K1 < K2 is neccesary!")
            
        if type(self.t).__name__ == 'str':
            self.t= dt.strptime(self.t, '%m/%d/%Y')
        if type(self.M).__name__ == 'str':  
            self.M = dt.strptime(self.M, '%m/%d/%Y')
       
        if self.t > self.M:
            raise ValueError("Pricing date later than maturity!")
        
        if type(self.t).__name__ in ['int', 'float']:
            self.T = self.M - self.t
        else:
            self.T = (self.M - self.t).days/365.0
    
    def d1_d2(self):
        
        ## d1 and d2 for put option
        self.d1_1 = (log(self.S0 / self.K1) + (self.r - self.div + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))
        self.d2_1 = self.d1_1 - self.sigma * sqrt(self.T)
        
        ## d1 and d2 for call option
        self.d1_2 = (log(self.S0 / self.K2) + (self.r - self.div + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))
        self.d2_2 = self.d1_2 - self.sigma * sqrt(self.T)
        
    def value(self):
        
        self.refresh()
        self.d1_d2()
        
        value_put = (self.K1 * exp(-self.r * self.T) * stats.norm.cdf(-self.d2_1, 0.0, 1.0) - self.S0 * exp(-self.div * self.T) * stats.norm.cdf(-self.d1_1, 0.0, 1.0))
        value_call = (self.S0 * exp(-self.div * self.T) * stats.norm.cdf(self.d1_2, 0.0, 1.0) - self.K2 * exp(-self.r * self.T) * stats.norm.cdf(self.d2_2, 0.0, 1.0))
        
        pv_risk_reversal = value_call - value_put
        return pv_risk_reversal
    
    def plot_payoff(self):
        
        strategy_pv = []
        for i in range(int(0.9 * self.K1), int(1.1 * self.K2)+1):
            options_pv = risk_reversal(i, self.K1, self.K2, self.t, self.M, self.r, self.sigma, self.div)
            strategy_pv.append([i,options_pv.value()])
        
        np.set_printoptions(precision=3, suppress=True)
        self.strategy_payoff = np.array(strategy_pv)
        print(self.strategy_payoff)
        
        plt.scatter(self.strategy_payoff[:,0], self.strategy_payoff[:,1], s=5)
        plt.xlabel('Present Value of Underlying Prices')
        plt.ylabel('Present Value of the Risk Reversal Strategy')
        plt.axhline(0, linewidth = 0.5, color = 'grey')
        plt.show()