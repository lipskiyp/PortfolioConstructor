'''
THINGS TO ADD:

Display interface + data export 
Get Quotes Tab
Methodology
Metrics
'''

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')

from flask import Flask, request, redirect, render_template, abort
from flask_session import Session

from backtest.backtest_run import backtest_run
from input.check_input import *
from input.format_input import format_input
from database.db import db
from quotes.get_quotes import get_quotes
from backtest.metrics import Metrics
from render_input import render_input


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
    return render_template('index.html',
                           render_input = render_input)


@app.route('/about')
def about():
    quotes, errors = get_quotes(tickers = ['MSFT'], start = datetime.strptime('2023-06-01', '%Y-%m-%d'), end = datetime.strptime('2023-07-01', '%Y-%m-%d'))
    print(errors)
    print(quotes)
    metrics = Metrics(quotes)
    print(metrics.get_maxdd())
    return render_template('index.html',
                           render_input = render_input)


@app.route('/constructor')
def constructor():
    # Render default constructor
    return render_template('constructor.html', 
                            render_input = render_input)


@app.route('/constructor/<path:constructor>', methods=['GET', 'POST'])
def constructor_all(constructor):
    route = f'/constructor/{constructor}'

    # Redirect to /constructor if non-active route requested
    if route not in render_input['active_routes']:
        return redirect('/constructor')
    
    # Copy render input with current constructor as selected constructor
    _render_input = render_input.copy()
    _render_input['selected_constructor'] = constructor
    
    if request.method == 'POST':
        # Check user input
        check, errors = check_input(user_input = request.form, render_input = _render_input)
 
        # If input is invalid
        if check == False:
            return render_template('constructor.html', 
                                   render_input = _render_input,
                                   errors = errors)
        
        # Format user input
        formated_user_input, errors = format_input(user_input = request.form, render_input = _render_input)
        
        # If could not format user input
        if formated_user_input is None:
            return render_template('constructor.html', 
                                   render_input = _render_input,
                                   errors = errors)
        
        # Get quotes
        quotes, quotes_errors = get_quotes(tickers = formated_user_input['Ticker'], 
                                            start = formated_user_input['StartDate'] , 
                                            end = formated_user_input['EndDate']) 

        # If failed to get any quotes
        if quotes is None:
            return render_template('constructor.html', 
                                   render_input = _render_input,
                                   errors = quotes_errors)

        # Execute backtest
        backtest, errors = backtest_run(user_input = formated_user_input, render_input = _render_input, quotes = quotes)

        # If failed to construct backtest
        if backtest is None:
            return render_template('constructor.html', 
                                   render_input = _render_input,
                                   errors = errors)
        
        # Time series for backtest 
        backtest_ts = backtest.get_backtest() 

        # Render constructorDisplay template to show backtest
        return render_template('constructorDisplay.html', 
                                render_input = _render_input,
                                labels = list(backtest_ts.index.strftime('%d-%m-%Y').values), 
                                values = list(backtest_ts.values), 
                                errors = quotes_errors)   

    else: # if request.method == 'GET':
        return render_template('constructor.html',
                               render_input = _render_input)
