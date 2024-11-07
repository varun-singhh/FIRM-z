from datetime import datetime, timedelta
import yfinance as yf

def get_next_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=1)
    return next_date.strftime("%Y-%m-%d")

def get_prev_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=-1)
    return next_date.strftime("%Y-%m-%d")

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
        date = get_prev_date(date)
        price = get_stock_price_data(ticker, date)
        if price is not None:
            results.append(price)

    results.reverse()      
    return results

def get_stock_price_data_range_next(ticker, date, interval=5):
    # Give date in the form of YYYY-MM-DD
    results = []
    while len(results) < interval:
        price = get_stock_price_data(ticker, date)
        if price is not None:
            results.append(price)
        date = get_next_date(date)   
    return results