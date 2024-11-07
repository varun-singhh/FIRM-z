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
from openai import OpenAI
from generate_stock_price import get_stock_price_data_range
from generate_twitter_data import get_tweets, ticker_to_company_name

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


GEMINI_api_key = ""
ChatGPT_key = ""
Finhub_key = ""
with open('./Keys/config.json') as config_file:
    config = json.load(config_file)
    GEMINI_api_key = config["Gemini_api_key"]
    ChatGPT_key = config["GPT_Key"]
    Finhub_key = config["Finhub_Key"]

genai.configure(api_key=GEMINI_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

client = OpenAI(api_key=ChatGPT_key)



def Prompt(situation, company_name, data = None, news_response = None, tweet_response = None , stock_history_data = None ):
    if situation == "news":
        prompt = f'''You are a financial analyst. I will be sharing with you a list of 
                    Newspaper headlines for {company_name}. I need you to choose the most relevant 
                    newspaper headlines which you believe can negatively or positively impact the 
                    company's value. Be very cautious while choosing the most relevant articles 
                    (limit it to a maximum of 20 articles) such that you are confident they will 
                    actually impact values without being so vague as to cause false alarms. 

                    Data: {data}

                    Return only the top articles in the following JSON format:
                    {{\"news\": [{{ \"headline\": string, \"summary\": string}}]}}
                    '''
    elif situation == "twitter":
        prompt = f'''You are a financial analyst. I will be sharing with you a list of tweets related to {company_name}. 
                    I need you to choose the most relevant tweets that you believe can provide insights into the company's 
                    performance and its impact on stock market value. 

                    Be very cautious when selecting the most relevant tweets, ensuring they are likely to provide indicators 
                    of the company's future stock market performance.

                    Data: {data}

                    Return only the top tweets in the following JSON format:
                    [{{ "text": string }}]
                    '''    
    elif situation == "final":
        prompt = f"""
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
    return prompt

def GeminiCall(prompt):
    prediction = model.generate_content(prompt)
    return prediction


def ChatGPTCall(prompt):
    # Not complete. Once we decide whether or not to use it for our project
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    print(completion.choices[0].message.content)

def brain(ticker, date):  # Maybe have a dicitonary later which can just convert company to tiker or vice versa
    company_name = ticker_to_company_name.get(ticker)
    news_articles = get_news(
    ticker= ticker,
    from_date="2024-08-10",
    to_date="2024-08-14",
    source="both",
    api_key_finnhub="cn8ooc1r01qocbpgs9h0cn8ooc1r01qocbpgs9hg",
    api_key_polygon="GdSGxrAOB7yW9hlw3Wym69h4MapsLye5",
)
    news_data = {"company_name": company_name, "news": news_articles}
    

    news_response = GeminiCall(Prompt("news", company_name , news_data ))
    # Add empty response
    #news_response = type('Response', (object,), {'text': ''})()
    print(news_response.text)
    print("\n")
    # Now we are working with the tweet
    tweet_scrap = get_tweets(ticker)
    tweet_data = {"company_name": company_name, "tweets": tweet_scrap}
    #tweet_response = GeminiCall(Prompt("twitter", company_name , tweet_data ))
    # Add empty tweet response
    tweet_response = type('Response', (object,), {'text': ''})()
    print(tweet_response.text)
    print("\n")
    # Stock market values
    stock_history_data = get_stock_price_data_range(ticker=ticker, date=date )

    #Final brain call
    final_prediction = GeminiCall(Prompt("final", company_name, news_response = news_response, tweet_response=tweet_response, stock_history_data=stock_history_data ))
    
    result = final_prediction.text
    print(f'The final result is {result}')
    result_list = [int(x.strip()) for x in result.split(',')]
    return result_list[0], result_list[1]   


    
    
#brain("AAPL", "2024-08-15" )

    