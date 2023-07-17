from datetime import datetime

def check_StartDate(user_input):
        '''
        check_StartDate() checks start date is in correct format 
        type: {} -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :return: True if start date is valid / False if invalid, list of errors, type: bool, []
        '''

        StartDate = user_input['StartDate']

        # Check start date is valid 
        try:
            StartDate = datetime.strptime(StartDate, '%Y-%m-%d')
        except:
            return False, ['Invalid Start Date']
        
        # Check start date is before today
        if StartDate > datetime.now():
            return False, ['Start date cannot be a future date']
        
        return True, []


def check_EndDate(user_input):
        '''
        check_EndDate() checks end date is in correct format 
        type: {} -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :return: True if end date is valid / False if invalid, list of errors, type: bool, []
        '''

        EndDate = user_input['EndDate']

        # Check end date is valid 
        try:
            EndDate = datetime.strptime(EndDate, '%Y-%m-%d')
        except:
            return False, ['Invalid End Date']
        
        # Check end date is before today
        if EndDate > datetime.now():
            return False, ['End date cannot be a future date']
        
        return True, []


def check_Ticker(user_input, render_input):
        '''
        check_Ticker() checks that selected tickers are not 'empty'
        type: ({}, {}) -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        :return: True if all tickers are valid / False if some are invalid, list of errors, type: bool, []
        '''

        # for all possible tickers
        for ticker_i in range(render_input['portfolio_size']):
             # If ticker selected 
             if f'AddTicker{ticker_i + 1}' in user_input.keys():
                  # If empty ticker
                  if user_input[f'Ticker{ticker_i + 1}'] == "":
                       return False, [f'Ticker {ticker_i + 1} not specified']  
        
        return True, []


def check_Weight(user_input, render_input):
        '''
        check_Weight() checks that weights/risk-budgets for selected tickers are positive floats
        type: ({}, {}) -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        :return: True if all weights are valid / False if some are invalid, list of errors, type: bool, []
        '''
                
        # for all possible tickers
        for ticker_i in range(render_input['portfolio_size']):
                # If ticker selected 
                if f'AddTicker{ticker_i + 1}' in user_input.keys():
                    # Check if weight is a float 
                    try:
                        float(user_input[f'Weight{ticker_i + 1}'])
                    except:
                        return False, [f'Invalid Weight/Risk-Budget for Ticker {ticker_i + 1}']
                    
                    # Check weight is positive
                    if float(user_input[f'Weight{ticker_i + 1}']) < 0:
                         return False, [f'Weight/Risk-Budget for Ticker {ticker_i + 1} must be positive']
                         
        return True, []


def check_VolLookbackWindow(user_input):
        '''
        check_VolLookbackWindow() checks volatility lookback window is a positive integer greater or equal to 1
        type: {} -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :return: True if volatility lookback window is valid / False if invalid, list of errors, type: bool, []
        '''

        VolLookbackWindow = user_input['VolLookbackWindow']

        # Check if volatility lookback window is a float 
        try:
            int(VolLookbackWindow)
        except:
            return False, [f'Invalid volatility lookback window']
        
        # Check volatility lookback window is >=1
        if int(VolLookbackWindow) < 1:
                return False, [f'Volatility lookback window must be greater or equal to 1']   
        
        return True, []


def check_VolLookbackOffset(user_input):
        '''
        check_VolLookbackOffset() checks volatility lookback offset is a positive integer greater or equal to 1
        type: {} -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :return: True if volatility lookback offset is valid / False if invalid, list of errors, type: bool, []
        '''

        VolLookbackOffset = user_input['VolLookbackOffset']

        # Check if volatility lookback offset is a float 
        try:
            int(VolLookbackOffset)
        except:
            return False, [f'Invalid volatility lookback offset']
        
        # Check volatility lookback offset is >=1
        if int(VolLookbackOffset) < 1:
                return False, [f'Volatility lookback offset must be greater or equal to 1']   
        
        return True, []


def check_RebalFreq(user_input, allowed_rebal_freq):
        '''
        check_RebalFreq() checks rebalancing frequency is valid
        type: ({}, int) -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :param allowed_rebal_freq: list of allowed rebalancing frequencies, type: []
        :return: True if rebalancing frequency is valid / False if invalid, list of errors, type: bool, []
        '''

        RebalFreq = user_input['RebalFreq']

        if RebalFreq not in allowed_rebal_freq:
              return False, [f'Invalid rebalancing frequency']   
        
        return True, []


def check_IgnoreMissing(user_input):
        '''
        check_IgnoreMissing() checks 'Ignore Missing' parameter is valid
        type: {} -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :return: True if 'Ignore Missing' parameter is valid / False if invalid, list of errors, type: bool, []
        '''

        IgnoreMissing = user_input['IgnoreMissing']

        try:
            bool(IgnoreMissing)
        except:
              return False, ["Invalid 'Ignore Missing' parameter"]   
        
        return True, []
              