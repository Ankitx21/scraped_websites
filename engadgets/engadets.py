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
    'A1': 'd=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI',
    'A3': 'd=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI',
    'A1S': 'd=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI',
    'cmp': 't=1722344972&j=0&u=1---',
    'gpp': 'DBAA',
    'gpp_sid': '-1',
    'axids': 'gam=y-OwmU7hlE2uJ8TCwmFLn76DgH4NZ6wBgr~A&dv360=eS13Y2YyRjF0RTJ1RWVaRGxXTEguYzdKdUdzOEdUYnlZWX5B&ydsp=y-qL.Qpg1E2uK2eQT83KSc6c7u.mi_GBqy~A&tbla=y-M3wvcy9E2uLlb3LzYYF13ZP77LFokx.V~A',
    'tbla_id': '290dbd19-1845-4973-a160-a510faeb227c-tuctda26b8e',
    'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D60aca256-e56f-4c88-a741-be55bdcdfbea-tuctda26b8e',
    'cto_bundle': 'LXH_j19scjkwTlp2VlZTVDRnM25LR0ZSdG5paUd4WW11aGVvSWwlMkJaeXhMaUV1bUFVQXRmSSUyQnpTZ1FYWGNCWjMlMkZHJTJGRkJBY2ZDMTJOcTVLJTJGYjdDNFJodmxrSzRGU2pFaVV1RmJvNVFPcmhnZzFPOEQyQXZYWGJHa210ZE9MejAzWUI2SmglMkIzOTRLRnBtQ2xBRTk4Q1UwVmkzS2clM0QlM0Q',
    '__gads': 'ID=1ddde46b9f0e9779:T=1722344975:RT=1722346047:S=ALNI_MbVMyumWo2wu4KAmTXv0op_11xeMg',
    '__gpi': 'UID=00000eadc42a1223:T=1722346112:RT=1722346112:S=ALNI_MZG97VrbvgQhgVi94QXLZzw390YLg',
    '__eoi': 'ID=d721f32c96871071:T=1722346112:RT=1722346112:S=AA-AfjbVvAGUmdkUmlI5rywQeCTg',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'A1=d=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI; A3=d=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI; A1S=d=AQABBAjmqGYCEFG10ABH4j-ASuZH3fpxPbwFEgEBAQE3qmayZlkWyyMA_eMAAA&S=AQAAAuddw77dBvBspiVjRC7RxFI; cmp=t=1722344972&j=0&u=1---; gpp=DBAA; gpp_sid=-1; axids=gam=y-OwmU7hlE2uJ8TCwmFLn76DgH4NZ6wBgr~A&dv360=eS13Y2YyRjF0RTJ1RWVaRGxXTEguYzdKdUdzOEdUYnlZWX5B&ydsp=y-qL.Qpg1E2uK2eQT83KSc6c7u.mi_GBqy~A&tbla=y-M3wvcy9E2uLlb3LzYYF13ZP77LFokx.V~A; tbla_id=290dbd19-1845-4973-a160-a510faeb227c-tuctda26b8e; trc_cookie_storage=taboola%2520global%253Auser-id%3D60aca256-e56f-4c88-a741-be55bdcdfbea-tuctda26b8e; cto_bundle=LXH_j19scjkwTlp2VlZTVDRnM25LR0ZSdG5paUd4WW11aGVvSWwlMkJaeXhMaUV1bUFVQXRmSSUyQnpTZ1FYWGNCWjMlMkZHJTJGRkJBY2ZDMTJOcTVLJTJGYjdDNFJodmxrSzRGU2pFaVV1RmJvNVFPcmhnZzFPOEQyQXZYWGJHa210ZE9MejAzWUI2SmglMkIzOTRLRnBtQ2xBRTk4Q1UwVmkzS2clM0QlM0Q; __gads=ID=1ddde46b9f0e9779:T=1722344975:RT=1722346047:S=ALNI_MbVMyumWo2wu4KAmTXv0op_11xeMg; __gpi=UID=00000eadc42a1223:T=1722346112:RT=1722346112:S=ALNI_MZG97VrbvgQhgVi94QXLZzw390YLg; __eoi=ID=d721f32c96871071:T=1722346112:RT=1722346112:S=AA-AfjbVvAGUmdkUmlI5rywQeCTg',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
}




def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%b %d %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def engadgets_article_list(residential_proxies ,ca_cert_path,cookies,headers):
    response = requests.get('https://www.engadget.com/', cookies=cookies, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)
    if response.status_code == 200:
        article_links =[]
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('main' ,class_ = 'W(100%)')
        if container:
            print('container found!')

        articles = container.find_all('a',class_='C(engadgetSteelGray)')
        if articles:
            for article in articles:
                link = article['href']
                if not link.startswith('https://www.engadget.com'):
                    url = 'https://www.engadget.com' + link
                    
                article_links.append(url)
        else:
            print("Article section was not found")            

        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

    


def engadgets_article_details(url):

    try:
        response = requests.get(url)
        if response.status_code ==200:
            soup = BeautifulSoup(response.content, 'lxml')
            title = soup.find('h1', id ='caas-lead-header-undefined').text.strip()
            if not title:
                print(f"Title not found for {url}")
            author = soup.find('div' ,class_='caas-attr-item-author').text.strip()
            if not author:
                author= ""

            published = soup.find('time').text.strip()
            if not published:
                print(f"published not found for {url}" )

            parts = published.split(", ")
            date_str = parts[1] + " " + parts[2]
            # date_str = date_str.replace(",", "")
            published_date = convert_date_format(date_str)

            paragraph_texts = []
            para_container = soup.find('div' ,class_='caas-body')
            paragraphs = para_container.find_all('p')
            if not paragraphs:
                print(f"body not found for {url}" )

            for para in paragraphs:
                para = para.text
                paragraph_texts.append(para)
                
            body_content = ' '.join(paragraph_texts)


            return {
                    'url': url,
                    'title': title,
                    'published': published,
                    'publish_date': published_date,
                    'author': author,
                    'body': body_content,
                }
                
        else:
            print( {'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            
            

    except Exception as e:
        print({'url': url, 'error': str(e)})


if __name__ == "__main__":

    total_article_links = engadgets_article_list(residential_proxies ,ca_cert_path,cookies,headers)

    articles_data = []
    for url in total_article_links:        
        article_details = engadgets_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("engadgets_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in engadgets_articles.json")