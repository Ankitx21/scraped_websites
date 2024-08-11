import time
from datetime import datetime, timedelta
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

SBR_WEBDRIVER = 'https://brd-customer-hl_e7bfdecb-zone-scraping_browser1:iv6mkqg7shne@brd.superproxy.io:9515'
BASE_URL = 'https://www.youtube.com/@CNBCtelevision/videos'

def cnbc_youtube_video_list(soup):
    """Extract video URLs and their titles from the page."""
    videos = []
    for video in soup.find_all('a', id='video-title-link'):
        title = video['title'].strip()
        url = 'https://www.youtube.com' + video['href']
        videos.append((title, url))
    return videos

def cnbc_youtube_convert_published(time_description):
    """Convert time descriptions like '1 day ago' or '2 hours ago' to actual dates in MM/DD/YYYY format."""
    now = datetime.now()

    if 'day' in time_description:
        days_ago = int(time_description.split()[0])
        date = now - timedelta(days=days_ago)
    elif 'hour' in time_description:
        hours_ago = int(time_description.split()[0])
        date = now - timedelta(hours=hours_ago)
    elif 'minute' in time_description:
        minutes_ago = int(time_description.split()[0])
        date = now - timedelta(minutes=minutes_ago)
    else:
        date = now  # Return current date if the description is not recognized

    return date.strftime('%m/%d/%Y')

def cnbc_youtube_video_details(url, title):
    """Extract video details including transcript and time."""
    video_id = url.split('v=')[-1]
    
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        paragraph = ' '.join(entry['text'].lower() for entry in transcript)
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        paragraph = ''
    
    # Create a new browser session for each URL
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    options = ChromeOptions()
    options.add_argument('--headless')  # Ensure the browser is in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    with Remote(sbr_connection, options=options) as driver:
        driver.get(url)
        time.sleep(10)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the parent div that contains the time information
        metadata_div = soup.find('div', id='metadata-line')
        if metadata_div:
            time_span = metadata_div.find_all('span', class_='inline-metadata-item style-scope ytd-video-meta-block')[1]
            time_description = time_span.get_text(strip=True)
            time_date = cnbc_youtube_convert_published(time_description)
        else:
            time_date = ''
    
    return {
        "title": title,
        "video_id": video_id,
        "published": time_date,
        "video_url": url,
        "transcript": paragraph,
    }

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to YouTube Channel')
        driver.get(BASE_URL)
        time.sleep(10)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos = cnbc_youtube_video_list(soup)

        for title, url in videos:
            try:
                video_details = cnbc_youtube_video_details(url, title)
                if video_details:
                    print(video_details)  # Print or save the details as needed
                time.sleep(5)  # Adding delay between articles
            except Exception as e:
                print(f'Error scraping {url}: {e}')
                time.sleep(5)  # Wait before retrying the next article

if __name__ == '__main__':
    main()
