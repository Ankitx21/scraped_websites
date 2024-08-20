import requests
from bs4 import BeautifulSoup
import re

def scrape_techcrunch_venture_article_links():
    residential_proxies = {
        'http': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225'
    }

    ca_cert_path = 'ca.crt'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': 'A1=d=AQABBCcnv2YCEOoJzC9Y4StFhMpboVZWzgwFEgEBAQF4wGbJZlkWyyMA_eMAAA&S=AQAAAhIGl5gaM6cMDgjFceyZSoM; A3=d=AQABBCcnv2YCEOoJzC9Y4StFhMpboVZWzgwFEgEBAQF4wGbJZlkWyyMA_eMAAA&S=AQAAAhIGl5gaM6cMDgjFceyZSoM; A1S=d=AQABBCcnv2YCEOoJzC9Y4StFhMpboVZWzgwFEgEBAQF4wGbJZlkWyyMA_eMAAA&S=AQAAAhIGl5gaM6cMDgjFceyZSoM',
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

    url = "https://techcrunch.com/category/venture/"

    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Regular expression to match URLs with date format after techcrunch.com
        date_pattern = re.compile(r'^https://techcrunch\.com/\d{4}/\d{2}/\d{2}/')

        # Searching for anchor tags that contain 'href'
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Apply the date pattern filter
            if date_pattern.match(href):
                article_links.add(href)

        # Print all collected article links
        for link in article_links:
            print(link)
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

scrape_techcrunch_venture_article_links()
