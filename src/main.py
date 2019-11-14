from scrapers.financial_web_scraper import Finviz_scraper
from scrapers.deep_scraping import make_request
from tripleizer import Tripleizer
import datetime
import time
import os
import json

debug_mode = True
max_blocked_loops = 10
FUSEKI_JAR = "C:/Users/anton/Desktop/apache-jena-fuseki-3.13.1/fuseki-server.jar"

def DEBUG(x):
    if debug_mode:
        print(x)

def main_loop():
    scraper = Finviz_scraper.scraper_factory()
    # tripleizer = Tripleizer()
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
            # tripleizer.generate_insert(news_pool=news)
            DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")
            
        except Exception as e:
            DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
            DEBUG("Exception "+str(e))
        time.sleep(5*60)

if __name__ == "__main__":
    DEBUG("Starting Fuseki..")
    os.system("java -jar "+FUSEKI_JAR)
    DEBUG("Fuseki is running!")
    
    main_loop()
