import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B%d,%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def blockworks_author_details(author_link):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_cb=ChIZ6zBniKWrD-lZxL; _ga=GA1.1.1583271354.1724155948; _fbp=fb.1.1724155948649.427331574309775685; __qca=P0-1977108577-1724155947981; _cb_svref=external; cf_clearance=CnBL16YWE.BoeZGE6Dt2a8fnOFRtZMgDCsF5eW.y8Go-1726149185-1.2.1.1-XGILgPIMGElDch.sWZcwxAb4ADf3KjMY911w6RV_RAVjH1QCvZcmuJ9fWH5is0MGWREUjswHrb9mVYdkc.iERn1vrcwXY4r4BPRkW3JfoGdZmJFauTT6F7rk5aO.4cu2KpbkGy585__RpkMMTJG8y_ttGoKbeXFqsPOLDgFpfU9Qi82sChed5vha7Oa6ZG5E5kPNAqMTRCyYpiPHoq34AZtdJS0sPxHFBOqSYH7WQNibk5GTklio835I_avUPYIvDJQLof0rZzVyhHWPi.mlAIJOReRL6uPH2IP2Ccq9WZEHAYCko_qONAJjxshCTlMqCPBwNvet2JYpUB8.fp9.KlB26gY2ygfHz4wnLfWcJsRUKn3TF6_XcTiFRXUYfQJYIO7ywpgZbQwMJ1HaQq23q4RgWmFGBDaOonAT0FYm0IQ; __gads=ID=6f085d0ee8e3e86d:T=1724155947:RT=1726149191:S=ALNI_MYf4QCxoch3Fx4cjHIa_VOEjH8VpQ; __gpi=UID=00000ecdd3773d49:T=1724155947:RT=1726149191:S=ALNI_MYOhynXbx6v2m9ZZlq_X869tPXfdQ; __eoi=ID=b3e3e645b6f07de0:T=1724155947:RT=1726149191:S=AA-AfjY30nHufXqiB_VxxQO8RWPK; _chartbeat2=.1724155947222.1726149482870.0000000000000001.DNl91TB9vUJC1AZ_RDGatVaKbZc7.7; _ga_GYL4BXXQX8=GS1.1.1726149185.3.1.1726149483.40.0.0; __cfwaitingroom=ChhjL1NmRWxPSGc4Ky85Tk0xTUtOS0RBPT0SlAJsdXZTb2lFN2x6QVNHTHlwdVVJUGE4MFhQeWpac09VS3FBdkJnNzBYK3NjQWo5RlhjaDBMY3dSTnk1Z0NLV1g4UVNVMnFOOGtnN2NLWEtaVDJIRjQ0YWlKb292MzBKdU1vK3ZtbkFPMnJtNHRwcUwxV1RSd1R2OStPQUhlQ3Zxb2RvbnFsUDUxMjMxVC9zUGNCMS9ETUluMVhQSG51SXRRQ0x4aDVYS1RwUDJsWHhUWTI4SXd6UFlhTVhrVElXU25rUDV5TWN0OHZHY2hDYnhtKzEzUHdnM3ZOdkJjQnE4RUd2R0VkbW5VYzRqYlRyTEJRc2NmS1dXWmRaMHZuVFBnS09takVrV2E0NjJkdEFjZUpvST0%3D; __cfwaitingroom=ChgzZi9MNllUa0dIN1YvUSt5MWdFVEhRPT0SlAJBbndET0pxUUpZcUJ5QS9id1VsS1dTODNBbXFPek9jQzdsc2kxN2FjeG9xZi9XZWNWaHNMS0hhaTVCWXNFQ2t4YnRyUWN2Z210bFZqb2tGbnVTZjFMc1BMTzBCdmVJTUFiUWYwNXNpZktPTHNyR1l5UnF2dlhHMGVNYUZxbWZEYkpVNndhRGpaSlVXRHQzaisxcDVLZE1yVVdCMWFiODUydGdlV3c3OThubGw5dGdGWmhHQnZwYUlxbU1MNFM4eEFTWUoybSs4SndnL1A0am0ya0dFWjB1SzJBdmJmV0k0Y3l0VVNCNmJibnk1NncvcUZvMmt6VmZsb2pwN21NUWtrUVU0eEppbDdrUVU0K0JTbUEzZz0%3D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    response = requests.request("GET", author_link,proxies=proxies , verify=ca_cert_path ,headers=headers)
    # print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_linkedin=''
    author_twitter=''
    author_img=''
    author_name = soup.find('p' , class_='self-stretch flex-grow-0 flex-shrink-0 w-full text-5xl text-left text-white').text.strip()
    # print(author_name)
    author_image = soup.find('div' ,class_='flex flex-col justify-start items-start flex-grow-0 flex-shrink-0 bg-[#f8b4e4]')

    if author_image:
        author_img = 'https://blockworks.co'+author_image.find('img')['src']
        
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details


