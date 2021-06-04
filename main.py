## Get line chart that plots price, volume, and mention frequency

from Stock2 import Stock, Forum

ticker = 'GME'

gme = Stock(ticker)

print(gme.plot())
