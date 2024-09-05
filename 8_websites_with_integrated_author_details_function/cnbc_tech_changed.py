import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

# Function to format the datetime string to 'YYYY-MM-DD'
def cnbc_tech_datetime(datetime_str):
    """
    Function to format the datetime string to 'YYYY-MM-DD'.
    """
    split_date = datetime_str.split("T")[0]
    try:
        dt = datetime.fromisoformat(split_date)
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Date format not recognized: {datetime_str}")


# Function to fetch the list of articles
def cnbc_tech_article_list():
    """
    Function to get article URLs from the main page.
    """
    article_url_bag = []
    main_url = "https://www.cnbc.com/technology/"

    try:
        response = requests.get(main_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <a> tags with the class 'Card-title'
            card_title_links = soup.find_all('a', class_='Card-title')
            # Find all <a> tags with the class 'TrendingNowItem-title'
            trending_now_links = soup.find_all('a', class_='TrendingNowItem-title')

            # Combine the links
            all_links = card_title_links + trending_now_links

            # Extract the URLs
            article_url_bag = [link.get('href') for link in all_links]
        else:
            print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching article list: {e}")

    return article_url_bag


# Function to fetch author details
def cnbc_tech_author_details(author_url):
    """
    Function to fetch author details from the author's page.
    """
    author_details = {
        "author_name": "",
        "author_img": "",
        "author_linkedin": "",
        "author_twitter": ""
    }

    try:
        response = requests.get(author_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Fetch the author image
            author_img_tag = soup.find('div', class_='RenderBioDetails-image')
            if author_img_tag and author_img_tag.find('img'):
                author_details["author_img"] = author_img_tag.find('img')['src']

            # Fetch the author LinkedIn
            linkedin_tag = soup.find('a', class_='icon-social_linkedin')
            if linkedin_tag:
                author_details["author_linkedin"] = linkedin_tag['href']

            # Fetch the author Twitter
            twitter_tag = soup.find('a', class_='icon-social_twitter')
            if twitter_tag:
                author_details["author_twitter"] = twitter_tag['href']

            # Fetch the author name (assuming the author name is in <h1>)
            author_name_tag = soup.find('h1')
            if author_name_tag:
                author_details["author_name"] = author_name_tag.text.strip()
        else:
            print(f"Failed to retrieve the author webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching author details: {e}")

    return author_details


# Function to fetch article details
def cnbc_tech_article_details(article_url):
    """
    Function to get details of an article from its URL.
    """
    article_data = {
        "url": article_url,
        "title": "No headline found",
        "published_date": "No date found",
        "author": "No author found",
        "author_details": {},
        "body": "No body content found"
    }

    try:
        response = requests.get(article_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Scrape the headline
            headline = soup.find('h1', class_='ArticleHeader-headline')
            article_data["title"] = headline.get_text(strip=True) if headline else article_data["title"]

            # Scrape the published date
            published_time = soup.find('time', {'data-testid': 'published-timestamp'})
            if published_time:
                datetime_str = published_time['datetime']
                article_data['published'] = str(published_time.text.strip()).split(", ")[1]
                article_data["published_date"] = cnbc_tech_datetime(datetime_str)

            # Scrape the author name and URL
            author_tag = soup.find('a', class_='Author-authorName')
            if author_tag:
                article_data["author"] = author_tag.text.strip()
                author_url = author_tag['href']
                # Fetch author details using the author URL
                article_data["author_details"] = cnbc_tech_author_details(author_url)

            # Scrape the key points
            key_points_div = soup.find('div', class_='RenderKeyPoints-list')
            article_data["key_points"] = key_points_div.get_text(strip=True) if key_points_div else article_data["key_points"]

            # Scrape the body content
            body_divs = soup.find_all('div', class_='group')
            body_texts = []
            for body_div in body_divs:
                paragraphs = body_div.find_all('p')
                body_texts.append(" ".join(p.get_text(strip=True) for p in paragraphs))
            article_data["body"] = " ".join(body_texts) if body_texts else article_data["body"]
        else:
            print(f"Failed to retrieve the article webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching article details: {e}")

    return article_data


def cnbc_tech_save():
    """
    Function to save articles by scraping them from the CNBC tech page.
    """
    domain = "cnbc.com"
    website = Website.objects.get(domain=domain)
    article_urls = cnbc_tech_article_list()

    for article_url in article_urls:
        if Articles.objects.filter(website=website, url=article_url).exists():
            art = Articles.objects.filter(url=article_url).first()
            article = {
                "author": art.author,
                "author_details": art.author_details,  # Use existing author details
                "title": art.title,
                "published": art.published,
                "published_date": art.published_date,
                "url": art.url,
                "body": art.body
            }
        else:
            try:
                article_details = cnbc_tech_article_details(article_url)
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details.get("published", ""),
                    published_date=article_details["published_date"],
                    # Assuming there's a category field; you might need to adjust this
                    category="technology"  # Replace with the appropriate category if different
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass

    return article_urls
