import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re

residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
ca_cert_path = 'ca.crt'

cookies = {
    '_chorus_geoip_continent': 'AS',
    '_vm_consent_type': 'opt-out',
    'vmidv1': '134d2782-e488-4b75-92c8-550562573108',
    'sailthru_visitor': '5296363c-011f-41e7-b6ce-e3f5545bb014',
    '_parsely_session': '{%22sid%22:1%2C%22surl%22:%22https://www.theverge.com/tech%22%2C%22sref%22:%22%22%2C%22sts%22:1722079984050%2C%22slts%22:0}',
    '_parsely_visitor': '{%22id%22:%22pid=ba672164-d04e-45eb-9b43-bae7c4491a85%22%2C%22session_count%22:1%2C%22last_session_ts%22:1722079984050}',
    'permutive-id': 'e4850f86-3a58-41ed-a32c-ede00bda7109',
    'OptanonAlertBoxClosed': '2024-07-27T11:33:08.020Z',
    '_gcl_au': '1.1.1296877070.1722079988',
    '_ga': 'GA1.1.1545367335.1722079984',
    '_lr_retry_request': 'true',
    '_lr_env_src_ats': 'false',
    '_lr_sampling_rate': '100',
    '_fbp': 'fb.1.1722079989706.798233689457213379',
    '_scor_uid': 'eb721d6b50114eb59e55e6616e15c4d9',
    'sailthru_pageviews': '9',
    'sailthru_content': 'd065a69a229e925515761361bebfd427a8e44ff2a0ef973799249e1ce43238ff09812d5e5dd4437980ebb826449c2c6b102f16c5093ee7783cc717d9fb9473c8afb6bc432a9c69bbfa31f9336725df63',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Jul+27+2024+17%3A06%3A13+GMT%2B0530+(India+Standard+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=33cecaa6-4c78-4b76-9349-c9e77549dd34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CBG136%3A1%2CC0004%3A1%2CC0005%3A1&hosts=H60%3A1%2CH369%3A1%2CH407%3A1%2CH236%3A1%2CH27%3A1%2CH42%3A1%2CH167%3A1%2CH486%3A1%2CH409%3A1%2CH410%3A1%2CH29%3A1%2CH62%3A1%2CH63%3A1%2CH4%3A1%2CH11%3A1%2CH64%3A1%2CH231%3A1%2CH12%3A1%2CH251%3A1%2CH71%3A1%2CH74%3A1%2CH17%3A1%2CH488%3A1%2CH297%3A1%2CH77%3A1%2CH275%3A1%2CH285%3A1%2CH82%3A1%2CH379%3A1%2CH381%3A1%2CH484%3A1%2CH89%3A1%2CH164%3A1%2CH90%3A1%2CH41%3A1%2CH46%3A1%2CH48%3A1%2CH244%3A1%2CH96%3A1%2CH290%3A1%2CH246%3A1%2CH489%3A1%2CH53%3A1%2CH490%3A1%2CH304%3A1%2CH487%3A1&genVendors=&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false',
    '_awl': '2.1722080173.5-5d0513103d7db09e922889a4bff06b89-6763652d617369612d6561737431-0',
    '__gads': 'ID=76e209a463bc6f0f:T=1722079983:RT=1722080655:S=ALNI_Ma7eDKgIMNjiT6ABG2DsU7Yb-QaFA',
    '__gpi': 'UID=00000ea96b22a489:T=1722079983:RT=1722080655:S=ALNI_MbRtbVJxKvKCGKe9A4r5bvBakqx9w',
    '__eoi': 'ID=9e54e344ab4f9700:T=1722079983:RT=1722080655:S=AA-AfjbrccSHg-zKP6qyHsQMA5W9',
    '_ga_9GXHZT6RVE': 'GS1.1.1722079984.1.1.1722080876.60.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_chorus_geoip_continent=AS; _vm_consent_type=opt-out; vmidv1=134d2782-e488-4b75-92c8-550562573108; sailthru_visitor=5296363c-011f-41e7-b6ce-e3f5545bb014; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.theverge.com/tech%22%2C%22sref%22:%22%22%2C%22sts%22:1722079984050%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=ba672164-d04e-45eb-9b43-bae7c4491a85%22%2C%22session_count%22:1%2C%22last_session_ts%22:1722079984050}; permutive-id=e4850f86-3a58-41ed-a32c-ede00bda7109; OptanonAlertBoxClosed=2024-07-27T11:33:08.020Z; _gcl_au=1.1.1296877070.1722079988; _ga=GA1.1.1545367335.1722079984; _lr_retry_request=true; _lr_env_src_ats=false; _lr_sampling_rate=100; _fbp=fb.1.1722079989706.798233689457213379; _scor_uid=eb721d6b50114eb59e55e6616e15c4d9; sailthru_pageviews=9; sailthru_content=d065a69a229e925515761361bebfd427a8e44ff2a0ef973799249e1ce43238ff09812d5e5dd4437980ebb826449c2c6b102f16c5093ee7783cc717d9fb9473c8afb6bc432a9c69bbfa31f9336725df63; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Jul+27+2024+17%3A06%3A13+GMT%2B0530+(India+Standard+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=33cecaa6-4c78-4b76-9349-c9e77549dd34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CBG136%3A1%2CC0004%3A1%2CC0005%3A1&hosts=H60%3A1%2CH369%3A1%2CH407%3A1%2CH236%3A1%2CH27%3A1%2CH42%3A1%2CH167%3A1%2CH486%3A1%2CH409%3A1%2CH410%3A1%2CH29%3A1%2CH62%3A1%2CH63%3A1%2CH4%3A1%2CH11%3A1%2CH64%3A1%2CH231%3A1%2CH12%3A1%2CH251%3A1%2CH71%3A1%2CH74%3A1%2CH17%3A1%2CH488%3A1%2CH297%3A1%2CH77%3A1%2CH275%3A1%2CH285%3A1%2CH82%3A1%2CH379%3A1%2CH381%3A1%2CH484%3A1%2CH89%3A1%2CH164%3A1%2CH90%3A1%2CH41%3A1%2CH46%3A1%2CH48%3A1%2CH244%3A1%2CH96%3A1%2CH290%3A1%2CH246%3A1%2CH489%3A1%2CH53%3A1%2CH490%3A1%2CH304%3A1%2CH487%3A1&genVendors=&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false; _awl=2.1722080173.5-5d0513103d7db09e922889a4bff06b89-6763652d617369612d6561737431-0; __gads=ID=76e209a463bc6f0f:T=1722079983:RT=1722080655:S=ALNI_Ma7eDKgIMNjiT6ABG2DsU7Yb-QaFA; __gpi=UID=00000ea96b22a489:T=1722079983:RT=1722080655:S=ALNI_MbRtbVJxKvKCGKe9A4r5bvBakqx9w; __eoi=ID=9e54e344ab4f9700:T=1722079983:RT=1722080655:S=AA-AfjbrccSHg-zKP6qyHsQMA5W9; _ga_9GXHZT6RVE=GS1.1.1722079984.1.1.1722080876.60.0.0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%b %d %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def theverge_article_list( cookies,headers,residential_proxies ,ca_cert_path,link ,total_article_links):
    response = requests.get('https://www.theverge.com/tech', cookies=cookies, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content , 'lxml')
        main_container = soup.find('div' ,class_ ='mx-auto max-w-container-lg')
        if main_container:
            section_link = main_container.find_all('a', class_= link)
            # print('from h2')
            for link in section_link:
                url = link['href']
                if not url.startswith('https://www.theverge.com') and url != '/':
                    url = 'https://www.theverge.com' + url
                    if url not in total_article_links:
                        total_article_links.append(url)
        else:
            print('not found')
    return total_article_links




def theverge_article_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            heading = soup.find('h1', class_='mb-28 hidden max-w-[900px] font-polysans text-45 font-bold leading-100 selection:bg-franklin-20 lg:block')
            if heading:
                heading_text = heading.text.strip()
                author_div = soup.find('div', class_='mb-2 text-blurple [&>p>span:first-child]:text-gray-13 [&_.duet--article-byline-and]:text-gray-13')
                author = author_div.find('a').text.strip()
                published = soup.find('time').text.strip()
                published_date = published.split(',')[0] + published.split(',')[1]
                published_date = convert_date_format(published_date)
            else:
                # print(f"Handling in else part{url}")
                heading = soup.find('h1', class_='duet--article--feature-headline')
                heading_text = heading.text.strip() if heading else 'No heading found'
                author_div = soup.find('p', class_='duet--article--article-byline max-w-[550px] font-polysans text-12 leading-120')
                author = author_div.find('a').text.strip() if author_div else 'No author found'
                published = soup.find('time').text.strip() if soup.find('time') else 'No publish date found'
                
                match = re.search(r'Updated (\w+ \d{1,2}, \d{4})', published)
                if match:
                    date = datetime.strptime(match.group(1), "%b %d, %Y").strftime("%b %d %Y") 
                else:
                    date = published.split(',')[0] + published.split(',')[1]
                
                published_date = convert_date_format(date)

            paragraph_texts = []
            paragraphs = soup.find_all('p', class_='duet--article--dangerously-set-cms-markup duet--article--standard-paragraph mb-20 font-fkroman text-18 leading-160 -tracking-1 selection:bg-franklin-20 dark:text-white dark:selection:bg-blurple [&_a:hover]:shadow-highlight-franklin dark:[&_a:hover]:shadow-highlight-blurple [&_a]:shadow-underline-black dark:[&_a]:shadow-underline-white')
            if paragraphs:
                for p in paragraphs:
                    paragraph_texts.append(p.get_text())
                body_content = ' '.join(paragraph_texts)
            else:
                print("No paragraphs found")
                body_content = 'No content'

            return {
                'article_url': url,
                'title': heading_text,
                'Author': author,
                'published': published,
                'publish_date': published_date,
                'body': body_content,
            }
        else:
            print(f"Failed to fetch the URL: {url} with status code: {response.status_code}")
    except Exception as e:
        print(url)
        print(f"Handling in except: {e}")


# Main execution
if __name__ == "__main__":
    # Fetch article URLs
    total_article_links =[]
    link_class =[
                'dark:group-hover:shadow-highlight-blurple',
                'dark:group-hover:shadow-underline-franklin'
                ]
    for link in link_class:
        total_article_links= theverge_article_list(cookies,headers,residential_proxies ,ca_cert_path,link ,total_article_links)

    print(len(total_article_links))

    # Scrape details for each article
    articles_data = []
    for url in total_article_links:        
        article_details = theverge_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("theverge_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in theverge_articles.json")