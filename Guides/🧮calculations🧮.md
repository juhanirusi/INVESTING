# Calculations You Should Make

Here are a couple of calculations that you should make when inputting values into your intrinsic value calculator. The list also contains some tips on what values should be used there...


> **DON'T BUY BAD BUSINESSES, IF THE CALCULATIONS DON'T ADD UP TO MAKE IT AN ATTRACTIVE INVESTMENT, DON'T CONSIDER BUYING IT... AT THAT PRICE!**


## 1. `Risk-free Rate`

- *For the risk-free rate, you should use the yield of a 5 or 10 year "zero coupon" treasury note, OR EVEN BETTER, instead of using bond returns for it, we should use stock index returns as we're already investing in a stock and because we could already put that momney into a index fund instead of bond for better returns. So:*

    - Use the all-time average return of that country's index fund (or ETF if a company doesn't belong to one)...

        - *If the company is a MID-CAP STOCK, use the all-time average return of that country's MID-CAP INDEX FUND as your risk-free rate.*

        - *If the company is a SMALL-CAP STOCK, use the all-time average return of that country's SMALL-CAP INDEX FUND as your risk-free rate.*

        - *If the company belongs to a small-cap cateogory and there isn't a small-cap index for that country, **LOOK FOR SMALL-CAP ETFS IN THAT CASE!***


## 2. `Market Risk Premium (MRP)`

The average historical market risk premium has been between 5.3% and 5.7%, so **using 5.5% as your market risk premium is a safe bet!**


## 3. `Beta`

To use a Beta in your intrinsic value calculation that doesn't reflect only that single company, we'll rather replace that with the beta that reflects the whole industry the company is in.

- But this isn't good enough because the debt these companies may have could dramatically affect their betas, so let's first unravel the beta first:


    - Unlevered Beta = Average Industry Beta / (1 + ((1 - Tax Rate) x Average Industry Debt To Equity Ratio))

        - Unlevered Beta = 1.1 / (1 + ((1 - 0.21) x 1.3) ≈ 0.5427)

            - *Tax Rate is the average corporate tax rate in the country!*


    - IT'S JUST EASIER TO GOOGLE THIS DATA...

        - https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html


- Next, let's calculate levered beta, which determines how risky a business really is that we're going to use on our intrinsic value calculator's beta section. We calculate levered beta like this:

    - Levered Beta = Unlevered Beta x (1 + ((1 - Tax Rate) x company D/E))

        - Levered Beta = 0.5427 x (1 + ((1 - 0.21) x 0.90)) ≈ 0.9286

            - *Tax Rate is the average corporate tax rate in the country!*
            - *D/E is the company specific Debt to Equity ratio!*
            - **LET'S USE THIS LEVERED BETA AS OUR BETA IN OUR CALCULATION!**


## 4. `Company Growth Estimates`

Instead of relying on Yahoo Finance's growth estimates, you can calculate the estimates yourself!

- We can't use the historical growth rate of the company to predict future growth, because as we know, previous success isn't a guarantee of future success and (GOOD) analysts don't tend to stay as analysts for long, so we can't rely on analysts either. To calculate growth estimates based on reinvested capital, we can do the following:

    1. **Calculate The Company's Total Investments**

        - Total Investments = Change In Non-cash Working Capital + Net Capital Expenditures

    Change In Non-cash Working Capital --> Current Assets - Cash & equivalents - Current Liabilities
    Net Capital Expenditures --> https://www.investopedia.com/terms/c/capitalexpenditure.asp.

    2. **Calculate The Reinvestment Rate...**

        - Reinvestment Rate = Total Reinvestments / (Net Income + Total Reinvestments)

    3. **Calculate The Return On Capital...**

        - Return On Capital = Operating Income After Depreciation / (Debt In Current Liabilities + Long Term Debt + Shareholder's Equity - Cash & Short Term Investments)

    4. **Calculate The Growth Rate...**

        - Growth Rate = ((1 + Reinvestment Rate) x (1 + Return On Capital)) - 1

            - Example...

                - Reinvestment Rate = 20%
                - Return On Capital = 15%

                Growth Rate = ((1 + 0.20) x (1 + 0.15) - 1) ≈ 0.38 -> 38%


NOW, THE GROWTH RATE IS WHAT WE CAN USE ON OUR INTRINSIC VALUE CALCULATOR!


5. `Simple Valuation`

- To come up with a simple valuation take three ratios:

    1. Price / Sales (Revenue)
    2. Discounted Cash Flow
    3. Price / Earnings

    Add them together ==> `(P/S + DCF + P/E /) 3` ==> **TARGET PRICE!**