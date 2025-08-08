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
        self.STOCK_EXCHANGES = ["NASDAQ", "NYSE", "HEL", "STO", "OSL", "CPH", "XETRA", "TSX"]

    def fetch_income_statements_from_fmp(self, stock_ticker) -> pd.DataFrame:

        try:
            URL = f"{self.FMP_BASE_URL}/income-statement/{stock_ticker}"

            income_statements = requests.get(URL, params={"period": self.DATA_PERIOD, "apikey": self.FMP_API_KEY}).json()

            income_statements = pd.DataFrame(data=income_statements)

            income_statements = income_statements.sort_values(by="date")
        except KeyError:
            income_statements = pd.DataFrame()
        finally:
            return income_statements


    def fetch_balance_sheets_from_fmp(self, stock_ticker) -> pd.DataFrame:

        try:
            URL = f"{self.FMP_BASE_URL}/balance-sheet-statement/{stock_ticker}"

            balance_sheets = requests.get(URL, params={"period": self.DATA_PERIOD, "apikey": self.FMP_API_KEY}).json()

            balance_sheets = pd.DataFrame(data=balance_sheets)

            balance_sheets = balance_sheets.sort_values(by="date")
        except KeyError:
            balance_sheets = pd.DataFrame()
        finally:
            return balance_sheets


    def fetch_cash_flow_statements_from_fmp(self, stock_ticker) -> pd.DataFrame:

        URL = f"{self.FMP_BASE_URL}/cash-flow-statement/{stock_ticker}?period={self.DATA_PERIOD}&apikey={self.FMP_API_KEY}"

        try:
            cash_flow_statements = requests.get(URL).json()

            cash_flow_statements = pd.DataFrame(data=cash_flow_statements)

            cash_flow_statements = cash_flow_statements.sort_values(by="date")
        except:
            cash_flow_statements = pd.DataFrame()
        finally:
            return cash_flow_statements


    def fetch_historical_stock_price_data_from_fmp(self, stock_ticker) -> pd.DataFrame:

        try:
            URL = f"{self.FMP_BASE_URL}/historical-price-full/{stock_ticker}?apikey={self.FMP_API_KEY}"

            historical_stock_price_data = requests.get(URL).json()

            historical_stock_price_data = pd.json_normalize(historical_stock_price_data, record_path=["historical"])

            historical_stock_price_data = historical_stock_price_data.sort_values(by="date")
        except KeyError:
            historical_stock_price_data = pd.DataFrame()
        finally:
            return historical_stock_price_data


    def fetch_dividend_history_data_from_fmp(self, stock_ticker) -> dict:

        try:
            URL = f"{self.FMP_BASE_URL}/historical-price-full/stock_dividend/{stock_ticker}?apikey={self.FMP_API_KEY}"

            dividend_history_data = requests.get(URL).json()

            dividend_history_data = pd.json_normalize(dividend_history_data, record_path=["historical"])
        except:
            dividend_history_data = pd.DataFrame()
        finally:
            if not dividend_history_data.empty:

                dividend_history_data["dividend_year"] = pd.to_datetime(dividend_history_data["paymentDate"]).dt.year.astype("Int64")

                dividend_history_data = dividend_history_data[["dividend", "dividend_year"]]

                dividend_history_data = dividend_history_data.groupby(["dividend_year"])["dividend"].sum().reset_index()

                dividend_history_data = dividend_history_data.set_index("dividend_year")["dividend"].to_dict()
                dividend_history_data = { int(key): value for key, value in dividend_history_data.items() }

            else:
                return {}

        return dividend_history_data


    def fetch_stock_tickers_into_csv_file(self) -> pd.DataFrame:

        URL = f"{self.FMP_BASE_URL}/stock/list"

        stock_tickers = requests.get(URL, params={"apikey": self.FMP_API_KEY}).json()

        stock_tickers = pd.DataFrame(data=stock_tickers)

        stock_tickers = stock_tickers.loc[stock_tickers["exchangeShortName"].isin(self.STOCK_EXCHANGES)]
        stock_tickers = stock_tickers.loc[stock_tickers["type"] == "stock"]
        stock_tickers = stock_tickers.sort_values(by="symbol", ascending=True)

        stock_tickers = stock_tickers[["symbol", "name", "price", "exchangeShortName"]]

        stock_tickers = stock_tickers.loc[stock_tickers["symbol"] != "NA"]

        return stock_tickers