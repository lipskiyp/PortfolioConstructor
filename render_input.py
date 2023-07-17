render_input = {}

render_input['portfolio_size'] = 5 # Max number of tickers in portfolio

render_input['portfolio_checked'] = 2 # Number of tickers to be "checked" by default 

render_input['selected_constructor'] = 'constructorFW' # Default constructor for /constructor route

# Active constructors
render_input['active_constructors'] = {'constructorFW': {'name': 'Fixed-Weight', 
                                                  'route': '/constructor/constructorFW'}, 
                                                        
                                        'constructorIV': {'name': 'Inverse-Volatility', 
                                                                'route': '/constructor/constructorIV'}, 

                                        'constructorRB': {'name': 'Risk-Budget', 
                                                        'route': '/constructor/constructorRB'},
                                        }

# Active routes 
render_input['active_routes'] = [constructor['route'] for constructor in render_input['active_constructors'].values()]

# Inputs to be displayed when /constructorXX routes are requested for each constructor
render_input['active_inputs'] = {'constructorFW': {'StartDate': {'show': True, 'show_as': 'Start Date'},
                                                    'EndDate': {'show': True, 'show_as': 'End Date'},
                                                    'Ticker': {'show': True, 'show_as': 'Ticker'}, 
                                                    'Weight': {'show': True, 'show_as': 'Weight'}, 
                                                    'VolLookbackWindow': {'show': False, 'show_as': 'Volatility Lookback Window'},
                                                    'VolLookbackOffset': {'show': False, 'show_as': 'Volatility Lookback Offset'},
                                                    'RebalFreq': {'show': False, 'show_as': 'Rebalancing Frequency'},
                                                    'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                    },

                                'constructorIV': {'StartDate': {'show': True, 'show_as': 'Start Date'},
                                                    'EndDate': {'show': True, 'show_as': 'End Date'},
                                                    'Ticker': {'show': True, 'show_as': 'Ticker'}, 
                                                    'Weight': {'show': False, 'show_as': 'Weight'},
                                                    'VolLookbackWindow': {'show': True, 'show_as': 'Volatility Lookback Window'},
                                                    'VolLookbackOffset': {'show': True, 'show_as': 'Volatility Lookback Offset'},
                                                    'RebalFreq': {'show': True, 'show_as': 'Rebalancing Frequency'},
                                                    'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                    },

                                'constructorRB': {'StartDate': {'show': True, 'show_as': 'Start Date'},
                                                    'EndDate': {'show': True, 'show_as': 'End Date'},
                                                    'Ticker': {'show': True, 'show_as': 'Ticker'}, 
                                                    'Weight': {'show': True, 'show_as': 'Risk-Budget'},
                                                    'VolLookbackWindow': {'show': True, 'show_as': 'Volatility Lookback Window'},
                                                    'VolLookbackOffset': {'show': True, 'show_as': 'Volatility Lookback Offset'},
                                                    'RebalFreq': {'show': True, 'show_as': 'Rebalancing Frequency'},
                                                    'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                    },
                                }








