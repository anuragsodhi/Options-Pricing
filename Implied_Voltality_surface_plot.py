# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 22:20:06 2018

@author: Anurag
"""
import pandas as pd
import numpy as np
import os
from math import log, sqrt, exp
from scipy import stats
from scipy.optimize import fsolve
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d 
from matplotlib import cm
mpl.rcParams['font.family'] = 'serif'

os.getcwd()
os.chdir('D:\Math Finance\Advanced Derivatives\HW4')

# Pricing Data
pdate = pd.Timestamp('2016-03-31')
tol = 0.2
S0 = 2059.74
r = 0.0059
div=0.0217

## Read in data
options = pd.read_csv("spxcalls20160331.csv")

## Create mid price
options['mid_price'] = (options.best_bid + options.best_offer)/2

## Convert from string to date format
options = options.assign(date=pd.to_datetime(options.date, format='%Y%m%d').values,
                         exdate=pd.to_datetime(options.exdate, format='%Y%m%d').values)
options = options.assign(days_maturity=((options.exdate - options.date).dt.days).values)

## Include only approx 1 week, 2 weeks, 1 month, 2 months, 3 months maturity options
time_in_month_allowed = [0.2,0.3, 0.4,0.5,0.6, 0.9,1.0,1.1, 1.9,2.0,2.1, 2.8,2.9,3.0,3.1,3.2]
options = options[(options['days_maturity']/30).round(1).isin(time_in_month_allowed)]

## Only keeping the options in 80% to 120% moneyness
options['forward'] = np.exp(r * options['days_maturity']/365) * S0
options = options[(abs(options['strike'] - options['forward']) / options['forward'])< tol]

## Calculate Imp Vol
def calculate_imp_vols(options):
    ''' Calculate all implied volatilities for the European call options
    '''
    for row in options.index:
        t = options['date'][row]
        T = options['exdate'][row]
        call = call_option(S0, options['strike'][row], t, T, r, 0.15)
        options.loc[row, 'Imp_Vol'] = call.imp_vol(options.loc[row, 'mid_price'])
    return options

## plot 3d voltality surface
## If no 3d graph then update matlibplot to atleast v1.2
def plot_imp_vols(options):
    ''' Plot the implied volatilites. '''
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(options['strike'].values, options['days_maturity'].values, options['Imp_Vol'].values, cmap=cm.jet)
    ax.set_xlabel('Strike Price')
    ax.set_ylabel('Days to Expiration')
    ax.set_zlabel('Implied Volatility')
    plt.suptitle('Implied Volatility Surface')
    plt.show()

## Class to calculate imp vol
class call_option(object):
    ''' Class for European call options in BSM Model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    t : datetime/Timestamp object
        pricing date
    M : datetime/Timestamp object
        maturity date
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term
        
    Methods
    =======
    value : float
        return present value of call option
    vega : float
        return vega of call option
    imp_vol : float
        return implied volatility given option quote
    '''
    
    def __init__(self, S0, K, t, M, r, sigma):
        self.S0 = float(S0)
        self.K = K
        self.t = t
        self.M = M
        self.r = r
        self.sigma = sigma

    def update_ttm(self):
        ''' Updates time-to-maturity self.T. '''
        if self.t > self.M:
            raise ValueError("Pricing date later than maturity.")
        self.T = (self.M - self.t).days / 365.

    def d1(self):
        ''' Helper function. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        return d1
        
    def value(self):
        ''' Return option value. '''
        self.update_ttm()
        d1 = self.d1()
        d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        value = (self.S0 * stats.norm.cdf(d1, 0.0, 1.0)
            - self.K * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0, 1.0))
        return value

    def imp_vol(self, C0, sigma_est=0.2):
        ''' Return implied volatility given option price. '''
        option = call_option(self.S0, self.K, self.t, self.M,
                             self.r, sigma_est)
        option.update_ttm()
        def difference(sigma):
            option.sigma = sigma
            return option.value() - C0
        iv = fsolve(difference, sigma_est)[0]
        return iv



