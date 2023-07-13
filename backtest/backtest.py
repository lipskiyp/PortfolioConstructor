import pandas as pd
import numpy as np


allowed_rebal_freq = ['Q', 'M', 'MS', 'W', 'B', 'D']


class _Backtest:
        '''
        Non-public base class for all backtests 

        :param quotes: quotes for tickers, type pandas.DataFrame
        '''
        def __init__(self, quotes):
            self._quotes = quotes

        
        # Returns calendar  
        def get_calendar(self):
            return self.get_quotes().index


        # Returns rebalance calendar (NB Non-Public, only works for some portfolio types)
        def _get_rebalcal(self):
            cal = self.get_calendar()[self._vol_lookback_window:] # exclude days used for vol calculation

            if self._rebal_freq in allowed_rebal_freq:
                return list(pd.bdate_range(start = cal[0], end = cal[-1], freq = self._rebal_freq))

            else: # 'D' by default
                return cal
        

        # Return list of tickers
        def get_tickers(self):
            return self._quotes.columns.values
        

        # Return quotes for all tickers with filled/dropped gaps
        def get_quotes(self):
            if self._ignore_missing:
                return self._quotes.dropna() # deleted days with missing quotes
            else:
                return self._quotes.fillna(method='ffill') # fill missing quotes with previous values
            

        # Return pandas.DataFrame with rolling standard deviation of daily returns for all tickers 
        def _get_vol(self):
            return self.get_quotes().pct_change().rolling(self._vol_lookback_window).std() * np.sqrt(252) # annualised standard deviation 
        

        # Returns pandas.DataFrame with backtest timeseries, indexed by calendar 
        def get_backtest(self):
            offset = self._vol_lookback_window + self._vol_lookback_offset # ignore days within first vol lookback window + vol lookback offset
            weighted_rs = (self.get_quotes()[offset:].pct_change().fillna(0) * self.get_weights()[offset:].fillna(0))
            return weighted_rs.sum(axis = 1).add(1).cumprod().mul(100)