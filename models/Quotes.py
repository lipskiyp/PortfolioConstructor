from datetime import datetime
import pytz

from database.db import db

# Define model class Quotes
class Quotes(db.Model):
    __table_args__ = (db.UniqueConstraint('ticker', 'date'), ) # restrict duplicated quotes 
    id = db.Column(db.Integer, primary_key=True) # quote id
    date_added = db.Column(db.DateTime, default = datetime.now(pytz.timezone('US/Eastern'))) # current US/Eastern time 
    date = db.Column(db.DateTime, nullable=False) # quote date
    ticker = db.Column(db.String, nullable=False) # ticker
    quote = db.Column(db.Float, nullable=False) # quote 