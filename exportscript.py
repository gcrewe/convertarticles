import requests
import os
from bs4 import BeautifulSoup

# Set your Zendesk subdomain, email, and API token
subdomain = 'YOUR_SUBDOMAIN'
email = 'YOUR_EMAIL'
token = 'YOUR_API_TOKEN'

# Set the endpoint to retrieve articles from
endpoint = f'https://convert.zendesk.com/api/v2/help_center/en-us/articles.json'

# Set the directory to save the articles to
directory = '/home/george/work/Convert/ZendeskExport/articles/'

# Make sure the directory exists
if not os.path.exists(directory):
    os.makedirs(directory)

# Set the parameters for the API request
params = {
    'per_page': 100
}

# Set the headers for the API request
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Loop through the pages of articles until there are no more pages
while True:
    response = requests.get(endpoint, auth=(email+'/token', token), headers=headers, params=params)
    if response.status_code != 200:
        print(f'Error: {response.status_code} - {response.text}')
        break
    
    data = response.json()
    
    # Loop through the articles and save them as text files
    for article in data['articles']:
        article_id = article['id']
        article_title = article['title']
        article_body = article['body']
        
        # Remove any HTML tags from the article body
        article_body = BeautifulSoup(article_body, 'html.parser').get_text()
        
        # Save the article as a text file
        filename = f'{article_id}_{article_title}.txt'
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
            f.write(article_title + "\n")
            f.write(article_body)
    
    # Check if there are more pages of articles
    if data['next_page']:
        params['page'] = data['next_page']
    else:
        break

print('Export complete.')
