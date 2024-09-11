import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%d %B %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def timesofisrael_author_details(author_link):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.1631156167.1725973998; _cb=CabSgoBM9r3UDKMJD6; _chartbeat2=.1725974000219.1725974000219.1.Dutn58BIJOBzB0TG8ZXh5-IDi57Nf.1; _gcl_au=1.1.2093392701.1725974001; ___nrbic=%7B%22isNewUser%22%3Atrue%2C%22previousVisit%22%3A1725973998%2C%22currentVisitStarted%22%3A1725973998%2C%22sessionId%22%3A%22ed5ad351-9304-4bc3-b471-010c29c2d8bd%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A1%2C%22landingPage%22%3A%22https%3A//www.timesofisrael.com/%22%2C%22referrer%22%3A%22%22%7D; ___nrbi=%7B%22firstVisit%22%3A1725973998%2C%22userId%22%3A%22feee48f1-2028-4312-bc5f-ac1fc5c6b541%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1725973998%2C%22timesVisited%22%3A1%7D; compass_uid=feee48f1-2028-4312-bc5f-ac1fc5c6b541; usprivacy=1---; _sharedid=f1d89232-ec17-4eeb-9d6a-1a53b56d0a18; _sharedid_cst=VyxHLMwsHQ%3D%3D; _fbp=fb.1.1725974007307.732594962810966416; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_ehYeHNoS3JbQ_Gxw3QGBF9RaQGrpDjFQCEy6tB69PPbykiOsg9JJYZNDaywxdEk1693ul_xNgwuosS-oYohsvmvE1vo3csnx-G0ABS81k2klJcgOdzZN1uo0W7PHikD%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _au_1d=AU1D-0100-001725974013-4RTD0TZM-O3AJ; __gads=ID=28371a38644947c6:T=1725974011:RT=1725974011:S=ALNI_MbXng3vsjSodJ68twRr_Cnei4XyHg; __gpi=UID=00000ef835ef46c9:T=1725974011:RT=1725974011:S=ALNI_MbFRAu9Gt9dmQwSnl9HPDWbky0evQ; __eoi=ID=c54baf760ea2a490:T=1725974011:RT=1725974011:S=AA-AfjY3W2mjwPne4ELi0417mpGA; _awl=2.1725974018.5-d9acd97f80daa7b73ebf00e9c539ce29-6763652d617369612d6561737431-0; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId_expiry=1726060418820; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; panoramaIdType=panoDevice; cto_bundle=DTMtX19scjkwTlp2VlZTVDRnM25LR0ZSdG5oSyUyQmxBMjRjb0tIa0JuMWtGZHNoSEtuQ3ZScjNDM2xheVZNdXglMkYlMkZpNGdGJTJCQkhxZlRvMzMxUG94JTJGbXh3VjRPWVd3ZExvUFRXZ24wNVBVNjRtRVBieUN5OEVtQm1Jd3UzMjBwQUlTTyUyQk1CcFFuZUtobGZlY1E4ZTVBJTJGOFdMeVNVQSUzRCUzRA; _lr_geo_location=IN; __qca=P0-171987755-1725974006552; _pbjs_userid_consent_data=3524755945110770; _pubcid=3f1e0535-0f0c-402a-a4e3-b7dae20ee712; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22320d74ce-8a08-49e4-882f-b111e5b9801c%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-09-10T13%3A13%3A49%22%7D; FCNEC=%5B%5B%22AKsRol8IYPMoqQqRbvia3H1eydksJgasVMOvYdeFCbmlgwihIcF9waQfKj9AyoUUbfo1h6l6ccmQVwzXquGreejylvTV74IXmCXw1WjXrTCDWGu6FJBg5NkrA3QGacxRHq228kWkxhNUmtHS39gXjySbjKxa3TamXA%3D%3D%22%5D%5D; _ga_RJR2XWQR34=GS1.1.1725974003.1.0.1725974231.0.0.0; _ga_51C8LVP5KH=GS1.1.1725974003.1.0.1725974297.0.0.0; _ga_FVWZ0RM4DH=GS1.1.1725974298.1.0.1725974298.60.0.0; _ga=GA1.1.2106971614.1725973998',
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

    response = requests.request("GET", author_link, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)

    # print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_linkedin=''
    author_twitter=''
    author_img=''
    author_name = soup.find('h1' , class_='name').text.strip()
    print(author_name)
    author_image = soup.find('div' ,class_='avatar')

    if author_image:
        author_img = author_image.find('img')['src']
    else:
        author_img=""
        
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details


