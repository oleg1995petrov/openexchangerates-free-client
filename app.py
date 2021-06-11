import datetime
from models import Grabber
from db_settings import connection, cursor


def main():
    API_KEY = 'Your API key'
    DATE = '2021-06-11'

    grb = Grabber(API_KEY)
    rates, ts = grb.historical(DATE)  # or grb.latest() 
    date = datetime.datetime.utcfromtimestamp(ts).date()
    query = """INSERT INTO exchange_rates (currency, rate, date) VALUES (%s, %s, %s)"""
    
    for curr, rate in rates.items():
        cursor.execute(query, (curr, rate, date))

    if connection:
        connection.commit()
        cursor.close()
        connection.close()
