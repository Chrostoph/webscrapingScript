import datetime

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
import pandas as pd
import re
from re import sub
import html
from decimal import Decimal
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://svatzaika:testmongodb@sviatcluster.kpxfarh.mongodb.net/?retryWrites=true&w=majority")
db = client.BoardGames
my_collection = db["Discounts"]
# result = my_collection.update_one({"name": "Carcassonne"}, {"$set": {"players": "2-5", "price": 18.99}}, upsert=True)
# found_docs = my_collection.find()
# def getItems (found_docs):
#     for doc in found_docs:
#         name = doc["name"]
#         players = doc["players"]
#         price = doc["price"]
#         print("name: " + name + "  " + "players: " + players + " price: " + str(price))
# getItems(found_docs)

page_num = 1
name = []
old_price = []
new_price = []
discount = []
price_diff = []
links = []

for j in range(80):
    print(j)

    url = 'https://eshop.albi.sk/hry/?page=' + str(page_num) + '#order=bestsellers'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    pageNames = soup.findAll('h3', {"class": "rf-ProductCard-title"})
    all_prices = soup.findAll('div', {"class": "rf-ProductCard-prices"})
    old_price_all = soup.findAll('span', {"class": "rf-ProductCard-originalPrice"})
    new_price_all = soup.findAll('span', {"class": "rf-Price "})
    links_all = soup.findAll('div', {"class": "rf-ProductCard-image"})

    for i in range(len(pageNames)):
        if all_prices[i].find('span', {"class": "rf-ProductCard-originalPrice"}):
            name.append(pageNames[i].find('a').text.strip())
            old_price_soup = all_prices[i].find('span', {"class": "rf-ProductCard-originalPrice"})
            old_price.append(sub(',', '.', (sub(r'[^\d.,]', '', old_price_soup.text.strip()))))
            new_price_soup = all_prices[i].find('span', {"class": "rf-ProductCard-price"})
            new_price.append(sub(',', '.', (sub(r'[^\d.,]', '', new_price_soup.text.strip()))))
            price_diff.append(round(float(old_price[-1]) / float(new_price[-1]) - 1, 2))
            links.append(str("https://eshop.albi.sk/" + links_all[i].find('a', href=True)['href']))
            # print(links[-1])
            print(i)
            # print("name: " + str(name[-1]) + " old price: " + str(old_price[-1]) + " new price: " + str(new_price[-1]))

            result = my_collection.update_one({"name": str(name[-1])}, {"$set": {"Old Price": old_price[-1],
                                                                                 "New Price": new_price[-1],
                                                                                 "Discount": price_diff[-1],
                                                                                 "Link": links[-1],
                                                                                 "Shop": "Albi",
                                                                                 "Update_Date": datetime.datetime.now()
                                                                                 }
                                                                        },
                                              upsert=True)
        else:
            delete = my_collection.delete_one({"name": pageNames[i].find('a').text.strip()})

    # print(url)
    # #print(pageNames)
    # print(len(pageNames))
    # print(name)
    # print(old_price)

    page_num = page_num + 1
