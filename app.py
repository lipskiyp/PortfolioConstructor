'''
THINGS TO ADD:

Display interface + data export 
Get Quotes Tab
Methodology
Metrics
'''

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')

from flask import Flask, redirect, render_template, request, session 
from flask_session import Session

from backtest.backtests import *
from input.check_input import *
from database.db import db
from quotes.get_quotes import get_quotes
from backtest.metrics import Metrics
from render_inputs import render_inputs


# Configure application
app = Flask(__name__)


# Configure Session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quotes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize the app with the extension
db.init_app(app)


# Create the table schema
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    quotes, errors = get_quotes(tickers = ['MSFT'], start = datetime.strptime('2023-06-01', '%Y-%m-%d'), end = datetime.strptime('2023-07-01', '%Y-%m-%d'))
    print(errors)
    print(quotes)
    metrics = Metrics(quotes)
    print(metrics.get_maxdd())
    return render_template('index.html')


@app.route('/constructor')
def constructor():
    # Render default constructor
    return render_template('constructor.html', 
                            render_inputs = render_inputs)


@app.route('/constructorFW', methods=['GET', 'POST'])
def constructorFW():
    render_inputs_current = render_inputs.copy()
    render_inputs_current['active_constructor'] = 'Fixed-Weight'

    if request.method == 'POST':
        # Check user input
        input, errors = check_input_FW(request.form, render_inputs_current.portfolio_n)

        # If input invalid
        if input is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = errors)
        
        # Get quotes
        quotes, quotes_errors = get_quotes(tickers = input['Tickers'], 
                                            start = input['StartDate'] , 
                                            end = input['EndDate']) 
        if quotes is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = quotes_errors)
        
        # Add quotes errors
        errors += quotes_errors

        # Execute backtest
        backtest = Fixed(quotes = quotes, 
                         weights = input['Weights'], 
                         ignore_missing = input['IgnoreMissing']).get_backtest() 

        return render_template('constructorDisplay.html', 
                                labels = list(backtest.index.strftime('%d-%m-%Y').values), 
                                values = list(backtest.values), 
                                errors = errors)

    else: # if request.method == 'GET':
        return render_template('constructor.html', 
                               render_inputs = render_inputs_current)


@app.route('/constructorIV', methods=['GET', 'POST'])
def constructorIV():
    render_inputs_current = render_inputs.copy()
    render_inputs_current['active_constructor'] = 'Inverse-Volatility'

    if request.method == 'POST':
        # Check user input
        input, errors = check_input_IV(request.form, render_inputs_current.portfolio_n)

        # If input invalid
        if input is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = errors)
        
        # Get quotes
        quotes, quotes_errors = get_quotes(tickers = input['Tickers'], 
                                            start = input['StartDate'], 
                                            end = input['EndDate']) 
        
        if quotes is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = quotes_errors)
        
        # Add quotes errors
        errors += quotes_errors

        # Execute backtest
        backtest = InverseVol(quotes = quotes, 
                              vol_lookback_window = input['VolLookbackWindow'], 
                              vol_lookback_offset = input['VolLookbackOffset'], 
                              rebal_freq = input['RebalFreq'], 
                              ignore_missing = input['IgnoreMissing']).get_backtest() 

        return render_template('constructorDisplay.html', 
                                labels = list(backtest.index.strftime('%d-%m-%Y').values), 
                                values = list(backtest.values), 
                                errors = errors)
    else:
        return render_template('constructor.html', 
                               render_inputs = render_inputs_current)


@app.route('/constructorRB', methods=['GET', 'POST'])
def constructorRB():
    render_inputs_current = render_inputs.copy()
    render_inputs_current['active_constructor'] = 'Risk-Budget'

    if request.method == 'POST':
        # Check user input
        input, errors = check_input_RB(request.form, render_inputs_current.portfolio_n)

        # If input invalid
        if input is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = errors)
        
        # Get quotes
        quotes, quotes_errors = get_quotes(tickers = input['Tickers'], 
                                            start = input['StartDate'], 
                                            end = input['EndDate']) 
        
        if quotes is None:
            return render_template('constructor.html', 
                                   render_inputs = render_inputs_current,
                                   errors = quotes_errors)
        
        # Add quotes errors
        errors += quotes_errors

        # Execute backtest
        backtest = RB(quotes = quotes, 
                      risk_budget = input['RiskBudgets'],
                      vol_lookback_window = input['VolLookbackWindow'], 
                      vol_lookback_offset = input['VolLookbackOffset'], 
                      rebal_freq = input['RebalFreq'], 
                      ignore_missing = input['IgnoreMissing']).get_backtest() 

        return render_template('constructorDisplay.html', 
                                labels = list(backtest.index.strftime('%d-%m-%Y').values), 
                                values = list(backtest.values), 
                                errors = errors)
    else:
        return render_template('constructor.html', 
                               render_inputs = render_inputs_current)

