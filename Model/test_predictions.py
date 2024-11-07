import csv
import os
from datetime import datetime, timedelta
from brain import brain
from generate_stock_price import get_stock_price_data, get_stock_price_data_range_next
import time

def read_file():
    file_path = os.path.join('.', 'Dataset/tickers.csv')
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tickers = [row['Company Ticker'] for row in reader]
    return tickers

def get_previous_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=-1)
    return next_date.strftime("%Y-%m-%d")

def get_ground_truth_prediction(ticker, date):

    today_price = get_stock_price_data(ticker, date)
    # Use for mean of next 5 days 
    # next_5_day_price = get_stock_price_data_range_next(ticker, date)
    # today_price = sum(next_5_day_price) / len(next_5_day_price)
    prev_day_price = get_stock_price_data(ticker, get_previous_date(date))
    if today_price < prev_day_price:
        return 0
    else:
        return 1

def test_one_day():
    results = []
    tickers = read_file()
    date = '2024-08-15'
    correct = 0 
    wrong  = 0 
    brier = 0

    for ticker in tickers:
        if 'BRK_A' in ticker:
            continue 
        prediction, probability = brain(ticker, date)
        ground_truth_prediction = get_ground_truth_prediction(ticker, date)
        # if prediction == 0:
        #     probability = 100 - probability 
        if prediction ==  ground_truth_prediction:
            correct += 1
        else:
            wrong += 1
        brier += (ground_truth_prediction - (probability/100)) ** 2
        results.append({
            'ticker': ticker,
            'prediction': prediction, 
            'probability': probability, 
            'ground_truth_prediction': ground_truth_prediction
        })
        
        print(f'Accuracy: {correct / (correct + wrong)}')
        print(f'Brier Score: {brier / (correct + wrong)}')
        print(results)
        time.sleep(40)

# def test_average_of_days():
test_one_day()


def get_ground_truth_prediction(ticker, date):

    #today_price = get_stock_price_data(ticker, date)
    #Use for mean of next 5 days 
    next_5_day_price = get_stock_price_data_range_next(ticker, date)
    today_price = sum(next_5_day_price) / len(next_5_day_price)
    prev_day_price = get_stock_price_data(ticker, get_previous_date(date))
    if today_price < prev_day_price:
        return 0
    else:
        return 1