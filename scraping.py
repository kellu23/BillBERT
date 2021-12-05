""" Genius Lyric Scraping Script

This scraping script uses lyricsgenius, an open-source Python package that provides an interface for accessing song information using the Genius API.

We handle two sets of songs: 1) past Billboard Hot 100 hits, and 2) songs that have not made the Billboard 100. For each dataset, we generate a csv 
containing the lyrics.

"""

import lyricsgenius
from api_key import client_access_token

import pandas as pd
from bs4 import BeautifulSoup
import requests
from pandas.core.frame import DataFrame
import re
#to fix later--some of these imports might be redundant

LyricsGenius = lyricsgenius.Genius(client_access_token)

songlist = pd.read_csv("data/trimmed_billboard_songs.csv")

songlist.drop(songlist.columns.difference(
    ['Unnamed: 0', 'artist', 'song']), 1, inplace=True)

print(songlist.shape)
songlist = songlist.drop_duplicates(["artist", "song"])
print(songlist.shape)


def scrapegenius(song, artist):
    songname = LyricsGenius.search_song(song, artist)
    lyrics = songname.lyrics
    return lyrics


data = pd.DataFrame(columns=['Name', 'Lyrics'])
errors = pd.DataFrame(columns=['song', 'artist'])


for id in songlist['Unnamed: 0']:
    song = songlist['song'][id]
    artist = songlist['artist'][id]
    try:
        lyrics = scrapegenius(song, artist)

        new_row = {'Name': song, 'Lyrics': re.sub("([\[]).*?([\)\]])", "", lyrics).replace("\n", "").replace(",", "")}
        data = data.append(new_row, ignore_index=True)
    except Exception as e:
        errors = errors.append({"song": song, "artist": artist}, ignore_index=True)
        print(e)

data.to_csv("data/billboard-lyrics.csv", index=False)
errors.to_csv("data/billboard-errors.csv", index=False)




songlist = pd.read_csv("data/trimmed_non_billboard_songs.csv")

songlist.drop(songlist.columns.difference(
    ['Unnamed: 0', 'artists', 'name']), 1, inplace=True)

print(songlist.shape)
songlist = songlist.sample(15000)
print(songlist.shape)

data = pd.DataFrame(columns=['Name', 'Lyrics'])
errors = pd.DataFrame(columns=['song', 'artist'])

for id in range(len(songlist)):
    song = songlist['name'].iloc[id]
    artist = songlist['artists'].iloc[id]

    try:
        lyrics = scrapegenius(song, artist)
        new_row = {'Name': song, 'Lyrics': re.sub("([\[]).*?([\)\]])", "", lyrics).replace("\n", "").replace(",", "")}
        data = data.append(new_row, ignore_index=True)
    except Exception as e:
        errors = errors.append({"song": song, "artist": artist}, ignore_index=True)
        print(e)

data.to_csv("data/non-billboard-lyrics.csv", index=False)
errors.to_csv("data/non-billboard-errors.csv", index=False)
