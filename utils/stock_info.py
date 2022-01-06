import yfinance as yf
from datetime import date

def stockInfo(ticker):
    today = date.today()
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    return stock_info




    


