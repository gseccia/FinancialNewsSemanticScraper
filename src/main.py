from scrapers.financial_web_scraper import Finviz_scraper
from scrapers.deep_scraping import make_request
from tripleizer import Tripleizer
from threading import Thread
import datetime
import time
import os
import json

import sys, traceback


debug_mode = True
max_blocked_loops = 10
FUSEKI_JAR = "C:/Users/anton/Desktop/apache-jena-fuseki-3.13.1/"

def DEBUG(x):
    if debug_mode:
        print(x)

def main_loop():
    scraper = Finviz_scraper.scraper_factory()
    tripleizer = Tripleizer()
    while True:
        try:
            # Retrieving fresh news
            #### filename da eliminare in funzionamento
            news = scraper.autoretrieve_news(filename = "../resources/news_scraper_files/news.csv")

            # Deep analysis of fresh news
            for link in news.keys():
                more_info = make_request(link)
                blocked_loops = 0
                while more_info is None:
                    more_info = make_request(link)
                    blocked_loops += 1
                    if blocked_loops == max_blocked_loops:
                        raise Exception("Impossible contact pages")
                
                # Update fresh news information
                news[link].update(more_info)

            DEBUG("INFO RETRIEVE "+str(news))

            ##########################################
            # Da cancellare quando sarà in funzione
            news_retr = {}
            with open("../resources/news.tmp",mode="r") as f:
                news_retr = json.load(f)
                f.close()
            news_retr.update(news)
            with open("../resources/news.tmp",mode="w") as f:
                f.write(json.dumps(news_retr))
                f.close()
            ##########################################

            # Generate and insert triples
            if len(news) != 0:
                DEBUG("Try to insert triples..")
                tripleizer.generate_insert(news_pool=news)
            else:
                DEBUG("No fresh news")
            DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")
            
        except Exception as e:
            DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
            DEBUG("Exception "+repr(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
        time.sleep(5*60)

def tarsier_execution():
    DEBUG("Starting Tarsier..")
    os.system("python ./tarsier/tarsier.py")
    DEBUG("Tarsier closed!")
    
if __name__ == "__main__":
    current_dir = os.getcwd()
    DEBUG("Starting Fuseki..")
    os.chdir(FUSEKI_JAR)
    os.system("java -jar fuseki-server.jar")
    os.chdir(current_dir)
    DEBUG("Fuseki is running!")
    th = Thread(target=tarsier_execution)
    th.start()
    main_loop()
    
    
    
    
    
