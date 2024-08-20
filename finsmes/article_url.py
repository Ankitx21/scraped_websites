import requests
from bs4 import BeautifulSoup

def scrape_finsmes_article_links():
    residential_proxies = {
        'http': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225'
    }

    ca_cert_path = 'ca.crt'

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    url = "https://www.finsmes.com/"

    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')
        for h2_tag in soup.find_all('h3', class_='entry-title td-module-title'):
            a_tag = h2_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                article_links.add(a_tag['href'])

        for link in article_links:
            print(link)
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

scrape_finsmes_article_links()
