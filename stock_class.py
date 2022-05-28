import os
import requests
import pandas as pd
from io import StringIO


class Stock():


    alpha_key = "OYLIQKP442QFEAPI"
    base_url = 'https://www.alphavantage.co/query?'


    def __init__(self, symbol):
        """
        Initializer function for a stock object
        """

        self.symbol = symbol
        self.monthly_data = self.get_monthly_data()


    def get_monthly_data(self, datatype = "csv", verify = False):
        """
        Method to retrieve monthly stock data from Alpha Vantage API
        """

        # define paramaters
        params =  {'function': 'TIME_SERIES_MONTHLY',
         'symbol': self.symbol,
		 'datatype': datatype,
		 'apikey': Stock.alpha_key}

        # retrieve data from API
        response = requests.get(Stock.base_url, params=params, verify = verify)

        # put the data in string format
        string_data = str(response.content, "utf-8")
        data = StringIO(string_data)

        # convert data into a dataframe
        df = pd.read_csv(data)

        # get necessary columns
        df["stock"] = [self.symbol] * len(df)
        df["month"] = df["timestamp"].apply(lambda d: d.month)

        return df


    @property
    def symbol(self):
        return self._symbol


    @symbol.setter
    def symbol(self, value):
        assert type(value) == str, f"{value} is not a string, please check the value"
        self._symbol = value