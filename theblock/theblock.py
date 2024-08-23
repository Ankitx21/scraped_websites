import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B%d,%Y,")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def theblock_article_list():
    proxies= {
        'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'

    }
    ca_cert_path = 'tem_ca.crt'
    url = "https://www.theblock.co/latest"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.245871744.1724415702; slireg=https://scout.us3.salesloft.com; free-newsletter-count=5; sliguid=4725bebd-4f70-4d67-85d9-8e43939451ba; slirequested=true; _mkto_trk=id:163-ZPL-324&token:_mch-www.theblock.co-1724415705134-94876; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.theblock.co/latest%22%2C%22sref%22:%22%22%2C%22sts%22:1724415705513%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=17451b3a-d666-4c0f-a5f2-d7838fdade92%22%2C%22session_count%22:1%2C%22last_session_ts%22:1724415705513}; _clck=1hldvsa%7C2%7Cfok%7C0%7C1696; OptanonAlertBoxClosed=2024-08-23T12:21:57.058Z; eupubconsent-v2=CQDyySQQDyySQAcABBENDgCsAP_AAH_AAChQg1NX_H__bW9r8X7_aft0eY1P9_j77sQxBhfJE-4F3LvW_JwXx2E5NF36tqoKmRoEu3ZBIUNlHJHUTVmwaogVryHsakWcoTNKJ6BkkFMRM2dYCF5vm4tjeQKY5_p_d3fx2D-t_dv839zzz8VHn3e5fue0-PCdU5-9Dfn9fRfb-9IP9_78v8v8_l_rk2_eT13_pcvr_D--f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuyJCQm0DCKBACIKwgIoEAAAAJA0QEALgwKdgYBLrCRACBFAAcEAIQAUZAAgAAEgAQiACQIoEAAEAgEAAIAEAgEADAwADgAtBAIAAQHQMUwoAFAsIEiMiIUwIQoEggJbKBBKCoQVwgCLDAigERsFAAgCQEVgACAsXgMASAlYkECXUG0AABAAgFFKFQik_MAQ4Jmy1V4om0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_gAD_gAAAAA; __cf_bm=ZwtgAvOCv4al_xAByqKDBzx2RluuLJCuNrNSPH_7qNs-1724416628-1.0.1.1-FBtmkD4hKp6lZniLxO.Lod7y170FLGL8eC5Ihu19k6IfzFWnTOJzAmlhu0.3oZh_QtSlIsBHlgQFVtgpQv.SVA; cf_clearance=58Tw9wBsJag8GxfPux.I5ysAa7WCw119dirtYz5uhr4-1724416630-1.2.1.1-cUpCf9vPgE.mTvyqIOqZrvETHnMtKaFy9jBNOQOLiUkVZCVoHH_j6js3w4mF7IZqcTlACFnN7yJyroCjE4Yq9falK7yv89pBLgeNO.U5vFF9p_FJNK5htQVeQLiEey4X3jHw0x0BUM.yHivMwuhBV5WjL7pGCY7c9LmIFryOK3mC5FLUSkixot7lOGyEqxKaIG.8cI81tHCrEhBG_sFhfE3LGVqUDdvptpiMAbpAEg7MnbLEYAxik1rs.iU8W9QIEsOwpiw9ZOYwAHzkeIxOW1xGtISnp2YPpCX0ue4F9DrpVxp4wvyiKVI5gd3EMyYHNyxAON2E56NZLjBPLiAoXeaAFNr0495GuQTwLMhNNyA464mIs.OrjG6aJ8jbuEK_vTEFlHsMuvodHMDCEIdy0KoTYdDvS9na63aQ79dgio0; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Aug+23+2024+18%3A07%3A10+GMT%2B0530+(India+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CSTACK42%3A1&geolocation=IN%3BMH&AwaitingReconsent=false; new-free-nl-exists=false; _ga=GA1.1.2010877447.1724415702; _ga_9S53DMZLMT=GS1.1.1724415706.1.1.1724416633.60.0.0; _clsk=n9jwqa%7C1724416633258%7C2%7C1%7Cr.clarity.ms%2Fcollect; _gat=1; __cf_bm=C1TVY6AazIc79aaVJBCrzpnq5rYr1IbJ7pS_pC.qePI-1724416844-1.0.1.1-4sxPa11rrJZsZ0LdknB8C_npOp3a2kp09EtGerOX4E9oinoRd9zkpaEjH2W9pqBkPytdESrup5frWeQuPsJFnw',
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

    response = requests.request("GET", url, headers=headers, data=payload ,proxies= proxies ,verify=ca_cert_path)

    print(response.status_code)
    # articles
    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        container = soup.find('div' ,class_ = 'articles')
        if container:
            print('container found!')

        h1= container.find_all('a' ,class_= 'articleCard__thumbnail')
        if h1:
            for tag in h1:
                link = tag['href']
                if 'https://www.theblock.co/' not in link:
                    url = 'https://www.theblock.co'+link
                    # print(url)
                    article_links.add(url)
        # print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})



# theblock_article_list()

