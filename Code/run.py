from fetch_data import FetchFinancialData
from functions import FunctionsToRun

fetch_financial_data = FetchFinancialData()
functions = FunctionsToRun()


###########################################################

STOCK_TICKER = "DFS"
CURRENT_SHARE_PRICE = 222.70
MINIMUM_CASH_YIELD = 0.08 # USE AT LEAST 5%

"""
MINIMUM_CASH_YIELD --> Risk Mitigation: A higher starting
cash yield reduces the reliance on future growth,
lowering investment risk.

Large and less risky companies --> 7% to 9%

Smaller and more risky --> 10% to 12%

Very small and very risky --> 15% or more
"""

###########################################################


if __name__ == "__main__":

    fmp_income_statements = fetch_financial_data.fetch_income_statements_from_fmp(stock_ticker=STOCK_TICKER)
    fmp_balance_sheets = fetch_financial_data.fetch_balance_sheets_from_fmp(stock_ticker=STOCK_TICKER)
    fmp_cash_flows = fetch_financial_data.fetch_cash_flow_statements_from_fmp(stock_ticker=STOCK_TICKER)

    # dividends = fetch_financial_data.fetch_dividend_history_data_from_fmp(stock_ticker=STOCK_TICKER)

    # functions.book_value_per_share(fmp_income_statements, fmp_balance_sheets)
    print("\n")
    company_tax_rates = functions.company_effective_tax_rate(fmp_income_statements)
    # print("\n")
    # roce = functions.return_on_capital_employed_ratio(fmp_income_statements, fmp_balance_sheets)
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
    # print("\n")
    # free_cash_flow_per_share = functions.free_cash_flow_per_share(fmp_income_statements, fmp_cash_flows)
    # print("\n")
    # functions.free_cash_flow_per_share_and_eps_difference_score(fmp_income_statements, free_cash_flow_per_share, roce)
    # print("\n")
    # functions.free_cash_flow_dividend_cover_ratio(free_cash_flow_per_share, dividends)

    # Debt

    # print("\n")
    # functions.debt_to_free_cash_flow_ratio(fmp_balance_sheets, fmp_cash_flows)
    # print("\n")
    # functions.debt_to_net_operating_cash_flow_ratio(fmp_balance_sheets, fmp_cash_flows)
    # print("\n")
    # functions.debt_to_assets_ratio(fmp_balance_sheets)
    # print("\n")
    # functions.interest_cover_ratio(fmp_income_statements)

    # Valuing A Company's Shares

    print("\n")
    owner_earnings = functions.owner_earnings(fmp_income_statements, fmp_cash_flows)
    print("\n")
    cash_interest_rate = functions.calculate_cash_interest_rate(owner_earnings, CURRENT_SHARE_PRICE)
    print("\n")
    desired_price_cash_yield = functions.calculate_desired_price_with_cash_yield(owner_earnings, MINIMUM_CASH_YIELD)
    print("\n")
    desired_price_epv = functions.calculate_desired_price_with_epv(
        fmp_income_statements, fmp_balance_sheets, fmp_cash_flows,
        company_tax_rates, MINIMUM_CASH_YIELD
    )


# FIX THE REPORT DATES TO BE IN CORRECT ORDER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
