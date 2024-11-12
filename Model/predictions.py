import google.generativeai as genai
from openai import OpenAI

from constants import GEMINI_API_KEY, GPT_API_KEY, MODEL
from data_initializer import ticker_to_company_name
from generate_stock_price import get_stock_price_data_range
from generate_news import get_news
from generate_twitter_data import get_tweets, ticker_to_company_name
from prompts import RELEVANT_NEWS_PROMPT, RELEVANT_TWEETS_PROMPT, STOCK_PREDICTION_PROMPT

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

client = OpenAI(api_key=GPT_API_KEY)

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

def call_llm(prompt):
    if MODEL == 'GEMINI':
        return GeminiCall(prompt)
    return ChatGPTCall(prompt)

def predict_stock_price_movement(ticker, date): 

    company_name = ticker_to_company_name.get(ticker)
    
    # News Articles
    news_articles = get_news(ticker= ticker, date=date, source="both")
    news_data = {"company_name": company_name, "news": news_articles}
    prompt = RELEVANT_NEWS_PROMPT.format(company_name=company_name, data=news_data)
    news_response = call_llm(prompt)

    # Tweets
    tweet_scrap = get_tweets(ticker, date) 
    tweet_data = {"company_name": company_name, "tweets": tweet_scrap}
    prompt = RELEVANT_TWEETS_PROMPT.format(company_name=company_name, data=tweet_data)
    tweet_response = call_llm(prompt)

    # Stock market values
    stock_history_data = get_stock_price_data_range(ticker=ticker, date=date)

    # Final call
    prompt = STOCK_PREDICTION_PROMPT.format(company_name=company_name, news_response = news_response, tweet_response=tweet_response, stock_history_data=stock_history_data)
    final_prediction = call_llm(prompt)
    
    result = final_prediction.text

    print(f'The final result is {result}')
    result_list = [int(x.strip()) for x in result.split(',')]
    return result_list[0], result_list[1]   