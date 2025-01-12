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
