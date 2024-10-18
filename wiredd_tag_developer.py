import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Base URL for Wired
base_url = "https://www.wired.com"

# Function to get all article URLs from the Wired developers page
def wired_developers_article_list():
    """
    Function to scrape all article URLs from the Wired developers tag page.
    """
    main_url = "https://www.wired.com/tag/developers/"
    
    # Custom headers with cookies
    headers = {
        'Cookie': 'CN_geo_country_code=IN; CN_segments=co.w2442; CN_xid=b21e96c7-2d55-4141-a442-0142933a072c; CN_xid_refresh=b21e96c7-2d55-4141-a442-0142933a072c'
    }

    # Send the GET request
    response = requests.get(main_url, headers=headers)
    
    # List to store article URLs
    article_urls = []

    # If request is successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with the specific class
        article_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp')

        # Loop through each <a> tag and extract the href value
        for link in article_links:
            href = link.get('href')
            # Concatenate with base URL to form the full article URL
            full_url = base_url + href
            article_urls.append(full_url)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    
    return article_urls

# Function to fetch author details
def wired_developer_author_details(author_url):
    """
    Function to fetch details of the author from the author's page.
    """
    author_details = {
        "author_name": "",
        "author_img": "",
        "author_twitter": "",
        "author_linkedin": ""
    }
    
    # Send the GET request to the author's page
    response = requests.get(author_url)
    
    # If the request is successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape the author name
        author_name_tag = soup.find('a', class_='BylineLink-gEnFiw')
        author_details["author_name"] = author_name_tag.get_text(strip=True) if author_name_tag else ""

        # Scrape the author image using the updated structure
        author_img_wrapper = soup.find('div', class_='ContributorAvatarImageWrapper-kSlnkT')
        if author_img_wrapper:
            picture_tag = author_img_wrapper.find('picture')
            if picture_tag:
                img_tag = picture_tag.find('img')
                author_details["author_img"] = img_tag['src'] if img_tag else ""

        # Scrape the Twitter link
        twitter_tag = soup.find('a', class_='SocialIconExternalLink-huuzOU', href=lambda x: x and "twitter" in x.lower())
        author_details["author_twitter"] = twitter_tag['href'] if twitter_tag else ""

        # LinkedIn is left blank as per request
        author_details["author_linkedin"] = ""

    return author_details

# Function to fetch the featured image
def wired_developer_article_image(soup):
    """
    Function to extract the featured image from the article's soup.
    """
    # Find the specific div containing the image
    img_div = soup.find('div', class_='aspect-ratio--overlay-container')
    if img_div:
        picture_tag = img_div.find('picture', class_='ResponsiveImagePicture-cWuUZO')
        if picture_tag:
            img_tag = picture_tag.find('img')
            return img_tag['src'] if img_tag else " "
    return " "

# Function to fetch article details
def wired_article_details(article_url):
    """
    Function to get details of an article from its URL.
    """
    article_data = {
        "title": "",
        "author_name": "",
        "published": "",
        "published_date": "",
        "body": "",
        "author_details": {},
        "article_img": ""
    }

    # Send the GET request
    response = requests.get(article_url)
    
    # If the request is successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape the title
        title_tag = soup.find('h1', {'data-testid': 'ContentHeaderHed'})
        article_data["title"] = title_tag.get_text(strip=True) if title_tag else ""

        # Scrape the author name and author URL
        author_tag = soup.find('a', class_='BylineLink-gEnFiw')
        if author_tag:
            article_data["author_name"] = author_tag.get_text(strip=True)
            author_url = base_url + author_tag['href']
            # Fetch author details using the author URL
            article_data["author_details"] = wired_developer_author_details(author_url)

        # Scrape the published date
        published_time = soup.find('time', {'data-testid': 'ContentHeaderPublishDate'})
        if published_time:
            datetime_str = published_time['datetime']
            article_data["published"] = published_time.get_text(strip=True)
            # Extract just the date (YYYY-MM-DD)
            article_data["published_date"] = datetime_str.split("T")[0]

        # Scrape the body content
        body_div = soup.find('div', class_='body__inner-container')
        if body_div:
            # Extract all paragraphs and join them to form the complete body text
            paragraphs = body_div.find_all('p')
            article_data["body"] = " ".join(p.get_text(strip=True) for p in paragraphs)

        # Fetch the featured image using a separate function
        article_data["article_img"] = wired_developer_article_image(soup)

    return article_data

# Final function to scrape articles and return the data
def wired_developer_save():
    """
    Scrapes Wired developers articles, fetches article details,
    and prints them for reference.
    
    Returns:
        List of dictionaries containing all the scraped article data.
    """
    # List to store all the article details
    all_articles_data = []
    
    # Get the list of article URLs
    article_urls = wired_developers_article_list()
    
    # Iterate over each URL and fetch details
    for url in article_urls:
        print(f"Scraping article: {url}")
        article_details = wired_article_details(url)
        
        # Print article details for reference
        print("Title:", article_details["title"])
        print("Author:", article_details["author_name"])
        print("Published:", article_details["published"])
        print("Published Date:", article_details["published_date"])
        print("Author Image:", article_details["author_details"]["author_img"])
        print("Author Twitter:", article_details["author_details"]["author_twitter"])
        print("Author LinkedIn:", article_details["author_details"]["author_linkedin"])
        print("Body:", article_details["body"])
        print("Article Image:", article_details.get("article_img", " "))
        print("\n" + "="*80 + "\n")  # Separator for readability
        
        # Add the article data to the list
        all_articles_data.append(article_details)
    
    # Return the full list of article data
    return all_articles_data

# Example usage
if __name__ == "__main__":
    articles_data = wired_developer_save()
