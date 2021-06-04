## Stock Class enables one to get stock price, volume, and reddit mentions by a given ticker
## Forum Class enables one to get top mentions after a given date

import sqlite3
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.gridspec import GridSpec

class Stock():

    def __init__(self, ticker):
        self.ticker = ticker
        
        connection = sqlite3.connect()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        yf.pdr_override()

        symb = yf.Ticker(self.ticker)
        self.ticker_df = symb.history(period = "1y", interval = '1d')
        self.ticker_df = self.ticker_df.drop(['Open', 'High', 'Low', 'Dividends', 'Stock Splits'], axis = 1)

        cursor.execute("""SELECT strftime('%Y-%m-%d', dt) as date, COUNT(stock_symb) as num_mentions FROM mention where stock_symb = ?
               group by strftime('%Y-%m-%d', dt)
               order by date asc""", (self.ticker,))

        rows2 = cursor.fetchall()
        dates2, mentions = ([] for i in range(2))
        for row in rows2:
                dates2.append(row[0])
                mentions.append(row[1])

        df2 = pd.DataFrame(list(zip(dates2, mentions)),
                        columns = ['date', 'mentions']).set_index('date')

        self.df3 = self.ticker_df.join(df2).fillna(0)
        self.df3['Returns'] = self.df3['Close'].pct_change()
        self.df3['Vol Change'] = self.df3['Volume'].pct_change()

    def get_df(self):
        return self.df3

    def plot(self):
        # Create 2x2 sub plots
        gs = GridSpec(11, 6)

        pl.figure()
        ax = pl.subplot(gs[:5, :]) # row 0, col 0
        plt.plot(self.df3.index, self.df3['Close'], color = 'black')
        plt.title('1-YR Price for ' + self.ticker, fontsize = 14)

        ax = pl.subplot(gs[6:8, :]) # row 0, col 1
        plt.bar(self.df3.index, self.df3['mentions'], color = 'orange')
        plt.title('1-YR Mentions', fontsize = 11)
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off

        ax = pl.subplot(gs[9:11, :]) # row 1, span all columns
        plt.bar(self.df3.index, self.df3['Volume'], color = 'green')
        plt.title('1-YR Volume', fontsize = 11)
        plt.gcf().set_size_inches(12,8)

        plt.show()
        
class Forum():

    def __init__(self, s_date):
        self.date = s_date
        
        connection = sqlite3.connect()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("""select stock_symb, count(*) as num_mentions from mention where dt > ?
                          group by mention.stock_symb
                          order by num_mentions desc""", (self.date,))

        rows3 = cursor.fetchall()
        stocks, num_mentions = ([] for i in range(2))
        for row in rows3:
                stocks.append(row[0])
                num_mentions.append(row[1])

        self.df = pd.DataFrame(list(zip(stocks, num_mentions)),
                        columns = ['stocks', 'num_mentions'])

    def get_movers(self):
        return self.df
