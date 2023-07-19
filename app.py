import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')

from flask import Flask, request, redirect, render_template
from flask_session import Session

from backtest.backtest_run import backtest_run
from backtest.metrics import Metrics
from database.db import db
from input.check_input import check_input
from input.format_input import format_input
from quotes.get_quotes import get_quotes
from render_input.render_input import render_input


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
    return render_template('index.html',
                           render_input = render_input)


@app.route('/backtest')
def backtest():
    # Render default backtest
    return render_template('backtest.html', 
                            render_input = render_input)


@app.route('/backtest/<path:backtest>', methods=['GET', 'POST'])
def backtest_all(backtest):
    route = f'/backtest/{backtest}'

    # Redirect to /backtest if non-active route requested
    if route not in render_input['active_routes']:
        return redirect('/backtest')
    
    # Copy render input with current backtest as selected backtest
    _render_input = render_input.copy()
    _render_input['selected_backtest'] = backtest
    
    if request.method == 'POST':
        # Check user input
        user_input_check, user_input_errors = check_input(user_input = request.form, render_input = _render_input)
 
        # If input is invalid
        if user_input_check == False:
            return render_template('backtest.html', 
                                   render_input = _render_input,
                                   errors = user_input_errors)
        
        # Format user input
        formated_user_input, format_input_errors = format_input(user_input = request.form, render_input = _render_input)
        print(formated_user_input)
        # If could not format user input
        if formated_user_input is None:
            return render_template('backtest.html', 
                                   render_input = _render_input,
                                   errors = format_input_errors)
        
        # Get quotes
        quotes, quotes_errors = get_quotes(tickers = formated_user_input['Ticker'], 
                                            start = formated_user_input['StartDate'] , 
                                            end = formated_user_input['EndDate']) 

        # If failed to get any quotes
        if quotes is None:
            return render_template('backtest.html', 
                                   render_input = _render_input,
                                   errors = quotes_errors)

        # Create backtest instance
        backtest, backtest_errors = backtest_run(user_input = formated_user_input, render_input = _render_input, quotes = quotes)

        # If failed to construct backtest
        if backtest is None:
            return render_template('backtest.html', 
                                   render_input = _render_input,
                                   errors = backtest_errors)
        
        # Time series for backtest 
        backtest_ts = backtest.get_backtest() 
        backtest_metrics = Metrics(quotes).get_all()

        # Render backtestDisplay template to show backtest
        return render_template('backtestDisplay.html', 
                                render_input = _render_input,
                                errors = quotes_errors,
                                labels = list(backtest_ts.index.strftime('%d-%m-%Y').values), 
                                values = list(backtest_ts.values), 
                                metrics = backtest_metrics)

    else: # if request.method == 'GET':
        return render_template('backtest.html',
                               render_input = _render_input)

app.run(debug=True)