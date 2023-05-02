import requests
import os
import csv
import string
from bs4 import BeautifulSoup

# Replace all invalid characters in a string with an underscore
def clean_filename(s):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c if c in valid_chars else '_' for c in s)

# Set up API endpoint and credentials
zendesk_url = 'https://convert.zendesk.com/api/v2/help_center/'
user = 'email@example.com/token'
pwd = 'your_api_token_here'

# Set up request parameters
locale = 'en-us'
include = 'translations'
per_page = 100

# Set up directory to export articles to
directory = 'articles'
if not os.path.exists(directory):
    os.mkdir(directory)

# Set up CSV file to export article metadata to
csv_filename = 'article_metadata.csv'
csv_file = open(csv_filename, 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Article ID', 'Title', 'URL'])

# Get first page of articles
url = f'{zendesk_url}/articles.json?locale={locale}&include={include}&per_page={per_page}'
response = requests.get(url, auth=(user, pwd))
articles = response.json()['articles']

# Loop through all pages of articles
while response.json()['next_page'] is not None:
    for article in articles:
        article_id = str(article['id'])
        article_title = article['title']
        article_body = article['body']

        # Clean up article title to make it a valid filename
        filename = clean_filename(article_title)

        # Export article body to a text file
        with open(os.path.join(directory, filename + '.txt'), 'w', encoding='utf-8') as f:
            f.write(article_title + "\n")
            f.write(article_body)

        # Write article metadata to CSV file
        csv_writer.writerow([article_id, article_title, f'{zendesk_url}/hc/{locale}/articles/{article_id}'])

    # Get next page of articles
    url = response.json()['next_page']
    response = requests.get(url, auth=(user, pwd))
    articles = response.json()['articles']

# Close CSV file
csv_file.close()
