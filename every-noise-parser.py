from bs4 import BeautifulSoup
import requests
import re
import json

URL = 'http://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity'

FILENAME = "genre-playlist.json"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table') #all the genres are embedded in a table
table_a = table.find_all('a') #the <a> tags in the table are the relevant ones

REGEX = "^https:\/\/embed.spotify.com\/\?uri=(spotify:playlist:\w*)$"

def uri(url):
    return re.match(REGEX,url)[1] #pull a spotify URI from a spotify embed link

it = iter(table_a)

# there are 2 <a> tags for each genre, first with the spotify embed, second with genre name
# loop over 2 tags at a time, taking the relevant info out of each tag
# also add a counter

tdict = {}
i = 0
for x in it:
    tdict[i] = (uri(x['href']),next(it).text)
    i += 1

#write to json file

with open(FILENAME, 'w') as outfile:
    json.dump(tdict, outfile)
