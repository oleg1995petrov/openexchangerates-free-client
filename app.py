import os

from argparse import ArgumentParser
from datetime import datetime
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import execute_values

from models import Client


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-t', '--type', default='latest', 
                        choices=['latest', 'historical'])
    parser.add_argument('-y', '--year')
    parser.add_argument('-m', '--month', type=int)
    parser.add_argument('-d', '--day', type=int)
    parser.add_argument('-c', '--currencies', nargs='+')
    args = parser.parse_args()
    return args


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    connection = connect(database=os.getenv('DB'),
                         user=os.getenv('DB_USER'),
                         password=os.getenv('DB_PASSWORD'),
                         host=os.getenv('DB_HOST'),
                         port=os.getenv('DB_PORT')) 
    client = Client(os.getenv('API_KEY'))
    args = get_args()
    rates, ts = client.get(args)

    sql_to_create = """CREATE TABLE IF NOT EXISTS exchange_rates (
                           id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                           currency VARCHAR(3) NOT NULL,
                           rate NUMERIC NOT NULL,
                           date TIMESTAMP NOT NULL)"""
    sql_to_insert = "INSERT INTO exchange_rates (currency, rate, date) VALUES %s"

    date = datetime.utcfromtimestamp(ts).date()
    data = [(currency, rate, date) for currency, rate in rates.items()]

    with connection as conn:
        cursor = conn.cursor()
        with cursor as cur:
            cur.execute(sql_to_create)
            execute_values(cur, sql_to_insert, data)
