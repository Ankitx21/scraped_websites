import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def vcnewsdaily_article_list():
    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'

    url = "https://vcnewsdaily.com/"

    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=885e1725197d8257cac9955976176528; __utmc=116890241; __utmz=116890241.1722868014.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); privacy=privacy; __utma=116890241.683597081.1722868014.1722868014.1722869906.2; __utmt=1; __utmb=116890241.1.10.1722869906',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('div' ,class_ = 'col-xl-9')
        if container:
            print('container found!')

        articles = container.find_all('a' , class_='d-block')
        
        if articles:

            for article in articles:
                link = article['href']
                if not link.startswith('https://vcnewsdaily.com/'):
                    url = 'https://vcnewsdaily.com' + link
                else:
                    url = link  
                # print(url)
                article_links.add(url)
        else:
            print("Article section was not found")            
        
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})



def vcnewsdaily_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h2', class_='mb-2 fw-600')
            if title_tag:
                title = title_tag.text.strip()
            
            else:
                title = ""
                missing_fields.append("Title")

            author_tag = soup.find('div' ,class_ = 'body py-4').text.strip()
            if author_tag:
                auth2 = author_tag.split(',')[0].strip()
                author = auth2.split(' ')[-1].strip()
                
            else:   
                author =""
                # print("Auhtor not found")
                missing_fields.append("Author")

            published_tag = soup.find('div' ,class_= 'posted-date d-block fs-13 mb-3 pb-2 position-relative b-bottom')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                published_date = published
                # print(published_date)
                
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            paragraph_texts = []
            summary_divs = soup.find_all('div', class_=['summary','fullArticle'])

            if summary_divs:

                filtered_summaries = [div for div in summary_divs if not div.find('div', class_='mb-2')]
                for summary in filtered_summaries:
                    para =summary.text.strip()
                    # print(para)
                    paragraph_texts.append(para)
                body_content = ' '.join(paragraph_texts)

            else:
                body_content = ""
                missing_fields.append("Paragraph Container")
            # print(body_content)

            if not title or not published or not body_content:
                if missing_fields:
                    print(f"Missing fields for {url}: {', '.join(missing_fields)}")
                return None

            return {
                'url': url,
                'title': title,
                'published': published,
                'publish_date': published_date,
                'author': author,
                'body': body_content,
            }
        
        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except Exception as e:
        print({'url': url, 'error': str(e)})
        return None

if __name__ == "__main__":

    total_article_links = vcnewsdaily_article_list()
    print(f"{len(total_article_links)} article links collected ")
    
    articles_data = []
    for url in total_article_links:        
        article_details = vcnewsdaily_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("scraped_websites/zzsample outputs/vcnewsdaily_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in vcnewsdaily_articles.json")