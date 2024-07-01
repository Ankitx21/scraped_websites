import requests
from bs4 import BeautifulSoup
import re

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
            print(link)
    
    # Scrape the FeaturedCard-title links
    feature_cards = soup.find_all('h2', class_='FeaturedCard-title')
    print("Feature Cards:")
    for card in feature_cards:
        link = card.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape the SecondaryCard-headline links
    secondary_cards = soup.find_all('div', class_='SecondaryCard-headline')
    print("\nSecondary Cards:")
    for card in secondary_cards:
        link = card.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Latest news section
    latest_news_section = soup.find_all('div', class_='LatestNews-container')
    print("\nLatest News:")
    for latest_news in latest_news_section:
        link = latest_news.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape the RiverHeadline-headline links
    main_articles = soup.find_all('div', class_='RiverHeadline-headline')
    print("\nMain Articles:")
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
    print("\nLatest Market News:")
    for news in latest_market_news:
        link = news.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape CNBC TV links
    cnbc_tv = soup.find_all('div', class_='VideoRecirculationLinks-card', role='link', tabindex='0')
    print("\nCNBC TV:")
    for tv in cnbc_tv:
        link = tv.find('a', href=True)
        if link:
            add_link(link['href'])
    
    # Scrape Special Reports links
    special_reports = soup.find_all('div', class_="PageBuilder-containerWidth100 PageBuilder-pageRow")
    print("\nSpecial Reports:")
    for report in special_reports:
        links = report.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
    # Scrape Trending Now links
    trending_now = soup.find('ul', class_='TrendingNow-storyContainer')
    print("\nTrending Now:")
    if trending_now:
        links = trending_now.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
    # Scrape Pro News Analysis links
    pro_news_analysis = soup.find('section', id='HomePageInternational-TwoColumnImageDense-ProNewsandAnalysis-18')
    print("\nPro News Analysis:")
    if pro_news_analysis:
        links = pro_news_analysis.find_all('a', href=True)
        for link in links:
            add_link(link['href'])
    
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
