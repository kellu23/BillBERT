import lyricsgenius
import pandas as pd
from bs4 import BeautifulSoup
import requests
from pandas.core.frame import DataFrame
from api_key import client_access_token
import re

LyricsGenius = lyricsgenius.Genius(client_access_token)

songlist = pd.read_csv("data/trimmed_billboard_songs.csv")

songlist.drop(songlist.columns.difference(
    ['Unnamed: 0', 'artist', 'song']), 1, inplace=True)


def scrapegenius(song, artist):
    songname = LyricsGenius.search_song(artist, song)
    lyrics = songname.lyrics
    return lyrics

data = pd.DataFrame(columns=['Name', 'Lyrics'])

for id in songlist['Unnamed: 0'][:10]:
    song = songlist['song'][id]
    artist = songlist['artist'][id]

    lyrics = scrapegenius(song, artist)
    new_row = {'Name': song, 'Lyrics': re.sub("([\[]).*?([\)\]])", "", lyrics)}
    data = data.append(new_row, ignore_index=True)

data.to_csv("data/lyrics.csv", index=False)
