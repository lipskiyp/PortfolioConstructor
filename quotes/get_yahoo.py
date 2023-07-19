import csv
from datetime import datetime, timezone
import requests 
import uuid
 
from database.db import db
from models.Quotes import Quotes


def add_yahoo(ticker, start, end):
    """ 
    add_yahoo() adds quotes for the ticker to database using get_yahoo().
    type: (str, datetime, datetime) -> (Bool, str[])
    
    :param ticker: ticker type: str (e.g. 'MSFT')
    :param start: start date, type: datetime  
    :param end: end date, type: datetime
    :return: True if successful/False otherwise, list of erros
    """
    
    # List to store all errors
    errors = [] 

    # Requests historical data
    quotes = get_yahoo(ticker = ticker, start = start, end = end)

    if quotes == None:
        errors += [f'Failed to request Yahoo data for: {ticker}']
        return False, errors
    
    for quote in quotes:
        try:
            query = Quotes(date = datetime.strptime(quote['Date'], '%Y-%m-%d'), ticker = ticker, quote = quote['Adj Close'])
            db.session.add(query)
            db.session.commit()
        except:
            errors += [f"failed to add quote for {ticker} on {quote['Date']}"]
    return True, errors


def get_yahoo(ticker, start, end):
    """ 
    get_yahoo() requests historical data for a ticker from Yahoo Finance: https://finance.yahoo.com
    type: (str, datetime, datetime) -> List[Dict]
    
    :param ticker: ticker type: str (e.g. 'MSFT')
    :param start: start date, type: datetime 
    :param end: end date, type: datetime
    :return: List[Dict]; None if API Query unsuccessful 

    NB Yahoo API does not include quotes for end date 
    Inspired by: https://cs50.harvard.edu/x/2023/psets/9/finance/ 
    """

    # Prepare Yahoo Finance API request
    ticker = ticker.upper()
    start = int(start.replace(tzinfo=timezone.utc).astimezone(tz=None).timestamp())
    end =  int(end.replace(tzinfo=timezone.utc).astimezone(tz=None).timestamp()) 
    interval = '1d'
    url = (f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval={interval}&events=history")

    # Query
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()
        DictReader_object = csv.DictReader(response.content.decode("utf-8").splitlines())
        return list(DictReader_object) 

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None