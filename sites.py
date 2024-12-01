from youtube_search import YoutubeSearch

# Debugging: Print the full structure of results
import pprint
# 

# Add according to days that came up today only and yday 
# 
# Search for videos
results = YoutubeSearch('Stocks', max_results=4).to_dict()
# pprint.pprint(results)
MainStokksArray = []
for v in results:
    Link = 'https://www.youtube.com' + v['url_suffix']
    MainStokksArray.append(Link)

results = YoutubeSearch('Stocks to buy now', max_results=12).to_dict()
# pprint.pprint(results)
for v in results:
    Link = 'https://www.youtube.com' + v['url_suffix']
    MainStokksArray.append(Link)

MainStokksArray = list(set(MainStokksArray))
print(MainStokksArray)

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
