import time
from datetime import datetime, timedelta
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

SBR_WEBDRIVER = 'https://brd-customer-hl_e7bfdecb-zone-scraping_browser1:iv6mkqg7shne@brd.superproxy.io:9515'
BASE_URL = 'https://www.youtube.com/@CNBCtelevision/videos'

def cnbc_youtube_video_list(soup):
    """Extract video URLs, titles, and published dates from the page."""
    videos = []
    for video in soup.find_all('a', id='video-title-link'):
        title = video['title']
        aria_label = video['aria-label']
        
        # Extract the time description (e.g., "2 days ago") from the aria-label
        time_description = aria_label.split(' views ')[-1].split()[:3]
        url = 'https://www.youtube.com' + video['href']
        published_date = cnbc_youtube_convert_published(' '.join(time_description))
        
        videos.append({
            "title": title,
            "url": url,
            "published": published_date
        })
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
    elif 'second' in time_description:
        seconds_ago = int(time_description.split()[0])
        date = now - timedelta(seconds=seconds_ago)
    else:
        date = now  # Return current date if the description is not recognized

    return date.strftime('%m/%d/%Y')

def fetch_transcript(video_id):
    """Fetch the transcript of a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        paragraph = ' '.join(entry['text'].lower() for entry in transcript)
        return paragraph
    except (NoTranscriptFound, TranscriptsDisabled):
        return ''

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to YouTube Channel')
        driver.get(BASE_URL)
        time.sleep(10)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos = cnbc_youtube_video_list(soup)

        for video in videos:
            video_id = video['video_url'].split('v=')[-1]
            video['transcript'] = fetch_transcript(video_id)
            print(video)  # Print or save the details as needed
            time.sleep(5)  # Adding delay between articles

if __name__ == '__main__':
    main()
