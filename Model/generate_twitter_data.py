import csv
import json
import os
from generate_stock_price import get_prev_date

companies = []
ticker_to_company_name = {}
company_name_to_file_name = {}

def get_company_name_for_ticker():
    file_path = os.path.join('.', 'Dataset/tickers.csv')
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
           ticker_to_company_name[row[0]] = row[1]
           companies.append(row[1])

def get_file_name_for_company_name():
    folder_path = os.path.join('.', 'Dataset/Tweets')
    files = os.listdir(folder_path)
    for file in files:
        for company in companies:
            file_nm = file.split(' ')[0].strip().lower()
            company_nm = company.split(' ')[0].strip().lower()
            if company_nm in file_nm:
                company_name_to_file_name[company] = file
                break
    

def get_tweet_for_a_date(data, date):
    tweets = []
    if date not in data:
        return []
    tweet_data = data[date]
    for d in tweet_data:
        tweets.append(d['text'])
    return tweets
    
def get_tweets(ticker, date='2024-08-15', interval = 5):
    
    tweets = []
    company_name = ticker_to_company_name.get(ticker)
    file_name  = company_name_to_file_name.get(company_name) 
    file_path = os.path.join('.', 'Dataset/Tweets', f'{file_name}')
    with open(file_path, 'r') as file:
        data = json.load(file)
    while interval > 0:
        date = get_prev_date(date)
        tweet_list = get_tweet_for_a_date(data, date)
        tweets.extend(tweet_list)
        interval -= 1
    return tweets

get_company_name_for_ticker()
get_file_name_for_company_name()


