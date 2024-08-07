import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def wmbdradio_article_list():
#     residential_proxies = {
#     'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
#     'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
# }
#     ca_cert_path = 'ca.crt'

    url = "https://wmbdradio.com/"

    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SERVERID=v1; _ga_BFCN2RTHR1=GS1.1.1723044154.1.0.1723044154.0.0.0; PHPSESSID=b1a5c2ae80d1667f37f66c26e8e3c250; _gid=GA1.2.1132317392.1723044155; _gat_gtag_UA_4991594_2=1; _gat_gtag_UA_62900807_6=1; _ga=GA1.1.904665151.1723044154; __gads=ID=2973fce66ee274e3:T=1723044154:RT=1723044154:S=ALNI_MboOzwSiAeyjeGpUdNozvW4mX1RGQ; __gpi=UID=00000eb8b441be6a:T=1723044154:RT=1723044154:S=ALNI_MZxRqXY0EfJ3NwRv3XqpHfLilSDvQ; __eoi=ID=97be71eb6f12f926:T=1723044154:RT=1723044154:S=AA-AfjbFEiljBeAmDR_M60LNJtFy; _fbp=fb.1.1723044155875.7829544523497104; _ga_QDKJKV3WE2=GS1.1.1723044155.1.0.1723044156.0.0.0; _ga_QLTWJ7V56Q=GS1.1.1723044155.1.0.1723044156.59.0.0; logglytrackingsession=42fb2215-4237-4234-a83d-3b979151716f; kndctr_C7884A3A64E46D6E0A495EEB_AdobeOrg_identity=CiYyOTgyODIzMTQzNjU3NTIzNzI1MjI0MDMzNjQ0ODk4NjkyOTM1MFITCPfMveuSMhABGAEqBElORDEwAPAB98y965Iy; kndctr_C7884A3A64E46D6E0A495EEB_AdobeOrg_cluster=ind1',
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

    response = requests.get(url, data=payload, headers=headers )
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        head_article = soup.find('a' , class_='sc-img-overlay-item aspect-ratio-container item sc-divider')['href']
        # print("Head article " ,head_article)
        article_links.add(head_article)
        container = soup.find_all('div' ,class_ = 'sc-card-item sc-divider item')
        if container:
            print('container found!')

        # articles = container.find_all('a' , class_='d-block')
            for article in container:
                link = article.find('a')['href']
                url = link  
                # print(url)
                article_links.add(url)           
        print(len(article_links))
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})


def wmbdradio_article_details(url):

    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SERVERID=v1; _ga_BFCN2RTHR1=GS1.1.1723044154.1.0.1723044154.0.0.0; PHPSESSID=b1a5c2ae80d1667f37f66c26e8e3c250; _gid=GA1.2.1132317392.1723044155; _gat_gtag_UA_4991594_2=1; _gat_gtag_UA_62900807_6=1; _ga=GA1.1.904665151.1723044154; __gads=ID=2973fce66ee274e3:T=1723044154:RT=1723044154:S=ALNI_MboOzwSiAeyjeGpUdNozvW4mX1RGQ; __gpi=UID=00000eb8b441be6a:T=1723044154:RT=1723044154:S=ALNI_MZxRqXY0EfJ3NwRv3XqpHfLilSDvQ; __eoi=ID=97be71eb6f12f926:T=1723044154:RT=1723044154:S=AA-AfjbFEiljBeAmDR_M60LNJtFy; _fbp=fb.1.1723044155875.7829544523497104; _ga_QDKJKV3WE2=GS1.1.1723044155.1.0.1723044156.0.0.0; _ga_QLTWJ7V56Q=GS1.1.1723044155.1.0.1723044156.59.0.0; logglytrackingsession=42fb2215-4237-4234-a83d-3b979151716f; kndctr_C7884A3A64E46D6E0A495EEB_AdobeOrg_identity=CiYyOTgyODIzMTQzNjU3NTIzNzI1MjI0MDMzNjQ0ODk4NjkyOTM1MFITCPfMveuSMhABGAEqBElORDEwAPAB98y965Iy; kndctr_C7884A3A64E46D6E0A495EEB_AdobeOrg_cluster=ind1',
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

    

    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url, data=payload, headers=headers )
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_='entry-title')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            
            else:
                title = ""
                missing_fields.append("Title")

            auth_container = soup.find('div' ,class_='author')
            if auth_container:
                author = auth_container.text.strip()
                # print(author)           
            else:   
                author =""
                missing_fields.append("Author")

            # post-date
            published_tag = soup.find('div', class_='post-date')
            if published_tag:
                published = published_tag.text.strip()
                part = published.split('|')[0].strip()
                published_date = convert_date_format(part)
                
                
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            paragraph_texts = []
            para_container = soup.find_all('article', class_='mainArticle')

            if para_container:
                for para_cont in para_container:
                
                    paragraphs = para_cont.find_all('p')
                    if paragraphs:
                        for para in paragraphs:
                            paragraph_texts.append(para.text)
                        body_content = ' '.join(paragraph_texts)
    
                    else:
                        body_content = ""
                        missing_fields.append("Body Content")
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


# wmbdradio_article_list()
# wmbdradio_article_details(url = 'https://wmbdradio.com/2024/08/07/democrats-harris-walz-to-campaign-in-crucial-michigan-wisconsin/')


if __name__ == "__main__":

    total_article_links = wmbdradio_article_list()
    print(f"{len(total_article_links)} article links collected ")
    
    articles_data = []
    for url in total_article_links:        
        article_details = wmbdradio_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/wmbdradio_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in wmbdradio_articles.json")