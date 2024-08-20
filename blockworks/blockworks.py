import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B%d,%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def blockworks_article_list():

    url = "https://news.crunchbase.com/"
    residential_proxies = {
            'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
        }
    ca_cert_path = 'ca.crt'

    url = "https://blockworks.co/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_cb=ChIZ6zBniKWrD-lZxL; cf_clearance=hBJBNbaEE11qJGIiGkY9WOImTOsY8LiFl9I_unL76.Y-1724155946-1.2.1.1-Poubu9RXKndvZ_v7_9juzGlgAH7zVPnC5kUb.qMOi_DcXHQoqEiAqA0vc4Rr.66o4gl.p3xBj26GV6FD5w4h7tR_50aU3Qdjjg4ObypTjnu0oB5fsFwKnQ4NF6lg9lsLiCUorqvHcOD0VmXTD7YQGKVr_M8Pml9Vl1gCvVysD4MdApJ4GcWRFTKmlmBUfvK2WOGu12uzlO4y5IXEf6ki_PLxbpmiFhgyzz8RcrUIbQWs3dTeXO3zwBOuvc6iamf9xf6gNF3rERw4Okpp16GArgkqGE9oLxdDSacq_Ofhe6n1h81YpVW2ERfVvSrCfTQHC2VhxwxP5AB6kH5UeNp4nXEOH8Hr3hKySFNhOO.V4DxR26W_b0u0wre9pcJWfYd68TenMW.IAMHIJtiykm6KT_fwolBPvrmq1W5XWzEs5tNu5D6p4wRxZKkmlLdadp.JpofImxDKxUrZlb_mXX7GQw; _ga=GA1.1.1583271354.1724155948; __gads=ID=6f085d0ee8e3e86d:T=1724155947:RT=1724155947:S=ALNI_MYf4QCxoch3Fx4cjHIa_VOEjH8VpQ; __gpi=UID=00000ecdd3773d49:T=1724155947:RT=1724155947:S=ALNI_MYOhynXbx6v2m9ZZlq_X869tPXfdQ; __eoi=ID=b3e3e645b6f07de0:T=1724155947:RT=1724155947:S=AA-AfjY30nHufXqiB_VxxQO8RWPK; _fbp=fb.1.1724155948649.427331574309775685; __qca=P0-1977108577-1724155947981; _chartbeat2=.1724155947222.1724156128099.1.D0oogFBSFxl5C7MHC2DywH5lLRrSe.1; _cb_svref=external; _ga_GYL4BXXQX8=GS1.1.1724155947.1.1.1724156128.60.0.0; __cfwaitingroom=ChhTQ1ZPbDVibkJtcVg2bVVKVHZ4Y1hRPT0SlAJ5WDFPV1VwYTRDeG05bVVxMUhaY2RHWHU4SDFVKytub0VTZ2dBcUUwK0dPcmE0NGdZbE5MQWxqeTF0WVVXNXluZmV6YVB5SU9hSit4VXUxSGxXaXVUMkhON0Q3UWs5MWwxakNJRC9XRDFxLzlhYWNOU0pIRWc1TjcwWktleEl5Z1M5Uk9jd3ZWVkdtSGpYb0pUWWlIYjRBN2ViR1pWMk5UNG52VWVJbEY4S2dNWWlGVGNiaE1ReW5ObWlKTWJTYnJzTHJkSHh5ckFtd3BabUdRcHRYNFNtQU9qUHRxbE93NStQVy9aNkhBeTh4aFU2UGczY1k3ME0zZS9nSDAzbDhHMUtqb0l4Yy9ldlhaSmNkcW9Gdz0%3D; __cfwaitingroom=Chg3R0tiUUFHWnJ6MXF2d2g1V1lERHNRPT0SkAJtUzdaYy9lZ0NUcXppNjJWdU1CYkF4enorT2g1ZFZyUnpmTlJtdEpzSXNOdXREcy9ScW1zTk9mNmtGMHZJOWhTSUwzSitwSXJIc1YvS0YxOFh1WG0wMUgrdjMwNWJLTFFhZnFCS3VWU0xqVXpuY2hKNkk3amtJZWdUTzBibXBhRTJwcGV2NjJOYmZQWUhFQmZkSjM4ZnZUQkZQc3Evcno4ZVJTcUhiRjVYdGhUcHoybVNWV3BqWmdUVHdYcmRaZHZXcnU3Uk5RRy8vaDdxbkNHQThzeWNnRU9SU05GSmtDRDVxSHR3MElndFF6S3FEV3lJdDN3V29hU0o5QUVZL2xReHVZeU4rZ3NpaWpIRllHaQ%3D%3D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    response = requests.request("GET", url, headers=headers, data=payload ,proxies=residential_proxies ,verify = ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        latest = soup.find('div' , class_='gap-10 px-10 py-5 divide-y divide-gray-200 w-full')
        if latest: print('container found')
        articles = latest.find_all('section' ,class_='flex gap-3 py-5 w-full')
        for article in articles:
            link = article.find('a')['href']
            if 'https://blockworks.co' not in link and 'research.com' not in link:
                url = 'https://blockworks.co'+link
                # print(url)
                article_links.add(url)
            else:
                article_links.add(link)

        print(len(article_links))
        return article_links

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

# blockwork_article_list()

def blockworks_article_details(url):

    missing_fields = []  # List to store missing fields

    residential_proxies = {
            'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
        }
    ca_cert_path = 'ca.crt'

    try:
        response = requests.get(url,proxies=residential_proxies ,verify=ca_cert_path)
        # print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            auth_div = soup.find('div',class_='flex flex-wrap justify-start items-start gap-1 text-xs')
            if auth_div:
                author = auth_div.find('a').text
                # print(author)

            else:
                author=""
                missing_fields.append("author")

            # Extract the published date
            published_tag = soup.find('time')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                parts = published.split(' ')

                date = parts[0]+parts[1]+parts[2]
                
                # print(date)
                published_date = convert_date_format(date)
                # print(published_date)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            par = soup.find('section', class_='w-full')
            paragraphs = par.find_all('p')
            # print(len(paragraphs))
            if paragraphs:
                for para in paragraphs:
                    paragraph_texts.append(para.text)
                body_content = ' '.join(paragraph_texts)
            else:
                body_content = ""
                missing_fields.append("Body Content")

            # print(body_content)
            
            # Only return data if title, published date, and body content are present
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

# blockworks_article_details('https://blockworks.co/news/on-the-margin-newsletter-bitcoin-miners-post-halving')

if __name__ == "__main__":

    total_article_links = blockworks_article_list()

    articles_data = []
    for url in total_article_links:   
        print('scraping for: ',url)     
        article_details = blockworks_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/blockworks_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in blockworks_articles.json")