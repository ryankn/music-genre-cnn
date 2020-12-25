import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests
import json

load_dotenv()

JSON_FILENAME = "genre-playlist.json"

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SAVE_PATH = os.getenv('SAVE_PATH')

READ_LIMIT = 50
ADD_LIMIT = 50

scope = "user-library-read user-read-private " + \
"playlist-read-private playlist-modify-private"

DESIRED_LENGTH = 10

PLAYLISTS = ['0','2','3','7','8']

with open(JSON_FILENAME) as json_file:
    pdict = json.load(json_file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

def song_list_helper(plist, slist):
    lolist = slist
    
    for item in plist['items']:
        t = item['track']
        if t['preview_url']:
            lolist.append([t['artists'][0]['name'].replace(" ","_"),
                        t['name'].replace(" ","_"),
                        t['preview_url']])
            if len(lolist) >= DESIRED_LENGTH : return lolist

def get_songs(indexes):
    for i in indexes:
        songs_list = []
        label = pdict[i][1].replace(" ","_")

        playlist = sp.playlist_tracks(pdict[i][0],
                                      fields='items(track(preview_url,artists(id,name),name,id)),next,offset',
                                      limit=READ_LIMIT)

        while not len(songs_list) >= DESIRED_LENGTH:
            songs_list = song_list_helper(playlist, songs_list)
            if playlist['next']:
                playlist = sp.next(playlist)
            else:
                break

        for i,s in enumerate(songs_list):
            url = s[2]
            r = requests.get(url, allow_redirects=True)
            fullpath = os.path.join(SAVE_PATH, "{}_{}.mp3".format(label,i))
            open(fullpath, 'wb').write(r.content)
            print("Downloaded {} - {} as {}_{}.mp3".format(s[0].replace("_"," "),
                                                           s[1].replace("_"," "),
                                                           label,
                                                           i))

get_songs(PLAYLISTS)