def timesofisrael_article_list():

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    url = "https://www.timesofisrael.com/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.1631156167.1725973998; _cb=CabSgoBM9r3UDKMJD6; _chartbeat2=.1725974000219.1725974000219.1.Dutn58BIJOBzB0TG8ZXh5-IDi57Nf.1; _gcl_au=1.1.2093392701.1725974001; ___nrbic=%7B%22isNewUser%22%3Atrue%2C%22previousVisit%22%3A1725973998%2C%22currentVisitStarted%22%3A1725973998%2C%22sessionId%22%3A%22ed5ad351-9304-4bc3-b471-010c29c2d8bd%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A1%2C%22landingPage%22%3A%22https%3A//www.timesofisrael.com/%22%2C%22referrer%22%3A%22%22%7D; ___nrbi=%7B%22firstVisit%22%3A1725973998%2C%22userId%22%3A%22feee48f1-2028-4312-bc5f-ac1fc5c6b541%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1725973998%2C%22timesVisited%22%3A1%7D; compass_uid=feee48f1-2028-4312-bc5f-ac1fc5c6b541; usprivacy=1---; _sharedid=f1d89232-ec17-4eeb-9d6a-1a53b56d0a18; _sharedid_cst=VyxHLMwsHQ%3D%3D; _fbp=fb.1.1725974007307.732594962810966416; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_ehYeHNoS3JbQ_Gxw3QGBF9RaQGrpDjFQCEy6tB69PPbykiOsg9JJYZNDaywxdEk1693ul_xNgwuosS-oYohsvmvE1vo3csnx-G0ABS81k2klJcgOdzZN1uo0W7PHikD%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _au_1d=AU1D-0100-001725974013-4RTD0TZM-O3AJ; __gads=ID=28371a38644947c6:T=1725974011:RT=1725974011:S=ALNI_MbXng3vsjSodJ68twRr_Cnei4XyHg; __gpi=UID=00000ef835ef46c9:T=1725974011:RT=1725974011:S=ALNI_MbFRAu9Gt9dmQwSnl9HPDWbky0evQ; __eoi=ID=c54baf760ea2a490:T=1725974011:RT=1725974011:S=AA-AfjY3W2mjwPne4ELi0417mpGA; _awl=2.1725974018.5-d9acd97f80daa7b73ebf00e9c539ce29-6763652d617369612d6561737431-0; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId_expiry=1726060418820; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; panoramaIdType=panoDevice; cto_bundle=DTMtX19scjkwTlp2VlZTVDRnM25LR0ZSdG5oSyUyQmxBMjRjb0tIa0JuMWtGZHNoSEtuQ3ZScjNDM2xheVZNdXglMkYlMkZpNGdGJTJCQkhxZlRvMzMxUG94JTJGbXh3VjRPWVd3ZExvUFRXZ24wNVBVNjRtRVBieUN5OEVtQm1Jd3UzMjBwQUlTTyUyQk1CcFFuZUtobGZlY1E4ZTVBJTJGOFdMeVNVQSUzRCUzRA; _lr_geo_location=IN; __qca=P0-171987755-1725974006552; _pbjs_userid_consent_data=3524755945110770; _pubcid=3f1e0535-0f0c-402a-a4e3-b7dae20ee712; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22320d74ce-8a08-49e4-882f-b111e5b9801c%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-09-10T13%3A13%3A49%22%7D; FCNEC=%5B%5B%22AKsRol8IYPMoqQqRbvia3H1eydksJgasVMOvYdeFCbmlgwihIcF9waQfKj9AyoUUbfo1h6l6ccmQVwzXquGreejylvTV74IXmCXw1WjXrTCDWGu6FJBg5NkrA3QGacxRHq228kWkxhNUmtHS39gXjySbjKxa3TamXA%3D%3D%22%5D%5D; _ga_RJR2XWQR34=GS1.1.1725974003.1.0.1725974231.0.0.0; _ga_51C8LVP5KH=GS1.1.1725974003.1.0.1725974297.0.0.0; _ga_FVWZ0RM4DH=GS1.1.1725974298.1.0.1725974298.60.0.0; _ga=GA1.1.2106971614.1725973998',
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

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)

    print(response.status_code)


    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        container = soup.find('div' , id = 'latest')
        if container:
            print('container found!')

        headline= container.find_all('div' ,class_= 'headline')
        if headline:
            for tag in headline:
                link = tag.find('a')['href']
                if 'blogs' not in link:
                    url =link
                    # print(url)
                    article_links.add(url)
        # print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})



