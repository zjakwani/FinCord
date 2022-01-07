import yfinance as yf

def stockInfo(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    print(stock.news)
    return stock_info




    


