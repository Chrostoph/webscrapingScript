
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
linksCount = 0


def findMails(url):

    global mailString
    mailSoup = BeautifulSoup(url.text, "html.parser")
    scriptsHtml = mailSoup.findAll('div', {"class": "span12 mainContact"})
    for i in range(len(scriptsHtml)):
        #print(scriptsHtml[i])
        stringFull = str(scriptsHtml[i])
        print(stringFull)
        match = (re.search('&#64;', stringFull))
        print(match)

    if match is not None:
        index = match.start()
        indexForward = index
        indexBackward = index
        mailString = ""

        while stringFull[indexBackward] != '\'':
            mailString += stringFull[indexBackward]
            indexBackward -= 1
        mailString = mailString[::-1]
        while stringFull[indexForward] != '\'':
            mailString += stringFull[indexForward]
            indexForward += 1
        print(stringFull)
        print(mailString)
        mailString = html.unescape(mailString)
        mail.append(mailString)
    else:
        mail.append("")


def findNumbers():
    numbers = soup.findAll('div', {"class": "span12 mainContact"})
    for i in range(len(numbers)):
        if numbers[i] is not None:
            if numbers[i].text.replace(" ", "").isdigit():
                number.append(numbers[i].text)
                break
            elif i == len(numbers)-1: number.append("")


def findAddresses(elements):
    adresses = mainPage.findAll('a', {"class": "address no_mobile",
                                  "onclick": "ga_track( 'search_results', 'address', 'click' ); h(this, '');"})
    while len(adresses) < elements:
        adresses.append(None)
    for i in range(elements):
        if adresses[i] is not None:
            address.append(adresses[i].text.strip())
        else:
            address.append("")


def findNamesAndLinks():
    global i
    names = mainPage.findAll('h2', {"class": "name"})
    linksCount = 0;
    for i in range(len(names)):
        if names[i] is not None:
            name.append(names[i].text.strip())
            links.append(names[i].find("a").attrs["href"])
            linksCount += 1

        else:
            name.append("")
            links.append("")
    return len(names)

mailString = ""
substringMail = "emailLink"

for i in range(1):

    if i == 0:
        url = 'https://www.azet.sk/katalog/potraviny/1/slovensko/'
        response = requests.get(url)
        mainPage = BeautifulSoup(response.text, "html.parser")
    else:
        newPage = mainPage.find('a', {"class": "s next"}).get("href")
        response = requests.get(newPage)
        mainPage = BeautifulSoup(response.text, "html.parser")

    findAddresses(findNamesAndLinks())

    for i in range(25):
        print(links[i])
        url = requests.get(links[i])
        soup = BeautifulSoup(url.text, "html.parser")
        findNumbers()
        findMails(url)


print(number)
print(mail)
print(address)

print(len(name), len(links), len(address), len(number), len(mail))
df = pd.DataFrame({'Name': name, 'Adress': address, 'Link': links, 'E-Mail': mail, 'Number': number})
df.to_csv('stores.csv', index=False, encoding='utf-8')
