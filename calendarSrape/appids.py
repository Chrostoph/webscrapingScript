import csv
import glob
import datetime
from bs4 import BeautifulSoup

export_file = open('export_data.csv', 'w', newline='')
writer = csv.writer(export_file)
headers = ['appid', 'mapped_appid', 'environment', 'status']
writer.writerow(headers)

acceptance_log_2 = open("acceptance2.log", 'r',encoding='utf-16').read()
acceptance_log_1 = open("acceptance1.log", 'r',encoding='utf-16').read()
staging_log = open("staging.log", 'r',encoding='utf-16').read()
production_log=open(r"D:\production.log", 'r',encoding='utf-16').read()

dir_path = r'C:\Users\svatz\appids\*.xml'
files = glob.glob(dir_path)
print(files)
for f in files:
    file = open(f, "r").read()
    soup = BeautifulSoup(file, "xml")
    # print(soup.prettify())

    applicationlist = soup.findAll('application')
    appids = []
    mapped = []
    env = []
    status = []

    for a in applicationlist:
        if a.find('appid'):
            appids.append(a.find('appid'))
        else: appids.append("")
        if a.find('mapped_appid'):
            mapped.append(a.find('mapped_appid'))
        else: mapped.append("")
        if "prod" in f:
            env.append("production")
            if appids[-1].text in production_log:
                status.append("active")
            else:
                status.append("inactive")
        elif "staging" in f:
            env.append("staging")
            if appids[-1].text in staging_log:
                status.append("active")
            else:
                status.append("inactive")
        elif "accept" in f:
            env.append("acceptance")
            # print(appids[-1].text)
            if (appids[-1].text in acceptance_log_1) | (appids[-1].text in acceptance_log_2):
                status.append("active")
            else:
                status.append("inactive")
        elif "performance" in f:
            env.append("performance")
            status.append("***")
        else: env.append("???")

        export_file = open('export_data.csv', 'a', newline='', encoding='utf-8')
        writer = csv.writer(export_file)
        headers = (appids[-1].text, mapped[-1].text, env[-1], status[-1])
        writer.writerow(headers)
        export_file.close()
