import requests
from bs4 import BeautifulSoup
import re
import json

# URL of the website to scrape
url = "https://www.cnbc.com/world/?region=world"

# Regular expression to match links with numbers after the website, optionally preceded by /video
pattern = re.compile(r"https://www\.cnbc\.com(/video)?/\d{4}/\d{2}/\d{2}/")

# Send a request to the website
response = requests.get(url)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Set to store unique links
    unique_links = set()
    
    # Function to add links to the set and print if unique and matches pattern
    def add_link(link):
        if link and pattern.match(link) and link not in unique_links:
            unique_links.add(link)
    
    # Scrape the FeaturedCard-title links
    feature_cards = soup.find_all('h2', class_='FeaturedCard-title')
    for card in feature_cards:
        link = card.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape the SecondaryCard-headline links
    secondary_cards = soup.find_all('div', class_='SecondaryCard-headline')
    for card in secondary_cards:
        link = card.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Latest news section
    latest_news_section = soup.find_all('div', class_='LatestNews-container')
    for latest_news in latest_news_section:
        link = latest_news.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape the RiverHeadline-headline links
    main_articles = soup.find_all('div', class_='RiverHeadline-headline')
    for article in main_articles:
        links = article.find_all('a', href=True)
        if links:
            # If there are two anchor tags and one has data-type="pro-button", print the other link
            if len(links) > 1 and links[0].get('data-type') == 'pro-button':
                add_link(links[1]['href'])
            else:
                add_link(links[0]['href'])
    
    # Scrape Latest Market News links
    latest_market_news = soup.find_all('div', class_='Card-titleContainer')
    for news in latest_market_news:
        link = news.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape CNBC TV links
    cnbc_tv = soup.find_all('div', class_='VideoRecirculationLinks-card', role='link', tabindex='0')
    for tv in cnbc_tv:
        link = tv.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape Special Reports links
    special_reports = soup.find_all('div', class_="PageBuilder-containerWidth100 PageBuilder-pageRow")
    for report in special_reports:
        links = report.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
    # Scrape Trending Now links
    trending_now = soup.find('ul', class_='TrendingNow-storyContainer')
    if trending_now:
        links = trending_now.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
    # Scrape Pro News Analysis links
    pro_news_analysis = soup.find('section', id='HomePageInternational-TwoColumnImageDense-ProNewsandAnalysis-18')
    if pro_news_analysis:
        links = pro_news_analysis.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
    # Function to scrape article details
    def scrape_article_details(article_url):
        response = requests.get(article_url)
        if response.status_code == 200:
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
            
            return article_data
        else:
            print(f"Failed to retrieve the article. Status code: {response.status_code}")
            return None

    # List to store all article details
    all_articles_data = []

    # Scrape details of each article
    for article_url in unique_links:
        article_details = scrape_article_details(article_url)
        if article_details:
            all_articles_data.append(article_details)
    
    # Convert the list of dictionaries to JSON and save it to a file
    with open('all_articles_data.json', 'w') as json_file:
        json.dump(all_articles_data, json_file, indent=4)
    
    print("All article data has been saved to all_articles_data.json")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
