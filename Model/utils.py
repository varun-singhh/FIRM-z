import csv
import os
from constants import COMPANY_COUNT
from datetime import datetime, timedelta

def get_all_tickers():
    file_path = os.path.join('.', 'Dataset/tickers.csv')
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tickers = [row['Company Ticker'] for row in reader]
    return tickers[:COMPANY_COUNT]

def get_previous_date(date_obj):
    return date_obj + timedelta(days=-1)

def get_n_prev_date(date_obj, n):
    return date_obj + timedelta(days=-1*n)

def get_next_date(date_obj):
    return date_obj + timedelta(days=1)

def get_date_time_object_from_string(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def get_string_from_date_time_object(date):
    return date.strftime("%Y-%m-%d")