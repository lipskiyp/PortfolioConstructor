from datetime import datetime

from backtest.backtest import allowed_rebal_freq


def check_input_FW(input, n_tickeers):
        '''
        check_input_FW() checks for: invalid start/end date, weights, tickers, IgnoreMissing
        type: ({}, int) -> ({}/None, [])

        :param input: original user input submitted by 'POST' (using request.form), type: ImmutableMultiDict
        :param n_tickeers: tickers allowed for selection, type: int
        :return: dictionary with all inputs/None if some input invalid, list of errors, type: {}/None, []
        '''
        
        # Collect all errors
        errors = []

        # Check dates 
        check, errors_dates = check_dates(input.get('StartDate'), input.get('EndDate'))
        # If dates incorrect 
        if check is None:
            return None, errors_dates

        # Check tickers and weights
        tickers, weights = [], []
        for ticker_i in range(n_tickeers): # for all possible ticker inputs
            if input.get(f'AddTicker{ticker_i + 1}') == 'on': # if ticker selected 
                tickers.append(input.get(f'Ticker{ticker_i + 1}').upper()) # make sure ticker is capitalised 
                try:
                    weights.append(float(input.get(f'Weight{ticker_i + 1}'))) # makes sure weight is a float 
                except: 
                    return None, [f'Invalid weight: {tickers[ticker_i]}']
                
        # Check that at least one ticker was selected
        if len(tickers) < 1:
            return None, ['No valid tickers selected']

        # If all tickers and weights valid         
        check['Tickers'] = tickers
        check['Weights'] = weights

        # Check IgnoreMissing 
        try:
            check['IgnoreMissing'] = input['IgnoreMissing']
        except:
            check['IgnoreMissing'] = False # Default 
            errors += "Ignore Missing set to 'No'"
  
        return check, errors


def check_input_IV(input, n_tickeers):
        '''
        check_input_IV() checks for: invalid start/end dates, tickers, volatility lookback window/offset, rebalancing frequency, IgnoreMissing 
        type: ({}, int) -> ({}/None, [])

        :param input: original user input submitted by 'POST' (using request.form), type: ImmutableMultiDict
        :param n_tickeers: tickers allowed for selection, type: int
        :return: dictionary with all inputs/None if some input invalid, list of errors, type: {}/None, []
        '''

        # Collect all errors
        errors = []

        # Check dates 
        check, errors = check_dates(input.get('StartDate'), input.get('EndDate'))
        # If dates incorrect 
        if check is None:
            return None, errors
        
        # Check tickers
        tickers = []
        for ticker_i in range(n_tickeers): # for all possible ticker inputs
            if input.get(f'AddTicker{ticker_i + 1}') == 'on': # if ticker selected 
                tickers.append(input.get(f'Ticker{ticker_i + 1}').upper()) # make sure ticker is capitalised        
        
        # Check that at least one ticker was selected
        if len(tickers) < 1:
            return None, ['No valid tickers selected']
        else:
            check['Tickers'] = tickers

        # Check Volatility Lookback Window
        if input['VolLookbackWindow'] == '':
             check['VolLookbackWindow'] = 20 # Default 
        else:
            try:
                check['VolLookbackWindow'] = int(input['VolLookbackWindow'])
            except:
                check['VolLookbackWindow'] = 20 # Default 
                errors += "Volatility Lookback Window set to 20"
             
        # Check Volatility Offset 
        if input['VolLookbackOffset'] == '':
             check['VolLookbackOffset'] = 1 # Default 
        else:
            try:
                check['VolLookbackOffset'] = int(input['VolLookbackOffset'])
            except:
                check['VolLookbackOffset'] = 1 # Default 
                errors += "Volatility Lookback Offset set to 1"

        # Rebalancing Frequency
        if input['RebalFreq'] in allowed_rebal_freq:
            check['RebalFreq'] = input['RebalFreq'] 
        else:
            check['RebalFreq'] = 'B'
            errors += "Rebalancing Frequency set to 'Daily'"
             
        # Check IgnoreMissing 
        try:
            check['IgnoreMissing'] = input['IgnoreMissing']
        except:
            check['IgnoreMissing'] = False # Default 
            errors += "Ignore Missing set to 'No'"
             
        return check, errors


