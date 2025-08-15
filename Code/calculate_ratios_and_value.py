from functions import CalculationsToMake


class CalculateRatiosAndCompanyValue:

    def financial_statements_and_constants(
        self,
        income_statements,
        balance_sheets,
        cash_flow_statements,
        historical_stock_price_data,
        dividend_history,
        analyze_one_company,
        stock_price,
        minimum_cash_yield,
        interest_rate,
        margin_of_safety
    ):
        self.INCOME_STATEMENTS = income_statements
        self.BALANCE_SHEETS = balance_sheets
        self.CASH_FLOW_STATEMENTS = cash_flow_statements
        self.HISTORICAL_STOCK_PRICE_DATA = historical_stock_price_data
        self.DIVIDEND_HISTORY = dividend_history
        self.ANALYZE_ONE_COMPANY = analyze_one_company
        self.STOCK_PRICE = stock_price
        self.MINIMUM_CASH_YIELD = minimum_cash_yield
        self.INTEREST_RATE = interest_rate
        self.MARGIN_OF_SAFETY = margin_of_safety

    def calculate_ratios(self, functions: CalculationsToMake):

        historical_returns = functions.historical_returns(
            historical_stock_price_data=self.HISTORICAL_STOCK_PRICE_DATA
        )
        book_value_per_share = functions.book_value_per_share(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )
        effective_tax_rates, company_effective_tax_rate = functions.company_effective_tax_rate(
            self.INCOME_STATEMENTS
        )
        return_on_capital_employed_ratios, roce = functions.return_on_capital_employed_ratio(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )
        gross_profit_points, operating_income_points = functions.rising_earnings_through_time(
            self.INCOME_STATEMENTS
        )

        #########################################################################
        # A operating cash conversion ratio of at least 100% and a depreciation
        # to operating cash flow ratio of under 30% make for a good compination

        operating_cash_conversion_ratio = functions.operating_cash_conversion_ratio(
            self.INCOME_STATEMENTS, self.CASH_FLOW_STATEMENTS
        )
        depreciation_to_operating_cash_flow_ratio = functions.depreciation_to_operating_cash_flow_ratio(
            self.CASH_FLOW_STATEMENTS
        )

        #########################################################################

         # Manufacturing & Retail Companies...
        inventory_and_stock_ratio = functions.inventory_and_stock_ratio(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )

        debtor_ratio = functions.debtor_ratio(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )

        capex_ratio = functions.capex_ratio(self.CASH_FLOW_STATEMENTS)

        capex_to_depreciation_ratio = functions.capex_to_depreciation_ratio(
            self.INCOME_STATEMENTS, self.CASH_FLOW_STATEMENTS
        )

        cash_return_on_capital_invested_ratio = functions.cash_return_on_capital_invested_ratio(
            self.BALANCE_SHEETS, self.CASH_FLOW_STATEMENTS
        )

        free_cash_flows_per_share, free_cash_flow_per_share = functions.free_cash_flow_per_share(
            self.INCOME_STATEMENTS, self.CASH_FLOW_STATEMENTS
        )

        free_cash_flow_per_share_and_eps_difference_score = functions.free_cash_flow_per_share_and_eps_difference_score(
            self.INCOME_STATEMENTS,
            free_cash_flows_per_share,
            return_on_capital_employed_ratios
        )

        # If company issues a dividend calculate the free cash flow
        # dividend cover ratio, else set it to zero...

        if bool(self.DIVIDEND_HISTORY):
            free_cash_flow_dividend_cover_ratio = functions.free_cash_flow_dividend_cover_ratio(
                free_cash_flows_per_share, self.DIVIDEND_HISTORY
            )
            company_issues_dividend = "Yes"
        else:
            free_cash_flow_dividend_cover_ratio = 0.00
            company_issues_dividend = "No"

        # Debt

        debt_to_free_cash_flow_ratio = functions.debt_to_free_cash_flow_ratio(
            self.BALANCE_SHEETS, self.CASH_FLOW_STATEMENTS
        )

        debt_to_net_operating_cash_flow_ratio = functions.debt_to_net_operating_cash_flow_ratio(
            self.BALANCE_SHEETS, self.CASH_FLOW_STATEMENTS
        )

        debt_to_assets_ratio = functions.debt_to_assets_ratio(self.BALANCE_SHEETS)

        interest_cover_ratio = functions.interest_cover_ratio(self.INCOME_STATEMENTS)

        # Valuing A Company's Shares

        owner_earnings = functions.owner_earnings(
            self.INCOME_STATEMENTS, self.CASH_FLOW_STATEMENTS
        )

        cash_interest_rate = functions.calculate_cash_interest_rate(
            owner_earnings, self.STOCK_PRICE
        )

        desired_price_cash_yield = functions.calculate_desired_price_with_cash_yield(
            owner_earnings, self.MINIMUM_CASH_YIELD
        )

        desired_price_epv = functions.calculate_desired_price_with_epv(
            self.INCOME_STATEMENTS,
            self.BALANCE_SHEETS,
            self.CASH_FLOW_STATEMENTS,
            effective_tax_rates,
            self.MINIMUM_CASH_YIELD
        )

        maximum_and_ideal_prices = functions.calculate_maximum_and_ideal_prices(
            owner_earnings, self.INTEREST_RATE, self.MARGIN_OF_SAFETY
        )


        if not self.ANALYZE_ONE_COMPANY:

            company_effective_tax_rate = round(company_effective_tax_rate * 100, 2)

            ratios = {
                "desired_price_cash_yield": desired_price_cash_yield,
                "desired_price_epv": desired_price_epv,
                "max_price_to_pay": maximum_and_ideal_prices["maximum_price"],
                "ideal_price_with_mos": maximum_and_ideal_prices["ideal_price"],
                "cash_yield_at_ideal_price": maximum_and_ideal_prices["cash_yield_ideal_price"],
                "total_return": historical_returns["total_return"],
                "total_return_as_percentage": historical_returns["total_return_as_percentage"],
                "compound_annual_growth_rate": historical_returns["compound_annual_growth_rate"],
                "last_number_years_of_data": historical_returns["last_number_years_of_data"],
                "book_value_per_share": book_value_per_share,
                "effective_tax_rate": company_effective_tax_rate,
                "return_on_capital_employed_ratio": roce,
                "gross_profit_points": gross_profit_points,
                "operating_income_points": operating_income_points,
                "operating_cash_conversion_ratio": operating_cash_conversion_ratio,
                "depreciation_to_operating_cash_flow_ratio": depreciation_to_operating_cash_flow_ratio,
                "inventory_and_stock_ratio": inventory_and_stock_ratio,
                "debtor_ratio": debtor_ratio,
                "capex_ratio": capex_ratio,
                "capex_to_depreciation_ratio": capex_to_depreciation_ratio,
                "cash_return_on_capital_invested_ratio": cash_return_on_capital_invested_ratio,
                "free_cash_flow_per_share": free_cash_flow_per_share,
                "free_cash_flow_per_share_and_eps_difference_score": free_cash_flow_per_share_and_eps_difference_score,
                "company_issues_dividend": company_issues_dividend,
                "free_cash_flow_dividend_cover_ratio": free_cash_flow_dividend_cover_ratio,
                "debt_to_free_cash_flow_ratio": debt_to_free_cash_flow_ratio,
                "debt_to_net_operating_cash_flow_ratio": debt_to_net_operating_cash_flow_ratio,
                "debt_to_assets_ratio": debt_to_assets_ratio,
                "interest_cover_ratio": interest_cover_ratio,
                "owner_earnings": owner_earnings["owner_earnings"],
                "owner_earnings_per_share": owner_earnings["owner_earnings_per_share"],
                "cash_interest_rate": cash_interest_rate
            }

            return ratios
