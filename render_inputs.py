render_inputs = {}

render_inputs['portfolio_n'] = 5 # Max number of tickers in portfolio

render_inputs['checked_n'] = 2 # Number of tickers to be "checked" by default 

render_inputs['active_constructor'] = 'Fixed-Weight' # Default constructor for /constructor route
 
# Constructors to be displayed when /constructorXX routes are requested 
render_inputs['constructors'] = {'Fixed-Weight': {'name': 'Fixed-Weight', 
                                                  'route': '/constructorFW'}, 
                                                  
                                 'Inverse-Volatility': {'name': 'Inverse-Volatility', 
                                                        'route': '/constructorIV'}, 

                                 'Risk-Budget': {'name': 'Risk-Budget', 
                                                 'route': '/constructorRB'},
                                 }


render_inputs['user_inputs'] = {'Fixed-Weight': {'default_constructor': {'name': 'Fixed-Weight', 'route': '/constructorFW'},
                                                'Weight': {'show': True, 'show_as': 'Weight'},
                                                'VolLookbackWindow': {'show': False, 'show_as': 'Volatility Lookback Window'},
                                                'VolLookbackOffset': {'show': False, 'show_as': 'Volatility Lookback Offset'},
                                                'RebalFreq': {'show': False, 'show_as': 'Rebalancing Frequency'},
                                                'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                },

                                'Inverse-Volatility': {'default_constructor': {'name': 'Inverse-Volatility', 'route': '/constructorIV'},
                                                       'Weight': {'show': False, 'show_as': 'Weight'},
                                                       'VolLookbackWindow': {'show': True, 'show_as': 'Volatility Lookback Window'},
                                                       'VolLookbackOffset': {'show': True, 'show_as': 'Volatility Lookback Offset'},
                                                       'RebalFreq': {'show': True, 'show_as': 'Rebalancing Frequency'},
                                                       'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                       },

                                'Risk-Budget': {'default_constructor': {'name': 'Risk-Budget', 'route': '/constructorRB'},
                                                'Weight': {'show': True, 'show_as': 'Risk-Budget'},
                                                'VolLookbackWindow': {'show': True, 'show_as': 'Volatility Lookback Window'},
                                                'VolLookbackOffset': {'show': True, 'show_as': 'Volatility Lookback Offset'},
                                                'RebalFreq': {'show': True, 'show_as': 'Rebalancing Frequency'},
                                                'IgnoreMissing': {'show': True, 'show_as': 'Ignore Missing'},
                                                },
                                }








