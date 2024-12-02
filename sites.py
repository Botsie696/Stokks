from youtube_search import YoutubeSearch

# Debugging: Print the full structure of results
import pprint
# 
import dataprovider
# pprint.pprint(MainStokksArray)
# Add according to days that came up today only and yday 
# 
# Search for videos
from youtube_search import YoutubeSearch
import pprint
from datetime import datetime, timedelta

# Helper function to check if the video is uploaded today or yesterday
def is_recent_upload(published_time):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
     
    # Adjust for string matching based on the format returned by YoutubeSearch
    if "ago" in published_time:
        if "day" in published_time and ("1 day" in published_time or "hours" in published_time or "2 days" in published_time):
            return True
        elif "hour" in published_time or "minute" in published_time:
            return True
    return False

# Search for videos with a higher max_results to ensure enough videos are available
results = YoutubeSearch('best Stocks to buy now', max_results=(dataprovider.NoSites * 10)).to_dict()
newResults = []
for n in dataprovider.Youtubers:
    Stocks = YoutubeSearch(('Stocks to buy with ' +n), max_results=(dataprovider.YoutubersDetailsSites * 3)).to_dict()
    BestStocks = []
    
    for video in Stocks:
      
        if is_recent_upload(video.get('publish_time', '')):
            print("nonese1")
            Link = 'https://www.youtube.com' + video['url_suffix']
            BestStocks.append(Link)
    newResults = newResults + BestStocks[:dataprovider.YoutubersDetailsSites ]
 
    
# Debugging: Print the full structure of results
 
# pprint.pprint(results)

# Filter for recently uploaded videos
MainStokksArray = []
for video in results:
    if is_recent_upload(video.get('publish_time', '')):
        Link = 'https://www.youtube.com' + video['url_suffix']
        MainStokksArray.append(Link)



 

# Ensure we get at least 10 videos
MainStokksArray = MainStokksArray[:dataprovider.NoSites]  # Get only the first 10 videos

# If fewer than 10 videos are found, fill the list with non-recent uploads
if len(MainStokksArray) < 10:
    for video in results:
        if len(MainStokksArray) >= 10:
            break
        Link = 'https://www.youtube.com' + video['url_suffix']
        if Link not in MainStokksArray:  # Avoid duplicates
            MainStokksArray.append(Link)

# Print the final list of 10 videos
# pprint.pprint(MainStokksArray)

results = YoutubeSearch('Stocks to buy now this month', max_results=int(dataprovider.NoSites / 2)).to_dict()
# pprint.pprint(results)
for v in results:
    Link = 'https://www.youtube.com' + v['url_suffix']
    print(v['url_suffix'])
    MainStokksArray.append(Link)
MainStokksArray = MainStokksArray + newResults
MainStokksArray = list(set(MainStokksArray))
print(len(MainStokksArray))
print(len(newResults))
# print(MainStokksArray)

# results = YoutubeSearch('Top Stocks to buy Now under 50$', max_results=12).to_dict()
# for v in results:
#     Link = 'https://www.youtube.com' + v['url_suffix']
#     MainStokksArray.append(Link)

 

print("Got the links")

# serve robotics 
# rocket lab 

# SOFI
# Nasdaq




 # severe robotics  -- invested 
 # SOFI -- invested 
 # Liberty global 
 # PLTR
 # Innodata