def theblock_article_details(url):
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.245871744.1724415702; slireg=https://scout.us3.salesloft.com; free-newsletter-count=5; sliguid=4725bebd-4f70-4d67-85d9-8e43939451ba; slirequested=true; _mkto_trk=id:163-ZPL-324&token:_mch-www.theblock.co-1724415705134-94876; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.theblock.co/latest%22%2C%22sref%22:%22%22%2C%22sts%22:1724415705513%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=17451b3a-d666-4c0f-a5f2-d7838fdade92%22%2C%22session_count%22:1%2C%22last_session_ts%22:1724415705513}; _clck=1hldvsa%7C2%7Cfok%7C0%7C1696; OptanonAlertBoxClosed=2024-08-23T12:21:57.058Z; eupubconsent-v2=CQDyySQQDyySQAcABBENDgCsAP_AAH_AAChQg1NX_H__bW9r8X7_aft0eY1P9_j77sQxBhfJE-4F3LvW_JwXx2E5NF36tqoKmRoEu3ZBIUNlHJHUTVmwaogVryHsakWcoTNKJ6BkkFMRM2dYCF5vm4tjeQKY5_p_d3fx2D-t_dv839zzz8VHn3e5fue0-PCdU5-9Dfn9fRfb-9IP9_78v8v8_l_rk2_eT13_pcvr_D--f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuyJCQm0DCKBACIKwgIoEAAAAJA0QEALgwKdgYBLrCRACBFAAcEAIQAUZAAgAAEgAQiACQIoEAAEAgEAAIAEAgEADAwADgAtBAIAAQHQMUwoAFAsIEiMiIUwIQoEggJbKBBKCoQVwgCLDAigERsFAAgCQEVgACAsXgMASAlYkECXUG0AABAAgFFKFQik_MAQ4Jmy1V4om0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_gAD_gAAAAA; __cf_bm=ZwtgAvOCv4al_xAByqKDBzx2RluuLJCuNrNSPH_7qNs-1724416628-1.0.1.1-FBtmkD4hKp6lZniLxO.Lod7y170FLGL8eC5Ihu19k6IfzFWnTOJzAmlhu0.3oZh_QtSlIsBHlgQFVtgpQv.SVA; cf_clearance=58Tw9wBsJag8GxfPux.I5ysAa7WCw119dirtYz5uhr4-1724416630-1.2.1.1-cUpCf9vPgE.mTvyqIOqZrvETHnMtKaFy9jBNOQOLiUkVZCVoHH_j6js3w4mF7IZqcTlACFnN7yJyroCjE4Yq9falK7yv89pBLgeNO.U5vFF9p_FJNK5htQVeQLiEey4X3jHw0x0BUM.yHivMwuhBV5WjL7pGCY7c9LmIFryOK3mC5FLUSkixot7lOGyEqxKaIG.8cI81tHCrEhBG_sFhfE3LGVqUDdvptpiMAbpAEg7MnbLEYAxik1rs.iU8W9QIEsOwpiw9ZOYwAHzkeIxOW1xGtISnp2YPpCX0ue4F9DrpVxp4wvyiKVI5gd3EMyYHNyxAON2E56NZLjBPLiAoXeaAFNr0495GuQTwLMhNNyA464mIs.OrjG6aJ8jbuEK_vTEFlHsMuvodHMDCEIdy0KoTYdDvS9na63aQ79dgio0; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Aug+23+2024+18%3A07%3A10+GMT%2B0530+(India+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CSTACK42%3A1&geolocation=IN%3BMH&AwaitingReconsent=false; new-free-nl-exists=false; _ga=GA1.1.2010877447.1724415702; _ga_9S53DMZLMT=GS1.1.1724415706.1.1.1724416633.60.0.0; _clsk=n9jwqa%7C1724416633258%7C2%7C1%7Cr.clarity.ms%2Fcollect; _gat=1; __cf_bm=C1TVY6AazIc79aaVJBCrzpnq5rYr1IbJ7pS_pC.qePI-1724416844-1.0.1.1-4sxPa11rrJZsZ0LdknB8C_npOp3a2kp09EtGerOX4E9oinoRd9zkpaEjH2W9pqBkPytdESrup5frWeQuPsJFnw',
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
    proxies= {
        'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'
    }
    ca_cert_path = 'tem_ca.crt'
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url ,headers=headers ,proxies = proxies ,verify=ca_cert_path)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1', class_= 'articleLabel_noMargin')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author_container = soup.find('div' ,class_='articleByline')
            if author_container:
                author = author_container.find('a').text
                # print(author)
            else:
                author=""
                missing_fields.append('Author')

            # Extract the published date
            published_tag = soup.find('div', class_='ArticleTimestamps__container timestamp tbcoTimestamp')
            if published_tag:
                published_data = published_tag.text.strip()
                published = published_data.split('•')[-1].strip()
                # print(published)
                parts = published.split(' ')
                date = parts[0]+parts[1]+parts[2]
                # print(date)
                published_date = convert_date_format(date)
                # print(published_date)
        
            else:
                published = ""
                # published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
            exclude_phrases = [
                'Disclaimer: The Block is an independent media outlet that delivers news, research, and data.',
                '© 2024 The Block. All Rights Reserved.'
            ]

            container = soup.find('div', id='articleContent')
            para_p = container.find_all('p', {'data-v-f87c67ca': ''})
            para_div = container.find_all('div', {'data-testid': 'tweetText'})

            if para_div:
                paragraphs = para_p + para_div
            else:
                paragraphs = para_p

            if paragraphs:
                for para in paragraphs:
                    para_content = para.text.strip()
                    
                    # Exclude paragraphs that contain any of the specified phrases
                    if not any(exclude_phrase in para_content for exclude_phrase in exclude_phrases):
                        paragraph_texts.append(para_content)
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
    

# theblock_article_details('https://www.theblock.co/post/312765/kraken-crypto-regulation-court-ruling-australia')

if __name__ == "__main__":

    total_article_links = theblock_article_list()
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = theblock_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample_outputs/theblock_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in theblock_articles.json")
