import yfinance as yf
from utils import get_previous_date, get_next_date, get_date_time_object_from_string

def get_stock_price_data(ticker, date):
    # Give date in the form of YYYY-MM-DD
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=date, end=get_next_date(date))
    if historical_data.empty:
        return None
    return float(historical_data.iloc[0]['Close'])

def get_stock_price_data_range(ticker, date, interval=10):
    # Give date in the form of YYYY-MM-DD
    results = []
    while len(results) < interval:
        date = get_previous_date(date)
        price = get_stock_price_data(ticker, date)
        if price is not None:
            results.append(price)

    results.reverse()      
    return results