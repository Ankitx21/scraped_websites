import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B%d,%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def bussiness_wire_article_list():

    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}

    url = "https://www.businesswire.com/portal/site/home/news/subject/?vnsId=31355"

    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=HGMPOIIPKMLKIGALGKICENADIBGJHLPOMEJDLAFMPFOOGKMMJFNCGOPFDCLBHOBMCBPDJLODLKJGCFMKPEJADHAMDCJHIGDKDEAOEFKEKICACOPPKNPALOGPACBIBCPD; portal.JSESSIONID=6kg0mHqGyjq3nmV3JQvfL2KcJW4PV7m0kFXDwhqZctSWKVwpZy3k!686088036!-400328206; TS01d0bfe4=0102e294400441977e5fd2b40d9fc763d15cf8abc88f33ba89a77d6085b7ea99e8a9b88c0d0dc4ca1aba076960de0d279b89c08c60fdf6bcf14a89c51db8ea083ea4b1c84c; ak_bmsc=54F93BECA9E6D8811E5E5485BAC6C240~000000000000000000000000000000~YAAQfXYsMZl+v3eRAQAAnyb+eRiP5bglg2SAXi6GC8DCRmwhaVPiNuTLV2roGyPfObfy/8DJOsi0TahBl+0I7uZlgEvjc4ZxMKwTK52UZzOqKkYkTsrzsUpyRQoeBn53bj7WNbUF9+fDlVXzj2XXeelfsJ2nF6Xdo7fNPgH0HGpdf5Nbowr/qRSfT7uDifqaKbKGiz41qk2AITNRlaiXkuOPbzRe3n9OJNYPr7Jh6yNRIv5iWYfYoBKx4mz8S/dsOOb+9IoNoEb0+ciX++dzhw9AK9A/+jixupxBPyuB83LNcU0rGGscBuwRGMo41j7pNwQ9Yx25b+M+5psM8c6rSBlJHeMTGkJE7ncPIQpvU6ppeiE/ebigTlZwGvlRKcvPrWmxvzdo4/d4EEV4jbgPbw1fnekqt5Tv/1FE9FxqWN4MUbYkXyk1/EGh8/gFf3zQww5Lw61GDw==; TS01c09a27=0102e294408956b9ba6a2582d87ead8f8fa706ab498f33ba89a77d6085b7ea99e8a9b88c0d74e96cf7ed7c72e34f314256df15e13016d63f685cded7a58bc2bd56519c96cf; bm_sv=82906AF7EA30CF990CD8610C5B1EA461~YAAQfXYsMbN+v3eRAQAAxSj+eRiSdG1QpL5HjFOWb9nvUUSjeLyTvowO/jIeHBCUwDtSt9ouGFQ0/6mLlrw7aRvg58svkn3bKsNQ4r+z7QHiVLsybfVGRoXy1rSnCsRU7jywNaC3vJL7BAPk6Oo2ff6BWioMmVRvcZnQ4HmfofscgKii75qT/+Y8bnorjf9oaxRygIEHIv++kOfdeBIfj2RngadzZDZqwML1MDTjaaCAnsJ7UHZxmcgPzxYU9sH8skCczMi0~1; _gcl_au=1.1.284380982.1724328586; _ga=GA1.1.1663181325.1724328587; __hstc=241090844.b5c5e64e8616334c6e7f76b06b2fe50c.1724328587118.1724328587118.1724328587118.1; hubspotutk=b5c5e64e8616334c6e7f76b06b2fe50c; __hssrc=1; __hssc=241090844.1.1724328587118; _ga_ZQWF70T3FK=GS1.1.1724328586.1.0.1724328587.59.0.0; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+22+2024+17%3A41%3A25+GMT%2B0530+(India+Standard+Time)&version=6.4.0&hosts=&consentId=b20d5811-49e0-49c6-905d-ca23d708e0a4&interactionCount=1&landingPath=https%3A%2F%2Fwww.businesswire.com%2Fportal%2Fsite%2Fhome%2Fnews%2Fsubject%2F%3FvnsId%3D31355&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1',
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

    response = requests.request("GET", url, headers=headers, data=payload)
    ca_cert_path = 'ca.crt'
    # print(response.text)


    # response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('ul' ,class_ = 'bwNewsList')
        if container:
            print('container found!')

        h1= container.find_all('a' ,class_= 'bwTitleLink')
        if h1:
            for tag in h1:
                link = tag['href']
                if 'https://www.businesswire.com/' not in link:
                    url = 'https://www.businesswire.com'+link
                    # print(url)
                    article_links.add(url)
        print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

# bussiness_wire_article_list()


def bussiness_wire_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_= ['epi-fontLg bwalignc','epi-fontLg'])
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author=""

            # Extract the published date
            published_tag = soup.find('time')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                parts = published.split(' ')
                date = parts[0]+parts[1]+parts[2]
                published_date = convert_date_format(date)
                # print(published_date)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            paragraphs = soup.find_all('div', class_='bw-release-story')
            # print(len(paragraphs))
            if paragraphs:
                for para in paragraphs:
                    paragraph_texts.append(para.text.strip())
                body_content = ' '.join(paragraph_texts)
                # print(body_content)
            else:
                body_content = ""
                missing_fields.append("Body Content")
            
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

    total_article_links = bussiness_wire_article_list()
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = bussiness_wire_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample_outputs/bussiness_wire_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in bussiness_wire_articles.json")