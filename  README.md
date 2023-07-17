# Flask Portfolio Constructor 
#### Video Demo:  <URL HERE>

Portfolio Constructor is a Flask application designed to construct and backtest equity portfolios.

## Introduction 

The app allows the user to construct backtests for equity-portfolios using a range construction techniques. The user can select desired tickers as well as additional paramaters (such as volatility look-back window) to get customized results. The app plots the resultant backtest along with some financial metrics (e.g. Sharpe Ratio) and let's the user export a csv file with the time-series for further analysis. 

All financial data is provided by Yahoo Finance. Each time a backtest is constructed the quotes are parsed from Yahoo using 'requests' library and are then cached in a database for future use (to avoid donwloading the same data multiple times for different requests).

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
* static/ : contains the frontend stylesheet file
* templates/ : contains the frontend HTML files

## app.py 

Flask application instance is initiated inside app.py file, with route() decorators triggering functions for the following URLs: '/', '/about', 'constructor', '/constructorIV' and '/constructorRB'. All routes() accept HTTP 'GET' requests to generate URLs by rendering corresponding html templates. '/constructorXX' routes() support both 'GET' and 'POST' methods. 

Database management is implemented using Flask-SQLAlchemy extension. The SQLite database is configured via SQLALCHEMY_DATABASE_URI key and app is initilaised with the SQLAlchemy extension. 

## backtest/

Base _Backtest class is defined inside backtest.py. The non-public class takes single argument 'quotes' of type pandas.DataFrame and is used to define common functions shared among all backtests. In particular, .get_backtest() method returns final time-series for the backtest. 

All backtests inherite the _Backtest behaviour and are defined inside backtests.py file. Some take additional arguments. Main distinguisher between the backtests is the get_weights(self) method that is used to calculate backtest weights using a specific technique (e.g. inverse-volatility weights).

Metrics class is defined inside the metrics.py file and is used to further analise backtests by calculating a range of financial 'metrics' (Sharpe Ratio etc.).

## database/

SQLAlchemy extension is created inside db.py file.

## input/

check_input.py file contains functions used to check user input submitted via 'POST' for different backtests. 

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

TO DO

## static/

Contains the stylesheet style.css that is linked to the layout.html template.

## templates/ 

TO DO