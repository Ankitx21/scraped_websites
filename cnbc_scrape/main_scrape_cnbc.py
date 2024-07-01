import requests
from bs4 import BeautifulSoup
import json

def scrape_article_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = []
        
        def extract_links(cards, tag='a'):
            for card in cards:
                link = card.find(tag, href=True)
                if link and link['href'].endswith('.html'):
                    links.append(link['href'])
        
        # Extract various sections
        feature_cards = soup.find_all('h2', class_='FeaturedCard-title')
        secondary_cards = soup.find_all('div', class_='SecondaryCard-headline')
        latest_news_section = soup.find_all('div', class_='LatestNews-container')
        main_articles = soup.find_all('div', class_='RiverHeadline-headline')
        latest_market_news = soup.find_all('div', class_='Card-titleContainer')
        cnbc_tv = soup.find_all('section', class_="FeaturedLiveTvModule-playlistContainer")
        special_reports = soup.find_all('div', class_="PageBuilder-containerWidth100 PageBuilder-pageRow")
        trending_now = soup.find('div', class_='TrendingNowItem-linkWrap')
        pro_news_analysis = soup.find('section', id='HomePageInternational-TwoColumnImageDense-ProNewsandAnalysis-18')
        uk_votes = soup.find('section', id='HomePageInternational-TwoColumnImageDense-UKVotes-19')
        sustainable_future = soup.find('section', id='HomePageInternational-TwoColumnImageDense-SustainableFuture-20')
        cnbc_travels = soup.find('section', id='HomePageInternational-TwoColumnImageDense-CNBCTravel-21')
        make_it = soup.find('div', class_='HomePageInternational-TwoColumnImageDense-MakeIt-22')
        cnbc_explains = soup.find('div', class_='SectionWrapper-content')
        
        # Call the extract_links function for each section
        extract_links(feature_cards, 'a')
        extract_links(secondary_cards, 'a')
        extract_links(latest_news_section, 'a')
        extract_links(main_articles, 'a')
        extract_links(latest_market_news, 'a')
        extract_links(cnbc_tv, 'a')
        extract_links(special_reports, 'a')
        if trending_now:
            extract_links(trending_now.find_all('a', href=True))
        if pro_news_analysis:
            extract_links(pro_news_analysis.find_all('a', href=True))
        if uk_votes:
            extract_links(uk_votes.find_all('a', href=True))
        if sustainable_future:
            extract_links(sustainable_future.find_all('a', href=True))
        if cnbc_travels:
            extract_links(cnbc_travels.find_all('a', href=True))
        if make_it:
            extract_links(make_it.find_all('a', href=True))
        if cnbc_explains:
            extract_links(cnbc_explains.find_all('a', href=True))
        
        return links
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

def scrape_article_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Article heading
        heading = soup.find('h1', class_="ArticleHeader-styles-makeit-headline--l_iUX").get_text(strip=True) if soup.find('h1', class_="ArticleHeader-styles-makeit-headline--l_iUX") else None
        
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
        
        return article_data
    else:
        print(f"Failed to retrieve the article. Status code: {response.status_code}")
        return {}

def main():
    main_page_url = "https://www.cnbc.com/world/?region=world"
    article_links = scrape_article_links(main_page_url)
    
    articles_data = []
    for link in article_links:
        article_data = scrape_article_details(link)
        if article_data:
            articles_data.append(article_data)
    
    # Convert the list of dictionaries to JSON and save it to a file
    with open('articles_data.json', 'w') as json_file:
        json.dump(articles_data, json_file, indent=4)
    
    print("All articles data has been scraped and saved.")

if __name__ == "__main__":
    main()
