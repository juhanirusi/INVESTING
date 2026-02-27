# Criticue For The DFS Valuation Method

Here's some criticue for the standard DFS method and an alternative valuation method instead:


## Criticue For The DFS...


*I'm not a fan of DCFs or reverse DCFs. People claim the latter is "less biased" but you still plug in an a made up number for your discount rate and a made up number for terminal value.*

*In most of the DCFs I've built the terminal value represents +60% of the value of the company so just plugging in a multiple here (terminal growth models are a whole nother thing I won't get into) dictate everything. You know how you get a reasonable estimate for an out year multiple? You build a model and have some measure of insight into the shape of future growth. It's an estimate but it's far more accurate in my opinion than just doing a fancy version of an ROI calculation.*

*Also, unless the company pays dividends the only thing that matters is the terminal value. Adding the present value of cash flows along the way is double counting. You can't say a company will be worth X in the future, never pays you a cent, but for some reason those cash flows along the way have intrinsic value. A Reverse DCF does this just like a standard DCF.*

*Build a basic company model (Income Statement, select Cash Floww and Balance Sheet line items) then you can say stuff like "hmm, three years out forward growth will probably similar to today. The company trades at X now and historically traded between Y and Z." Sensitize future value multiples, slap an =XIRR on it and you have a rough idea of how much money you can make. Compare that to other opportunities. Call it a day.*

*No magic. No lazy person black boxes. Try to figure out what position the company will be in down the road. The rest is academic and subject to market forces.*


## Answer By ChatGPT...


*The text critiques the use of Discounted Cash Flow (DCF) and Reverse DCF models for valuing companies, arguing that they rely too heavily on assumptions and arbitrary inputs. Here's a breakdown of the main points:*

1. `Discount Rates and Terminal Values` --> *Both DCF and Reverse DCF models require you to input a discount rate and a terminal value. These inputs are often subjective and can significantly affect the valuation, making the models prone to bias.*

2. `Terminal Value Dominance` --> *In many DCF models, the terminal value (the value of the company at the end of the projection period) accounts for a large portion of the overall valuation, often over 60%. The critic argues that determining a terminal value is highly speculative and has a significant impact on the valuation.*

3. `Estimating Future Multiples` --> *Instead of relying on arbitrary terminal values, the author suggests building a financial model of the company to estimate future growth and derive future value multiples. This approach is deemed more accurate as it is based on the company's projected performance.*

4. `Double Counting Issue` --> *The text claims that for companies that do not pay dividends, the present value of intermediate cash flows should not be considered in addition to the terminal value, as it constitutes double counting. The terminal value alone should suffice for such companies.*

5. `Practical Valuation Approach` --> The author advocates for a simpler and more intuitive method:

    - *Build a basic financial model of the company, including the Income Statement (IS), key Cash Flow (CF), and Balance Sheet (BS) line items.*

    - *Assess future growth prospects and compare current trading multiples to historical ranges.*

    - *Use the XIRR function (which calculates the internal rate of return) to estimate potential returns.*

    - *Compare this rough estimate to other investment opportunities.*


## 1. Example Valuation Using The Critic's Approach


Let's say we're evaluating Company XYZ, a tech company with no dividends...

1. `Build a Basic Financial Model`

    - *Project the Income Statement (revenue, expenses, and net income) for the next few years.*

    - *Identify key Cash Flow and Balance Sheet items (e.g., capital expenditures, debt).*

2. `Assess Future Growth`

    - *Suppose XYZ has been growing at 10% annually and you expect this to continue for the next three years.*

    - *Currently, XYZ trades at a Price-to-Earnings (P/E) ratio of 20.*

    - *Historically, XYZ has traded between a P/E of 15 and 25.*

3. `Future Value Multiples`

    - *Estimate that in three years, XYZ's P/E ratio will be 18 (a conservative assumption based on historical trading ranges).*

4. `Calculate Future Value`

    - *Projected earnings in three years: $200 million (assuming current earnings of $150 million growing at 10% annually).*

    - *Estimated market value in three years: $200 million * 18 = $3.6 billion.*

5. `Estimate Internal Rate of Return (IRR)`

    - *Current market value: $2.5 billion.*

    - *Use the XIRR function to estimate the IRR over the three-year period based on the current and projected market values.*

6. `In Excel, you would set up the following cash flows`

    - Year 0: -$2.5 billion (initial investment)

    - Year 3: $3.6 billion (projected market value)

    - Using the XIRR function:


        - XIRR(values={−2500000000,3600000000},dates={today’s date,date three years from now})


