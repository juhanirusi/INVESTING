Capital Asset Pricing Model


	- Expected Return = Risk Free Rate + (Beta * Market Risk Premium)

		- Yield of Goverment Bond (Risk Free Rate) = 1.75%
		- Market return of the index the stock belongs to is 8.75%, so the Market Risk Premium = 7% (8.75% - 1.75%)
		- Beta of the stock we look up is 1.5 = The return of the stock is 1.5x more volatile than the index

		--> Risk Free Rate ==> 1.75%
		--> Market Risk Premium ==> 7%
		--> Beta ==> 1.5

		Expected Return for the Stock = 1.75% + (1.5 * 7%) = 12.25%


The Weighted Average Cost of Capital Formula (WACC) --> The WACC represents the average rate of return a company is expected to pay to its security holders to finance its assets. It takes into account both the cost of equity and the cost of debt, weighted by the proportion of each in the company’s capital structure.


	- WACC = (E/V * Re) + ((D/V * Rd) * (1 - T)

	- WACC = (Cost of Equity * % of Equity) + (Cost of Debt % of Debt) * (1 - Tax Rate)

		- E ==> Market value of Equity (Market Cap) --> Market value of equity (market capitalization)
		- D ==> Market value of Debt --> Market value of debt
		- V ==> Total Value of Capital (Equity + Debt) --> Total value of capital (equity + debt) 𝑉 = 𝐸 + 𝐷
		- E/V ==> % of Equity
		- D/V ==> % of Debt
		- Re ==> Cost of Equity (CAPM) --> 12.25% (from CAPM calculation)
		- Rd ==> Cost of Debt (YTM) --> The interest rate on the company's debt
		- T ==> Tax Rate --> Corporate tax rate, which reduces the cost of debt because interest is tax-deductible.


APPLE EXAMPLE...


WACC = [E / (E + D) × Cost of Equity] + [D / (E + D) × Cost of Debt × (1 - Tax Rate)]

Inputs:

	- Market Value of Equity (E): Apple's market capitalization is approximately $3.7 trillion.

	- Market Value of Debt (D): Apple's total debt is around $119.06 billion.

	- Cost of Debt: The effective interest rate Apple pays on its debt. Estimates suggest it's around 5.0%.

	- Tax Rate: Apple's effective tax rate is approximately 24.09%.

Calculations:

	Equity Weight (We):

		We = E / (E + D) = $3.7 trillion / ($3.7 trillion + $119.06 billion) ==> 0.9688

	Debt Weight (Wd):

		Wd = D / (E + D) = $119.06 billion / ($3.7 trillion + $119.06 billion) ==> 0.0312

	After-Tax Cost of Debt:

		= Cost of Debt × (1 - Tax Rate) ==> 5.0% × (1 - 0.2409) ==> 5.0% × 0.7591 ==> 3.7955%

	WACC:

		WACC = (We × Cost of Equity) + (Wd × After-Tax Cost of Debt) ==> (0.9688 × 10.045%) + (0.0312 × 3.7955%) ==> 9.726% + 0.118% ==> 9.844%

Therefore, Apple's WACC is approximately 9.844%.





















def calculate_dcf(free_cash_flows, discount_rate, growth_rate, periods):
    """
    Calculate the Discounted Cash Flow (DCF) including the terminal value.

    Parameters:
    - free_cash_flows: List of free cash flows for each period.
    - discount_rate: The discount rate (as a decimal, e.g., 0.1 for 10%).
    - growth_rate: The perpetual growth rate for the terminal value (as a decimal).
    - periods: Number of periods over which the cash flows are forecasted.

    Returns:
    - dcf_value: The present value of the cash flows, including terminal value.
    """
    # Calculate the present value of free cash flows
    dcf_value = 0
    for t in range(1, periods + 1):
        dcf_value += free_cash_flows[t - 1] / (1 + discount_rate) ** t

    # Calculate the terminal value
    terminal_value = (free_cash_flows[-1] * (1 + growth_rate)) / (discount_rate - growth_rate)

    # Discount the terminal value to present
    terminal_value_discounted = terminal_value / (1 + discount_rate) ** periods

    # Add the terminal value to the DCF value
    dcf_value += terminal_value_discounted

    return dcf_value

# Example usage:

free_cash_flows = [1000000, 1100000, 1210000, 1331000]  # Example FCFs for 4 years
discount_rate = 0.1  # 10% discount rate
growth_rate = 0.03  # 3% perpetual growth rate
periods = 4  # Number of forecasted periods

dcf_value = calculate_dcf(free_cash_flows, discount_rate, growth_rate, periods)
print(f"DCF Value: ${dcf_value:,.2f}")
