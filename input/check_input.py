from datetime import datetime

from backtest.backtest import allowed_rebal_freq
from input.checks import *

def check_input(user_input, render_input):
        '''
        check_input() checks for user input for all 'shown' render inputs
        type: ({}, {}) -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        :return: True if all input valid / False if some are invalid, list of errors, type: bool, []
        '''
        
        constructor = render_input['selected_constructor']
        
        # For every render input
        for render_input_key, render_input_value in render_input['active_inputs'][constructor].items():
        
            # If render input is shown
            if render_input_value['show'] == True:
                check, error = check_all(user_input, render_input, render_input_key)
                # If input invalid
                if check == False:
                    return check, error
        
        return True, []
        

def check_all(user_input, render_input, check_item):
        '''
        check_all() checks for: 

            StartDate
            EndDate
            Ticker
            Weight
            VolLookbackWindow
            VolLookbackOffset
            RebalFreq
            IgnoreMissing

        type: ({}, {}, str) -> (bool, [])
        
        :param user_input: user input dictionary, type: {}
        :param render_input: render input dictionary, type: {}
        ;param check_item: input item to chek, type: str
        :return: True if all input valid / False if some are invalid, list of errors, type: bool, []
        '''

        if check_item == 'StartDate':
            try:
                check, check_error = check_StartDate(user_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'EndDate':
            try:
                check, check_error = check_EndDate(user_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'Ticker':
            try:
                check, check_error = check_Ticker(user_input, render_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'Weight':
            try:
                check, check_error = check_Weight(user_input, render_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'VolLookbackWindow':
            try:
                check, check_error = check_VolLookbackWindow(user_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'VolLookbackOffset':
            try:
                check, check_error = check_VolLookbackOffset(user_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'RebalFreq':
            try:
                check, check_error = check_RebalFreq(user_input, allowed_rebal_freq)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']

        elif check_item == 'IgnoreMissing':
            try:
                check, check_error = check_IgnoreMissing(user_input)
                if check == False:
                    return check, check_error
            except:
                return False, [f'Could not check {check_item}']
        
        return True, []