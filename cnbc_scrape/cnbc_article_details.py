import requests
from bs4 import BeautifulSoup
import json

# URL of the article to scrape
url = "https://www.cnbc.com/2024/06/20/india-aims-to-be-developed-nation-by-2047-priorities-modi-cant-ignore.html"

# Send a request to the website
response = requests.get(url)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Article heading
    heading = soup.find('h1', class_='ArticleHeader-headline').get_text(strip=True) if soup.find('h1', class_='ArticleHeader-headline') else None
    
    # Publish date
    publish_date = soup.find('time', {'data-testid': 'published-timestamp'}).get_text(strip=True) if soup.find('time', {'data-testid': 'published-timestamp'}) else None
    
    # Author name
    author_name = soup.find('div', class_='Author-authorNameAndSocial').get_text(strip=True) if soup.find('div', class_='Author-authorNameAndSocial') else None
    
    # Key points
    key_points_div = soup.find('div', class_='RenderKeyPoints-keyPoints')
    key_points = [point.get_text(strip=True) for point in key_points_div.find_all('li')] if key_points_div else []
    
    # Article body text and links
    article_body_div = soup.find('div', class_='ArticleBody-articleBody')
    article_text = []
    article_links = []
    if article_body_div:
        for element in article_body_div.find_all(['p', 'a']):
            if element.name == 'p':
                article_text.append(element.get_text(strip=True))
            elif element.name == 'a' and element.has_attr('href'):
                article_links.append(element['href'])
    
    # Create a dictionary to store the scraped data
    article_data = {
        "url": url,
        "heading": heading,
        "publish_date": publish_date,
        "author_name": author_name,
        "key_points": key_points,
        "article_body": {
            "text": article_text,
            "links": article_links
        }
    }
    
    # Convert the dictionary to JSON and save it to a file
    with open('article_data.json', 'w') as json_file:
        json.dump(article_data, json_file, indent=4)
    
    print("Article data has been ")