def blockworks_article_list():
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}

    ca_cert_path = 'ca.crt'

    url = "https://blockworks.co/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_cb=ChIZ6zBniKWrD-lZxL; _ga=GA1.1.1583271354.1724155948; _fbp=fb.1.1724155948649.427331574309775685; __qca=P0-1977108577-1724155947981; _cb_svref=external; cf_clearance=CnBL16YWE.BoeZGE6Dt2a8fnOFRtZMgDCsF5eW.y8Go-1726149185-1.2.1.1-XGILgPIMGElDch.sWZcwxAb4ADf3KjMY911w6RV_RAVjH1QCvZcmuJ9fWH5is0MGWREUjswHrb9mVYdkc.iERn1vrcwXY4r4BPRkW3JfoGdZmJFauTT6F7rk5aO.4cu2KpbkGy585__RpkMMTJG8y_ttGoKbeXFqsPOLDgFpfU9Qi82sChed5vha7Oa6ZG5E5kPNAqMTRCyYpiPHoq34AZtdJS0sPxHFBOqSYH7WQNibk5GTklio835I_avUPYIvDJQLof0rZzVyhHWPi.mlAIJOReRL6uPH2IP2Ccq9WZEHAYCko_qONAJjxshCTlMqCPBwNvet2JYpUB8.fp9.KlB26gY2ygfHz4wnLfWcJsRUKn3TF6_XcTiFRXUYfQJYIO7ywpgZbQwMJ1HaQq23q4RgWmFGBDaOonAT0FYm0IQ; __gads=ID=6f085d0ee8e3e86d:T=1724155947:RT=1726149191:S=ALNI_MYf4QCxoch3Fx4cjHIa_VOEjH8VpQ; __gpi=UID=00000ecdd3773d49:T=1724155947:RT=1726149191:S=ALNI_MYOhynXbx6v2m9ZZlq_X869tPXfdQ; __eoi=ID=b3e3e645b6f07de0:T=1724155947:RT=1726149191:S=AA-AfjY30nHufXqiB_VxxQO8RWPK; _chartbeat2=.1724155947222.1726149482870.0000000000000001.DNl91TB9vUJC1AZ_RDGatVaKbZc7.7; _ga_GYL4BXXQX8=GS1.1.1726149185.3.1.1726149483.40.0.0; __cfwaitingroom=ChhjL1NmRWxPSGc4Ky85Tk0xTUtOS0RBPT0SlAJsdXZTb2lFN2x6QVNHTHlwdVVJUGE4MFhQeWpac09VS3FBdkJnNzBYK3NjQWo5RlhjaDBMY3dSTnk1Z0NLV1g4UVNVMnFOOGtnN2NLWEtaVDJIRjQ0YWlKb292MzBKdU1vK3ZtbkFPMnJtNHRwcUwxV1RSd1R2OStPQUhlQ3Zxb2RvbnFsUDUxMjMxVC9zUGNCMS9ETUluMVhQSG51SXRRQ0x4aDVYS1RwUDJsWHhUWTI4SXd6UFlhTVhrVElXU25rUDV5TWN0OHZHY2hDYnhtKzEzUHdnM3ZOdkJjQnE4RUd2R0VkbW5VYzRqYlRyTEJRc2NmS1dXWmRaMHZuVFBnS09takVrV2E0NjJkdEFjZUpvST0%3D; __cfwaitingroom=ChgzZi9MNllUa0dIN1YvUSt5MWdFVEhRPT0SlAJBbndET0pxUUpZcUJ5QS9id1VsS1dTODNBbXFPek9jQzdsc2kxN2FjeG9xZi9XZWNWaHNMS0hhaTVCWXNFQ2t4YnRyUWN2Z210bFZqb2tGbnVTZjFMc1BMTzBCdmVJTUFiUWYwNXNpZktPTHNyR1l5UnF2dlhHMGVNYUZxbWZEYkpVNndhRGpaSlVXRHQzaisxcDVLZE1yVVdCMWFiODUydGdlV3c3OThubGw5dGdGWmhHQnZwYUlxbU1MNFM4eEFTWUoybSs4SndnL1A0am0ya0dFWjB1SzJBdmJmV0k0Y3l0VVNCNmJibnk1NncvcUZvMmt6VmZsb2pwN21NUWtrUVU0eEppbDdrUVU0K0JTbUEzZz0%3D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload, proxies= proxies , verify = ca_cert_path)
    print(response.status_code)
    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        container = soup.find('div' , class_ = 'gap-10 px-10 py-5 divide-y divide-gray-200 w-full')
        if container:
            print('container found!')

        headline= container.find_all('section' ,class_= 'flex gap-3 py-5 w-full')
        if headline:
            for tag in headline:
                link = tag.find('a')['href']
                if not link.startswith('https://blockworks.co') and 'https://app.' not in link: 
                    url = 'https://blockworks.co'+link
                    # print(url)
                    article_links.add(url)
        # print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

