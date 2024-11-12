import os
import csv

ticker_to_company_name = {}
companies = []
company_name_to_file_name = {}

is_initialized = False

def get_company_name_for_ticker():
    global ticker_to_company_name, companies
    file_path = os.path.join('.', 'Dataset/tickers.csv')
    
    if not ticker_to_company_name:  # Check if the dictionary is empty
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                ticker_to_company_name[row[0]] = row[1]
                companies.append(row[1])

def get_file_name_for_company_name():
    global company_name_to_file_name
    folder_path = os.path.join('.', 'Dataset/Tweets')
    files = os.listdir(folder_path)
    
    if not company_name_to_file_name: 
        for file in files:
            for company in companies:
                file_nm = file.split(' ')[0].strip().lower()
                company_nm = company.split(' ')[0].strip().lower()
                if company_nm in file_nm:
                    company_name_to_file_name[company] = file
                    break
    else:
        print("Data already populated.")

def initialize_data():
    global is_initialized
    if not is_initialized:
        get_company_name_for_ticker()
        get_file_name_for_company_name()
        is_initialized = True

initialize_data()