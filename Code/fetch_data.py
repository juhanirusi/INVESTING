import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

class FetchFinancialData:

    def __init__(self):
        self.FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
        self.FMP_API_KEY = os.getenv("FMP_API_KEY")
        self.DATA_PERIOD = "annual"


    def fetch_income_statements_from_fmp(self, stock_ticker):

        URL = f"{self.FMP_BASE_URL}/income-statement/{stock_ticker}"

        income_statements = requests.get(URL, params={"period": self.DATA_PERIOD, "apikey": self.FMP_API_KEY}).json()

        income_statements = pd.DataFrame(data=income_statements)

        income_statements = income_statements.sort_values(by="date")

        print(income_statements.columns)

        return income_statements


    def fetch_balance_sheets_from_fmp(self, stock_ticker):

        URL = f"{self.FMP_BASE_URL}/balance-sheet-statement/{stock_ticker}"

        balance_sheets = requests.get(URL, params={"period": self.DATA_PERIOD, "apikey": self.FMP_API_KEY}).json()

        balance_sheets = pd.DataFrame(data=balance_sheets)

        balance_sheets = balance_sheets.sort_values(by="date")

        print(balance_sheets.columns)

        return balance_sheets


    def fetch_cash_flow_statements_from_fmp(self, stock_ticker):

        URL = f"{self.FMP_BASE_URL}/cash-flow-statement/{stock_ticker}?period={self.DATA_PERIOD}&apikey={self.FMP_API_KEY}"

        cash_flow_statements = requests.get(URL).json()

        cash_flow_statements = pd.DataFrame(data=cash_flow_statements)

        cash_flow_statements = cash_flow_statements.sort_values(by="date")

        print(cash_flow_statements.columns)

        return cash_flow_statements


    def fetch_dividend_history_data_from_fmp(self, stock_ticker):

        URL = f"{self.FMP_BASE_URL}/historical-price-full/stock_dividend/{stock_ticker}?apikey={self.FMP_API_KEY}"

        dividend_history_data = requests.get(URL).json()

        dividend_history_data = pd.json_normalize(dividend_history_data, record_path=["historical"])

        dividend_history_data["dividend_year"] = pd.to_datetime(dividend_history_data["paymentDate"]).dt.year.astype("Int64")

        dividend_history_data = dividend_history_data[["dividend", "dividend_year"]]

        dividend_history_data = dividend_history_data.groupby(["dividend_year"])["dividend"].sum().reset_index()

        dividend_history_data = dividend_history_data.set_index("dividend_year")["dividend"].to_dict()
        dividend_history_data = {int(key): value for key, value in dividend_history_data.items()}

        print(dividend_history_data)

        return dividend_history_data
