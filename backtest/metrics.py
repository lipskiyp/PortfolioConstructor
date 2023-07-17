import pandas as pd
import numpy as np
from datetime import datetime 

from quotes.get_quotes import get_quotes

class Metrics:
    '''
    Calculates financial metrics for time-series (e.g. Sharpe, Annualized Vol etc.)

    :param ts: single-column time-series, type: pandas.DataFrame
    '''
    def __init__(self, ts):
        # Check timeseries is not empty 
        if len(ts) < 1:
            raise ValueError('Invalid time series')
        
        self.ts = ts.dropna().values


    def get_avgr(self, offset = 1):
        '''
        Calculates average annualised log return

        :param offset: day lag used to calculate returns, type: int
        '''
        return np.average(np.log(self.ts[offset:]/self.ts[:-offset])) * np.sqrt(252/offset) # Average annualised log return


    def get_vol(self, offset = 1):
        '''
        Calculates annualised standard deviation of log returns 

        :param offset: day lag used to calculate returns, type: int
        '''
        return np.std(np.log(self.ts[offset:]/self.ts[:-offset])) * np.sqrt(252/offset) # Annualised standard deviation of log returns 


    def get_sharpe(self, offset = 1):
        '''
        Calculates Sharpe Ratio

        :param offset: day lag used to calculate returns, type: int
        '''
        return self.get_avgr(offset = offset)/self.get_vol(offset = offset) # Sharpe Ratio


    def get_maxdd(self):
        '''
        Calculates maximum drawdown
        ''' 
        ts = self.ts
        return np.min([quote / np.max(ts[:q + 1]) - 1 for q, quote in enumerate(ts)]) # Maximum Drawdown 
        