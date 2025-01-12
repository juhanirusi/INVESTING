from fetch_data import FetchFinancialData
from functions import FunctionsToRun

fetch_financial_data = FetchFinancialData()
functions = FunctionsToRun()


###########################################################

STOCK_TICKER = "AAPL"
CURRENT_SHARE_PRICE = 0

###########################################################


if __name__ == "__main__":

    fmp_income_statements = fetch_financial_data.fetch_income_statements_from_fmp(stock_ticker=STOCK_TICKER)
    fmp_balance_sheets = fetch_financial_data.fetch_balance_sheets_from_fmp(stock_ticker=STOCK_TICKER)
    fmp_cash_flows = fetch_financial_data.fetch_cash_flow_statements_from_fmp(stock_ticker=STOCK_TICKER)

    functions.book_value_per_share(fmp_income_statements, fmp_balance_sheets)
    print("\n")
    functions.company_effective_tax_rate(fmp_income_statements)
    print("\n")
    functions.operating_cash_conversion_ratio(fmp_income_statements, fmp_cash_flows)