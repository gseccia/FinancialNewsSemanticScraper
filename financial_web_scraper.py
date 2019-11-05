from bs4 import BeautifulSoup
import requests
import datetime
import csv
import time
import os.path
import re

def retrieve_news(news_URL = "https://finviz.com/news.ashx"):
    """ Returns a list of news or None if there aren't """
    request = requests.get(news_URL)
    if request.status_code == 200:
        parser = BeautifulSoup(request.text, "html.parser")
        news_table = parser.select(".news > table:nth-child(2) > tr:nth-child(2) > td > table")[0]
        news = []
        for rows in news_table.find_all("tr",class_="nn"):
            news.append({"date":None,"text":None,"link":None,"authors":""})
            news[-1]["link"] = re.findall("http.*',",rows.attrs["onclick"])[0][:-2]
            for col in rows.find_all("td"):
                if col.has_attr("title"):
                    news[-1]["text"] = col.a.text
                if "class" in col.attrs and "nn-date" in col.attrs["class"]:
                    news[-1]["date"] = col.text
        return news
    else:
        return None

def autoretrieve_news():
    # retrieve news
    news = retrieve_news()

    # Select today news
    current_time = datetime.datetime.now()
    today_news = []
    fresh_news = []
    today = datetime.date.today()
    today_sec = (datetime.datetime(today.year,today.month,today.day)-datetime.datetime(1970,1,1)).total_seconds() - 2*60*60
    for row in news:
        try:
            date_time = datetime.datetime.strptime(row["date"],"%I:%M%p")
            total_sec = (date_time-datetime.datetime(1900,1,1)).total_seconds() + today_sec
            date_time = datetime.datetime.fromtimestamp(total_sec)
            row["date"] = date_time
            today_news.append(row)
        except Exception as e:
            pass

    # Sorting by datetime
    today_news = sorted(today_news,key=(lambda row: row["date"]))

    # Get the datetime of last saved news and select only fresh news
    if os.path.exists("news.csv"):
        # Check the last news saved
        with open("news.csv","r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                last_date = datetime.datetime.strptime(row["date"],"%Y-%m-%d %H:%M:%S")
            for row in today_news:
                if row["date"] > last_date:
                    fresh_news.append(row)
            newfile = False
    else:
        fresh_news = today_news
        newfile = True
                    
    
    # Update the news
    with open('news.csv', mode='a+') as csv_file:
        fieldnames = ['date', 'text', 'link','authors']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if newfile:
            writer.writeheader()
        for row in fresh_news:
            writer.writerow(row)
        csv_file.close()

    return fresh_news
    
if __name__=="__main__":
    while True:
        try:
            autoretrieve_news()
            print("Acquisition at ",datetime.datetime.now(), "SUCCESS")
        except:
            print("Acquisition at ",datetime.datetime.now(), "FAILED")
        time.sleep(5*60)
