import requests
from bs4 import BeautifulSoup
import json

# Function to get top 20 article URLs from the BBC Innovation page
def bbc_innovation_article_urls(base_url="https://www.bbc.com/innovation"):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all anchor tags (<a>) with href attribute, filter the relevant ones
    article_urls = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Filter to include only relevant article links and avoid duplicates
        if href.startswith("/news/articles"):
            full_url = "https://www.bbc.com" + href
            if full_url not in article_urls:
                article_urls.append(full_url)
            if len(article_urls) >= 20:  # Get only the top 20 URLs
                break
    return article_urls

# Function to extract article details: title, author, published date, and body text
def bbc_innovation_article_details(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_tag = soup.find('h1', class_="sc-518485e5-0 bWszMR")
    title = title_tag.text.strip() if title_tag else ""

    # Extract author and published date from ld+json script
    author_name = ""
    full_published_date = ""
    short_published_date = ""
    json_data = soup.find("script", type="application/ld+json")
    
    if json_data:
        try:
            json_content = json.loads(json_data.string)
            if "author" in json_content:
                author_name = json_content['author'][0]['name']
            
            if "datePublished" in json_content:
                # Extract full published date (with time)
                full_published_date = json_content["datePublished"]
                # Extract only the date (YYYY-MM-DD)
                short_published_date = full_published_date.split("T")[0]
        except (json.JSONDecodeError, KeyError):
            pass

    # Extract article body from HTML (optional, not in JSON-LD)
    body_tag = soup.find_all('div', class_='sc-18fde0d6-0 dlWCEZ')
    body = ' '.join([p.text.strip() for div in body_tag for p in div.find_all('p', class_='sc-eb7bd5f6-0 fYAfXe')])

    return {
        "url": article_url,
        "title": title,
        "author": author_name,
        "published": full_published_date,
        "published_date": short_published_date,
        "body": body
    }

# Example usage
if __name__ == "__main__":
    # Step 1: Get the top 20 article URLs
    article_urls = bbc_innovation_article_urls()
    print("Top 20 Article URLs:")
    for url in article_urls:
        print(url)

    # Step 2: Get the details of each article
    for article_url in article_urls:
        details = bbc_innovation_article_details(article_url)
        print("\nArticle Details:")
        print(details)
