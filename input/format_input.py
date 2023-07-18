from datetime import datetime

def format_input(user_input, render_input):
        '''
        format_input() converts user input to correct format 
        type: ({}, {}) -> ({}/None, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        :return: dictionary with user input in correct format / None if failed to convert, list of errors, type: {}/None, []
        '''

        constructor = render_input['selected_constructor']

        formatted_user_input = {}
        
        # For every render input
        for render_input_key, render_input_value in render_input['active_inputs'][constructor].items():   
            # If render input is shown
            if render_input_value['show'] == True:
                formatted_user_input_item, error = format_all(user_input, render_input, render_input_key)
                # If input invalid
                if formatted_user_input_item == None:
                    return None, error
                else:
                     formatted_user_input[render_input_key] = formatted_user_input_item
        
        return formatted_user_input, []


def format_all(user_input, render_input, format_item):
        '''
        format_all() formats user input: 

            StartDate
            EndDate
            Ticker
            Weight
            VolLookbackWindow
            VolLookbackOffset
            RebalFreq
            IgnoreMissing

        type: ({}, {}, str) -> (formated_item/None, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        ;param format_item: input item to be formated, type: str
        :return: formated item / None if failed to format, list of errors, type: formated_item/None, []
        '''

        if format_item == 'StartDate':
            try:
                StartDate = user_input['StartDate']
                return datetime.strptime(StartDate, '%Y-%m-%d'), []
            except:
                return None, [f'Could not format {format_item}']

        elif format_item == 'EndDate':
            try:
                EndDate = user_input['EndDate']
                return datetime.strptime(EndDate, '%Y-%m-%d'), []
            except:
                return None, [f'Could not format {format_item}']
            
        elif format_item == 'Ticker':
            try:
                tickers = [user_input[f'Ticker{ticker_i + 1}'].upper() for ticker_i in range(render_input['portfolio_size']) if f'AddTicker{ticker_i + 1}' in user_input.keys()]
                return tickers, []
            except:
                return None, [f'Could not format {format_item}']
            
        elif format_item == 'Weight':
            try:
                weights = [float(user_input[f'Weight{ticker_i + 1}']) for ticker_i in range(render_input['portfolio_size']) if f'AddTicker{ticker_i + 1}' in user_input.keys()]
                return weights, []
            except:
                return None, [f'Could not format {format_item}']
            
        elif format_item == 'VolLookbackWindow':
            try:
                VolLookbackWindow = user_input['VolLookbackWindow']
                return int(VolLookbackWindow), []
            except:
                return None, [f'Could not format {format_item}']

        elif format_item == 'VolLookbackOffset':
            try:
                VolLookbackOffset = user_input['VolLookbackOffset']
                return int(VolLookbackOffset), []
            except:
                return None, [f'Could not format {format_item}']

        elif format_item == 'RebalFreq':
            try:
                RebalFreq = user_input['RebalFreq']
                return RebalFreq, []
            except:
                return None, [f'Could not format {format_item}']
            
        elif format_item == 'IgnoreMissing':
            try:
                IgnoreMissing = user_input['IgnoreMissing']
                return bool(IgnoreMissing), []
            except:
                return None, [f'Could not format {format_item}']
            
        else:
            return None, [f'Unknown input {format_item}']



