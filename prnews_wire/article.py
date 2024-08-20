import requests
from bs4 import BeautifulSoup
import time

def scrape_businesswire_article_links(retries=3):
    residential_proxies = {
        'http': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225'
    }

    ca_cert_path = 'ca.crt'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'AMCVS_A807776A5245B2E10A490D44%40AdobeOrg=1; __cf_bm=3HDAGMbN73i1ex8f7o3VXq14TJjzFmctoxo.4GuHlbo-1723961111-1.0.1.1-aRmphivhMwszkrRVeZ2ouwyZ1KhBOiTb4vLcBp4dkUBpW5e5esqqoUpthUb21ByOgmI073Wtfzh2SqKFI7KcDA; AMCV_A807776A5245B2E10A490D44%40AdobeOrg=179643557%7CMCIDTS%7C19954%7CMCMID%7C20437730203168731479034136563262621208%7CMCOPTOUT-1723968317s%7CNONE%7CvVersion%7C5.5.0; __cf_bm=BIdrF4f0PUCpm_lzXBe23AZpLps1B7CjoE_UJb2dn6M-1723961115-1.0.1.1-5gyyvbphsmNOi1zakOHAELOy_Mg2w0t63p.YAchQHogR7HjK2fmd6G3VlpHg8H7SBWm88xtCrzLaerDce0Xk8g; __cf_bm=_lRdLCPfrTyo0Q63py8bSQ3NOyFY4VCBrD.UJZZp3UU-1723961228-1.0.1.1-ux9Qd6LYacnv1bfaRr7CFo2eu2gsk4eqI2744k1lqpWJJ4MPbFJar49WTv0bp0wYVl7f658zMTGL7E7jY0czmg',
        'if-modified-since': 'Sun, 18 Aug 2024 06:05:10 GMT',
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

    url = "https://www.prnewswire.com/news-releases/financial-services-latest-news/financing-agreements-list/"


    article_links = set()
    
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
            response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all links with the specified class
                links = soup.find_all('a', class_='newsreleaseconsolidatelink display-outline w-100')
                
                # Extract href attribute and create full URL
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = f"https://www.prnewswire.com{href}"
                        article_links.add(full_url)
            
            break  # Exit loop if successful

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            time.sleep(2)  # Wait before retrying

    return article_links

# Example usage
if __name__ == "__main__":
    links = scrape_businesswire_article_links()
    for link in links:
        print(link)
