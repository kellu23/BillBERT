from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import pandas as pd

songlist = pd.read_csv("data/trimmed_billboard_songs.csv")

songlist.drop(songlist.columns.difference(['Unnamed: 0','artist','song']), 1, inplace=True)

def scrapegenius(song, artist):
    return artist

data = pd.DataFrame(columns=['Name', 'Lyrics'])

for id in songlist['Unnamed: 0'][:10]:
    song = songlist['song'][id]
    artist = songlist['artist'][id]

    lyrics = scrapegenius(song, artist)
    
    new_row = {'Name': song, 'Lyrics': lyrics}
    data = data.append(new_row, ignore_index=True)

data.to_csv("data/lyrics.csv", index=False)