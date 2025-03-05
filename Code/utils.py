import pandas as pd
from dateutil.relativedelta import relativedelta


class WorkWithDataFrame:

    def __init__(self, stock_tickers_path, company_valuations_path):
        self.PATH_TO_SAVE_STOCK_TICKERS = stock_tickers_path
        self.PATH_TO_SAVE_COMPANY_VALUATIONS = company_valuations_path

        self.TODAY = pd.Timestamp.today().date()
        self.DATE_SIX_MONTHS_BEFORE = self.TODAY - relativedelta(months=6)

        self.COMPANY_VALUATION_COLUMNS = {
            "stock_ticker": "string",
            "company_name": "string",
            "current_share_price": "float64",
            "desired_price_cash_yield": "float64",
            "desired_price_epv": "float64",
            "max_price_to_pay": "float64",
            "ideal_price_with_mos": "float64",
            "cash_yield_at_ideal_price": "float64",
            "book_value_per_share": "float64",
            "effective_tax_rate": "float64",
            "return_on_capital_employed_ratio": "float64",
            "gross_profit_points": "float64",
            "operating_income_points": "float64",
            "operating_cash_conversion_ratio": "float64",
            "depreciation_to_operating_cash_flow_ratio": "float64",
            "inventory_and_stock_ratio": "float64",
            "debtor_ratio": "float64",
            "capex_ratio": "float64",
            "capex_to_depreciation_ratio": "float64",
            "cash_return_on_capital_invested_ratio": "float64",
            "free_cash_flow_per_share": "float64",
            "free_cash_flow_per_share_and_eps_difference_score": "int64",
            "company_issues_dividend": "string",
            "free_cash_flow_dividend_cover_ratio": "float64",
            "debt_to_free_cash_flow_ratio": "float64",
            "debt_to_net_operating_cash_flow_ratio": "float64",
            "debt_to_assets_ratio": "float64",
            "interest_cover_ratio": "float64",
            "owner_earnings": "float64",
            "owner_earnings_per_share": "float64",
            "cash_interest_rate": "float64",
        }


    def open_or_create_valuation_csv_file(self, file_path) -> pd.DataFrame:

        try:
            csv_file_as_df = pd.read_csv(
                file_path,
                dtype=self.COMPANY_VALUATION_COLUMNS,
                sep=";",
                decimal=","
            )

        except FileNotFoundError:
            csv_file_as_df = pd.DataFrame({
                col: pd.Series(dtype=dtype) for col, dtype in self.COMPANY_VALUATION_COLUMNS.items()
            })

        finally:
            if "date_created" not in csv_file_as_df.columns:
                csv_file_as_df.insert(loc=0, column = "date_created", value=None)

            csv_file_as_df["date_created"] = pd.to_datetime(csv_file_as_df["date_created"]).dt.date

            return csv_file_as_df


    def stock_not_present_or_too_old_valuation(
        self, stock_ticker: str, company_valuation_df: pd.DataFrame
    ) -> bool:

        try:
            last_date_calculated = company_valuation_df.loc[company_valuation_df["stock_ticker"] == stock_ticker, "date_created"].iloc[0]
            last_date_calculated = pd.Timestamp(last_date_calculated).date()

            if last_date_calculated < self.DATE_SIX_MONTHS_BEFORE:
                return True
            else:
                return False
        except IndexError:
            return True


    def add_valuation_to_dataframe(
        self,
        stock_ticker: str,
        company_name: str,
        company_valuations: pd.DataFrame,
        values_dict: dict,
        current_share_price: float
    ) -> pd.DataFrame:

        values_dict["date_created"] = self.TODAY
        values_dict["stock_ticker"] = stock_ticker
        values_dict["company_name"] = company_name
        values_dict["current_share_price"] = current_share_price

        # First, check if DataFrame is empty
        if stock_ticker not in company_valuations["stock_ticker"].dropna().values:
            company_valuations = pd.concat([company_valuations, pd.DataFrame([values_dict])], ignore_index=True)
        else:
            # Locate the row that matches the conditions
            row_for_stock = (company_valuations["stock_ticker"] == stock_ticker)

            if company_valuations.loc[row_for_stock].empty:
                company_valuations = pd.concat([company_valuations, pd.DataFrame([values_dict])], ignore_index=True)
            else:
                update_dict_rows = { company_valuations.index[company_valuations["stock_ticker"]== stock_ticker].tolist()[0]: values_dict }

                for idx, values in update_dict_rows.items():
                    company_valuations.loc[idx] = values

        return company_valuations


    def save_dataframe_as_csv_file(
        self, dataframe: pd.DataFrame, path_to_save_file
    ):
        dataframe.to_csv(
            path_to_save_file,
            sep=";",
            decimal=',',
            encoding="utf-8",
            index=False,
            header=True
        )


class CleanData:

    def keep_common_financial_reports(
        self,
        income_statements: pd.DataFrame,
        balance_sheets: pd.DataFrame,
        cash_flow_statements: pd.DataFrame,
        dividends: dict
    ):
        # Find the common dates across all DataFrames
        common_dates = set(income_statements["date"]) & set(balance_sheets["date"]) & set(cash_flow_statements["date"])

        # Sort common dates in descending order (newest to oldest)
        sorted_common_dates = sorted(common_dates, reverse=True)

        # Determine the maximum number of shared dates (smallest dataset)
        max_common_dates = min(len(income_statements), len(balance_sheets), len(cash_flow_statements))

        # Keep only the top max_common_dates most recent dates
        final_dates = sorted_common_dates[:max_common_dates]
        final_years = []

        for date in final_dates:
            final_years.append(int(date[:4]))

        # Filter DataFrames (and dividends dict)
        income_statements = income_statements[income_statements['date'].isin(final_dates)]
        balance_sheets = balance_sheets[balance_sheets['date'].isin(final_dates)]
        cash_flow_statements = cash_flow_statements[cash_flow_statements['date'].isin(final_dates)]
        dividends = { key: value for key, value in dividends.items() if key in final_years }

        return income_statements, balance_sheets, cash_flow_statements, dividends