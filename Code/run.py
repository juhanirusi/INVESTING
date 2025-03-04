import time

from calculate_ratios_and_value import CalculateRatiosAndCompanyValue
from fetch_data import FetchFinancialData
from functions import CalculationsToMake
from utils import CleanData, WorkWithDataFrame

###########################################################

ANALYZE_ONE_COMPANY = False

STOCK_TICKER = "ALSN"
CURRENT_SHARE_PRICE = 101.00

MINIMUM_CASH_YIELD = 0.08 # USE AT LEAST 5%
INTEREST_RATE = 0.0457 # 4.57% (Average U.S. 10 Year Treasury Yield)
MARGIN_OF_SAFETY = 0.15 # 15%

PATH_TO_SAVE_STOCK_TICKERS = r"C:\Users\juhan\OneDrive\Omat Tiedostot\GitHub\INVESTING\Code\Data\stock_tickers.csv"
PATH_TO_SAVE_COMPANY_VALUATIONS = r"C:\Users\juhan\OneDrive\Omat Tiedostot\GitHub\INVESTING\Code\Data\company_valuations.csv"

"""
MINIMUM_CASH_YIELD --> Risk Mitigation: A higher starting
cash yield reduces the reliance on future growth,
lowering investment risk.

Large and less risky companies --> 7% to 9%

Smaller and more risky --> 10% to 12%

Very small and very risky --> 15% or more
"""

###########################################################

work_with_dataframe = WorkWithDataFrame(
    stock_tickers_path=PATH_TO_SAVE_STOCK_TICKERS,
    company_valuations_path=PATH_TO_SAVE_COMPANY_VALUATIONS
)
clean_data = CleanData()

fetch_financial_data = FetchFinancialData()
functions = CalculationsToMake(analyze_one_company=ANALYZE_ONE_COMPANY)
calculate_ratios_and_value = CalculateRatiosAndCompanyValue()

###########################################################


if __name__ == "__main__":

    stock_tickers = fetch_financial_data.fetch_stock_tickers_into_csv_file()
    work_with_dataframe.save_dataframe_as_csv_file(
        stock_tickers,
        PATH_TO_SAVE_STOCK_TICKERS
    )

    if not ANALYZE_ONE_COMPANY:

        company_valuations = work_with_dataframe.open_or_create_valuation_csv_file(
            PATH_TO_SAVE_COMPANY_VALUATIONS
        )

        for _, stock in stock_tickers.iterrows():

            if work_with_dataframe.stock_not_present_or_too_old_valuation(
                stock["symbol"], company_valuations
            ):
                fmp_income_statements = fetch_financial_data.fetch_income_statements_from_fmp(stock_ticker=stock["symbol"])
                fmp_balance_sheets = fetch_financial_data.fetch_balance_sheets_from_fmp(stock_ticker=stock["symbol"])
                fmp_cash_flows = fetch_financial_data.fetch_cash_flow_statements_from_fmp(stock_ticker=stock["symbol"])

                dividends = fetch_financial_data.fetch_dividend_history_data_from_fmp(stock_ticker=stock["symbol"])

                # Skip this company if they don't have financial statements
                if fmp_income_statements.empty or fmp_balance_sheets.empty or fmp_cash_flows.empty:
                    continue

                fmp_income_statements, fmp_balance_sheets, fmp_cash_flows, dividends = clean_data.keep_common_financial_reports(
                    income_statements=fmp_income_statements,
                    balance_sheets=fmp_balance_sheets,
                    cash_flow_statements=fmp_cash_flows,
                    dividends=dividends
                )

                calculate_ratios_and_value.financial_statements_and_constants(
                    income_statements=fmp_income_statements,
                    balance_sheets=fmp_balance_sheets,
                    cash_flow_statements=fmp_cash_flows,
                    dividend_history=dividends,
                    analyze_one_company=ANALYZE_ONE_COMPANY,
                    stock_price=stock["price"],
                    minimum_cash_yield=MINIMUM_CASH_YIELD,
                    interest_rate=INTEREST_RATE,
                    margin_of_safety=MARGIN_OF_SAFETY
                )

                values_dict = calculate_ratios_and_value.calculate_ratios(functions)

                company_valuations = work_with_dataframe.add_valuation_to_dataframe(
                    stock_ticker=stock["symbol"],
                    company_name=stock["name"],
                    company_valuations=company_valuations,
                    values_dict=values_dict,
                    current_share_price=stock["price"]
                )

                work_with_dataframe.save_dataframe_as_csv_file(
                    company_valuations,
                    PATH_TO_SAVE_COMPANY_VALUATIONS,
                )

                time.sleep(0.1) # <-- Just in case to stay under FMP API limit

            else:
                continue

    else:

        fmp_income_statements = fetch_financial_data.fetch_income_statements_from_fmp(stock_ticker=STOCK_TICKER)
        fmp_balance_sheets = fetch_financial_data.fetch_balance_sheets_from_fmp(stock_ticker=STOCK_TICKER)
        fmp_cash_flows = fetch_financial_data.fetch_cash_flow_statements_from_fmp(stock_ticker=STOCK_TICKER)

        dividends = fetch_financial_data.fetch_dividend_history_data_from_fmp(stock_ticker=STOCK_TICKER)

        fmp_income_statements, fmp_balance_sheets, fmp_cash_flows, dividends = clean_data.keep_common_financial_reports(
            income_statements=fmp_income_statements,
            balance_sheets=fmp_balance_sheets,
            cash_flow_statements=fmp_cash_flows,
            dividends=dividends
        )

        calculate_ratios_and_value.financial_statements_and_constants(
            income_statements=fmp_income_statements,
            balance_sheets=fmp_balance_sheets,
            cash_flow_statements=fmp_cash_flows,
            dividend_history=dividends,
            analyze_one_company=ANALYZE_ONE_COMPANY,
            stock_price=CURRENT_SHARE_PRICE,
            minimum_cash_yield=MINIMUM_CASH_YIELD,
            interest_rate=INTEREST_RATE,
            margin_of_safety=MARGIN_OF_SAFETY
        )

        calculate_ratios_and_value.calculate_ratios(functions)
