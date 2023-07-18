# Flask Portfolio Constructor 
#### Video Demo:  <URL HERE>

Portfolio Constructor is a Flask application designed to construct and backtest equity portfolios.

## Introduction 

The app can be used to construct and backtest equity-portfolios using a range portfolio-construction techniques. Any ticker available on Yahoo Finance can be added to the portfolio and the backtest parameters (such as volatility lookback-window) can be manually adjusted. 

The resultant time-series is plotted inside the app using chart.js along with some financial metrics (e.g. Sharpe Ratio). The app let's the user export a csv file with the time-series for further analysis. 

All financial data is provided by Yahoo Finance, whcih is parsed from Yahoo Finance API.

The 'About' page contains detailed methodologies for the construction techniques and the metrics.

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
* quotes/ : contains the backend Python modules for data queiries 
* render_input/ : contains the parameters for template rendering
* static/ : contains the frontend stylesheet file
* templates/ : contains the frontend HTML files

## app.py 

Flask application instance is initiated inside the app.py file. All routes() accept HTTP 'GET' requests to generate URLs by rendering corresponding html templates. '/constructor/' route() supports both, 'GET' and 'POST' methods. 

Database management is implemented using Flask-SQLAlchemy extension. The SQLite database is configured via SQLALCHEMY_DATABASE_URI key and app is initialised with the SQLAlchemy extension. 

## backtest/

Base _Backtest class is defined inside the backtest.py file. The non-public class takes a single argument 'quotes' of type pandas.DataFrame and defines common features shared among the portfolio-construction techniques. In particular, .get_backtest() method returns the time-series for the backtest. 

All backtests inherite the _Backtest behaviour and are defined inside backtests.py file. Some take additional arguments. Main distinguisher between the portfolio-constructors (i.e. backtests) is the get_weights(self) method that is used to calculate backtest weights using a specific technique (e.g. inverse-volatility weights).

Metrics class is defined inside the metrics.py file and is used provide further analysis on the time-series.

## database/

SQLAlchemy extension is created inside db.py file.

## input/

check_input() module inside the check_input.py file checks all 'shown' user input fields given a selected constructor. The module returns True/False if all of the user inputs are valid/invalid, as well as a list of errors incurred during the check. checks.py file contains all of the insidvidual 'check' modules for every user input. 

format_input() module inside the format_input.py file formats the user input from str to a required format for all all 'shown' user input fields given a selected constructor. The module returns dict with all of the formatted inputs/None if user input was formatted successfully/failed to format, as well as a list of errors incurred during the formatting.

## instance/

Database quotes.db is used to store all quotes from the previous get_quotes() requests (see below). Database has the following .schema:

CREATE TABLE quotes (  
        id INTEGER NOT NULL,  
        date_added DATETIME,  
        date DATETIME NOT NULL,  
        ticker VARCHAR NOT NULL,  
        quote FLOAT NOT NULL,  
        PRIMARY KEY (id)  
);

## models/

Model class Quotes is defined inside the Quotes.py file.

## quotes/

get_quotes() module inside the get_quotes.py file returns pandas.DataFrame object with the historical quotes for the selected tickers and date range. Every time get_quotes() module is called, add_missing() module checks if some of the requested quotes already exist inside the database. It then uses add_yahoo() module to add missing quotes to the database (if any). Once the missing quotes have been added, get_quotes() module collects all of the data from the database and returns it to the user along with the list of errors inccurred in the process. 

add_yahoo() module inside the get_yahoo.py file calls the get_yahoo() module to parse financial time series from the Yahoo Finance API for a given ticker. If the data is parsed successfully, add_yahoo() adds the requested data to the database and returns True/False if successfull/ussuccessfull as well as a list of errors inccurred in the process.

## render_input/

render_input dictionary stores the parameters used to render the dynamic constructor.html template. 

portfolio_size: determines the maximum number of tickers allowed in the portfolio (limits the number of 'ticker' inputs shown when the template is rendered)
portfolio_checked: determines the number of tickers pre-checked (selected) when the template is rendered
selected_constructor: determines the constructor for which the template is rendered (set to constructorFW as default)
active_constructors: determines the constructors accessible to the user 
active_routes: determines the allowed routes for '/constructor/<route>' URLs
active_inputs: determines which inputs are shown for a selected constructor when the template is rendered

NB Only user inputs that are 'shown' inside the active_inputs dict will be checked and formatted when check_input() and format_input() modules are called.

## static/

Contains the stylesheet style.css that is linked to the layout.html template.

## templates/ 

All of the html templates extend layout.html, which sets the general layout of the app and contains the navigation bar. 

constructor.html is a dynamic template used to display input menue for the constructors. The template takes two arguments: render_input and errors. render_input determined the user inputs to be shown for a given constructor. Errors dispalys all of the errors incurred in the process of preparing and running the backtest below the navigation bar. 

constructorDisplay.html template is used to display the backtest timeseries using chart.js, as well as a table of financial metrcis for the backtest. The template takes five arguments: render_input, errors, labels, values and metrics. 