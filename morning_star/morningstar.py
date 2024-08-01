
import requests

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
    'msession': 'd056bf85-3c95-445d-83ea-7a420b8478e2.8b7f2a4dea5869b0d297471440c8701681cd21a7ac7c321727330f2f1f10c60d',
    'mid': '10621179049021167403',
    '_gcl_au': '1.1.855271061.1722352658',
    '_cb': 'B3bVVpBegQQ0BkMH-N',
    '_cb_svref': 'external',
    '_ga': 'GA1.2.235679065.1722352669',
    '_gid': 'GA1.2.1531668638.1722352672',
    '_uetsid': 'e3e673a04e8611efbc28d14977a33c35',
    '_uetvid': 'e3e6d0704e8611efaae03f96d1474f43',
    '_gd_visitor': 'b9c52cfb-4487-4c3e-8cf8-0b1107866993',
    '_gd_session': '68a56cdc-caa9-4af8-8a88-0e37765c4419',
    '_an_uid': '142607902762018855',
    'ELQCOUNTRY': 'IN',
    'ELOQUA': 'GUID=3827C6982A3242C6AA382F809F8C2889',
    '_v__chartbeat3': 'BuwEVOnhvJrDjw3O9',
    'mbuddy': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXSyIsImtpZCI6IjE2NjYwMjExMjkifQ.eyJzZXNzaW9uIjoiZDA1NmJmODUtM2M5NS00NDVkLTgzZWEtN2E0MjBiODQ3OGUyLjhiN2YyYTRkZWE1ODY5YjBkMjk3NDcxNDQwYzg3MDE2ODFjZDIxYTdhYzdjMzIxNzI3MzMwZjJmMWYxMGM2MGQiLCJpYXQiOjE3MjIzNTM5OTEsImlzcyI6Imh0dHBzOi8vaW52ZXN0b3IubW9ybmluZ3N0YXIuY29tIiwiZXhwIjoxNzIyMzU0MjkxfQ.N6WCW30TIJpG4pZXHdMuT6XmmLd_RClS6yM2_6eR_gUtJeKkQJXR0G62In56Q14kS-TFCKbhwEM2w8-Mv--H4SAmO12tR90flSneuR3sL2tvZ7Kbbn9HrRM4G6TqIPf0WRRcfvu1dl5IdmWPoVmqRb0h9pb2o0dh1AnJ6NgDt22y6DQeZoTeqQ3bTCzsm8-m0xD5RfpUjDc-bnQ3vivxmPXfIpdhZb5r4uhCGtEV0kLkcZH6NrxebhDSQfplLvaZ_iIA0fkUj-0ewGO6p1B_u2KG54_JzpUbCCehPYyU2OwM5PJnaIeLF3N3kEmVcxHVn552Pb2lGhpHz0UblEXTkA',
    '_chartbeat2': '.1722352671422.1722354070338.1.CX3T43jONjlCHau2bBmWY25CwW6Hn.7',
    '_ga_G8C0R44VCK': 'GS1.1.1722352669.1.1.1722354072.40.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'msession=d056bf85-3c95-445d-83ea-7a420b8478e2.8b7f2a4dea5869b0d297471440c8701681cd21a7ac7c321727330f2f1f10c60d; mid=10621179049021167403; _gcl_au=1.1.855271061.1722352658; _cb=B3bVVpBegQQ0BkMH-N; _cb_svref=external; _ga=GA1.2.235679065.1722352669; _gid=GA1.2.1531668638.1722352672; _uetsid=e3e673a04e8611efbc28d14977a33c35; _uetvid=e3e6d0704e8611efaae03f96d1474f43; _gd_visitor=b9c52cfb-4487-4c3e-8cf8-0b1107866993; _gd_session=68a56cdc-caa9-4af8-8a88-0e37765c4419; _an_uid=142607902762018855; ELQCOUNTRY=IN; ELOQUA=GUID=3827C6982A3242C6AA382F809F8C2889; _v__chartbeat3=BuwEVOnhvJrDjw3O9; mbuddy=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXSyIsImtpZCI6IjE2NjYwMjExMjkifQ.eyJzZXNzaW9uIjoiZDA1NmJmODUtM2M5NS00NDVkLTgzZWEtN2E0MjBiODQ3OGUyLjhiN2YyYTRkZWE1ODY5YjBkMjk3NDcxNDQwYzg3MDE2ODFjZDIxYTdhYzdjMzIxNzI3MzMwZjJmMWYxMGM2MGQiLCJpYXQiOjE3MjIzNTM5OTEsImlzcyI6Imh0dHBzOi8vaW52ZXN0b3IubW9ybmluZ3N0YXIuY29tIiwiZXhwIjoxNzIyMzU0MjkxfQ.N6WCW30TIJpG4pZXHdMuT6XmmLd_RClS6yM2_6eR_gUtJeKkQJXR0G62In56Q14kS-TFCKbhwEM2w8-Mv--H4SAmO12tR90flSneuR3sL2tvZ7Kbbn9HrRM4G6TqIPf0WRRcfvu1dl5IdmWPoVmqRb0h9pb2o0dh1AnJ6NgDt22y6DQeZoTeqQ3bTCzsm8-m0xD5RfpUjDc-bnQ3vivxmPXfIpdhZb5r4uhCGtEV0kLkcZH6NrxebhDSQfplLvaZ_iIA0fkUj-0ewGO6p1B_u2KG54_JzpUbCCehPYyU2OwM5PJnaIeLF3N3kEmVcxHVn552Pb2lGhpHz0UblEXTkA; _chartbeat2=.1722352671422.1722354070338.1.CX3T43jONjlCHau2bBmWY25CwW6Hn.7; _ga_G8C0R44VCK=GS1.1.1722352669.1.1.1722354072.40.0.0',
    'if-none-match': '"e3373-eAsnrXHpxRR2vgWyekT9BC8AC5I"',
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
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def morningstar_article_list(residential_proxies ,ca_cert_path,cookies,headers):
    response = requests.get('https://www.morningstar.com', cookies=cookies, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    
    if response.status_code == 200:
        article_links =[]
        soup = BeautifulSoup(response.content ,'lxml')

        direct_anchor = soup.find_all('a',class_='mdc-grid-item__title')
        for links in direct_anchor:
            link = links['href']
            if not link.startswith('https') and '/best-investments/' not in link:
                url = 'https://www.morningstar.com' + link

            if url not in article_links:
                article_links.append(url)

        ul_links = soup.find_all('ul' ,class_='mdc-content-list-grid-item__links')
        for ul in ul_links:
            links= ul.find_all('a')

            for link in links:
                link = link['href']
                if not link.startswith('https'):
                    url = 'https://www.morningstar.com' + link

                if url not in article_links:
                    article_links.append(url)

        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})


def morningstar_article_details(url):
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

            # Extract the author
            author_tag = soup.find('span', class_=['story__byline-text__mdc', 'mdc-link__mdc mdc-link--no-underline__mdc'])
            if author_tag:
                author = author_tag.text.strip()
            else:
                    
                author =""
                missing_fields.append("Author")

            # Extract the published date
            published_tag = soup.find('time')
            if published_tag:
                published = published_tag.text.strip()
                published_date = convert_date_format(published)
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
            para_container = soup.find_all('div', class_=['mdc-story-body__mdc mdc-story-body--large__mdc story__body__mdc', 'specials__rich-text-content specials__body'])

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


if __name__ == "__main__":

    total_article_links = morningstar_article_list(residential_proxies ,ca_cert_path,cookies,headers)
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = morningstar_article_details(url)
        # print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    articles_data.append(article_details)
    with open("morningstar_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in morningstar_articles.json")