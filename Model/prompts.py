RELEVANT_TWEETS_PROMPT = """
You are a financial analyst. I will be sharing with you a list of tweets related to {company_name}. 
I need you to choose the most relevant tweets that you believe can provide insights into the company's 
performance and its impact on stock market value. 

Be very cautious when selecting the most relevant tweets, ensuring they are likely to provide indicators 
of the company's future stock market performance.

Data: {data}

Return only the top tweets in the following JSON format:
[{{ "text": string }}]

"""

RELEVANT_NEWS_PROMPT = """
You are a financial analyst. I will be sharing with you a list of 
Newspaper headlines for {company_name}. I need you to choose the most relevant newspaper headlines which you believe can negatively or positively impact the company's value. 
Be very cautious while choosing the most relevant articles (limit it to a maximum of 20 articles) such that you are confident they will actually impact values 
without being so vague as to cause false alarms. 

Data: {data}

Return only the top articles in the following JSON format:
{{\"news\": [{{ \"headline\": string, \"summary\": string}}]}}

"""

STOCK_PREDICTION_PROMPT = """
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