def blockworks_article_details(url):

    missing_fields = [] 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_cb=ChIZ6zBniKWrD-lZxL; _ga=GA1.1.1583271354.1724155948; _fbp=fb.1.1724155948649.427331574309775685; __qca=P0-1977108577-1724155947981; _cb_svref=external; cf_clearance=CnBL16YWE.BoeZGE6Dt2a8fnOFRtZMgDCsF5eW.y8Go-1726149185-1.2.1.1-XGILgPIMGElDch.sWZcwxAb4ADf3KjMY911w6RV_RAVjH1QCvZcmuJ9fWH5is0MGWREUjswHrb9mVYdkc.iERn1vrcwXY4r4BPRkW3JfoGdZmJFauTT6F7rk5aO.4cu2KpbkGy585__RpkMMTJG8y_ttGoKbeXFqsPOLDgFpfU9Qi82sChed5vha7Oa6ZG5E5kPNAqMTRCyYpiPHoq34AZtdJS0sPxHFBOqSYH7WQNibk5GTklio835I_avUPYIvDJQLof0rZzVyhHWPi.mlAIJOReRL6uPH2IP2Ccq9WZEHAYCko_qONAJjxshCTlMqCPBwNvet2JYpUB8.fp9.KlB26gY2ygfHz4wnLfWcJsRUKn3TF6_XcTiFRXUYfQJYIO7ywpgZbQwMJ1HaQq23q4RgWmFGBDaOonAT0FYm0IQ; __gads=ID=6f085d0ee8e3e86d:T=1724155947:RT=1726149191:S=ALNI_MYf4QCxoch3Fx4cjHIa_VOEjH8VpQ; __gpi=UID=00000ecdd3773d49:T=1724155947:RT=1726149191:S=ALNI_MYOhynXbx6v2m9ZZlq_X869tPXfdQ; __eoi=ID=b3e3e645b6f07de0:T=1724155947:RT=1726149191:S=AA-AfjY30nHufXqiB_VxxQO8RWPK; _chartbeat2=.1724155947222.1726149482870.0000000000000001.DNl91TB9vUJC1AZ_RDGatVaKbZc7.7; _ga_GYL4BXXQX8=GS1.1.1726149185.3.1.1726149483.40.0.0; __cfwaitingroom=ChhjL1NmRWxPSGc4Ky85Tk0xTUtOS0RBPT0SlAJsdXZTb2lFN2x6QVNHTHlwdVVJUGE4MFhQeWpac09VS3FBdkJnNzBYK3NjQWo5RlhjaDBMY3dSTnk1Z0NLV1g4UVNVMnFOOGtnN2NLWEtaVDJIRjQ0YWlKb292MzBKdU1vK3ZtbkFPMnJtNHRwcUwxV1RSd1R2OStPQUhlQ3Zxb2RvbnFsUDUxMjMxVC9zUGNCMS9ETUluMVhQSG51SXRRQ0x4aDVYS1RwUDJsWHhUWTI4SXd6UFlhTVhrVElXU25rUDV5TWN0OHZHY2hDYnhtKzEzUHdnM3ZOdkJjQnE4RUd2R0VkbW5VYzRqYlRyTEJRc2NmS1dXWmRaMHZuVFBnS09takVrV2E0NjJkdEFjZUpvST0%3D; __cfwaitingroom=ChgzZi9MNllUa0dIN1YvUSt5MWdFVEhRPT0SlAJBbndET0pxUUpZcUJ5QS9id1VsS1dTODNBbXFPek9jQzdsc2kxN2FjeG9xZi9XZWNWaHNMS0hhaTVCWXNFQ2t4YnRyUWN2Z210bFZqb2tGbnVTZjFMc1BMTzBCdmVJTUFiUWYwNXNpZktPTHNyR1l5UnF2dlhHMGVNYUZxbWZEYkpVNndhRGpaSlVXRHQzaisxcDVLZE1yVVdCMWFiODUydGdlV3c3OThubGw5dGdGWmhHQnZwYUlxbU1MNFM4eEFTWUoybSs4SndnL1A0am0ya0dFWjB1SzJBdmJmV0k0Y3l0VVNCNmJibnk1NncvcUZvMmt6VmZsb2pwN21NUWtrUVU0eEppbDdrUVU0K0JTbUEzZz0%3D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, proxies= proxies , verify = ca_cert_path)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1')
            if title_tag:
                title = title_tag.text.strip()
                print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author_container=soup.find('div' , class_ ='flex flex-wrap gap-1 uppercase')
            if author_container:
                author = author_container.find('a', class_='link-gray').get_text()
                author_link = 'https://blockworks.co'+author_container.find('a')['href']
                # print(author_link)
                author_info = blockworks_author_details(author_link)
                # print(author)
            else:
                author = ''
                missing_fields.append('Author')

            # Extract the published date
            published_tag = soup.find('time')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                parts = published.split(' ')
                date_str = parts[0]+parts[1]+parts[2]   
                published_date = convert_date_format(date_str)
                # print(published_date)
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []           
            paragraphs = soup.find('section', class_='w-full').find_all('p')[1:-3]
            # print(len(paragraphs))
            if paragraphs:
                for para in paragraphs:
                    p_text = para.text.strip()
                    paragraph_texts.append(p_text)
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
                'author_info':author_info,
                'body': body_content,
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except Exception as e:
        print({'url': url, 'error': str(e)})
        return None

if __name__ == "__main__":

    total_article_links = blockworks_article_list()
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = blockworks_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample_outputs/blockworks_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in blockworks_articles.json")