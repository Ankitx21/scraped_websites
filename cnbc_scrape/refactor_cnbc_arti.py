import requests
from bs4 import BeautifulSoup
import re
import json

# URL of the website to scrape
BASE_URL = "https://www.cnbc.com/world/?region=world"
ARTICLE_PATTERN = re.compile(r"https://www\.cnbc\.com(/video)?/\d{4}/\d{2}/\d{2}/")

def get_soup(url):
    """Fetches the content from the URL and returns a BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def add_link(links_set, link):
    """Adds a unique link to the set if it matches the article pattern."""
    if link and ARTICLE_PATTERN.match(link) and link not in links_set:
        links_set.add(link)

def scrape_links(soup):
    """Scrapes all relevant article links from the given BeautifulSoup object."""
    unique_links = set()
    
    # Define the sections and corresponding CSS selectors
    sections = [
        ('h2', 'FeaturedCard-title'),
        ('div', 'SecondaryCard-headline'),
        ('div', 'LatestNews-container'),
        ('div', 'RiverHeadline-headline'),
        ('div', 'Card-titleContainer'),
        ('div', 'VideoRecirculationLinks-card'),
        ('div', 'PageBuilder-containerWidth100 PageBuilder-pageRow'),
        ('ul', 'TrendingNow-storyContainer'),
        ('section', 'HomePageInternational-TwoColumnImageDense-ProNewsandAnalysis-18'),
        ('div', 'Card-titleContainer'),
    ]
    
    # Iterate through each section and scrape links
    for tag, class_name in sections:
        elements = soup.find_all(tag, class_=class_name)
        for element in elements:
            links = element.find_all('a', href=True)
            for link in links:
                add_link(unique_links, link['href'])
    
    return unique_links

def scrape_article_details(article_url):
    """Scrapes details from a given article URL and returns a dictionary of the data."""
    soup = get_soup(article_url)
    if not soup:
        return None
    
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
    
    return {
        "url": article_url,
        "heading": heading,
        "publish_date": publish_date,
        "author_name": author_name,
        "key_points": key_points,
        "article_body": {
            "text": article_text,
            "links": article_links
        }
    }

def save_to_json(data, filename):
    """Saves the given data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    soup = get_soup(BASE_URL)
    if not soup:
        return
    
    unique_links = scrape_links(soup)
    all_articles_data = []
    
    for article_url in unique_links:
        article_details = scrape_article_details(article_url)
        if article_details:
            all_articles_data.append(article_details)
    
    save_to_json(all_articles_data, 'all_articles_datas.json')
    print("All article data has been saved to all_articles_data.json")

if __name__ == "__main__":
    main()
