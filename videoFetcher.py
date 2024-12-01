from youtube_transcript_api import YouTubeTranscriptApi
import sites
import requests
import re
import requests
 
import requests
ProxyToggles = False
def get_proxies_from_api():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
    response = requests.get(url)
    proxies = response.text.splitlines()
    return proxies

# Example usage
proxies = get_proxies_from_api()
# print(proxies)

# Convert proxies to the required format
def convert_to_proxy_list(proxies):
    proxy_list = []
    for proxy in proxies:
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        proxy_list.append(proxy_dict)
    return proxy_list

# Fetch proxies and convert them
proxies = get_proxies_from_api()
PROXIES_LIST = convert_to_proxy_list(proxies)
# print(PROXIES_LIST)
ProxyWorks = ""

def test_proxy(proxy):
    try:
        # Test if the proxy works
        response = requests.get("https://www.youtube.com", proxies=proxy, timeout=5)
        if response.status_code == 200:
            print(f"Proxy works: {proxy}")
            
            return True
    except Exception as e:
        # print(f"Failing proxy  + {proxy}")
        # print(f"Proxy failed: ==={proxy}=== - {e}")
        pass
    return False

def get_youtube_transcriptOnce(video_url):
        global ProxyWorks
        proxy = ProxyWorks
        if test_proxy(ProxyWorks):
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
                # ProxyToggles = False
                pass
                 
        print("All proxies failed.")
        return None
def get_youtube_transcript(video_url):
    global ProxyToggles  # Declare ProxyToggles as global to modify its value
    global ProxyWorks    #
    for proxy in PROXIES_LIST:
        proxWorker = proxy
            
        if test_proxy(proxWorker):
            try:
                # Extract video ID from the URL
                video_id = video_url.split("v=")[-1]
                # Fetch transcript using the working proxy
                transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
                # Combine transcript segments into a single string
                transcript_text = ' '.join([entry['text'] for entry in transcript])
                ProxyWorks = proxWorker
                ProxyToggles = True
                return transcript_text
            except Exception as e:
                print(f"Failed to retrieve transcript with proxy {proxy}: {e}")
                # ProxyToggles = False
                continue
                 
    print("All proxies failed.")
    return None

# https://youtu.be/haDjmBT9tu4?si=K_a1Fu-SaUTnvniE
# Example usage
if __name__ == "__main__":
    transcript = get_youtube_transcript(sites.MainStokksArray[0])
    i = 0
    # print(transcript)
    transcript = "Subtitles are disabled for this video"
    while ((transcript == None or len(transcript) < 40) and i < len(sites.MainStokksArray)):
        transcript = get_youtube_transcript(sites.MainStokksArray[i])
        print("Trans ==> ")
        i += 1
    print("Next")
    # transcript = get_youtube_transcriptOnce(sites.MainStokksArray[0])
    # for n in sites.MainStokksArray: 
    #     video_url = n
    #     transcript = get_youtube_transcript(video_url)
    #     if transcript:
    #         print("transcript received")
