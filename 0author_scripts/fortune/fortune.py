import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%Y/%m/%d")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def fortune_author_details(author_link):

    response = requests.get(author_link)
    # print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_linkedin=''
    author_twitter=''
    author_img=''
    author_name = soup.find('h1' , class_='sc-bc5dbd8-0 sc-e7a39763-1 iKMmeb doNfRC').text.strip()
    author_image = soup.find('div' ,class_='sc-e7a39763-2 jKGwyj')

    if author_image:
        author_img = author_image.find('img')['src']
    else:
        author_img=""
        
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details

def fortune_article_list():

    base_url = "https://fortune.com/"

    residential_proxies = {'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'}
    
    ca_cert_path = 'tem_ca.crt'

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_vwo_uuid_v2=DCD1E05F115A9A945941D2C2F5D0DC2ED|d761ac1c16c696026f5937e7ec240c83; pushly.user_puuid_GvbR9fxg=Ahfglpx1RxK9CzIcOueNyyf0T1YTenAT; _pnss_GvbR9fxg=none; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBmAVgCZ%2B3ABwB2cQDYB40fwAMIAL5A; _pcid=%7B%22browserId%22%3A%22lz9wrshm3h03ewbz%22%7D; __pid=.fortune.com; __pat=-14400000; _pbjs_userid_consent_data=3524755945110770; _li_dcdm_c=.fortune.com; _lc2_fpi=00366f952340--01j44h4axmzwd4593sgrxwv7sq; _pubcid=dab487b4-4f6f-4644-8e1c-50fe4d49f6f7; cX_G=cx%3A1gs1g24nstwp51ms3ujd003qer%3A39sx8lloxbbqs; permutive-id=45ee7083-b9f3-4ca2-abda-d60e025d3e4b; _pnlspid_GvbR9fxg=29459; ajs_anonymous_id=a54a6391-e327-46b4-9902-b927cc5cb80d; _ga=GA1.1.1936473159.1722434075; _gcl_au=1.1.93871804.1722434075; _lr_retry_request=true; _lr_env_src_ats=false; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://fortune.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1722434076660%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=3db77d5f-a737-4eef-8ea9-f5d7e9d69a71%22%2C%22session_count%22:1%2C%22last_session_ts%22:1722434076660}; _ce.irv=new; cebs=1; _ce.clock_event=1; pbjs-unifiedid=%7B%22TDID%22%3A%22db70ec1e-7260-4161-b586-dfacdfd438bf%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-07-31T13%3A54%3A37%22%7D; panoramaId_expiry=1722520477310; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; __li_idex_cache_e30=%7B%7D; pbjs_li_nonid=%7B%7D; _ce.clock_data=505%2C152.58.16.203%2C1%2Cc28c178f7fc01e92a5161b6c80153add%2CEdge%2CIN; _CEFT=Q%3D%3D%3D; bounceClientVisit6717v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgGYD2ATggK4B2ApgHQDGpAtkSADQjkwhcgAligD6Ac1IiUdFCkGkaMYgEMw07sPEQpMuQqWrpAXyA; __pnahc=0; __pvi=eyJpZCI6InYtbHo5d3JzaXJobmtqZ3U1dyIsImRvbWFpbiI6Ii5mb3J0dW5lLmNvbSIsInRpbWUiOjE3MjI0MzQxMTkxMjh9; __tbc=%7Bkpex%7DfXfGjj5poN4GJhijJ-LSb-OfhPYOwqyObQhWQKNQf29gXV-1yL6pUGiO6fHiK9w0; xbc=%7Bkpex%7Dy-v5j-NmbMgnRKQvRGNIRHLBsxr4b55HfwBSbzR7oio; _pcus=eyJ1c2VyU2VnbWVudHMiOnsiQ09NUE9TRVIxWCI6eyJzZWdtZW50cyI6WyJMVHM6MDVjNTVjYTVmODM1ZDk0N2YxNjBjYjRkZDJmZTg3ZmFlZDE2N2IyMTo5IiwiTFRjOjE2NmIxNDEzMzViYWJlODJjMmRiMWFhNTM1NGIzZTkwNjUzMmY5ODk6bm9fc2NvcmUiLCJDU2NvcmU6NjE0NzMxN2NmZjEzYjRhNTljMzBlOWJhNGQwMTdjODBlNTRkMmRjMjpub19zY29yZSIsIkxUcmVnOmQ1NzUxODQ4NzU1ZmU2MDUwYzk0OWJhY2M3Y2YxMDY2NGEwOWE0MWE6NSIsIkxUcmV0dXJuOmUwNmFhMTFlNmNlMmNlNzcxMDFlZDg2ZTRhYmMwNGFhZTNmZDNhN2Q6NiJdfX19; cebsp_=3; _ga_T498R2CHRG=GS1.1.1722434075.1.1.1722434221.0.0.0; cX_P=lz9wrshm3h03ewbz; __gads=ID=6b7c692932b2cb48:T=1722434074:RT=1722435635:S=ALNI_MbWVEG-VhNCsGDomMWdkGRXRlDNWw; __gpi=UID=00000eaf67503499:T=1722434074:RT=1722435635:S=ALNI_MZDBFbd61beXdMQUqD-evW7h0Q12A; __eoi=ID=9ca5d673baf11f5c:T=1722434074:RT=1722435635:S=AA-AfjYMUJHcje8xz_lHbiaZ4UoS; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jul+31+2024+19%3A51%3A12+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=1311a5dd-98eb-4ce6-8b6a-f7ec507128c3&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Ffortune.com%2F&groups=C0001%3A1%2CC0003%3A1%2CSSPD_BG%3A1%2CC0005%3A1%2CC0004%3A1%2CC0002%3A1; _ce.s=v~f79cabb6d3df54c30783b5c1c6929e3c2bd50837~lcw~1722435668810~lva~1722434077746~vpv~0~v11.cs~388300~v11.s~6dec5530-4f44-11ef-b947-6df8f7a7e84b~v11.sla~1722435668807~gtrk.la~lz9xq0vy~v11.send~1722435672722~lcw~1722435672722; bounceClientVisit6717=N4IgJglmIFwgjAJkQThQBhQdgCzoBwBsAzMTvouuiADQgBuUs8WyOZBArIp8YvljoAzegBdmrROxxJBIAIYB7WOjoAbAA6wQAC1GiNAZwCkxAILHEAMUtWhigE6iArgDsApgDoAxooC2trQKhip09Br0sIh00HDQdA7aQd5iEmwc+Jx0hkww8MR0AObeiTDIdH6hIGqpeZLSsjGFVhAOhqIAMorysaIOzu4AvkA',
    'if-none-match': '"gfnjc31pizb917"',
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
    response = requests.get(base_url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    
    if response.status_code == 200:
        article_links =[]
        soup = BeautifulSoup(response.content ,'lxml')

        articles = soup.find_all('a', class_ = 'sc-93594058-0 fowfrQ title-link styled-custom-link')
        if articles:
            for article in articles:
                link = article['href']
                url = link

                if 'recommends' not in link and 'ranking' not in link :
                    if url not in article_links:
                        article_links.append(url)
                
        else:
            print("Article section was not found")            
        print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})


