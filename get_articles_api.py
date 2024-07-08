import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

# load enviroment variables from the .env file
load_dotenv()
api_key = os.getenv("NYT_API_KEY")


# Function to get NYT articles for a specific date and page
def get_articles_for_date(query, date, page):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json"
    payload = {
        "api-key": api_key,
        "fq": query,
        "begin_date": date,
        "end_date": date,
        "page": page,
        "sort": "relevance",
    }
    response = requests.get(url, params=payload)
    return response.json()


# List to store all JSON responses
query = '"climate change" OR "global warming"'
begin_date = datetime(2010, 1, 1)
end_date = datetime(2010, 12, 31)
delta = timedelta(days=1)

# store responses in a list
all_responses = []

while begin_date <= end_date:
    formatted_date = begin_date.strftime("%Y-%m-%d")
    hits = 1
    page = 0

    while hits > 0 and page < 100:  # Pagination loop, max 100 pages
        articles = get_articles_for_date(
            query, formatted_date, page
        )  # collect response
        hits = articles["response"]["meta"]["hits"]
        # Add the JSON response to the list
        all_responses.extend(articles["response"]["docs"])
        print(f"Processed page {page} for {formatted_date} with {hits} hits")
        page += 1

        # Check if there are more pages to process
        if page * 10 >= hits:
            break

    begin_date += delta
    sleep(12)


# Reference: https://martinheinz.dev/blog/31

