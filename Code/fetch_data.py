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