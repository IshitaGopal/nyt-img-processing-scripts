# https://developer.nytimes.com/docs/articlesearch-product/1/overview
# https://stackoverflow.com/questions/77526631/using-new-york-times-api-with-no-returns

import os
import json
from dotenv import load_dotenv, dotenv_values
import requests
from datetime import datetime, timedelta
from time import sleep
import argparse
import re

# load enviroment variables from the .env file
load_dotenv()
api_key = os.getenv("NYT_API_KEY")

# config = dotenv_values(".env")
# api_key = config["NYT_API_KEY"]

# Function to get NYT articles for a specific date and page
# YYYYMMDD

def get_articles_for_date(api_key, filter_query, begin_date, page, output_dir):
    sort = 'relevance'
    query_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    payload = {
        'api-key': api_key,
        'begin_date': begin_date,
        'end_date': begin_date,
        'fq': filter_query,
        'page': page,
        'sort': sort
    }
    response = requests.get(query_url, params=payload)
    print(response.json())
    response_json = response.json()

    return response_json

#test
# get_articles_for_date(api_key, 'global warming', '20100101', 0, 'data/json')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Collect articles from New York Times API between 2 dates and store in a folder.')
    #parser.add_argument('api_key', type=str, help='Your New York Times API key')
    parser.add_argument('--filter_query', type=str, help='Filter query (e.g., "global warming")')
    parser.add_argument('--begin_date', type=str, help='Begin date (YYYYMMDD)')
    parser.add_argument('--end_date', type=str, help='End date (YYYYMMDD)')
    parser.add_argument('--output_dir', type=str, help='Output directory for JSON files')
    args = parser.parse_args()

    filter_query = args.filter_query
    begin_date = args.begin_date
    end_date = args.end_date
    output_dir = args.output_dir

    begin_date = datetime.strptime(begin_date, '%Y%m%d').date()
    end_date = datetime.strptime(end_date, '%Y%m%d').date()
    delta = timedelta(days=1)
    print(f'Collecting articles between {begin_date}-{end_date}')

    while begin_date <= end_date:
        formatted_date = begin_date.strftime('%Y%m%d')
        print(formatted_date)
        hits = 1
        page = 0
        while hits > 0 and page < 100:  # Pagination loop, max 100 pages
            articles = get_articles_for_date(
                api_key, filter_query, formatted_date, page, output_dir
            )  # collect response
            sleep(15)
            hits = articles["response"]["meta"]["hits"]
            # Add the JSON response to the list
            print(f"Processing page {page} for {formatted_date} with {hits} hits")
            if hits == 0:
                break

            # Prepare the file name
            query_sanitized = filter_query.replace(':', ' ')
            query_sanitized = '_'.join(re.sub(r'[^\w\s]',' ',query_sanitized).split())
            fname = f'{query_sanitized}_date_{begin_date}_page_{page}.json'
            file_path = os.path.join(output_dir, fname)

            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Store the response as a JSON file
            with open(file_path, 'w') as f:
                json.dump(articles['response']['docs'], f)

            page += 1
            # Check if there are more pages to process
            if page * 10 >= hits:
                break

        begin_date += delta

# Example query:
# python get_articles_api.py --filter_query '(headline:("global warming" OR "climate change")) OR (body:("global warming" OR "climate change"))' --begin_date '20101224' --end_date '20101231' --output_dir 'data/json'


# # Reference: https://martinheinz.dev/blog/31
# query = "politics"
# begin_date = "20200701"  # YYYYMMDD
# filter_query = "\"body:(\"Trump\") AND glocations:(\"WASHINGTON\")\""  # http://www.lucenetutorial.com/lucene-query-syntax.html
# page = "0"  # <0-100>
# sort = "relevance"  # newest, oldest
# query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
#             f"q={query}" \
#             f"&api-key={api_key}" \
#             f"&begin_date={begin_date}" \
#             f"&fq={filter_query}" \
#             f"&page={page}" \
#             f"&sort={sort}"
#
# r = requests.get(query_url)
# print(r.json())

