""" Genius Lyric Scraping Script

This scraping script uses lyricsgenius, an open-source Python package that provides an interface for accessing song information using the Genius API.

We handle two sets of songs: 1) past Billboard Hot 100 hits, and 2) songs that have not made the Billboard 100. For each dataset, we generate a csv
containing the lyrics. Note that the csv contains the song name, the artist name **that we queried Genius by**, and the lyrics.

"""

import lyricsgenius
from api_key import client_access_token
import cleantext

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

data = pd.DataFrame(columns=['Name', 'Artist', 'Lyrics'])
errors = pd.DataFrame(columns=['song', 'artist'])


for id in songlist['Unnamed: 0']:
    song = songlist['song'][id]
    artist = songlist['artist'][id]
    #remove featured artist from `artist` -- otherwise messes up lyricsgenius search
    feature_delim = [" Featuring ", " & ", " X "]
    if any(x in artist for x in feature_delim):
        match = next((x for x in feature_delim if x in artist), False)
        artist = artist[:artist.find(match)]

    try:
        lyrics = scrapegenius(song, artist)

        new_row = {'Name': song, 'Artist': artist, 'Lyrics': re.sub("([\[]).*?([\)\]])", " ", lyrics).replace("\n", " ").replace(",", " ")}
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

data = pd.DataFrame(columns=['Name', 'Artist', 'Lyrics'])
errors = pd.DataFrame(columns=['song', 'artist'])

for id in range(len(songlist)):
    song = songlist['name'].iloc[id]
    #remove additional information like " - Live at..." or " - Remaster" that messes with lyricsgenius
    if ' - ' in song:
        song = song[:song.find(' - ')]
    artist = songlist['artists'].iloc[id]
    # feature_delim = [" Featuring ", " & ", " X "]
    # #remove featured artist from `artist` -- otherwise messes up lyricsgenius search
    # if any(x in artist for x in feature_delim):
    #     match = next((x for x in feature_delim if x in artist), False)
    #     artist = artist[:artist.find(match)]

    try:
        lyrics = scrapegenius(song, artist)
        if (cleantext.usable(lyrics)):
            lyrics = cleantext.cleanup(lyrics)
            new_row = {'Name': song, 'Artist': artist, 'Lyrics': re.sub("([\[]).*?([\)\]])", " ", lyrics).replace("\n", " ").replace(",", " ")}
            data = data.append(new_row, ignore_index=True)
    except Exception as e:
        errors = errors.append({"song": song, "artist": artist}, ignore_index=True)
        print(e)

data.to_csv("data/non-billboard-lyrics.csv", index=False)
errors.to_csv("data/non-billboard-errors.csv", index=False)
