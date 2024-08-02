import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def entrepreneur_article_list():

    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'



    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'language=en; geo={\'latitude\':\'19.300\',\'longitude\':\'73.050\',\'city\':\'bhiwandi\',\'continent_code\':\'AS\',\'country_code\':\'IN\',\'country_code3\':\'IND\',\'country_name\':\'india\',\'postal_code\':\'421308\',\'region\':\'MH\',\'area_code\':\'0\',\'metro_code\':\'356002\'}; entrepreneur_permutive=Pv-px-3-B2; entrepreneur_permutive_cs=Pv-px-3-B2; _gcl_au=1.1.1772268083.1722522764; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.entrepreneur.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1722522774760%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=97d77791beabc469c8208bcc7068e98d%22%2C%22session_count%22:1%2C%22last_session_ts%22:1722522774760}; permutive-id=58253639-8e83-48cc-92ee-2781296dd03a; __hstc=229039816.0e158c4a02bbc02b0a59400a18d83151.1722522795602.1722522795602.1722522795602.1; hubspotutk=0e158c4a02bbc02b0a59400a18d83151; __hssrc=1; _ga=GA1.1.714508801.1722522797; _fbp=fb.1.1722522798889.755047145505697511; g_state={"i_p":1722530006513,"i_l":1}; pbjs_debug=0; _pbjs_userid_consent_data=3524755945110770; panoramaId_expiry=1722609339024; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; __hssc=229039816.8.1722522795602; FCNEC=%5B%5B%22AKsRol-ArFJsGFsdR5xWdCvkoGq93NCOs5IOlT0RvNOLG9MwoppEhfl9JmYRqXobuua7cE6VbY_tFx8Nb4lKuBlSApEvKnZbLuzLba-iQPc-Z05E6ZKQJeurZp3DOkzkQFA_sbSsKWkKox3lvcw8YdKyzs6NjiZ6CQ%3D%3D%22%5D%5D; _rdt_uuid=1722522809014.83e79080-5e80-4dc5-9259-48b02ea1e477; __gads=ID=eb5f218fbbbd7936:T=1722522803:RT=1722523430:S=ALNI_MapRzuIiphvUZ5Y8dnhXMRpE9yLsw; __gpi=UID=00000eb10f8f0b4c:T=1722522803:RT=1722523430:S=ALNI_MYPgf0WGgllrPfH8PivO914g2IWlQ; __eoi=ID=67bdc9e7278bcf94:T=1722522803:RT=1722523430:S=AA-AfjbXdZMoOZPDFrMWMxQMTf1h; _ga_E50Y29T6V1=GS1.1.1722522796.1.1.1722523431.60.0.0',
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

    url = "https://www.entrepreneur.com/"
    response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)
    
    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('main' ,id = 'content')
        if container:
            print('container found!')

        articles_by_class = container.find_all('a', class_='text-base font-medium hover:underline leading-6')
        articles_by_attribute = container.find_all('a', {'tracking-element': 'headline'})
        print(len(articles_by_attribute))
        unique_articles = articles_by_class + articles_by_attribute

        for article in unique_articles:
            link = article['href']
            if link:
                if not link.startswith('https'):
                    url = 'https://www.entrepreneur.com' + link
                # print(url)
                article_links.add(url)                
        print(len(article_links))
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

    
# entrepreneur_article_list(residential_proxies ,ca_cert_path,payload,headers)

def entrepreneur_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1') 
            if title_tag:
                title = title_tag.text.strip()
            else:
                missing_fields.append("Title")

            # Extract the author
            author_tag = soup.find('a' ,class_= 'hover:underline uppercase font-semibold tracking-wider text-blue-600')
            if author_tag:
                author = author_tag.text.strip()
            else:
                author = ""
                missing_fields.append("Author")
            
            # Extract the published date
            published = soup.find('time')
            if published:
                published = published.text.strip()
                published_date = convert_date_format(published)
            else:
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
            para_container = soup.find('div', class_='gate-check first-letter:float-left first-letter:text-8xl first-letter:pr-1 first-letter:-mt-1 first-letter:font-black first-letter:text-gray-500 prose prose-blue max-w-3xl text-lg leading-relaxed mb-12')

            if para_container:
                # Find the div to exclude
                exclude_div = para_container.find('div', class_='border-t-4 border-gray-200 bg-white')
                for child in para_container.children:
                    if child.name == 'p':
                        paragraph_texts.append(child.text)
                    elif child == exclude_div:
                        break 
                body_content = ' '.join(paragraph_texts)
            else:
                body_content = ""
                missing_fields.append("Paragraph Container")

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


if __name__ == "__main__":

    total_article_links = entrepreneur_article_list()
    articles_data = []
    for url in total_article_links:        
        article_details = entrepreneur_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/entrepreneur_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in entrepreneur_articles.json")

    