def check_input_RB(input, n_tickeers):
        '''
        check_input_RB() checks for: invalid start/end dates, risk-budgets, tickers, volatility lookback window/offset, rebalancing frequency, IgnoreMissing 
        type: ({}, int) -> ({}/None, [])

        :param input: original user input submitted by 'POST' (using request.form), type: ImmutableMultiDict
        :param n_tickeers: tickers allowed for selection, type: int
        :return: dictionary with all inputs/None if some input invalid, list of errors, type: {}/None, []
        '''

        # Collect all errors
        errors = []

        # Check dates 
        check, errors = check_dates(input.get('StartDate'), input.get('EndDate'))
        # If dates incorrect 
        if check is None:
            return None, errors
        
        # Check tickers and RBs
        tickers, risk_budgets = [], []
        for ticker_i in range(n_tickeers): # for all possible ticker inputs
            if input.get(f'AddTicker{ticker_i + 1}') == 'on': # if ticker selected 
                tickers.append(input.get(f'Ticker{ticker_i + 1}').upper()) # make sure ticker is capitalised 
                try:
                    risk_budgets.append(float(input.get(f'RiskBudget{ticker_i + 1}'))) # makes sure weight is a float 
                except: 
                    return None, [f'Invalid risk-budget: {tickers[ticker_i]}']      
        
        # Check that at least one ticker was selected
        if len(tickers) < 1:
            return None, ['No valid tickers selected']

        # If all tickers and weights valid         
        check['Tickers'] = tickers
        check['RiskBudgets'] = risk_budgets

        # Check Volatility Lookback Window
        if input['VolLookbackWindow'] == '':
             check['VolLookbackWindow'] = 20 # Default 
        else:
            try:
                check['VolLookbackWindow'] = int(input['VolLookbackWindow'])
            except:
                check['VolLookbackWindow'] = 20 # Default 
                errors += "Volatility Lookback Window set to 20"
             
        # Check Volatility Offset 
        if input['VolLookbackOffset'] == '':
             check['VolLookbackOffset'] = 1 # Default 
        else:
            try:
                check['VolLookbackOffset'] = int(input['VolLookbackOffset'])
            except:
                check['VolLookbackOffset'] = 1 # Default 
                errors += "Volatility Lookback Offset set to 1"

        # Rebalancing Frequency
        if input['RebalFreq'] in allowed_rebal_freq:
            check['RebalFreq'] = input['RebalFreq'] 
        else:
            check['RebalFreq'] = 'B'
            errors += "Rebalancing Frequency set to 'Daily'"
             
        # Check IgnoreMissing 
        try:
            check['IgnoreMissing'] = input['IgnoreMissing']
        except:
            check['IgnoreMissing'] = False # Default 
            errors += "Ignore Missing set to 'No'"
             
        return check, errors


def check_dates(start, end):
        '''
        check_dates() checks start and end date are in correct format 
        type: (str, str) -> ({}/None, [])
        
        :param start: start date, type: str
        :param end: end date, types: str
        :return: dictionary with StartDate and EndDate as datetime / None if invalid, list of errors, type: {}/None, []
        '''

        checked_dates = {}
        # Check start date is valid 
        try:
            checked_dates['StartDate'] = datetime.strptime(start, '%Y-%m-%d')
        except:
            return None, ['Invalid Start Date']
        
         # Check end date is valid 
        try:
            checked_dates['EndDate'] = datetime.strptime(end, '%Y-%m-%d')
        except:
            return None, ['Invalid End Date']
        
        # Check end date is not before start date
        if checked_dates['StartDate'] >= checked_dates['EndDate']:
            return None, ['Start date must be before end date']
        
        # Check end date is before today
        if checked_dates['EndDate'] > datetime.now():
            return None, ['End date cannot be a future date']
        
        return checked_dates, []