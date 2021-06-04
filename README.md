# wsb
#### Code to track submissions on reddit/wallstreetbets, compare with trading volume and price, and store in SQL for further data manipulation.

#### WSB extraction code uses similar methodology as @hackingthemarkets
#### Made an account with alpaca's api (https://alpaca.markets/), use that to get access to 10k+ stock tickers and data. Also used yfinance / pandas_datareader for more efficient processing of data once I had the tickers. 
#### Then created a SQL database with stock and WSB mention data. Under current configuration, have 45,000+ unique post data from WSB by stock ticker. Able to update with a desired frequency by running 
