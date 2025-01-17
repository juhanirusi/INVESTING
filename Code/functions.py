import pandas as pd


class FunctionsToRun:


    def book_value_per_share(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ) -> dict:

        book_values_per_share = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            shareholders_equity = balance_sheet["totalStockholdersEquity"]
            weighted_average_shares_outstanding = income_statement["weightedAverageShsOutDil"]

            report_date = income_statement["date"]

            bvps = shareholders_equity / weighted_average_shares_outstanding

            book_values_per_share[report_date] = bvps

            print(f"Book Value Per Share (for year - {report_date}) ==> ${bvps:.2f}")

        return book_values_per_share


    def company_effective_tax_rate(self, fmp_income_statements: pd.DataFrame) -> dict:

        effective_tax_rates = {}

        for index, row in fmp_income_statements.iterrows():

            income_before_tax = row["incomeBeforeTax"]
            income_tax_expense = row["incomeTaxExpense"]

            report_date = row["date"]

            company_effective_tax_rate = (income_tax_expense / income_before_tax) * 100

            effective_tax_rates[report_date] = company_effective_tax_rate

            print(f"Effective Tax Rate (for year - {report_date}) ==> {company_effective_tax_rate:.2f} %")

        return effective_tax_rates


    def rising_earnings_through_time(self, fmp_income_statements: pd.DataFrame):

        gross_profit_growth_years = 0
        operating_income_growth_years = 0

        total_years = len(fmp_income_statements) - 1  # Total possible growth years

        # Calculate year-over-year growth

        for i in range(1, len(fmp_income_statements)):

            if fmp_income_statements.iloc[i]["grossProfit"] > fmp_income_statements.iloc[i-1]["grossProfit"]:
                gross_profit_growth_years += 1

            if fmp_income_statements.iloc[i]["operatingIncome"] > fmp_income_statements.iloc[i-1]["operatingIncome"]:
                operating_income_growth_years += 1

        # Assign points proportionally to the number of years with growth
        gross_profit_points = (gross_profit_growth_years / total_years) * 10
        operating_income_points = (operating_income_growth_years / total_years) * 10

        # Print results, rounded to 2 decimal places
        print(f"Gross Profit Points: {round(gross_profit_points, 2)} / 10")
        print(f"Operating Income Points: {round(operating_income_points, 2)} / 10")


    def operating_cash_conversion_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ) -> dict:

        operating_cash_conversion_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_cash_flow_statements.iterrows()
        )

        for (_, income_statement), (_, cash_flow_statement) in financial_statements:

            operating_profit = income_statement["operatingIncome"] # EBIT
            operating_cash_flow = cash_flow_statement["operatingCashFlow"]

            report_date = income_statement["date"]

            occr = (operating_cash_flow / operating_profit) * 100

            operating_cash_conversion_ratios[report_date] = occr

            print(f"Operating Cash Conversion Ratio (for year - {report_date}) ==> {occr:.2f} %")

        return operating_cash_conversion_ratios


    def depreciation_to_operating_cash_flow_ratio(self, fmp_cash_flow_statements: pd.DataFrame) -> dict:

        """
        'Depreciation to Operating Cash Flow Ratio' is calculated
        because some (capital intensive) companies have high
        'Operating Cash Conversion Ratio's', which falsely
        showcases them as hugely successful companies.

        ---------------------------------------------------------------------

        Less than 30% is good / acceptable, because some companies are
        really capital intensive and they might own a lot of capital assets
        like property, plant, equipment, machinery, etc, so a ratio higher
        than 30% means that over 30% of the operating cash flow will have
        to be spent maintaining assets !!!
        """

        depreciation_to_operating_cash_flow_ratios = {}

        for index, row in fmp_cash_flow_statements.iterrows():

            depreciation_and_amortization = row["depreciationAndAmortization"]
            operating_cash_flow = row["operatingCashFlow"]

            report_date = row["date"]

            dtocfr = (depreciation_and_amortization / operating_cash_flow) * 100

            depreciation_to_operating_cash_flow_ratios[report_date] = dtocfr

            print(f"Depreciation to Operating Cash Flow Ratio (for year - {report_date}) ==> {dtocfr:.2f} %")

        return depreciation_to_operating_cash_flow_ratios


    def inventory_and_stock_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ) -> dict:

        """
        Inventory and stock ratio compares the value of inventory against
        the company's revenue (turnover) to assess how much of the
        company's revenue is tied up in inventory.
        """

        inventory_and_stock_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            revenue = income_statement["revenue"] # Turnover
            inventory = balance_sheet["inventory"] # Stock

            report_date = income_statement["date"]

            sr = (inventory / revenue) * 100

            inventory_and_stock_ratios[report_date] = sr

            print(f"Operating Cash Conversion Ratio (for year - {report_date}) ==> {sr:.2f} %")

        return inventory_and_stock_ratios


    def debtor_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ) -> dict:

        debtor_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            net_receivables = balance_sheet["netReceivables"] # Trade Debtors (also known as Accounts Receivable)
            revenue = income_statement["revenue"] # Turnover

            report_date = income_statement["date"]

            dr = (net_receivables / revenue) * 100

            debtor_ratios[report_date] = dr

            print(f"Debtor Ratio (for year - {report_date}) ==> {dr:.2f} %")

        return debtor_ratios


    def capex_ratio(self, fmp_cash_flow_statements: pd.DataFrame) -> dict:

        """
        A low Capex ratio (typically below 30%) suggests that the company
        isn't heavily reliant on reinvesting its cash to maintain or grow
        operations. This is often a characteristic of high-quality
        companies with efficient operations and high
        returns on capital.
        """

        capex_ratios = {}

        for index, row in fmp_cash_flow_statements.iterrows():

            capital_expenditure = row["capitalExpenditure"]
            operating_cash_flow = row["operatingCashFlow"]

            report_date = row["date"]

            cr = (capital_expenditure / operating_cash_flow) * 100

            capex_ratios[report_date] = cr

            print(f"Capex Ratio (for year - {report_date}) ==> {cr:.2f} %")

        return capex_ratios


    def capex_to_depreciation_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ) -> dict:

        """
        Comparing this ratio with industry peers and historical data can
        offer deeper insights into a company's investment strategy and
        financial health. An optimal ratio (>= 100%), along with a rising
        ROCE, can signal that the company is poised for sustainable
        growth and enhanced free cash flow generation.

        ON FMP, THE capex NUMBER IS TREATED AS A NEGATIVE NUMBER ON THE
        CASH FLOW STATEMENT, SO NOTE THAT IN OUR CODE, NEGATIVE NUMBERS
        THAT ARE OVER 100% ARE ACTUALLY A GOOD THING !!!
        """

        capex_to_depreciation_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_cash_flow_statements.iterrows()
        )

        for (_, income_statement), (_, cash_flow_statement) in financial_statements:

            capital_expenditure = cash_flow_statement["capitalExpenditure"]
            depreciation_and_amortization = income_statement["depreciationAndAmortization"]

            report_date = income_statement["date"]

            ctdr = (capital_expenditure / depreciation_and_amortization) * 100

            capex_to_depreciation_ratios[report_date] = ctdr

            print(f"Capex to Depreciation Ratio (for year - {report_date}) ==> {ctdr:.2f} %")

        return capex_to_depreciation_ratios