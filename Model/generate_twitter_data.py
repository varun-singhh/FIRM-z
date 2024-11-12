import csv
import json
import os

from constants import TWEETS_RANGE

from data_initializer import company_name_to_file_name, ticker_to_company_name
from utils import get_previous_date, get_string_from_date_time_object

def get_tweet_for_a_date(data, date):
    date = get_string_from_date_time_object(date)
    tweets = []
    if date not in data:
        return []
    tweet_data = data[date]
    for d in tweet_data:
        tweets.append(d['text'])
    return tweets
    
def get_tweets(ticker, date):
    
    tweets = []
    interval = int(TWEETS_RANGE)

    company_name = ticker_to_company_name.get(ticker)
    file_name  = company_name_to_file_name.get(company_name) 
    file_path = os.path.join('.', 'Dataset/Tweets', f'{file_name}')
    with open(file_path, 'r') as file:
        data = json.load(file)

    while interval > 0:
        date = get_previous_date(date)
        tweet_list = get_tweet_for_a_date(data, date)
        tweets.extend(tweet_list)
        interval -= 1
    return tweets

