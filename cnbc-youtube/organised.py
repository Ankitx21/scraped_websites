from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# Scraping browser WebDriver URL
SBR_WEBDRIVER = 'https://brd-customer-hl_e7bfdecb-zone-scraping_browser1:iv6mkqg7shne@brd.superproxy.io:9515'

def save_transcript_as_paragraph_to_json(video_url):
    # Extract the video ID from the URL
    video_id = video_url.split('v=')[-1]
    
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Extract and concatenate texts into one paragraph
        paragraph = ' '.join(entry['text'].lower() for entry in transcript)
        
        # Prepare the data to be saved
        transcript_data = {
            "video_id": video_id,
            "video_url": video_url,
            "transcript": paragraph
        }
        print(transcript_data)
        print(f"Transcript paragraph for video {video_id} saved.")
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"No transcript found for video {video_id}.")
    except Exception as e:
        print(f"An error occurred for video {video_id}: {e}")

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to YouTube Channel')
        driver.get('https://www.youtube.com/@CNBCtelevision/videos')
        time.sleep(10)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos = soup.find_all('a', id='video-title-link')

        for video in videos:
            title = video['title'].strip()
            url = 'https://www.youtube.com' + video['href']
            
            # Find the parent div that contains the time information
            metadata_div = video.find_next('div', id='metadata-line')
            if metadata_div:
                time_span = metadata_div.find_all('span', class_='inline-metadata-item style-scope ytd-video-meta-block')[1]
                time_text = time_span.get_text(strip=True)
            else:
                time_text = 'Time not found'
            
            print(f'Title: {title}, URL: {url}, Time: {time_text}')
            
            # Get and save the transcript for each video
            save_transcript_as_paragraph_to_json(url)

if __name__ == '__main__':
    main()
