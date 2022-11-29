import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
import pandas as pd
import re
import html

url = 'https://azbyka.ru/days/'
picture = []
name = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


def find_pictures():
    global pictureNames
    pictureNames = []
    picturesToday = soup.findAll('a', {"data-fancybox-group": "day"})
    for i in range(len(picturesToday)):
        picture.append(picturesToday[i].attrs["data-fancybox-href"])
        pictureNames.append(picturesToday[i].attrs["title"])


def get_day_names():
    global currentDayName, currentDayOldStyle, currentDayNewStyle
    currentDayAllInfo = soup.find('div', {"class": "cal calendar__day__current"})
    currentDayName = currentDayAllInfo.find('div', {"class": "days-mobile desk-hide"}).text.strip()
    currentDayOldStyle = "Старый стиль: " + currentDayAllInfo.find('div', {"class": "oldstyle"}).find(
        'strong').text.strip()
    currentDayNewStyle = "Новый стиль: " + currentDayAllInfo.find('div', {"class": "newstyle"}).find(
        'strong').text.strip()


def save_pics():
    for i in range(len(picture)):
        picToFile = requests.get(picture[i])
        open(pictureNames[i].replace(" ", "_") + ".jpg", "wb").write(picToFile.content)


get_day_names()

find_pictures()

save_pics()

print(currentDayName)
print(currentDayOldStyle)
print(currentDayNewStyle)