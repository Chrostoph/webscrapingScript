import csv
import glob
import datetime

import pandas as pandas
from bs4 import BeautifulSoup
import fileinput
import pandas

acceptance_log_2 = open("acceptance2.log", 'r',encoding='utf-16').read()
acceptance_log_1 = open("acceptance1.log", 'r',encoding='utf-16').read()

# print(log)

file_input = fileinput.input(files=('acceptance1.log', 'acceptance2.log'), encoding='utf-16')
appids = []
file = pandas.readcsv("appids.csv", 'r'))
for col in file:
    appids.append(col[0])
# appids = file.read().splitlines()
file.close()
print(appids)

# for a in appids:
#     if a in (acceptance_log_2, acceptance_log_1):
#         print("active")
#     else:
#         print("inactive")

