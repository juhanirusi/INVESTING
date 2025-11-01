# Guide On Moving File To Excel

1. Open a blank Excel sheet
2. Use the `Data` > `From Text/CSV` option to import a new CSV file.
3. Transform data by:

    - Replacing commas with dots
    - Removing rows with errors

4. Formatting cells by other cells

    1. Create a simple rule for a cell you want to format, for example, something like this `=H16>D16` (NOTE, NEEDS TO HAVE THE NUMBER OF THE CORRECT ROW!)
    2. To make the whole column use this, copy the cell created earlier with the rule, and click `Home` > `Format painter`
    3. Click the whole column, and now every cell in that whole column should have the same rule formatting.