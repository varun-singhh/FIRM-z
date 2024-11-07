import google.generativeai as genai
from datasets import Dataset
import random
from typing import Callable, List, Any
import json
import requests
import datetime
import pandas as pd
import json
import os

from generate_stock_price import get_stock_price_data_range

def get_news(
    ticker, from_date, to_date, source, api_key_finnhub=None, api_key_polygon=None
):
    news = []

    # Finnhub API
    if source in ["finnhub", "both"] and api_key_finnhub:
        finnhub_url = "https://finnhub.io/api/v1/company-news"
        finnhub_params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": api_key_finnhub,
        }

        response_finnhub = requests.get(finnhub_url, params=finnhub_params)

        if response_finnhub.status_code == 200:
            finnhub_data = response_finnhub.json()
            for article in finnhub_data:
                news.append(
                    {"headline": article["headline"], "summary": article["summary"]}
                )
        else:
            print(
                f"Failed to retrieve Finnhub data. Status code: {response_finnhub.status_code}"
            )

    # Polygon API
    if source in ["polygon", "both"] and api_key_polygon:
        polygon_url = "https://api.polygon.io/v2/reference/news"
        polygon_params = {
            "ticker": ticker,
            "published_utc.gte": from_date,
            "published_utc.lte": to_date,
            "apiKey": api_key_polygon,
        }

        response_polygon = requests.get(polygon_url, params=polygon_params)

        if response_polygon.status_code == 200:
            polygon_data = response_polygon.json().get("results", [])
            for article in polygon_data:
                news.append(
                    {"headline": article["title"], "summary": article["description"]}
                )
        else:
            print(
                f"Failed to retrieve Polygon data. Status code: {response_polygon.status_code}"
            )

    return news

def get_tweets(ticker, date='2024-08-15'):
    
    tweets = []
    file_path = os.path.join('..', 'Dataset', 'Final_Tweets', date, ticker, 'tweets.json')
    file_path = f'/Users/anuragmudgil/Desktop/Study/FIRM/Dataset/Final_Tweets/{date}/{ticker}/tweets.json'

    with open(file_path, 'r') as file:
        data = json.load(file)
    for d in data:
        tweets.append(d['text']) 
    return tweets

GEMINI_api_key = ""
ChatGPT_key = ""
Finhub_key = ""
with open('./Keys/config.json') as config_file:
    config = json.load(config_file)
    GEMINI_api_key = config["Gemini_api_key"]
    ChatGPT_key = config["GPT_Key"]
    Finhub_key = config["Finhub_Key"]

def brain(company_name, ticker, date):  # Maybe have a dicitonary later which can just convert company to tiker or vice versa
    news_articles = get_news(
    ticker= ticker,
    from_date="2024-08-15",
    to_date="2024-10-21",
    source="both",
    api_key_finnhub="cn8ooc1r01qocbpgs9h0cn8ooc1r01qocbpgs9hg",
    api_key_polygon="GdSGxrAOB7yW9hlw3Wym69h4MapsLye5",
)
    news_data = {"company_name": company_name, "news": news_articles}
    
    genai.configure(api_key=GEMINI_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    news_response = model.generate_content(
    "You are a financial analyst. I will be sharing with you a list "
    f"of Newspaper headlines for  {company_name}. I need you to choose the most relavent newspaper headlines which you believe can negatively or positively impact a company's value."
    "Be very incredibly cautious while choosing the most relavent articles (limit it to 30 articles as max) such that you are confident they will actually impact values but not vague that it causes false alarms."
    f"Data: {news_data}"
    "Return only the top articles in the following JSON format: {\"news\": [{ \"headline\": string, \"summary\": string}]}"
    )
    print(news_response.text)
    print("\n")
    # Now we are working with the tweet
    tweet_scrap = get_tweets(ticker)
    tweet_data = {"company_name": company_name, "tweets": tweet_scrap}
    tweet_response = model.generate_content(
    f"You are a financial analyst. I will be sharing with you a list of tweets related to {company_name}"
    "I need you to choose the most relavent tweets which you believe can provide information about the performance of the company and how it impacts their stock market value"
    "Be incredibly cautious while choosing the most relavent tweets such that you are confident they will actually provide indicators of the company's future stock market performance."
    f"Data: {tweet_data}"
    "Return only the top tweets in following JSON format:[{ \"text\": string}"
)
    print(tweet_response.text)
    print("\n")
    # Stock market values
    stock_history_data = get_stock_price_data_range(ticker=ticker, date=date )

    #Final brain call
    final_prediction = model.generate_content(
        f"""
        You are a financial analyst. Based on the given datasets which include newspaper headlines, tweets and the stock market price history of company {company_name}
        We need you to give a prediction whether the stock market price of company {company_name} will either increase or decrease. 
        Return prediction as 0 if you forcast stock price will decrease and 1 if you forcast stock price will increase along with probability.
        Probability must be an integer from 0 to 100 representing the percentage probability of the forecast
        INPUT:
        News Data: {news_response.text}
        Tweets: {tweet_response.text}
        Stock Market History: {stock_history_data}

        OUTPUT:
        prediction, probability

        SAMPLE OUTPUT:
        If you think stock price will decrease with a probability of 75 return
        OUTPUT: 0, 75
        DO NOT GIVE ANY EXPLANATION
        """

    )

    result = final_prediction.text
    print(f'The final result is {result}')
    result_list = [int(x.strip()) for x in result.split(',')]
    return result_list[0], result_list[1]   


    
    
#brain("Apple", "AAPL", "2024-08-15" )

    