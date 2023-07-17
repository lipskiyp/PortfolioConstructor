from backtest.backtests import *

def backtest_run(user_input, render_input, quotes):
        '''
        backtest_run() returns an instance of a backtest for selected constructor
        type: ({}, {}, pd.DataFrame) -> (backtest instance/None, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        :param quotes: quotes for tickers, type pandas.DataFrame
        :return: backtest instance / None, list of errors, type: backtest instance/None, []
        '''
        
        constructor = render_input['selected_constructor']

        if constructor == 'constructorFW':
            return backtestFW(quotes = quotes, 
                         weights = user_input['Weight'], 
                         ignore_missing = user_input['IgnoreMissing']), []
        
        elif constructor == 'constructorIV':
            return backtestIV(quotes = quotes, 
                              vol_lookback_window = user_input['VolLookbackWindow'], 
                              vol_lookback_offset = user_input['VolLookbackOffset'], 
                              rebal_freq = user_input['RebalFreq'], 
                              ignore_missing = user_input['IgnoreMissing']), []
        
        elif constructor == 'constructorRB':
            return backtestRB(quotes = quotes, 
                      risk_budget = user_input['RiskBudgets'],
                      vol_lookback_window = user_input['VolLookbackWindow'], 
                      vol_lookback_offset = user_input['VolLookbackOffset'], 
                      rebal_freq = user_input['RebalFreq'], 
                      ignore_missing = user_input['IgnoreMissing']), []
        
        else:
            return None, ['Failed to construct backtest']
