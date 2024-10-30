# -*- coding: utf-8 -*-
import os
from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader
import os
from openai import OpenAI

def get_date_range():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    return start_date, end_date

def download_sec_filings(ticker, start_date, end_date):
    dl = Downloader(ticker, "varun.singh@" + ticker + ".com")
    forms = ["8-K", "10-K", "10-Q"]
    for form in forms:
        dl.get(form, ticker, after=start_date.strftime('%Y-%m-%d'), before=end_date.strftime('%Y-%m-%d'),download_details=True)


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator=' ', strip=True)

    tables = soup.find_all('table')
    table_texts = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.get_text(strip=True) for col in cols]
            table_texts.append('\t'.join(cols))
    return text, table_texts

def save_to_text_file(filename, text_content, table_contents):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text_content + "\n\n")
        f.write("Extracted Tables:\n")
        for table in table_contents:
            f.write(table + "\n")

def downloadFilings(ticker, start_date, end_date):
    download_sec_filings(ticker, start_date, end_date)

    download_path = os.path.join("/content/sec-edgar-filings", ticker)

    for form in ["8-K", "10-K", "10-Q"]:

        form_path = os.path.join("/content/sec-edgar-filings", ticker, form)

        for filename in os.listdir(form_path):
            new_path = os.path.join(form_path, filename+"/full-submission.txt")
            if new_path.endswith(".txt"):
                with open(new_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    text_content, table_contents = extract_text_from_html(html_content)

                cleaned_filename = f"cleaned-data/{ticker}_{form}_{filename}.txt"
                save_to_text_file(cleaned_filename, text_content, table_contents)

def getSumarizedData(prompt,ticker):
    start_date, end_date = get_date_range()
    downloadFilings(ticker, start_date, end_date)

    documents = SimpleDirectoryReader('cleaned-data').load_data()
    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine()

    retrieved_docs = query_engine.query(prompt)

    prompt = f"Using the information provided, {retrieved_docs}, please answer: {prompt}"

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    generated_response = response.choices[0].message.content
    return generated_response


getSumarizedData("What is the company Net Sales in last year","AAPL")

