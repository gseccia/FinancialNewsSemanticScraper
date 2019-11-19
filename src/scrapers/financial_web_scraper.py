from bs4 import BeautifulSoup
import requests
import datetime
import csv
import time
import os.path
import re
import pickle

class Finviz_scraper:

    def scraper_factory(last_date = None):
        if last_date == None and os.path.exists("../resources/scraper.dat"):
            with open("../resources/scraper.dat","r") as f:
                retr_date = datetime.datetime.strptime(f.readline(),"%Y-%m-%dT%H:%M:%S+02:00")
                f.close()
            # print(retr_date,type(retr_date))
            scraper = Finviz_scraper(retr_date)
        else:
            scraper = Finviz_scraper(datetime.datetime(1970,1,1))
        return scraper
    
    def __init__(self,last_date = None):
        self.last_date = last_date
        
    def retrieve_news(self,news_URL = "https://finviz.com/news.ashx"):
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

    def autoretrieve_news(self,filename = None):
        # retrieve news
        news = self.retrieve_news()

        # Select today news
        current_time = datetime.datetime.now()
        today_news = []
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
        if filename is not None:
            fresh_news = {}
            if os.path.exists(filename):
                # Check the last news saved
                with open(filename,"r") as f:
                    csv_reader = csv.DictReader(f,dialect="excel",delimiter=';',lineterminator='\n')
                    for row in csv_reader:
                        last_date = datetime.datetime.strptime(row["date"],"%Y-%m-%dT%H:%M:%S+02:00")
                    newfile = False
            else:
                newfile = True

            for row in today_news:
                if row["date"] > last_date:
                    fresh_news[row["link"]] = row

            # Update the news
            with open(filename, mode='a+') as csv_file:
                fieldnames = ['date', 'text', 'link','authors','category']
                writer = csv.DictWriter(csv_file,fieldnames=fieldnames,dialect="excel",delimiter=';',lineterminator='\n')
                if newfile:
                    writer.writeheader()
                for row in fresh_news.values():
                    print(row)
                    row["date"] = row["date"].strftime("%Y-%m-%dT%H:%M:%S+02:00")
                    writer.writerow(row)
                csv_file.close()
            
        # Build news dictionary
        fresh_news = {}
        for row in today_news:
            if type(row["date"]) == str:
                row["date"] = datetime.datetime.strptime(row["date"],"%Y-%m-%dT%H:%M:%S+02:00")
            if row["date"] > self.last_date:
                fresh_news[row["link"]] = dict(row)
                if "bloomberg" in row["link"]:
                    fresh_news[row["link"]]["source"] = "bloomberg"
                elif "reuters" in row["link"]:
                    fresh_news[row["link"]]["source"] = "reuters"
                else:
                    fresh_news[row["link"]]["source"] = "other"
                fresh_news[row["link"]]["date"] = fresh_news[row["link"]]["date"].strftime("%Y-%m-%dT%H:%M:%S+02:00")
                del fresh_news[row["link"]]["link"]
                self.last_date = row["date"]
        # Update last_date of scraper
        with open("../resources/scraper.dat","w") as f:
            f.write(self.last_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"))
            f.close()
        
        return fresh_news

if __name__=="__main__":
    scraper = Finviz_scraper.scraper_factory()
    while True:
        try:
            print(scraper.autoretrieve_news())
            print("Acquisition at ",datetime.datetime.now(), "SUCCESS")
            print("last_date",scraper.last_date)
        except Exception as e:
            print("Acquisition at ",datetime.datetime.now(), "FAILED")
        time.sleep(5*60)
