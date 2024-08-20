import requests
from bs4 import BeautifulSoup

def scrape_globenewswire_article_links():
    residential_proxies = {
        'http': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225'
    }

    ca_cert_path = 'ca.crt'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': '__RequestVerificationToken=MbKd2CLlRY1by1ZKeQGi6B_CRmfwKPACzD4GoRqsvutLwd1NZNy44Ez2qyEZVkK2AnFN6Kjdmp9pvNysPEjUEr2Q5z01; ASP.NET_SessionId=4lirgd4xr2mi3ftprum1m00j; ak_bmsc=780A87EC3E21C51D50CCCEADF4E69D31~000000000000000000000000000000~YAAQD/Y3F9IYZ12RAQAANCXfYxjJR3LRx3Nl0lhYjsQBsiWBCUo+CElzSCJpGacdKRRJ9720vnizFq4UHxi9VMyTj9Nsir6boYRDJNS4W1cZKDNExlHuTjfbI2XiFAC2IT/els/Uhads6S6qZyQoqUUiJXehiLptlal9WsrkD/4zOyY2Rzt8+xjhpqAz5SQFjwrV5FILjM/ymRBuzEJE1Fv7d6fP0LiZElRv8NKZIfH2LrRLD82/ShkNIynn1VBc6YjnOB9SHIFrLwBonJFTUXMYDk86Iocl6YXSvaxYfKkB1cvwcJir5n0yklYTHJxpUPTOJlK2y5LpaAV3jRQfxC149dxdlHqsxWPc7GG+PDP8PhIrVEVSfRWn1hmN4ElsvO7gRG2PZSs4VMKO/5m1EcTfScc+1BaRqUMHcjddYJrtyAulC2O6rZG5bmyJ0XCCiSRZY7DbtoMhIzGxmZNy80A1gW791v5SFZyyV0Z2dEz2LlYAQarpDC8lP1+/1A==; bm_sv=ECF05B7F2D3A154E61033FB5DAEBC9B9~YAAQD/Y3F/JjZ12RAQAAvdfrYxjw/hnyzUE3StlMfsfVNcIsDbMHpHAPUMh8k525ILAe99V9kB2CXk7BYVlLLJZyTXK6gn9ireNdkBv9b63Qn2IyJCyzIXEjdB4dVIMJ+4Fy7fYjZsVqix2gFz2+yuG40dxr7QfwrN86xgO72ZLe2BylHab78b7c95j/feOE71zUylzyGQncvt2f7q6eUHF/DLI9VYKTzl2/0N+duqFzFFv/TMYmTm2EN9uc915PXxmyLkzuM9k=~1; bm_sv=ECF05B7F2D3A154E61033FB5DAEBC9B9~YAAQFa3OFwe0SmKRAQAAujrzYxjFbNSRZ6qh192moX31TAo0y1DaoHM9uBj2CNHIW6kzQDcWhswOo660OGH4Q/JY6v78J8jeE5yUnVfRgPSSYEb7xUqWZuBqdahqmWXVcGqqHPIoGpk4SKKuv9NfKkp2r2fJaHx6Rw1CNgOIb7gdn3h233pG9fkqR866x1x18bu8klbQatNfWeExcMhb18L3PcFmoHR/GktYSOQJkUxDtetT9OIU9Jr67iLJhkErnJV0bXEIO/Q=~1',
        'if-modified-since': 'Sun, 18 Aug 2024 05:04:21 GMT',
        'priority': 'u=0, i',
        'referer': 'https://www.globenewswire.com/search/date/24HOURS/subject/fin',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    url = "https://www.globenewswire.com/newsroom"

    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting hrefs for all <a> tags with the attribute 'data-section' = 'article-url'
        links = soup.find_all('a', {'data-section': 'article-url'})
        for link in links:
            article_url = link.get('href')
            if article_url:
                # Convert relative URLs to absolute URLs
                if not article_url.startswith('https'):
                    article_url = 'https://www.globenewswire.com' + article_url
                article_links.add(article_url)

        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

if __name__ == "__main__":
    article_urls = scrape_globenewswire_article_links()
    if article_urls:
        for url in article_urls:
            print(url)
