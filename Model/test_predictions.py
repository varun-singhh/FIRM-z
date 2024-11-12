import time

from constants import START_DATE, PREDICTION_RANGE
from predictions import predict_stock_price_movement
from generate_stock_price import get_stock_price_data
from utils import get_all_tickers, get_date_time_object_from_string, get_string_from_date_time_object, get_next_date, get_previous_date


def get_ground_truth_prediction(ticker, date):

    today_price = get_stock_price_data(ticker, date)
    prev_day_price = get_stock_price_data(ticker, get_previous_date(date))
    return int(today_price > prev_day_price)

def test():

    results = []
    tickers = get_all_tickers()
    correct, wrong, brier = 0, 0, 0
    start_date = get_date_time_object_from_string(START_DATE)
    interval = int(PREDICTION_RANGE)

    while interval > 0:
        for ticker in tickers:
            if 'BRK_A' in ticker:
                continue 
            prediction, probability = predict_stock_price_movement(ticker, start_date)
            ground_truth_prediction = get_ground_truth_prediction(ticker, start_date)
            if prediction ==  ground_truth_prediction:
                correct += 1
            else:
                wrong += 1
            brier += (ground_truth_prediction - (probability/100)) ** 2
            results.append({
                'ticker': ticker,
                'date': get_string_from_date_time_object(start_date), 
                'prediction': prediction, 
                'probability': probability, 
                'ground_truth_prediction': ground_truth_prediction
            })
        start_date = get_next_date(start_date)
        interval -= 1
        
        print(f'Accuracy: {correct / (correct + wrong)}')
        print(f'Brier Score: {brier / (correct + wrong)}')
        print(results)
        time.sleep(40)

test()