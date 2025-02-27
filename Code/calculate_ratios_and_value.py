from functions import FunctionsToRun


class CalculateRatiosAndCompanyValue:

    def financial_statements(
        self,
        income_statements,
        balance_sheets,
        cash_flow_statements,
        analyze_one_company
    ):
        self.INCOME_STATEMENTS = income_statements
        self.BALANCE_SHEETS = balance_sheets
        self.CASH_FLOW_STATEMENTS = cash_flow_statements
        self.ANALYZE_ONE_COMPANY = analyze_one_company

    def calculate_ratios(self, functions: FunctionsToRun):
        book_value_per_share = functions.book_value_per_share(self.INCOME_STATEMENTS, self.BALANCE_SHEETS, self.ANALYZE_ONE_COMPANY)

        if not self.ANALYZE_ONE_COMPANY:

            ratios = {
                "book_value_per_share": book_value_per_share
            }

            return ratios