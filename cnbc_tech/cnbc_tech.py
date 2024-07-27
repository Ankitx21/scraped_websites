import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_article_urls(main_url):
    """
    Function to get article URLs from the main page.
    """
    response = requests.get(main_url)
    article_urls = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with the class 'Card-title'
        card_title_links = soup.find_all('a', class_='Card-title')
        # Find all <a> tags with the class 'TrendingNowItem-title'
        trending_now_links = soup.find_all('a', class_='TrendingNowItem-title')

        # Combine the links
        all_links = card_title_links + trending_now_links

        # Extract the URLs
        article_urls = [link.get('href') for link in all_links]
    else:
        print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")

    return article_urls

def format_datetime(datetime_str):
    """
    Function to format the datetime string.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return 'Invalid datetime format'

def get_article_details(article_url):
    """
    Function to get details of an article from its URL.
    """
    article_data = {
        "url": article_url,
        "headline": "No headline found",
        "published_date": "No date found",
        "author_name": "No author found",
        "key_points": "No key points found",
        "body_content": "No body content found"
    }

    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape the headline
        headline = soup.find('h1', class_='ArticleHeader-headline')
        article_data["headline"] = headline.get_text(strip=True) if headline else article_data["headline"]

        # Scrape the published date
        published_time = soup.find('time', {'data-testid': 'published-timestamp'})
        if published_time:
            datetime_str = published_time['datetime']
            article_data["published_date"] = format_datetime(datetime_str)

        # Scrape the author name
        author = soup.find('a', class_='Author-authorName')
        article_data["author_name"] = author.get_text(strip=True) if author else article_data["author_name"]

        # Scrape the key points
        key_points_div = soup.find('div', class_='RenderKeyPoints-list')
        article_data["key_points"] = key_points_div.get_text(strip=True) if key_points_div else article_data["key_points"]

        # Scrape the body content
        body_divs = soup.find_all('div', class_='group')
        body_texts = []
        for body_div in body_divs:
            paragraphs = body_div.find_all('p')
            body_texts.append("\n".join(p.get_text(strip=True) for p in paragraphs))
        article_data["body_content"] = "\n\n".join(body_texts) if body_texts else article_data["body_content"]
    else:
        print(f"Failed to retrieve the article webpage. Status code: {response.status_code}")

    return article_data

def main():
    # Define the URL of the main page
    main_url = 'https://www.cnbc.com/technology/'

    # Get article URLs
    article_urls = get_article_urls(main_url)

    # Initialize a list to store the data
    articles_data = []

    for article_url in article_urls:
        print(f"Scraping article: {article_url}")
        # Get article details
        article_details = get_article_details(article_url)
        articles_data.append(article_details)

        print(articles_data)


    # Save the data to a JSON file
    # with open('articles_data.json', 'w') as json_file:
    #     json.dump(articles_data, json_file, indent=4)

    print("Scraping completed and data saved to 'articles_data.json'")

if __name__ == "__main__":
    main()
