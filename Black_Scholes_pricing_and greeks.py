# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 16:02:35 2018

@author: Anurag
"""
from datetime import datetime as dt
from scipy import stats
from math import log, sqrt, exp
from scipy.optimize import fsolve

class european_option:
    
    def __init__(self, S0, K, t, M, r, sigma, d, CP, C=10):
        
        '''
        Attributes:
        ------------------------------------------------------------------------------------------
        S0 (initial underlying level), 
        K (option strike price), 
        t (pricing date),                  ## Can enter in datetime format or str ('dd/mm/yyyy') or years (float)
        M (maturity date),                 ## Same as t
        r (constant risk-free short rate), ## For 5%, enter 0.05
        sigma (volatility),                ## For 5%, enter 0.05
        d (continuous dividend rate),      ## For 5%, enter 0.05
        CP (call or put),                  ## Enter 'Call'/'C' or 'Put'/'P' in any case
        C (market price of the option)     ## Optional - only used for implied vol. method (default = 10)
        ------------------------------------------------------------------------------------------
        
        Methods:
        ------------------------------------------------------------------------------------------
        value (return present value of the option), 
        imp_vol (implied volatility given market price), 
        delta (option delta), 
        gamma (option gamma), 
        vega (option vega), 
        theta (option theta), 
        rho (option rho)
        ------------------------------------------------------------------------------------------
        '''
        
        self.S0 = S0
        self.K = K
        self.t = t
        self.M = M
        self.r = r
        self.sigma = sigma
        self.d = d
        self.CP = CP
        self.C = C
        self.refresh()
    
    def refresh(self):

        if type(self.t).__name__ == 'str':
            self.t= dt.strptime(self.t, '%m/%d/%Y')
        if type(self.M).__name__ == 'str':  
            self.M = dt.strptime(self.M, '%m/%d/%Y')
        if self.CP.lower() in ['call', 'c']:
            self.CP = 'call'
        elif self.CP.lower() in ['put', 'p']:
            self.CP = 'put'
        else:
            raise ValueError("Check value of variable CP - Call/C or Put/P allowed!")
        if self.t > self.M:
            raise ValueError("Pricing date later than maturity!")
        
        if type(self.t).__name__ in ['int', 'float']:
            self.T = self.M - self.t
        else:
            self.T = (self.M - self.t).days/365.0
		 
    
    def d1_d2(self):

        self.d1 = (log(self.S0 / self.K) + (self.r - self.d + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))
        self.d2 = self.d1 - self.sigma * sqrt(self.T)
        
    def value(self):
        
        self.refresh()
        self.d1_d2()
        
        if self.CP == 'call':
            value = (self.S0 * exp(-self.d * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0) - self.K * exp(-self.r * self.T) * stats.norm.cdf(self.d2, 0.0, 1.0))
        else:
            value = (self.K * exp(-self.r * self.T) * stats.norm.cdf(-self.d2, 0.0, 1.0) - self.S0 * exp(-self.d * self.T) * stats.norm.cdf(-self.d1, 0.0, 1.0))
        return value
    
    def imp_vol(self):
        
        self.refresh()
        self.d1_d2()
        
        option = european_option(self.S0, self.K, self.t, self.M, self.r, self.sigma, self.d, self.CP, self.C)
        option.refresh()
        option.d1_d2()
        
        def difference(sig):
            option.sigma = sig
            return option.value() - option.C
        iv = fsolve(difference, option.sigma)[0]
        return iv
    
    def delta(self):
        
        self.refresh()
        self.d1_d2()
        
        if self.CP == 'call': 
            delta = exp(-self.d * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0)
        else:
            delta = exp(-self.d * self.T) * (stats.norm.cdf(self.d1, 0.0, 1.0) - 1)    
        return delta
    
    def gamma(self):
        
        self.refresh()
        self.d1_d2()
        
        gamma = (exp(-self.d * self.T) * stats.norm.pdf(self.d1, 0.0, 1.0)) / (self.S0 * self.sigma * sqrt(self.T))
        return gamma
    
    def vega(self):
        
        self.refresh()
        self.d1_d2()
        
        vega = self.S0 * exp(-self.d * self.T) * stats.norm.pdf(self.d1, 0.0, 1.0) * sqrt(self.T)
        return vega
    
    def theta(self):
        
        self.refresh()
        self.d1_d2()
        
        if self.CP == 'call':
            theta = ( -(self.S0 * exp(-self.d * self.T) * stats.norm.pdf(self.d1, 0.0, 1.0) * self.sigma / (2 * sqrt(self.T)))
                        - (self.r * self.K * exp(-self.r * self.T) * stats.norm.cdf(self.d2, 0.0, 1.0))
                        + (self.d * self.S0 * exp(-self.d * self.T) * stats.norm.cdf(self.d1, 0.0, 1.0)))
        else:
            theta = ( -(self.S0 * exp(-self.d * self.T) * stats.norm.pdf(self.d1, 0.0, 1.0) * self.sigma / (2 * sqrt(self.T)))
                        + (self.r * self.K * exp(-self.r * self.T) * stats.norm.cdf(-self.d2, 0.0, 1.0))
                        - (self.d * self.S0 * exp(-self.d * self.T) * stats.norm.cdf(-self.d1, 0.0, 1.0)))
        return theta
    
    def rho(self):
        
        self.refresh()
        self.d1_d2()
        
        if self.CP == 'call':
            rho = self.K * self.T * exp(-self.r * self.T) * stats.norm.cdf(self.d2, 0.0, 1.0)
        else:
            rho = - self.K * self.T * exp(-self.r * self.T) * stats.norm.cdf(-self.d2, 0.0, 1.0)
        return rho
     