def timesofisrael_article_details(url):
    missing_fields = [] 
    
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_gid=GA1.2.1631156167.1725973998; _cb=CabSgoBM9r3UDKMJD6; _chartbeat2=.1725974000219.1725974000219.1.Dutn58BIJOBzB0TG8ZXh5-IDi57Nf.1; _gcl_au=1.1.2093392701.1725974001; ___nrbic=%7B%22isNewUser%22%3Atrue%2C%22previousVisit%22%3A1725973998%2C%22currentVisitStarted%22%3A1725973998%2C%22sessionId%22%3A%22ed5ad351-9304-4bc3-b471-010c29c2d8bd%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A1%2C%22landingPage%22%3A%22https%3A//www.timesofisrael.com/%22%2C%22referrer%22%3A%22%22%7D; ___nrbi=%7B%22firstVisit%22%3A1725973998%2C%22userId%22%3A%22feee48f1-2028-4312-bc5f-ac1fc5c6b541%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1725973998%2C%22timesVisited%22%3A1%7D; compass_uid=feee48f1-2028-4312-bc5f-ac1fc5c6b541; usprivacy=1---; _sharedid=f1d89232-ec17-4eeb-9d6a-1a53b56d0a18; _sharedid_cst=VyxHLMwsHQ%3D%3D; _fbp=fb.1.1725974007307.732594962810966416; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_ehYeHNoS3JbQ_Gxw3QGBF9RaQGrpDjFQCEy6tB69PPbykiOsg9JJYZNDaywxdEk1693ul_xNgwuosS-oYohsvmvE1vo3csnx-G0ABS81k2klJcgOdzZN1uo0W7PHikD%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _au_1d=AU1D-0100-001725974013-4RTD0TZM-O3AJ; __gads=ID=28371a38644947c6:T=1725974011:RT=1725974011:S=ALNI_MbXng3vsjSodJ68twRr_Cnei4XyHg; __gpi=UID=00000ef835ef46c9:T=1725974011:RT=1725974011:S=ALNI_MbFRAu9Gt9dmQwSnl9HPDWbky0evQ; __eoi=ID=c54baf760ea2a490:T=1725974011:RT=1725974011:S=AA-AfjY3W2mjwPne4ELi0417mpGA; _awl=2.1725974018.5-d9acd97f80daa7b73ebf00e9c539ce29-6763652d617369612d6561737431-0; _cc_id=d3ea27bf2c58f0b63af6cb4266d081a; panoramaId_expiry=1726060418820; panoramaId=d71fdea5f489bfd90eee42d092dda9fb927a132323e7291c64e7f96cff70f69c; panoramaIdType=panoDevice; cto_bundle=DTMtX19scjkwTlp2VlZTVDRnM25LR0ZSdG5oSyUyQmxBMjRjb0tIa0JuMWtGZHNoSEtuQ3ZScjNDM2xheVZNdXglMkYlMkZpNGdGJTJCQkhxZlRvMzMxUG94JTJGbXh3VjRPWVd3ZExvUFRXZ24wNVBVNjRtRVBieUN5OEVtQm1Jd3UzMjBwQUlTTyUyQk1CcFFuZUtobGZlY1E4ZTVBJTJGOFdMeVNVQSUzRCUzRA; _lr_geo_location=IN; __qca=P0-171987755-1725974006552; _pbjs_userid_consent_data=3524755945110770; _pubcid=3f1e0535-0f0c-402a-a4e3-b7dae20ee712; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22320d74ce-8a08-49e4-882f-b111e5b9801c%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-09-10T13%3A13%3A49%22%7D; FCNEC=%5B%5B%22AKsRol8IYPMoqQqRbvia3H1eydksJgasVMOvYdeFCbmlgwihIcF9waQfKj9AyoUUbfo1h6l6ccmQVwzXquGreejylvTV74IXmCXw1WjXrTCDWGu6FJBg5NkrA3QGacxRHq228kWkxhNUmtHS39gXjySbjKxa3TamXA%3D%3D%22%5D%5D; _ga_RJR2XWQR34=GS1.1.1725974003.1.0.1725974231.0.0.0; _ga_51C8LVP5KH=GS1.1.1725974003.1.0.1725974297.0.0.0; _ga_FVWZ0RM4DH=GS1.1.1725974298.1.0.1725974298.60.0.0; _ga=GA1.1.2106971614.1725973998',
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
        response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_= 'headline')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author_container=soup.find('span' , id ='follow-block-wrap')
            if author_container:
                author = author_container.find('a').get_text()
                author_link = author_container.find('a')['href']
                # print(author_link)

                author_info = timesofisrael_author_details(author_link)
                # print(author)
            else:
                author = ''
                missing_fields.append('Author')

            # Extract the published date
            published_tag = soup.find('span' ,class_='date')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                date_part = published.split(',')[0]
    
                if 'today' == date_part.lower():
                    published_date = datetime.now().date().isoformat()
                
                else:
                    published_date = convert_date_format(date_part)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            paragraphs = soup.find('div', class_='the-content').find_all('p')
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
                'author info': author_info,
                'body': body_content,
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except Exception as e:
        print({'url': url, 'error': str(e)})
        return None
    
if __name__ == "__main__":

    total_article_links = timesofisrael_article_list()
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = timesofisrael_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample_outputs/timesofisrael_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in timesofisrael_articles.json")
