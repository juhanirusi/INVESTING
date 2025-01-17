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

    # functions.book_value_per_share(fmp_income_statements, fmp_balance_sheets)
    # print("\n")
    # company_tax_rates = functions.company_effective_tax_rate(fmp_income_statements)
    # print("\n")
    roce = functions.return_on_capital_employed_ratio(fmp_income_statements, fmp_balance_sheets)
    # print("\n")
    # functions.rising_earnings_through_time(fmp_income_statements)
    # print("\n")

    #########################################################################
    # A operating cash conversion ratio of at least 100% and a depreciation
    # to operating cash flow ratio of under 30% make for a good compination

    # functions.operating_cash_conversion_ratio(fmp_income_statements, fmp_cash_flows)
    # print("\n")
    # functions.depreciation_to_operating_cash_flow_ratio(fmp_cash_flows)
    #########################################################################

    # print("\n")
    # functions.inventory_and_stock_ratio(fmp_income_statements, fmp_balance_sheets) # <-- Manufacturing & Retail Companies
    # print("\n")
    # functions.debtor_ratio(fmp_income_statements, fmp_balance_sheets)
    # print("\n")
    # functions.capex_ratio(fmp_cash_flows)
    # print("\n")
    # functions.capex_to_depreciation_ratio(fmp_income_statements, fmp_cash_flows)
    # print("\n")
    # functions.cash_return_on_capital_invested_ratio(fmp_balance_sheets, fmp_cash_flows)
    print("\n")
    free_cash_flow_per_share = functions.free_cash_flow_per_share(fmp_income_statements, fmp_cash_flows)
    print("\n")
    functions.free_cash_flow_per_share_and_eps_difference_score(fmp_income_statements, free_cash_flow_per_share, roce)