*...this would give you the annualized return you might expect from investing in XYZ, allowing you to compare this to other investment opportunities.*

*This approach simplifies the valuation process and focuses on key assumptions about future growth and market multiples, rather than relying on potentially arbitrary inputs for discount rates and terminal values.*


## 2. Example Valuation Using The Critic's Approach Apple's Financials:


*To illustrate the practical approach described, let's use Apple's previous year's financials and growth estimates. Here's a simplified example:*

1. **Income Statement (IS)**

- `Revenue` --> $394.33 billion
- `Net Income` --> $94.68 billion

2. **Balance Sheet (BS)**

- `Cash and Equivalents` --> $34.94 billion
- `Total Assets` --> $351.00 billion
- `Total Liabilities` --> $287.91 billion

3. **Cash Flow Statement (CF)**

- `Operating Cash Flow` --> $104.04 billion
- `Capital Expenditures` --> $10.50 billion
- `Free Cash Flow` --> $93.54 billion


ASSUME GROWTH RATES...


*Next, let's estimate future growth by assuming that Apple's revenue growth rate is projected to be 5% per year for the next three years. We also assume a terminal growth rate of 2% and a discount rate (WACC) of 8%.*


CALCULATE FUTURE EARNINGS AND CASH FLOWS...


Forecast the next three years' net income and free cash flow based on the growth estimates.

Year	    Revenue ($B)	Net Income ($B)	Free Cash Flow ($B)
Current	    394.33	        94.68	        93.54
2025	    414.04	        99.41	        98.22
2026	    434.74	        104.38	        103.13
2027	    456.48	        109.59	        108.28


DETERMINE TERMINAL VALUE...


Using the terminal growth rate and Year 3 Free Cash Flow:

- `Year 3 FCF` × (`1` + `Terminal Growth Rate`) / `Discount Rate` − `Terminal Growth Rate`​

- `108.28` × `1.02` / `0.08` − `0.02` ==> 1843.46 billion USD


DISCOUNT FUTURE CASH FLOWS TO PRESENT VALUE...


PV (Year 1 FCF) = 98.22 / (1 + 0.08)¹ = 90.94 billion USD
PV (Year 2 FCF) = 103.13 / (1 + 0.08)² = 88.45 billion USD
PV (Year 3 FCF) = 108.28 / (1 + 0.08)³ = 85.98 billion USD
PV (Terminal Value) = 1843.46 / (1 + 0.08)³ = 1463.89 billion USD


SUM PRESENT VALUES...


Total Value = 90.94 + 88.45 + 85.98 + 1463.89 = 1729.26 billion USD


COMPARE WITH CURRENT MARKET VALUE...


Compare the calculated value with Apple's current market capitalization (approximately $2.5 trillion as of the latest available data) --> OVERVALUED !!!


### SAME, BUT WITH `=XIRR` IN EXCEL...


SET UP CASH FLOWS AND DATES


*Assume today's date is January 1, 2024. We'll use the same cash flows and terminal value from the previous example, spreading them out over the next three years.*

1. `Cash Flows`

    - Year 1 (January 1, 2025)          -->     $98.22 billion
    - Year 2 (January 1, 2026)          -->     $103.13 billion
    - Year 3 (January 1, 2027)          -->     $108.28 billion
    - Terminal Value (January 1, 2027)  -->     $1843.46 billion

2. `Dates`

    - Today (start date)            -->     January 1, 2024
    - Cash Flow 1                   -->     January 1, 2025
    - Cash Flow 2                   -->     January 1, 2026
    - Cash Flow 3 & Terminal Value  -->     January 1, 2027


In Excel, set up the cash flows and dates as follows:


Dates           Cash Flows (USD billion)
01/01/2024      -2500 ( <-- APPLE'S CURRENT VALUE !!! )
01/01/2025      98.22
01/01/2026      103.13
01/01/2027      1951.74

```JS
// THIS IS EXCEL VISUAL BASIC...

=XIRR(B2:B5, A2:A5)

/*
The XIRR function will output the internal rate of return based on
the given cash flows and dates. This rate represents the annualized
return you can expect from the investment given the projected
future cash flows and terminal value.

The expected annualized return on the investment in Apple
at its current market value is:

-------------------------------------------------
--------------------> 7.32% <--------------------
-------------------------------------------------
*/
```