# Mean-Inversion-Trader

The program takes CSV files containing 1yr historical stock price data and performs a mean inversion trading strategy to determine profitability. 

It will loop through each price and it's corresponding 5 day average. If the price falls far enough below its 5 day average the program will buy and wait until the price rises far enough above the 5 day average at which point it will sell. 