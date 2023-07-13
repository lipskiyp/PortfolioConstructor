import pandas as pd
import numpy as np

from backtest.backtest import _Backtest


# Fixed Weights
class Fixed(_Backtest):
        '''
        Creates an insatnce of _Backtest with fixed-weights 

        :param weights: list of fixed weights, type: float[] 
        :param ignore_missing: if True - drops rows if any quotes missing, if False - usses ffill method to fill missing quotes, type: bool 
        '''
        def __init__(self, quotes, weights, ignore_missing = False):
            super().__init__(quotes)
            self._ignore_missing = ignore_missing
            self._weights = weights
            self._vol_lookback_offset = 0 # enforce
            self._vol_lookback_window = 0 # enforce


        def get_weights(self):
            tickers = self.get_tickers()
            weights = self._weights
            cal = self.get_calendar()
            
            weights = [[weights[t] for t, ticker in enumerate(tickers)] for day in cal]
            return pd.DataFrame(data = weights, index = cal, columns = tickers)


# Risk-Budget weights
class RB(_Backtest): 
        '''
        Creates an insatnce of _Backtest with risk-budget/vol weights (using rolling returns), allows leverage 

        :param risk_budget: list of risk-budgets, type: int[]
        :param vol_lookback_offset: bdays to offset vol-window, type: int >= 1
        :param vol_lookback_window: window used to calculate vol, type: int >= 1
        :param rebal_freq: weight rebalance frequency ['Q', 'M', 'W', 'B' etc.], type: str
        :param ignore_missing: if True - drops rows if any quotes missing, if False - usses ffill method to fill missing quotes, type: bool
        '''
        def __init__(self, quotes, risk_budget, vol_lookback_window = 20, vol_lookback_offset = 1, rebal_freq = 'M', ignore_missing = False):
            super().__init__(quotes)
            self._ignore_missing = ignore_missing
            self._risk_budget = risk_budget
            self._vol_lookback_offset = max(1, vol_lookback_offset) # must be >= 1
            self._vol_lookback_window = min(vol_lookback_window, len(self.get_calendar()) - vol_lookback_offset) # must be <= len of quotes
            self._rebal_freq = rebal_freq
        

        def get_weights(self):
            tickers = self.get_tickers()
            vol = self._get_vol().shift(self._vol_lookback_offset)
            risk_budget = self._risk_budget
            cal = self.get_calendar()
            cal_0 = cal[self._vol_lookback_window + self._vol_lookback_offset] # rebalance on first day
            rebalcal = self._get_rebalcal()
            
            rb_vol_rebal = [ [risk_budget[t] / vol[ticker][day] for t,ticker in enumerate(tickers)] if day in rebalcal or day == cal_0 else [np.nan for ticker in tickers] for day in cal] # rb/vol on rebal dates else np.nan
            rb_vol_all = pd.DataFrame(data = rb_vol_rebal, index = cal, columns = tickers).fillna(method='ffill') # fill non-rebal dates with previous values
            return rb_vol_all.div(rb_vol_all.sum(axis = 1)/sum(self._risk_budget), axis = 0) # div rb/vol by sum(rb/vol) * sum(rb) for each row


# Inverse-Vol weights
class InverseVol(RB):
        '''
        NB InverseVol is a special case of RB with equal risk-budgets that sum to 1
        '''
        def __init__(self, quotes, vol_lookback_window = 20, vol_lookback_offset = 1, rebal_freq = 'M', ignore_missing = False):
            self._risk_budget = [1/len(quotes.columns)] * len(quotes.columns) # equal risk-budgets that sum to 1
            super().__init__(quotes, self._risk_budget, vol_lookback_window, vol_lookback_offset, rebal_freq, ignore_missing)