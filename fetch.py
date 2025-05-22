
import requests
import os
from dotenv import load_dotenv
from db import Database
import pandas as pd
from datetime import datetime
import psycopg2

class Fetch():
    def __init__(self, db=None):
        self.db = db

    # Fetch last 100 5-minute interval datapoints for the stock #
    def fetch_stocks(self, symbol, store=False):

        load_dotenv()
        api_key = os.getenv("API_KEY")
        URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey={api_key}'
        # URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'

        time_series_data = None

        try:
            response = requests.get(URL)
            response.raise_for_status()  # will raise an HTTPError for bad responses (e.g., 4xx, 5xx)
            time_series_data = response.json()['Time Series (5min)']
    
        except requests.exceptions.RequestException as e:
            print("Issues accessing API data:", e)
            return

        except KeyError:
            print("Expected key not found in the response JSON")
            return
        
        if store:

            try:
                conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                port="5432",
                user="jmgiorgi",
                password="riverplate10"
                )
                cur = conn.cursor()
            except psycopg2.Error as e:
                print("Database connection failed:", e)

            for timestamp, values in time_series_data.items():

                open = values["1. open"]
                high = values["2. high"]
                low = values["3. low"]
                close = values["4. close"]
                volume = values["5. volume"]
                
                # import pdb; pdb.set_trace()
                sql0 = """
                INSERT INTO Stocks (name, open, high, low, close, volume, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql0, (symbol, open, high, low, close, volume, timestamp))
                conn.commit()

            data_frame = pd.DataFrame(time_series_data)
            data_frame = data_frame.transpose()
            features = ['1. open', '2. high', '3. low', '4. close', '5. volume']
            return data_frame[features]

      

        



