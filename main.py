import bottle
from bottle import *
from pprint import pprint
import yfinance as yf

app = bottle.default_app()

@bottle.route('/')
def home():
    return '''
        <p> Welcome! Please enter the Stock Symbol of the Stock you want to look up! </p>
        <form action="/result" method="post">
             <label for="sym">Enter the Stock Symbol you want to look up:</label>
             <input type="text" id="sym" name="sym"><br>
             <input type="submit" value="submit"><br>
        </form>
        <a href="/top"><button>Top 5 Company Stocks</button></a>
    '''

@bottle.route('/result', method='POST')
def result():
    sym = request.forms.get('sym')
    if sym:
      return template('''
        <p>The Stock Symbol you entered is: {{sym}}</p>
        <a href="/stock/{{sym}}"><button>Yes, this is what I entered</button></a><br><br>
        <a href="/"><button>Go Back</button></a>
      ''', sym=sym)
    else:
        return template('''
            <p>No Stock Symbol was entered, please go back and enter and Stock Symbol<p><br>
            <a href="/"><button>Go Back</button></a>
        ''')

@bottle.route('/stock/<ticker>')
def stock(ticker):
   try:
       ticker = yf.Ticker(ticker).info
       companyName = ticker['shortName']
       symbol = ticker['symbol']
       marketPrice = ticker['currentPrice']
       todayHigh = ticker['regularMarketDayHigh']
       todayLow = ticker['regularMarketDayLow']
       previousClosePrice = ticker['regularMarketPreviousClose']
       response.content_type = 'text/plain'
       information = f"Name of Company: {companyName}\nSymbol: {symbol}\nMarket Price: {marketPrice}\nToday's Market Low Price: {todayLow}\nToday's Market High Price: {todayHigh}\nPrevious Regular Market Close Price: {previousClosePrice}"
       return information
   except Exception as e:
       return template('''
          <p>The Stock Symbol you entered is not an actual symbol. Please go back and enter another one.<p>
          <a href="/"><button>Go back to home</button></a>
       ''')

@bottle.route('/top')
def pop():
    pop_stock = ["MSFT","AAPL","GOOGL","AMZN","NVDA"]
    list = ["Top 5 Company Stocks:\n\n"]
    for string in pop_stock:
        pTicker = yf.Ticker(string).info
        companyN = pTicker['shortName']
        s = pTicker['symbol']
        mPrice = pTicker['currentPrice']
        tHigh = pTicker['regularMarketDayHigh']
        tLow = pTicker['regularMarketDayLow']
        pClosePrice = pTicker['regularMarketPreviousClose']
        response.content_type = 'text/plain'
        list.append(f"Name of Company: {companyN}\nSymbol: {s}\nMarket Price: {mPrice}\nToday's Market Low Price: {tLow}\nToday's Market High Price: {tHigh}\nPrevious Regular Market Close Price: {pClosePrice}\n\n")
    return list


if __name__ == '__main__':

    run(host='0.0.0.0', port='8080')