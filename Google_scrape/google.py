import requests
import json

base_url = "https://blog.google/api/v2/latest/"
params = {
    'author_ids': '',
    'hero_template': 'heroArticleItem',
    'image_format': 'webp',
    'cursor': 1,  # Starting cursor value
    'paginate': 6,
    'show_hero': True,
    'site_id': 2,
    'tags': 'search'
}

headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'priority': 'u=1, i',
  'referer': 'https://blog.google/products/search/',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Iterate over cursor values from 1 to 5
for cursor_value in range(1, 6):
    params['cursor'] = cursor_value

    response = requests.get(base_url, headers=headers, params=params)
    print(response)
    json_response = response.json()

    # Process each article in the current response
    for num, data in enumerate(json_response['results']):
        print(data["full_url"], "===> ", num)

    # # Optional: Add a separator between different cursor iterations
    # print("\n=======================\n")
