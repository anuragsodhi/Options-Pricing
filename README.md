# Black-Scholes pricing (including dividend parameter) with greeks calculation and implied voltality - 

Class with :

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
