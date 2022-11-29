import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
import pandas as pd
import re
import html

name = []
links = []
address = []
mail = []
number = []
substringMail = "emailLink"
url = 'https://www.azet.sk/katalog/potraviny/1/slovensko/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
names = soup.findAll('h2', {"class": "name"})
adresses = soup.findAll('a', {"class": "address no_mobile",
                              "onclick": "ga_track( 'search_results', 'address', 'click' ); h(this, '');"})
newPage = soup.find('a', {"class": "s next"}).get("href")
df = pd.DataFrame({'Name': name, 'Adress': address, 'Link': links})
df.to_csv('stores.csv', index=False, encoding='utf-8')
for i in range(len(names)):
    name.append(names[i].text.strip())
    links.append(names[i].find("a").attrs["href"])
for i in range(len(adresses)):
    address.append(adresses[i].text.strip())
"""# for i in range(31, 65) :
#         response = requests.get(newPage)
#         soup = BeautifulSoup(response.text, "html.parser")
#         names = soup.findAll('h2', {"class":"name"})
#         adresses = soup.findAll('a', {"class":"address no_mobile", "onclick":"ga_track( 'search_results', 'address', 'click' ); h(this, '');"})
#         newPage = soup.find('a', {"class" : "s next"}).get("href")
#         for i in range(len(names)) :
#                     name.append(names[i].text.strip())
#                     links.append(names[i].find("a").attrs["href"])
#         for i in range(len(adresses)) :
#                     address.append(adresses[i].text.strip()) """
for i in range(10):
    print(links[i])
    url = requests.get(links[i])
    stringFull = url.text.strip()
    soup = BeautifulSoup(url.text, "html.parser")
    numbers = soup.findAll('div', {"class": "span12 mainContact"})
    # string2 = url.content.decode('cp1252')
    # print(string2)
    # print(url.headers)
    # print(stringFull)
    match = (re.search('&#64;', stringFull))
    for i in range(len(numbers)):
        print(numbers[i])
        if numbers[i].text.replace(" ", "").isdigit() :
            number.append(numbers[i].text)
            break

    if match is not None:
        index = match.start()
        indexForward = index
        indexBackward = index
        mail = ""

        while stringFull[indexBackward] != '\'':
            mail += stringFull[indexBackward]
            indexBackward -= 1
        mail = mail[::-1]
        while stringFull[indexForward] != '\'':
            mail += stringFull[indexForward]
            indexForward += 1
        # mail = mail.replace("&#46;", ".").replace("&&#64;", "@")
        print(html.unescape(mail))
        # mails = soup.find('div', {"class":"emailLink eyJpIjoiZyJ9"})
        # print(mails)
        # mail.append(mails.text.strip())
    else:
        mail += ""
print(number)
while len(address) != len(name):
    address.append("")

    print(len(name), len(links), len(address))
    df = pd.DataFrame({'Name': name, 'Adress': address, 'Link': links})
    df.to_csv('stores.csv', index=False, encoding='utf-8')
