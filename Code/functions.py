import pandas as pd


class CalculationsToMake:

    def __init__(self, analyze_one_company):
        self.ANALYZE_ONE_COMPANY = analyze_one_company


    def historical_returns(
        self, historical_stock_price_data: pd.DataFrame
    ) -> dict:

        """
        With this function, we calculate the cash and percentage
        return on investment of a specific stock and it's compound
        annual growth rate (CAGR) over the period of time
        that the stock price data has.
        """

        historical_stock_returns_dict = {}

        try:
            historical_stock_price_data["date"] = pd.to_datetime(historical_stock_price_data["date"])

            historical_stock_price_data = historical_stock_price_data.sort_values("date")

            initial_price = historical_stock_price_data["close"].iloc[0]
            final_price = historical_stock_price_data["close"].iloc[-1]
            start_date = historical_stock_price_data["date"].iloc[0]
            end_date = historical_stock_price_data["date"].iloc[-1]

            years = (end_date - start_date).days / 365.25

            total_return = final_price - initial_price
            percent_return = (total_return / initial_price) * 100
            cagr = ((final_price / initial_price) ** (1 / years) - 1) * 100

            historical_stock_returns_dict["total_return"] = round(total_return, 2)
            historical_stock_returns_dict["total_return_as_percentage"] = round(percent_return, 2)
            historical_stock_returns_dict["compound_annual_growth_rate"] = round(cagr, 2)

        except KeyError:
            historical_stock_returns_dict["total_return"] = None
            historical_stock_returns_dict["total_return_as_percentage"] = None
            historical_stock_returns_dict["compound_annual_growth_rate"] = None

        finally:
            if self.ANALYZE_ONE_COMPANY:
                print(f"Return ($): {total_return:.2f}")
                print(f"Return (%): {percent_return:.2f}%")
                print(f"Compound Annual Growth Rate (CAGR): {cagr:.2f}%")

            return historical_stock_returns_dict


    def book_value_per_share(
        self,
        fmp_income_statements: pd.DataFrame,
        fmp_balance_sheets: pd.DataFrame,
    ):
        book_values_per_share = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            shareholders_equity = balance_sheet["totalStockholdersEquity"]
            weighted_average_shares_outstanding = income_statement["weightedAverageShsOutDil"]

            report_date = income_statement["date"]

            try:
                bvps = shareholders_equity / weighted_average_shares_outstanding

                book_values_per_share[report_date] = bvps

            except ZeroDivisionError:
                book_values_per_share[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Book Value Per Share (for year - {report_date}) ==> ${bvps:.2f}")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest book value per share

            try:
                max_date = max(book_values_per_share.keys())
                book_value_per_share = book_values_per_share[max_date]
                book_value_per_share = round(book_value_per_share, 2)
            except ValueError:
                book_value_per_share = 0.00
            finally:
                return book_value_per_share

        return book_values_per_share


    def company_effective_tax_rate(self, fmp_income_statements: pd.DataFrame):

        effective_tax_rates = {}

        for _, row in fmp_income_statements.iterrows():

            income_before_tax = row["incomeBeforeTax"]
            income_tax_expense = row["incomeTaxExpense"]

            report_date = row["date"]

            try:
                company_effective_tax_rate = (income_tax_expense / income_before_tax)

                effective_tax_rates[report_date] = round(company_effective_tax_rate, 2)

                company_effective_tax_rate = company_effective_tax_rate * 100

            except ZeroDivisionError:
                effective_tax_rates[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Effective Tax Rate (for year - {report_date}) ==> {company_effective_tax_rate:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest effective tax rate

            try:
                max_date = max(effective_tax_rates.keys())
                effective_tax_rate = effective_tax_rates[max_date]
            except ValueError:
                effective_tax_rate = 0.00
            finally:
                return effective_tax_rates, effective_tax_rate

        return effective_tax_rates, None


    def return_on_capital_employed_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ):

        return_on_capital_employed_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            ebit = income_statement["operatingIncome"] # EBIT

            total_assets = balance_sheet["totalAssets"]
            current_liabilities = balance_sheet["totalCurrentLiabilities"]

            report_date = income_statement["date"]

            try:
                roce = ebit / (total_assets - current_liabilities) * 100

                return_on_capital_employed_ratios[report_date] = roce

            except ZeroDivisionError:
                return_on_capital_employed_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Return on Capital Employed Ratio (for year - {report_date}) ==> {roce:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest return on capital employed ratio

            try:
                max_date = max(return_on_capital_employed_ratios.keys())
                return_on_capital_employed_ratio = return_on_capital_employed_ratios[max_date]
                return_on_capital_employed_ratio = round(roce, 2)
            except ValueError:
                return_on_capital_employed_ratio = 0.00
            finally:
                return return_on_capital_employed_ratios, return_on_capital_employed_ratio

        return return_on_capital_employed_ratios, None


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

        try:
            gross_profit_points = (gross_profit_growth_years / total_years) * 10
        except ZeroDivisionError:
            gross_profit_points = 0

        try:
            operating_income_points = (operating_income_growth_years / total_years) * 10
        except ZeroDivisionError:
            operating_income_points = 0

        if self.ANALYZE_ONE_COMPANY:
            # Print results, rounded to 2 decimal places
            print(f"Gross Profit Points: {round(gross_profit_points, 2)} / 10")
            print(f"Operating Income Points: {round(operating_income_points, 2)} / 10")

            return None, None
        else:
            return round(gross_profit_points, 2), round(operating_income_points, 2)


    def operating_cash_conversion_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ):

        operating_cash_conversion_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_cash_flow_statements.iterrows()
        )

        for (_, income_statement), (_, cash_flow_statement) in financial_statements:

            operating_profit = income_statement["operatingIncome"] # EBIT
            operating_cash_flow = cash_flow_statement["operatingCashFlow"]

            report_date = income_statement["date"]

            try:
                occr = (operating_cash_flow / operating_profit) * 100

                operating_cash_conversion_ratios[report_date] = occr

            except ZeroDivisionError:
                operating_cash_conversion_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Operating Cash Conversion Ratio (for year - {report_date}) ==> {occr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest operating cash conversion ratio

            try:
                max_date = max(operating_cash_conversion_ratios.keys())
                operating_cash_conversion_ratio = operating_cash_conversion_ratios[max_date]
                operating_cash_conversion_ratio = round(operating_cash_conversion_ratio, 2)
            except ValueError:
                operating_cash_conversion_ratio = 0.00
            finally:
                return operating_cash_conversion_ratio

        return operating_cash_conversion_ratios


    def depreciation_to_operating_cash_flow_ratio(self, fmp_cash_flow_statements: pd.DataFrame):

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

        for _, row in fmp_cash_flow_statements.iterrows():

            depreciation_and_amortization = row["depreciationAndAmortization"]
            operating_cash_flow = row["operatingCashFlow"]

            report_date = row["date"]

            try:
                dtocfr = (depreciation_and_amortization / operating_cash_flow) * 100

                depreciation_to_operating_cash_flow_ratios[report_date] = dtocfr

            except ZeroDivisionError:
                depreciation_to_operating_cash_flow_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Depreciation to Operating Cash Flow Ratio (for year - {report_date}) ==> {dtocfr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest depreciation to operating cash flow ratio

            try:
                max_date = max(depreciation_to_operating_cash_flow_ratios.keys())
                depreciation_to_operating_cash_flow_ratio = depreciation_to_operating_cash_flow_ratios[max_date]
                depreciation_to_operating_cash_flow_ratio = round(depreciation_to_operating_cash_flow_ratio, 2)
            except ValueError:
                depreciation_to_operating_cash_flow_ratio = 0.00
            finally:
                return depreciation_to_operating_cash_flow_ratio

        return depreciation_to_operating_cash_flow_ratios


    def inventory_and_stock_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ):
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

            try:
                sr = (inventory / revenue) * 100

                inventory_and_stock_ratios[report_date] = sr

            except ZeroDivisionError:
                inventory_and_stock_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Inventory and Stock Ratio (for year - {report_date}) ==> {sr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest inventory and stock Ratio

            try:
                max_date = max(inventory_and_stock_ratios.keys())
                inventory_and_stock_ratio = inventory_and_stock_ratios[max_date]
                inventory_and_stock_ratio = round(inventory_and_stock_ratio, 2)
            except ValueError:
                inventory_and_stock_ratio = 0.00
            finally:
                return inventory_and_stock_ratio

        return inventory_and_stock_ratios


    def debtor_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_balance_sheets: pd.DataFrame
    ):

        debtor_ratios = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_balance_sheets.iterrows()
        )

        for (_, income_statement), (_, balance_sheet) in financial_statements:

            net_receivables = balance_sheet["netReceivables"] # Trade Debtors (also known as Accounts Receivable)
            revenue = income_statement["revenue"] # Turnover

            report_date = income_statement["date"]

            try:
                dr = (net_receivables / revenue) * 100

                debtor_ratios[report_date] = dr

            except ZeroDivisionError:
                debtor_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Debtor Ratio (for year - {report_date}) ==> {dr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest debtor ratio

            try:
                max_date = max(debtor_ratios.keys())
                debtor_ratio = debtor_ratios[max_date]
                debtor_ratio = round(debtor_ratio, 2)
            except ValueError:
                debtor_ratio = 0.00
            finally:
                return debtor_ratio

        return debtor_ratios


    def capex_ratio(self, fmp_cash_flow_statements: pd.DataFrame):

        """
        A low Capex ratio (typically below 30%) suggests that the company
        isn't heavily reliant on reinvesting its cash to maintain or grow
        operations. This is often a characteristic of high-quality
        companies with efficient operations and high
        returns on capital.
        """

        capex_ratios = {}

        for _, row in fmp_cash_flow_statements.iterrows():

            capital_expenditure = abs(row["capitalExpenditure"]) # Get absolute value (remove negative sign)
            operating_cash_flow = row["operatingCashFlow"]

            report_date = row["date"]

            try:
                cr = (capital_expenditure / operating_cash_flow) * 100

                capex_ratios[report_date] = cr

            except ZeroDivisionError:
                capex_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Capex Ratio (for year - {report_date}) ==> {cr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest CapEx ratio

            try:
                max_date = max(capex_ratios.keys())
                capex_ratio = capex_ratios[max_date]
                capex_ratio = round(capex_ratio, 2)
            except ValueError:
                capex_ratio = 0.00
            finally:
                return capex_ratio

        return capex_ratios


    def capex_to_depreciation_ratio(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ):

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

            capital_expenditure = abs(cash_flow_statement["capitalExpenditure"]) # Get absolute value (remove negative sign)
            depreciation_and_amortization = income_statement["depreciationAndAmortization"]

            report_date = income_statement["date"]

            try:
                ctdr = (capital_expenditure / depreciation_and_amortization) * 100
                capex_to_depreciation_ratios[report_date] = ctdr

            except ZeroDivisionError:
                capex_to_depreciation_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Capex to Depreciation Ratio (for year - {report_date}) ==> {ctdr:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest CapEx to Depreciation Ratio

            try:
                max_date = max(capex_to_depreciation_ratios.keys())
                capex_to_depreciation_ratio = capex_to_depreciation_ratios[max_date]
                capex_to_depreciation_ratio = round(capex_to_depreciation_ratio, 2)
            except ValueError:
                capex_to_depreciation_ratio = 0.00
            finally:
                return capex_to_depreciation_ratio

        return capex_to_depreciation_ratios


    def cash_return_on_capital_invested_ratio(
        self, fmp_balance_sheets: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ):

        """
        A Cash Return on Capital Invested of at least 10% indicates that
        the company is effectively converting capital into cash and is
        generating value for investors. It signals efficient
        management and healthy returns on investments.
        """

        cash_return_on_capital_invested_ratios = {}

        total_assets_last_year = None
        current_liabilities_last_year = None

        financial_statements = zip(
            fmp_balance_sheets.iterrows(), fmp_cash_flow_statements.iterrows()
        )

        for (_, balance_sheet), (_, cash_flow_statement) in financial_statements:

            if total_assets_last_year != None and current_liabilities_last_year != None:

                total_assets = balance_sheet["totalAssets"]
                current_liabilities = balance_sheet["totalCurrentLiabilities"]

                report_date = balance_sheet["date"]

                capital_employed = total_assets - current_liabilities
                capital_employed_last_year = total_assets_last_year - current_liabilities_last_year

                average_capital_employed = (capital_employed + capital_employed_last_year) / 2

                operating_cash_flow = cash_flow_statement["operatingCashFlow"]
                capital_expenditure = abs(cash_flow_statement["capitalExpenditure"]) # Get absolute value (remove negative sign)

                # Free Cash Flow to the Firm
                fcff = operating_cash_flow - capital_expenditure

                try:
                    croci = (fcff / average_capital_employed) * 100

                    cash_return_on_capital_invested_ratios[report_date] = croci

                except ZeroDivisionError:
                    cash_return_on_capital_invested_ratios[report_date] = 0.00

                finally:
                    if self.ANALYZE_ONE_COMPANY:
                        print(f"Cash Return on Capital Invested (for year - {report_date}) ==> {croci:.2f} %")

            total_assets_last_year = balance_sheet["totalAssets"]
            current_liabilities_last_year = balance_sheet["totalCurrentLiabilities"]

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Cash Return on Capital Invested ratio

            try:
                max_date = max(cash_return_on_capital_invested_ratios.keys())
                cash_return_on_capital_invested_ratio = cash_return_on_capital_invested_ratios[max_date]
                cash_return_on_capital_invested_ratio = round(cash_return_on_capital_invested_ratio, 2)
            except ValueError:
                cash_return_on_capital_invested_ratio = 0.00
            finally:
                return cash_return_on_capital_invested_ratio

        return cash_return_on_capital_invested_ratios


    def free_cash_flow_per_share(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ):

        free_cash_flows_per_share = {}

        financial_statements = zip(
            fmp_income_statements.iterrows(), fmp_cash_flow_statements.iterrows()
        )

        for (_, income_statement), (_, cash_flow_statement) in financial_statements:

            free_cash_flow = cash_flow_statement["freeCashFlow"]
            weighted_average_shares_outsanding = income_statement["weightedAverageShsOut"]

            report_date = income_statement["date"]

            try:
                fcfps = free_cash_flow / weighted_average_shares_outsanding

                free_cash_flows_per_share[report_date] = fcfps

            except ZeroDivisionError:
                free_cash_flows_per_share[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Free Cash Flow Per Share (for year - {report_date}) ==> ${fcfps:.2f}")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Free Cash Flow Per Share

            try:
                max_date = max(free_cash_flows_per_share.keys())
                free_cash_flow_per_share = free_cash_flows_per_share[max_date]
                free_cash_flow_per_share = round(free_cash_flow_per_share, 2)
            except ValueError:
                free_cash_flow_per_share = 0.00
            finally:
                return free_cash_flows_per_share, free_cash_flow_per_share

        return free_cash_flows_per_share, None


    def free_cash_flow_per_share_and_eps_difference_score(
        self,
        fmp_income_statements: pd.DataFrame,
        free_cash_flows_per_share: dict,
        roce: dict
    ):
        """
        1 --> EPS is negative - AVOID
        2 --> FCF per share is negative - AVOID
        3 --> Avoid, FCF per share is less than 80% of EPS and ROCE is falling.
        4 --> Maybe. FCF per share is less than 80% of EPS, but ROCE is increasing.
        5 --> YES, FCF per share is 80% or more of EPS.
        """

        fcfps_and_eps_difference_statuses = {}

        roce_previous = None

        score = None

        for _, row in fmp_income_statements.iterrows():

            if roce_previous != None:

                report_date = row["date"]

                eps = row["eps"]
                free_cash_flow_per_share = free_cash_flows_per_share.get(report_date)
                roce_current = roce.get(report_date)

                if eps <= 0:
                    score = 1
                else:
                    fcfps_to_eps_ratio = (free_cash_flow_per_share / eps) * 100

                    if fcfps_to_eps_ratio >= 80:
                        score = 5
                    elif fcfps_to_eps_ratio < 80:
                        if roce_current > roce_previous:
                            score = 4
                        else:
                            score = 3
                    elif free_cash_flow_per_share <= 0:
                        score = 2

                if self.ANALYZE_ONE_COMPANY:
                    print(f"Free Cash Flow Per Share & EPS Difference Score: {score}/5")

                fcfps_and_eps_difference_statuses[report_date] = score

            roce_previous = roce.get(row["date"])

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Free Cash Flow Per Share & EPS Difference Score

            try:
                max_date = max(fcfps_and_eps_difference_statuses.keys())
                fcfps_and_eps_difference_status = fcfps_and_eps_difference_statuses[max_date]
            except ValueError:
                fcfps_and_eps_difference_status = 0
            finally:
                return fcfps_and_eps_difference_status

        return fcfps_and_eps_difference_statuses


    def free_cash_flow_dividend_cover_ratio(
        self, free_cash_flow_per_shares: dict, dividends: dict
    ):
        """
        If free cash flow is sufficient to pay dividends,
        then the ratio will be more than 1

        ---------------------------------------------------------------------

        NOTE --> When analyzing a company, it's a good idea
        to compare free cash flow per share with dividends
        per share over a period of 10 years.
        """

        free_cash_flow_dividend_cover_ratios = {}

        for report_date, free_cash_flow_per_share in free_cash_flow_per_shares.items():

            report_year = int(report_date[:4])

            dividend_per_share = dividends.get(report_year)

            if dividend_per_share != None:

                try:
                    fcfdc = free_cash_flow_per_share / dividend_per_share
                    free_cash_flow_dividend_cover_ratios[report_date] = fcfdc

                    if self.ANALYZE_ONE_COMPANY:
                        print(f"Free Cash Flow Dividend Cover Ratio (for year - {report_date}) ==> {fcfdc:.2f}")

                except:
                    print("NO DIVIDEND !!!")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Free Cash Flow Dividend Cover Ratio

            try:
                max_date = max(free_cash_flow_dividend_cover_ratios.keys())
                free_cash_flow_dividend_cover_ratio = free_cash_flow_dividend_cover_ratios[max_date]
                free_cash_flow_dividend_cover_ratio = round(free_cash_flow_dividend_cover_ratio, 2)
            except ValueError:
                free_cash_flow_dividend_cover_ratio = 0.00
            finally:
                return free_cash_flow_dividend_cover_ratio

        return free_cash_flow_dividend_cover_ratios


    def debt_to_free_cash_flow_ratio(
        self, fmp_balance_sheets: pd.DataFrame, fmp_cash_flows: pd.DataFrame
    ):
        """
        How many years would it take for the company to pay
        back it's debt based on it's free cash flow.

        I would RARELY look at a company with a ratio that
        has been consistently MORE THAN 10 !!!
        """

        debt_to_free_cash_flow_ratios = {}

        financial_statements = zip(
            fmp_balance_sheets.iterrows(), fmp_cash_flows.iterrows()
        )

        for (_, balance_sheet), (_, cash_flow_statement) in financial_statements:

            total_debt = balance_sheet["totalDebt"]
            free_cash_flow = cash_flow_statement["freeCashFlow"]

            report_date = balance_sheet["date"]

            try:
                dtfcfr = (total_debt / free_cash_flow)

                debt_to_free_cash_flow_ratios[report_date] = dtfcfr

            except ZeroDivisionError:
                debt_to_free_cash_flow_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Debt To Free Cash Flow Ratio (for year - {report_date}) ==> {dtfcfr:.2f}")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Debt To Free Cash Flow Ratio

            try:
                max_date = max(debt_to_free_cash_flow_ratios.keys())
                debt_to_free_cash_flow_ratio = debt_to_free_cash_flow_ratios[max_date]
                debt_to_free_cash_flow_ratio = round(debt_to_free_cash_flow_ratio, 2)
            except ValueError:
                debt_to_free_cash_flow_ratio = 0.00
            finally:
                return debt_to_free_cash_flow_ratio

        return debt_to_free_cash_flow_ratios


    def debt_to_net_operating_cash_flow_ratio(
        self, fmp_balance_sheets: pd.DataFrame, fmp_cash_flows: pd.DataFrame
    ):
        """
        You wouldn't really want to see a debt to net operating
        cash flow ratio of more than 3, because once you are
        starting to get a value for this ratio of over 5,
        you are looking at companies with significant
        amounts of debt relative to their cash flows.
        """

        debt_to_net_operating_cash_flow_ratios = {}

        financial_statements = zip(
            fmp_balance_sheets.iterrows(), fmp_cash_flows.iterrows()
        )

        for (_, balance_sheet), (_, cash_flow_statement) in financial_statements:

            total_debt = balance_sheet["totalDebt"]
            net_operating_cash_flow = cash_flow_statement["netCashProvidedByOperatingActivities"]

            report_date = balance_sheet["date"]

            try:
                dtnocfr = (total_debt / net_operating_cash_flow)

                debt_to_net_operating_cash_flow_ratios[report_date] = dtnocfr

            except ZeroDivisionError:
                debt_to_net_operating_cash_flow_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Debt To Net Operating Cash Flow Ratio (for year - {report_date}) ==> {dtnocfr:.2f}")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Debt To Net Operating Cash Flow Ratio

            try:
                max_date = max(debt_to_net_operating_cash_flow_ratios.keys())
                debt_to_net_operating_cash_flow_ratio = debt_to_net_operating_cash_flow_ratios[max_date]
                debt_to_net_operating_cash_flow_ratio = round(debt_to_net_operating_cash_flow_ratio, 2)
            except ValueError:
                debt_to_net_operating_cash_flow_ratio = 0.00
            finally:
                return debt_to_net_operating_cash_flow_ratio

        return debt_to_net_operating_cash_flow_ratios


    def debt_to_assets_ratio(self, fmp_balance_sheets: pd.DataFrame):

        """
        Debt to assets is very much like a loan-to-value measure
        on a house. It tells you what percentage of a company's
        assets is taken up by debt.

        Generally, it's good to avoid companies with a debt to
        assets ratio of more than 50%

        THE HIGHER THE PERCENTAGE, THE MORE RISKY A COMPANY GENERALLY IS !!!
        """

        debt_to_assets_ratios = {}

        for _, row in fmp_balance_sheets.iterrows():

            total_debt = row["totalDebt"]
            total_assets = row["totalAssets"]

            report_date = row["date"]

            try:
                dtar = (total_debt / total_assets) * 100

                debt_to_assets_ratios[report_date] = dtar

            except ZeroDivisionError:
                debt_to_assets_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Debt to Assets Ratio (for year - {report_date}) ==> {dtar:.2f} %")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Debt to Assets Ratio

            try:
                max_date = max(debt_to_assets_ratios.keys())
                debt_to_assets_ratio = debt_to_assets_ratios[max_date]
                debt_to_assets_ratio = round(debt_to_assets_ratio, 2)
            except ValueError:
                debt_to_assets_ratio = 0.00
            finally:
                return debt_to_assets_ratio

        return debt_to_assets_ratios


    def interest_cover_ratio(
        self, fmp_income_statements: pd.DataFrame
    ):
        """
        The higher the ratio, the better, but it's
        preferable to have a ratio that's at least 5.
        """

        interest_cover_ratios = {}

        for _, row in fmp_income_statements.iterrows():

            operating_income = row["operatingIncome"] # EBIT
            interest_payable = row["interestExpense"]

            report_date = row["date"]

            try:
                icr = (operating_income / interest_payable)
                interest_cover_ratios[report_date] = icr

            except ZeroDivisionError:
                interest_cover_ratios[report_date] = 0.00

            finally:
                if self.ANALYZE_ONE_COMPANY:
                    print(f"Interest Cover Ratio (for year - {report_date}) ==> {icr:.2f}")

        if not self.ANALYZE_ONE_COMPANY: # Return the latest Interest Cover Ratio

            try:
                max_date = max(interest_cover_ratios.keys())
                interest_cover_ratio = interest_cover_ratios[max_date]
                interest_cover_ratio = round(interest_cover_ratio, 2)
            except ValueError:
                interest_cover_ratio = 0.00
            finally:
                return interest_cover_ratio

        return interest_cover_ratios


    def owner_earnings(
        self, fmp_income_statements: pd.DataFrame, fmp_cash_flow_statements: pd.DataFrame
    ) -> dict:

        """
        NOTE --> Here we're using the 'Historical Average Capex'
        to calculate the 'Maintenance Capex'
        """

        income_statements = fmp_income_statements.sort_values(by="date", ascending=False)
        cash_flows = fmp_cash_flow_statements.sort_values(by="date", ascending=False)

        divider = 0
        sum_of_capex = 0
        owner_earnings_dict = {}

        for _, row in cash_flows.iterrows():
            capex = abs(row["capitalExpenditure"]) # Get absolute value (remove negative sign)

            sum_of_capex += capex

            divider += 1

        # Calculate the historical average CapEx...

        try:
            maintenance_capex = sum_of_capex / divider

            net_income = income_statements["netIncome"].iloc[0]
            depreciation_and_amortization = income_statements["depreciationAndAmortization"].iloc[0]
            other_non_cash_items = cash_flows["otherNonCashItems"].iloc[0]
            shares_outstanding = income_statements["weightedAverageShsOut"].iloc[0]

            owner_earnings = net_income + depreciation_and_amortization + other_non_cash_items - maintenance_capex
            owner_earnings_per_share = owner_earnings / shares_outstanding

            owner_earnings_dict["owner_earnings"] = round(owner_earnings, 2)
            owner_earnings_dict["owner_earnings_per_share"] = round(owner_earnings_per_share, 2)

        except ZeroDivisionError:
            owner_earnings_dict["owner_earnings"] = 0.00
            owner_earnings_dict["owner_earnings_per_share"] = 0.00

        finally:
            if self.ANALYZE_ONE_COMPANY:
                print(f"Owner Earnings ==> ${owner_earnings:.2f}")
                print(f"Owner Earnings (per share) ==> ${owner_earnings_per_share:.2f}")

            return owner_earnings_dict


    def calculate_cash_interest_rate(self, owner_earnings: dict, stock_price: float) -> float:

        """
        Calculate the cash interest rate (yield)

        You can compare this with the interest rates
        on savings accounts or bonds.
        """

        # Cash Profit Per Share
        owner_earnings_per_share = owner_earnings.get("owner_earnings_per_share")

        cash_interest_rate = (owner_earnings_per_share / stock_price) * 100
        cash_interest_rate = round(cash_interest_rate, 2)

        if self.ANALYZE_ONE_COMPANY:
            print(f"Company cash interest rate (yield) ==> {cash_interest_rate}%")

        return cash_interest_rate


    def calculate_desired_price_with_cash_yield(
        self, owner_earnings: dict, minimum_cash_yield: float
    ) -> float:

        """
        Determine a fair buying price for a stock by setting a
        minimum acceptable cash yield and solving for price.
        """

        # Cash Profit Per Share
        owner_earnings_per_share = owner_earnings.get("owner_earnings_per_share")

        desired_price = owner_earnings_per_share / minimum_cash_yield
        desired_price = round(desired_price, 2)

        if self.ANALYZE_ONE_COMPANY:
            print(f"A fair buying price ==> ${desired_price}")

        return desired_price


    def calculate_desired_price_with_epv(
        self,
        fmp_income_statements: pd.DataFrame,
        fmp_balance_sheets: pd.DataFrame,
        fmp_cash_flow_statements: pd.DataFrame,
        company_tax_rates: dict,
        minimum_cash_yield: float
    ) -> float:

        """
        Earnings Power Value (EPV) estimates the value of a company based
        solely on its current, normalized cash profits, assuming no future
        growth. It focuses on what the business is worth today, given its
        ability to generate steady profits over time.

        If the current share price is significantly higher, a large portion
        of the price is based on future growth expectations. On the other
        hand, if the current share price is near or below EPV,
        the stock may be undervalued.
        """

        income_statements = fmp_income_statements.sort_values(by="date", ascending=False)
        balance_sheets = fmp_balance_sheets.sort_values(by="date", ascending=False)
        cash_flow_statements = fmp_cash_flow_statements.sort_values(by="date", ascending=False)

        try:
            report_date = income_statements["date"].iloc[0]

            ebit = income_statements["operatingIncome"].iloc[0] # EBIT
            shares_outstanding = income_statements["weightedAverageShsOut"].iloc[0]

            total_debt = balance_sheets["totalDebt"].iloc[0]
            cash_and_cash_equivalents = balance_sheets["cashAndCashEquivalents"].iloc[0]

            depreciation_and_amortization = cash_flow_statements["depreciationAndAmortization"].iloc[0]
            capital_expenditure = abs(cash_flow_statements["capitalExpenditure"]).iloc[0]

            tax_rate = company_tax_rates.get(report_date)

            #------------------------------------------------------------

            normalized_cash_profit = ebit + depreciation_and_amortization - capital_expenditure

            after_tax_cash_profit = normalized_cash_profit * (1 - tax_rate)

            enterprise_value = after_tax_cash_profit / minimum_cash_yield

            equity_value = enterprise_value - total_debt + cash_and_cash_equivalents

            epv_per_share = equity_value / shares_outstanding
            epv_per_share = round(epv_per_share, 2)

        except:
            epv_per_share = 0.00
        finally:
            if self.ANALYZE_ONE_COMPANY:
                print(f"Earnings Power Value (EPV) Per Share ==> ${epv_per_share}")

            return epv_per_share


    def calculate_maximum_and_ideal_prices(
        self, owner_earnings: dict, interest_rate: float, margin_of_safety: float
    ) -> dict:

        """
        This calculation focuses on determining the maximum price you
        should pay for a company's shares based on its cash profits
        (or "owner earnings") relative to prevailing interest
        rates (adjusted for inflation and risk).
        """

        ideal_prices_and_cash_yield = {}

        try:
            # Cash Profit Per Share
            owner_earnings_per_share = owner_earnings.get("owner_earnings_per_share")

            maximum_price = owner_earnings_per_share / interest_rate

            # Price with Margin of Safety
            ideal_price_with_mos = maximum_price * (1 - margin_of_safety)

            cash_yield_at_ideal_price = (owner_earnings_per_share / ideal_price_with_mos) * 100

            ideal_prices_and_cash_yield["maximum_price"] = round(maximum_price, 2)
            ideal_prices_and_cash_yield["ideal_price"] = round(ideal_price_with_mos, 2)
            ideal_prices_and_cash_yield["cash_yield_ideal_price"] = round(cash_yield_at_ideal_price, 2)

        except:
            ideal_prices_and_cash_yield["maximum_price"] = 0.00
            ideal_prices_and_cash_yield["ideal_price"] = 0.00
            ideal_prices_and_cash_yield["cash_yield_ideal_price"] = 0.00

        finally:
            if self.ANALYZE_ONE_COMPANY:
                print(f"Maximum Price ==> ${maximum_price:.2f}")
                print(f"Ideal Price ({(margin_of_safety * 100):.2f}% Discount) ==> ${ideal_price_with_mos:.2f}")
                print(f"Cash Yield at Ideal Price ==> {cash_yield_at_ideal_price:.2f}%")

            return ideal_prices_and_cash_yield
