import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re

def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%d %B, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def businessinsider_article_list():
    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'

    import requests

    url = "https://www.businessinsider.in/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cookie': 'geo_continent=AS; geo_country=IN; geo_region=MH; _ga_BESHS5W3FG=GS1.1.1722874300.1.0.1722874300.60.0.0; _ga=GA1.1.1930108869.1722874301; newuserDetails=undefined; Usercookie=undefined; UserDetail=undefined; ssoid=undefined; ssec=undefined; ticketId=undefined; tksec=undefined; identifier=undefined; LoggedinCookie=undefined; _grx=003a3607-c523-4345-a5a6-516ff015a3d6; _grxs=6c9918f7-2103-4dc2-bb62-7401c0d64e03; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId_expiry=1722960702318; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; panoramaIdType=panoDevice; __gads=ID=423eca580dac0697:T=1722874302:RT=1722874302:S=ALNI_MbABDgXC4hFswpkMBbmPiqqEsDYRQ; __gpi=UID=00000eb4d7b2f764:T=1722874302:RT=1722874302:S=ALNI_Mb2hYGoDKUEojMmStmUq-d9uiq9Sg; __eoi=ID=869ee30bcd7734f8:T=1722874302:RT=1722874302:S=AA-AfjYeAhTf90OMxT99EOBW2x5t; _col_uuid=c61ac7d0-2bca-410e-b23a-9bcf580e0aaa-10rio; _iibeat_session=14b0b170-5863-45e5-bca4-1518d0d6a55a; _iibeat_vt=20240705; _li_dcdm_c=.businessinsider.in; _lc2_fpi=ace253a503ac--01j4hmz8sg7bzsh3fs65tdmy14; _lc2_fpi_meta=%7B%22w%22%3A1722874307376%7D; SharedID=e9b4468e-8b0c-4a7d-9aa7-cd2ecc2896cd; SharedID_cst=zix7LPQsHA%3D%3D; _sharedID=03fc673f-eb87-4b5d-a9e1-0f2fa277c4e1; _sharedID_cst=zix7LPQsHA%3D%3D',
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

    response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('div' ,class_ = 'other-bi-components')
        if container:
            print('container found!')

            articles = container.find_all('a' , {'rel':'noreferrer'})
            if articles:
                for article in articles:
                    link = article['href']
                    if link not in article_links:
                        url = link  
                        # print(url)
                        article_links.add(url)
        else:
            print("Article section was not found")            
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})


def businessinsider_article_details(url):
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
                title = ""
                missing_fields.append("Title")
# published and published date
            published_tag = soup.find('meta' ,{'http-equiv':'Last-Modified'})
            if published_tag:
                published = published_tag.get('content')
                pattern = r"\d{2} \w+?, \d{4}"
                match = re.search(pattern, published)
                if match:
                    date_part = match.group()
                    published_date = convert_date_format(date_part)
            else:
                published = ""
                published_date = ""
                print('not found')
                missing_fields.append("Publish Date")
# author
            auth_container = soup.find('div' ,class_='w-full bi-articleshow')
            if auth_container:
                author = auth_container.find('h2' ,class_= 'font-bold text-[14px] md:text-[16px] text-blue-600').text.strip()
                
            else:   
                author =""
                missing_fields.append("Author")
# article body
            paragraph_texts = []
            para_container = soup.find('div', class_='article-contents')

            if para_container:
                paragraphs = para_container.text
                if paragraphs:
                    paragraph_texts.append(paragraphs)
                    body_content = ' '.join(paragraph_texts)
                    # print(body_content)
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


if __name__ == "__main__":

    total_article_links = businessinsider_article_list()
    print(f"{len(total_article_links)} article links collected ")
    
    articles_data = []
    for url in total_article_links:        
        article_details = businessinsider_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/businessinsider_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in businessinsider_articles.json")