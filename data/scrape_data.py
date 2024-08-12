import argparse
import datetime
import requests
import json
import os

# Define the API key and endpoint
api_key = os.getenv("NEWS_API_KEY")
endpoint = 'https://newsapi.org/v2/everything'

# Define the list of keyword topics
queries = [
    'AI startup',
    'healthcare startup',
    'fintech startup',
    'Andreessen horowitz',
    'sequoia capital',
    'startup',
    'startup funding',
    'emerging tech',
    'kleiner perkins',
    'techcrunch',
    'startup acquisition',
    'series c',
    'series b',
    'series a'
]

# Function to format article data
def format_article(article):
    content = article.get("content", "")
    return {
        "content": content,
        "summary": article.get("description", ""),
        "name": article.get("title", ""),
        "url": article.get("url", ""),
        "created_on": article.get("publishedAt", ""),
        "updated_at": article.get("publishedAt", ""),
        "category": "news",
        "_run_ml_inference": False,
        "rolePermissions": ["demo", "manager"]
    }

# Function to fetch and format articles for a given query
def fetch_articles(query, api_key, page_size=100):
    params = {
        'q': query,
        'pageSize': page_size,
        'domains': 'techcrunch.com',
        'language': 'en',
        'apiKey': api_key
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        print(len(articles), "found for", query)
        return [format_article(article) for article in articles]
    else:
        print(f"Failed to retrieve articles for query '{query}':", response.status_code)
        return []

# Compile articles for all queries
def main():
    all_articles = []

    for query in queries:
        all_articles.extend(fetch_articles(query, api_key))

    # Define the file path
    file_path = './data/articles.json'

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Check if the file already exists
    if os.path.exists(file_path):
        # Load existing articles
        with open(file_path, 'r') as json_file:
            existing_articles = json.load(json_file)
    else:
        existing_articles = []

    # Append new articles to existing ones
    existing_articles.extend(all_articles)

    # Save all articles back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_articles, json_file, indent=2)

    print(f"Saved {len(all_articles)} articles to articles.json")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Fetch and save news articles.')
    parser.add_argument('--date', type=str, required=True, help='The date to fetch articles from (format: YYYY-MM-DD).')

    args = parser.parse_args()
    date_param = args.date

    # Validate the date format
    try:
        datetime.datetime.strptime(date_param, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    main(date_param)
