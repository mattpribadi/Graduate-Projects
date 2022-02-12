#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request


#import python functions for Spotify and Genius pulls
import spotify_playlist_genius_lyrics
import requests
import pprint
import json
import re
import json



app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')



def get_playlist_json(playlist_id):
    CLIENT_ID = 'ec1ed293110d439f872a8c7adb83a3e4'
    CLIENT_SECRET = 'c38e39f4c660429d8cf5c700ab97a8b5'
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']
    
    # base URL of all Spotify API endpoints
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    BASE_URL = 'https://api.spotify.com/v1/'
    
    r = requests.get(BASE_URL + 'playlists/' + playlist_id, 
                 headers=headers, 
                 params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    playlist_dict, name = create_playlist_dict(d)
    return playlist_dict

def create_playlist_dict(d):
    playlist_dict = {}
    count = 1
    name=d['name']
    playlist_dict['name']=name
    for item in d['tracks']['items']:
        track_dict = {}
        artists = []
        for track in item['track']['artists']:
            artists.append(track['name'])
        join_artists = ", ".join(artists)
        
        track_dict['artist'] = join_artists
        track_dict['song'] = item['track']['name']
        track_dict['song_id'] = item['track']['id']

        playlist_dict[count] = track_dict

        count += 1
    return playlist_dict, name


def lyrics_from_song_api_path(song_api_path, headers):
    from bs4 import BeautifulSoup
    base_url = "http://api.genius.com"
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #html scraping
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    #removing script symbols
    page=re.sub('<br/>', '\n', page.text)
    #removing words [Verse...] and [Chorus...]
    page=re.sub('\[.*.\]', ' ', page)
    #removing extra spaces
    page=re.sub('\n{2}', ' ', page)
    html = BeautifulSoup(page, "html.parser")
    #finding tag called 'lyrics'!
    lyrics = html.find("div", class_=re.compile("Lyrics|^lyrics$|Lyrics_Root")).get_text() #updated css where the lyrics are based in HTML
    #removing Test Section stuck at the front
    lyrics=re.sub('test placeholderSaveSave.*','',lyrics)
    #removing Embedded Section stuck at the end
    lyrics=re.sub('[0-9].*.EmbedShare URLCopyEmbedCopy|EmbedShare URLCopyEmbedCopy', ' ', lyrics)
    #removing (') as it confuses code
    lyrics=re.sub('\'','', lyrics)
    #removing all line breaks (\n)
    lyrics=list(lyrics)
    lyrics = [", " if elem == "\n" else elem for elem in lyrics]
    lyrics.remove(", ")
    lyrics="".join(lyrics)
    return lyrics

def get_info_genius_API(song_title, artist_name, headers):
    base_url = "http://api.genius.com"
    search_url = base_url + "/search"
    song_title=re.sub('\(.*\)', '', song_title)
    data = {'q': song_title+', '+artist_name}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        hit_title=hit["result"]["title"]
        
        primary_hit_title=re.sub('\(.*\)', '', hit_title).lower().strip()
        primary_song_title=re.sub('-.*','',song_title).lower().strip()
        
        hit_artist_name=hit["result"]["primary_artist"]["name"]
        primary_artist_name=re.sub('(,|&).*', '', artist_name).lower()
        primary_hit_artist_name=re.sub('(,|&).*', '', hit_artist_name).lower()  
        
        if (primary_hit_title== primary_song_title): return hit
        elif (primary_hit_artist_name == primary_artist_name): return hit
    return None 


def get_lyrics_genius_API(song_title, artist_name):
    client_access_token='Q56ffH3XEyFV-Obd4uUhh2E8aZvC3ncgNXRPef5qP1nhyJaLUbr5ENYuZNtB472_'
    headers = {'Authorization': 'Bearer '+client_access_token}
    song_info = get_info_genius_API(song_title, artist_name, headers)
    if song_info: 
        song_api_path = song_info["result"]["api_path"]
        return lyrics_from_song_api_path(song_api_path, headers)
    else:
        artist_name=re.sub('(,|&).*', '', artist_name)
        song_info = get_info_genius_API(song_title, artist_name, headers)
        if song_info: 
            song_api_path = song_info["result"]["api_path"]
            return lyrics_from_song_api_path(song_api_path, headers)
    print("Error: No Match "+song_title+" by "+artist_name)
    return None
    
def get_lyrics_dict(json_data):
    lyrics_json={}
    for index, value in json_data.items():
        track_lyrics_dict={}
        artist = value['artist']
        track =  value['song']
        song_id= value['song_id']
        lyrics=get_lyrics_genius_API(song_title= track, artist_name= artist)
        try:
            track_lyrics_dict["song_id"]=song_id
            track_lyrics_dict["lyrics"]=lyrics
            lyrics_json[index]=track_lyrics_dict
        except TypeError:
            print(index)
            continue
    return lyrics_json
            

def get_playlist_and_lyrics(playlist_id):
    #get dictionaries
    playlist_dict=get_playlist_json(playlist_id)
    lyrics_dict=get_lyrics_dict(playlist_dict)
    #return dictionaries
    return playlist_dict, lyrics_dict

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    
@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

@app.route("/get_playlist")
def get_playlist_event():
    #USA "Today's Top Hits"
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'

    # Top 50 in Germany
    #playlist_id = '2vWo3FE3W86L3DHTGh2B2l'

    # Top 50 in Russia
    #playlist_id = '3MxLHSEh0admoYDH0GaY2'

    # Top 50 in Japan
    #playlist_id = '37i9dQZF1DXayDMsJG9ZBv'

    # Top 50 in Vietnam
    #playlist_id = '37i9dQZF1DX0F4i7Q9pshJ'
    
    playlist_event = get_playlist_json(playlist_id)

    log_to_kafka('playlist', playlist_event)
    return "Playlist Obtained!\n"

@app.route("/get_lyrics")
def get_lyrics_event():
    #USA "Today's Top Hits"
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'

    # Top 50 in Germany
    #playlist_id = '2vWo3FE3W86L3DHTGh2B2l'

    # Top 50 in Russia
    #playlist_id = '3MxLHSEh0admoYDH0GaY2'

    # Top 50 in Japan
    #playlist_id = '37i9dQZF1DXayDMsJG9ZBv'

    # Top 50 in Vietnam
    #playlist_id = '37i9dQZF1DX0F4i7Q9pshJ'
    
    playlist_event, lyrics_event = get_playlist_and_lyrics(playlist_id)

    log_to_kafka('event', lyrics_event)
    return "Lyrics Obtained!\n"
