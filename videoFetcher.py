from youtube_transcript_api import YouTubeTranscriptApi
import sites
import requests
# Define the proxies
PROXIES_LIST = [

    {"http": "http://200.174.198.86:8888", "https": "http://200.174.198.86:8888"},

]

def test_proxy(proxy):
    try:
        # Test if the proxy works
        response = requests.get("https://www.youtube.com", proxies=proxy, timeout=5)
        if response.status_code == 200:
            print(f"Proxy works: {proxy}")
            return True
    except Exception as e:
        print(f"Proxy failed: {proxy} - {e}")
    return False

def get_youtube_transcript(video_url):
    for proxy in PROXIES_LIST:
        if test_proxy(proxy):
            try:
                # Extract video ID from the URL
                video_id = video_url.split("v=")[-1]
                # Fetch transcript using the working proxy
                transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
                # Combine transcript segments into a single string
                transcript_text = ' '.join([entry['text'] for entry in transcript])
                return transcript_text
            except Exception as e:
                print(f"Failed to retrieve transcript with proxy {proxy}: {e}")
    print("All proxies failed.")
    return None

# https://youtu.be/haDjmBT9tu4?si=K_a1Fu-SaUTnvniE
# Example usage
# if __name__ == "__main__":
#     for n in sites.MainStokksArray: 
#         video_url = n
        
#         if transcript:
#             print(transcript)
