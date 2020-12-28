
from bs4 import BeautifulSoup
import requests
import json

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"

def findLinks(artist):
    hehe = artist
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base + first_char + "/" + artist + ".html"
    req = requests.get(url, headers=headers)
    artist = {
        'artist': artist,
        'albums': {}
    }

    soup = BeautifulSoup(req.content, 'html.parser')
    all_albums = soup.find('div', id='listAlbum')
    all_songs = all_albums.find_all('div', class_='listalbum-item')
    all_links = []
    for x in range(len(all_songs)):
        temp = all_songs[x].find('a').get('href')
        if temp[0] == "." and temp[1] == ".":
            all_links.append(base + temp[3:])
        
    getLyrics(all_links, hehe)

def getLyrics(links, artist):
    filename = artist + ".txt"
    f = open(filename, "a")
    for song in links:
        req = requests.get(song, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        l = soup.find_all("div", attrs={"class": None, "id": None})
        l = str([x.getText() for x in l])
        l = l[2:].replace('\\n', ' ').replace('\\r', '').replace("[", "").replace("]", "")
        f.write(l)
    f.close()

findLinks('Adele')