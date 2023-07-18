from sqlalchemy import func
from datetime import timedelta
import pandas as pd

from quotes.get_yahoo import add_yahoo
from database.db import db
from models.Quotes import Quotes

def get_quotes(tickers, start, end):
    """ 
    get_quotes() collects quotes for tickers: checks if quotes already exist in Quotes, adds missing quotes to Quotes from Yahoo Finance and returns pandas.DataFrame with all quotes.
    type: (str[], datetime, datetime) -> (pandas.DataFrame/None, str[])
    
    :param tickers: list of tickers type: str[] (e.g. ['MSFT', 'AAPL'])
    :param start: start date, type: datetime 
    :param end: end date, type: datetime
    :return: pandas.DataFrame with quotes for tickers between start and end dates/None if no data collected, list of errors
    """

    bcal = pd.bdate_range(start = start, end = end - timedelta(days = 1)) # business day calendar 
    quotes = pd.DataFrame(index = bcal) # return pandas.DataFrame
    errors = []

    # For every requested ticker
    for ticker in tickers:
        # Add missing data to Quotes (if any)
        status, error = add_missing(ticker = ticker, start = start, end = end)
        errors += error

        # If add_missing successful, try to collect all quotes from Quotes
        if status == True:
            try:  
                # Execute query for the ticker 
                subquery = db.select(Quotes.date, Quotes.quote).where((Quotes.ticker == ticker) & (Quotes.date >= start) & (Quotes.date <= end))
                query = db.session.execute(subquery).fetchall()

                # Create DataFrame with data from query 
                quote = pd.DataFrame(query, columns = ['Date', ticker])
                quote['Date'] = pd.to_datetime(quote['Date'])
                quote.set_index('Date', inplace = True)

                # Concat quote with return DataFrame
                quotes = pd.concat([quotes, quote], axis=1)

            except:
                errors += [f"Failed to collect data from database for: {ticker}"]

    if len(quotes.columns) == 0: # if no data was collected, return None, errors
        return None, errors
    
    else:
        return quotes, errors # else return pandas.DataFrame, errors
        

def add_missing(ticker, start, end):
    """ 
    add_missing() adds missing quotes to Quotes using add_yahoo() module.
    type: (str, datetime, datetime) -> (Bool, str[])
    
    :param ticker: ticker type: str (e.g. 'MSFT')
    :param start: start date, type: datetime 
    :param end: end date, type: datetime
    :return: True if successful (including when no data had to be added)/False otherwise, list of errors
    """
        
    # Get minimum and maximum dates in Quotes for the ticker 
    min_date, max_date = get_dbdates(ticker = ticker)
    
    # If no min_date add all quotes
    if min_date == None or max_date == None:
        return add_yahoo(ticker = ticker, start = start, end = end)

    else: 
        # Declare status and errors placeholders
        status_start, status_end = True, True
        errors_start, errors_end = [], []

        # If start is before min_date add missing quotes before min_date
        if start < min_date:
            status_start, errors_start = add_yahoo(ticker = ticker, start = start, end = min_date - timedelta(days = 1))

        # If end is after max_date add missing quotes after max_date
        if end > max_date + timedelta(days = 1):
            status_end, errors_end = add_yahoo(ticker = ticker, start = max_date + timedelta(days = 1), end = end)

        return all([status_start, status_end]), errors_start + errors_end


def get_dbdates(ticker):
    """ 
    get_dbdates() gets min and max date for quotes stored in Quotes for the ticker.
    type: (str) -> (str, str)/(None, None)
    
    :param ticker: ticker, type: str (e.g. 'MSFT')
    :return: minumum date / None, maximum date / None, type: str, str
    """

    try:
        subquery = db.select(db.func.min(Quotes.date), db.func.max(Quotes.date)).where(Quotes.ticker == ticker)
        query = db.session.execute(subquery)#.scalars()
        dates = list(query)[0]

    except:
        dates = [None, None]

    return dates[0], dates[1]