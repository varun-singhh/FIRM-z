import requests

def get_news(ticker, from_date, to_date, source, api_key_finnhub=None, api_key_polygon=None):
    news = []
    
    # Finnhub API
    if source in ["finnhub", "both"] and api_key_finnhub:
        finnhub_url = "https://finnhub.io/api/v1/company-news"
        finnhub_params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": api_key_finnhub
        }
        
        response_finnhub = requests.get(finnhub_url, params=finnhub_params)
        
        if response_finnhub.status_code == 200:
            finnhub_data = response_finnhub.json()
            for article in finnhub_data:
                news.append({
                    "headline": article["headline"],
                    "summary": article["summary"]
                })
        else:
            print(f"Failed to retrieve Finnhub data. Status code: {response_finnhub.status_code}")
    
    # Polygon API
    if source in ["polygon", "both"] and api_key_polygon:
        polygon_url = "https://api.polygon.io/v2/reference/news"
        polygon_params = {
            "ticker": ticker,
            "published_utc.gte": from_date,
            "published_utc.lte": to_date,
            "apiKey": api_key_polygon
        }
        
        response_polygon = requests.get(polygon_url, params=polygon_params)
        
        if response_polygon.status_code == 200:
            polygon_data = response_polygon.json().get("results", [])
            for article in polygon_data:
                news.append({
                    "headline": article["title"],
                    "summary": article["description"]
                })
        else:
            print(f"Failed to retrieve Polygon data. Status code: {response_polygon.status_code}")
    
    return news


# news_articles = get_news(
#     ticker="AAPL",
#     from_date="2024-08-15",
#     to_date="2024-10-21",
#     source="both",
#     api_key_finnhub="cn8ooc1r01qocbpgs9h0cn8ooc1r01qocbpgs9hg",
#     api_key_polygon="GdSGxrAOB7yW9hlw3Wym69h4MapsLye5"
# )

# for article in news_articles:
#     print(f"Headline: {article['headline']}\nSummary: {article['summary']}\n")
