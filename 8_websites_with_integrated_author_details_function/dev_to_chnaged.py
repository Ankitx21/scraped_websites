import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

# Function to convert the published date to just a date
def dev_to_date(published):
    current_year = datetime.now().year
    try:
        # Format: "Jul 2" (e.g., "Jul 2")
        date_object = datetime.strptime(f"{published} {current_year}", '%b %d %Y').date()
    except ValueError:
        try:
            # Format: "1 Jul" (e.g., "1 Jul")
            date_object = datetime.strptime(f"{published} {current_year}", '%d %b %Y').date()
        except ValueError:
            raise ValueError(f"Date format not recognized: {published}")
    return date_object

# Function to fetch author details
def dev_to_author_details(author_url):
    author_page = requests.get(author_url)
    author_soup = BeautifulSoup(author_page.text, "html.parser")
    
    # Extract author details
    author_name = author_soup.find('h1').text.strip() if author_soup.find('h1') else ''
    author_img = author_soup.find('span', class_="crayons-avatar").find('img')['src'] if author_soup.find('span', class_="crayons-avatar") else ''
    
    # Since LinkedIn and Twitter details are not mentioned, keeping them blank
    author_linkedin = ""
    author_twitter = ""

    author_details = {
        "author_name": author_name,
        "author_img": author_img,
        "author_linkedin": author_linkedin,
        "author_twitter": author_twitter
    }
    
    return author_details

# Function to fetch the list of articles
def dev_to_article_list(request_page=1):
    article_url_bag = []
    base_url = "https://dev.to"
    page = 0

    while True:
        url = f"https://dev.to/search/feed_content?per_page=100&page={page}&tag=news&sort_by=hotness_score&sort_direction=desc&tag_names%5B%5D=news&approved=&class_name=Article"
        headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }

        try: 
            response = requests.get(url, headers=headers)
            articles = response.json()
            for article in articles["result"]:
                article_url = base_url + article['path']
                article_url_bag.append(article_url)

            page += 1
            if len(articles['result']) < 99 or page == request_page:
                break
        except Exception as e:
            print(f"Error fetching article list: {e}")
            break

    return article_url_bag

# Function to fetch article details
def dev_to_article_details(article_url):
    html = requests.get(article_url)
    soup = BeautifulSoup(html.text, "html.parser")

    # Extract author information
    author_tag = soup.find(class_="pl-3 flex-1").find('a')
    author_name = author_tag.text.strip()
    author_url = "https://dev.to" + author_tag['href']
    
    # Get author details from separate author page
    author_details = dev_to_author_details(author_url)

    # Extract other article details
    published = soup.find(class_="pl-3 flex-1").find("time").text.strip()
    published_date = dev_to_date(published=published)
    title = soup.find(class_="crayons-article__header__meta").find("h1").text.strip()

    article_body = soup.find(class_="crayons-article__body text-styles spec__body").find_all("p")
    article_without_line_break = " ".join([b.text for b in article_body])

    # Construct article dictionary with author details
    article_dict = {
        "author": author_name,
        "author_details": author_details,
        "title": title,
        "published": published,
        "published_date": published_date,
        "url": article_url,
        "body": article_without_line_break
    }

    return article_dict

def dev_to_save():
    domain = "dev.to"
    website = Website.objects.get(domain=domain)
    article_urls = dev_to_article_list()

    for i, article_url in enumerate(article_urls):
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
                article_details = dev_to_article_details(article_url)
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    # Assuming there's a category field; you might need to adjust this
                    category="news"  # Replace with the appropriate category if different
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass

    return article_urls
