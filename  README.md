# Flask Portfolio Constructor 
#### Video Demo:  <URL HERE>

Portfolio Constructor is a Flask application designed to construct and backtest equity portfolios.

## Introduction 

The app allows the user to construct backtests for equity-portfolios using a range construction techniques. The user can select desired tickers as well as additional paramaters (such as volatility look-back window) to get customized results. The app plots the resultant backtest along with some financial metrics (e.g. Sharpe Ratio) and let's the user export a csv file with the time-series for further analysis. 

All financial data is provided by Yahoo Finance. Each time a backtest is constructed the quotes are parsed using Yahoo Finance API with 'requests' library and are cached in a database for future use (to avoid donwloading the same data multiple times for different requests).

The 'About' page contains detailed methodologies for metrics and every construction technique.

## Installation

Use the package manager pip3:

```bash
$ pip3 install -r requirements.txt
```

## Overview 

* app.py : contains the Flask app
* backtest/ : contains the backend Python modules for backtest construction
* database/ : contains the SQLAlchemy extension creation
* input/ : contains the backend Python modules for user input checks
* instance/ : contains the database instance 
* models/ : contains the database model class definition 
* quotes/ : contains backend Python modules for data queiries 
* render_input/ : contains backened Python modules for input rendering
* static/ : contains the frontend stylesheet file
* templates/ : contains the frontend HTML files

## app.py 

Flask application instance is initiated inside app.py file. All routes() accept HTTP 'GET' requests to generate URLs by rendering corresponding html templates. '/constructor/' route() supports both 'GET' and 'POST' methods. 

Database management is implemented using Flask-SQLAlchemy extension. The SQLite database is configured via SQLALCHEMY_DATABASE_URI key and app is initilaised with the SQLAlchemy extension. 

## backtest/

Base _Backtest class is defined inside backtest.py. The non-public class takes single argument 'quotes' of type pandas.DataFrame and is used to define common functions shared among all backtests. In particular, .get_backtest() method returns final time-series for the backtest. 

All backtests inherite the _Backtest behaviour and are defined inside backtests.py file. Some take additional arguments. Main distinguisher between the backtests is the get_weights(self) method that is used to calculate backtest weights using a specific technique (e.g. inverse-volatility weights).

Metrics class is defined inside the metrics.py file and is used to further analise backtests by calculating a range of financial 'metrics' (Sharpe Ratio etc.).

## database/

SQLAlchemy extension is created inside db.py file.

## input/

check_input() module inside check_input.py checks user input for all 'shown' fields for selected constructor. The module returns True/False if all user input is valid/invalid, as well as a list of errors. checks.py file contains all insidvidual checks for every user input. 

format_input() module inside format_input.py file formats user input from str to required format for all 'shown' fields for selected constructor. The module returns dict with all formatted inputs/None if user input was formatted/faile to format, as a list of errors.

## instance/

Database quotes.db is used to store all quotes from previous requests, with the following .schema:

CREATE TABLE quotes (  
        id INTEGER NOT NULL,  
        date_added DATETIME,  
        date DATETIME NOT NULL,  
        ticker VARCHAR NOT NULL,  
        quote FLOAT NOT NULL,  
        PRIMARY KEY (id)  
);

## models/

Model class Quotes is defined inside Quotes.py file.

## quotes/

get_quotes() module inside the get_quotes.py file returns pandas.DataFrame object with historical quotes for selected tickers and date range. Every time get_quotes() module is called, add_missing() module checks if some of the requested quotes already exist inside the database. It then uses add_yahoo() module to add missing quotes to the database (if any). Once the missing data is added, get_quotes() module collects all of the data from the database and returns it to the user along with a list of errors. 

add_yahoo() module inside get_yahoo.py file calls get_yahoo() module to parse financial time series from Yahoo Finance for a given ticker. If the data is parsed successfully, add_yahoo() adds the requested data to the database. 

## render_input/

render_input dictionary stores parameters used to render the dynamic constructor.html template. 

portfolio_size: determines the maximum number of tickers allowed in the portfolio (limits the number of inputs when the template is rendered)
portfolio_checked: determines the number of tickers pre-checked (selected) when the template is rendered
selected_constructor: determines the constructor for which the template is rendered (set to constructorFW as default)
active_constructors: determines the constructors accessible to the user 
active_routes: determines allowed routes for '/constructor/<route>' URLs
active_inputs: determines which inputs are shown for a selected constructor when the template is rendered

NB Only user inputs that are 'shown' inside active_inputs will be checked and formatted when check_input() and format_input() modules are called.

## static/

Contains the stylesheet style.css that is linked to the layout.html template.

## templates/ 

All html templates extend layout.html, which set the general layout of the page and contains the navigation bar. 

constructor.html is a dynamic template used to display constructors. The template takes two arguments: render_input and errors. render_input determined the user inputs to be shown for a given constructor. Errors dispalys errors from a list below the navigation bar. 

constructorDisplay.html template is used to display the backtest timeseries using chart.js as well as a table for financial metrcis. The template takes five arguments: render_input, errors, labels, values and metrics. 