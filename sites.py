from youtube_search import YoutubeSearch

import pprint

import dataprovider

from youtube_search import YoutubeSearch
import pprint
from datetime import datetime, timedelta

# Helper function to check if the video is uploaded today or yesterday
def is_recent_upload(published_time):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
     
    published_time = str(published_time)
    # Adjust for string matching based on the format returned by YoutubeSearch
    if "ago" in published_time:
        if "day" in published_time and ("1 day" in published_time or "hours" in published_time or '0' in published_time):
            return True
        elif "hour" in published_time or "minute" in published_time:
            return True
    return False

# Search for videos with a higher max_results to ensure enough videos are available
results = YoutubeSearch('best Stocks to buy now', max_results=(dataprovider.NoSites * 50)).to_dict()
newResults = []
for n in dataprovider.Youtubers:
    Stocks = YoutubeSearch(('Latest stocks with ' + n), max_results=(dataprovider.YoutubersDetailsSites * 150)).to_dict()
    BestStocks = []
    # pprint.pprint(Stocks)
    for video in Stocks:
        
        if is_recent_upload(video.get('publish_time', '')) and n.lower() in video.get('channel').lower() :
            
            Link = 'https://www.youtube.com' + video['url_suffix']
            BestStocks.append(Link)
        
    newResults = newResults + BestStocks[:dataprovider.YoutubersDetailsSites ]
    # print("==========" , len(BestStocks)  , n)
    
# Debugging: Print the full structure of results
 


# Filter for recently uploaded videos
MainStokksArray = []
# for video in results:
#     if is_recent_upload(video.get('publish_time', '')):
#         Link = 'https://www.youtube.com' + video['url_suffix']
#         MainStokksArray.append(Link)

youtubers = ["mr. sicko Trading"]

 

# More videos of youtubers
MainStokksArray = MainStokksArray[:dataprovider.NoSites]  # Get only the first 10 videos
for n in youtubers:
    Stocks = YoutubeSearch(('Latest stocks with ' + n), max_results=(dataprovider.YoutubersDetailsSites * 150)).to_dict()
    BestStocks = []
    # pprint.pprint(Stocks)
    for video in Stocks:
        
        if is_recent_upload(video.get('publish_time', '')):
            
            Link = 'https://www.youtube.com' + video['url_suffix']
            BestStocks.append(Link)
        
    newResults = newResults + BestStocks[:10]
    # print("==========" , len(BestStocks)  , n)
    


MainStokksArray = MainStokksArray + newResults
MainStokksArray = list(set(MainStokksArray))
print(len(MainStokksArray))