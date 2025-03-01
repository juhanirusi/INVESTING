from functions import CalculationsToMake


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

    def calculate_ratios(self, functions: CalculationsToMake):

        book_value_per_share = functions.book_value_per_share(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )
        company_effective_tax_rate = functions.company_effective_tax_rate(
            self.INCOME_STATEMENTS
        )
        roce = functions.return_on_capital_employed_ratio(
            self.INCOME_STATEMENTS, self.BALANCE_SHEETS
        )

        if not self.ANALYZE_ONE_COMPANY:

            ratios = {
                "book_value_per_share": book_value_per_share,
                "effective_tax_rate": (company_effective_tax_rate * 100),
                "return_on_capital_employed_ratio": roce
            }

            return ratios