def fortune_article_details(url):
    missing_fields = []  # List to store missing fields
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
        auth_container = soup.find('div', class_="sc-4fb61e76-5 inTIUb")
        if auth_container:
            author_tag = auth_container.find('a')
            author_info = fortune_author_details(author_tag['href'])
            if author_tag:
                author = author_tag.text.strip()
            else:
                author = ""
                missing_fields.append("Author")
        else:
            author = ""
            missing_fields.append("Author Container")

        # Extract the published date
        date_pattern = re.compile(r'/(\d{4}/\d{2}/\d{2})/')
        match = date_pattern.search(url)
        if match:
            published = match.group(1)
            published_date = convert_date_format(published)
        else:
            published=""
            published_date = ""
            missing_fields.append("Publish Date")

        # Extract the body content
        paragraph_texts = []
        para_container = soup.find('div', class_='rawHtml-content-no-nativo')
        if para_container:
            paragraphs = para_container.find_all('p')
            if paragraphs:
                for para in paragraphs:
                    paragraph_texts.append(para.text)
                body_content = ' '.join(paragraph_texts)
            else:
                body_content = ""
                missing_fields.append("Paragraphs")
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
            'published_date': published_date,
            'author': author,
            'author_info':author_info,
            'body': body_content,
        }

    #         return None

    # except Exception as e:
    #     print({'url': url, 'error': str(e)})
    #     return None


if __name__ == "__main__":

    total_article_links = fortune_article_list()

    articles_data = []
   
    for url in total_article_links:        
        article_details = fortune_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file  scraped_websites\zzsample outputs
    with open("fortune_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in fortune_articles.json")

