#********************************************************************************#
#       Author : Sanjay Sengupta - Enterprise Cloud & Big Data Analytics Architect
# Last Updated : July 6, 2022
#********************************************************************************#

from yahoo_fin import stock_info as si
import time

# yahoo finance API sourced streaming ticker price provider function
def get_ticker_price(ticker):
    while True:
        for item in ticker:
            ticker_price = si.get_live_price(item)
            # ticker_price_rounded = '{\n\t"Ticker" : "' + item + '" , \n\t"Price" : "' + str(round(ticker_price, 2)) + '"\n}'
            ticker_price_rounded = '{"' + item + '":"' + str(round(ticker_price, 2)) + '"}'
            print(ticker_price_rounded.upper())
        time.sleep(5)

get_ticker_price(ticker = ['aapl', 'amzn', 'cmg', 'fb', 'googl', 'msft', 'nvda', 'shop', 'snap', 'tsla'])
