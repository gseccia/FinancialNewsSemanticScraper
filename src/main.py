from scrapers.financial_web_scraper import Finviz_scraper
from scrapers.deep_scraping import make_request
from tripleizer import Tripleizer
from threading import Thread
import datetime
import time
import os
import json
from resources.gui.client_gui import Ui_finNSEMA
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import traceback


debug_mode = True
max_blocked_loops = 10
FUSEKI_JAR = "C:/Users/anton/Desktop/apache-jena-fuseki-3.13.1/"
TARSIER_PATH = "C:/Users/anton/Desktop/Big Data e Tecnologie Semantiche/FinancialNewsSemanticScraper/src/tarsier/"
SLEEP_TIME = 5*60 # in seconds

def DEBUG(x):
    if debug_mode:
        # ui.add_log_message(x)
        print(x)

def main_loop():
    counter_news = 0
    scraper = Finviz_scraper.scraper_factory()
    tripleizer = Tripleizer()
    while True:
        try:
            # Retrieving fresh news
            #### filename da eliminare in funzionamento
            news = scraper.autoretrieve_news(filename = "../resources/news_scraper_files/news_news.csv")

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
                counter_news += len(more_info)

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
            # DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")

            ui.add_log_message("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")
            ui.news_counter_label.setText("News processed up to now: "+str(counter_news))
            ui.news_counter_label.repaint()
            ui.scrollAreaWidgetContents.repaint()
        except Exception as e:
            # DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
            ui.add_log_message("Acquisition at " + str(datetime.datetime.now()) + " FAILED")
            print("Exception "+repr(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
        time.sleep(SLEEP_TIME)

def tarsier_execution():
    DEBUG("Starting Tarsier..")
    os.startfile(TARSIER_PATH + "tarsier.py")
    DEBUG("Tarsier is running!")

def fuseki_execution():
    DEBUG("Starting Fuseki..")
    os.startfile(FUSEKI_JAR+"fuseki-server.jar")
    DEBUG("Fuseki is running!")

# Interaction function with GUI
def show_tarsier():
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("localhost:8080")

def launch_clicked():
    # Main background thread
    update_thread = Thread(target=main_loop)
    update_thread.start()
    ui.launch_button.setText("Running")
    ui.launch_button.disconnect()

def config_clicked():
    pass

if __name__ == "__main__":
    # RUN GUI
    app = QtWidgets.QApplication(sys.argv)
    finNSEMA = QtWidgets.QDialog()
    ui = Ui_finNSEMA()
    ui.setupUi(finNSEMA, show_tarsier, launch_clicked, config_clicked)

    # Starting Fuseki
    fuseki_execution()
    time.sleep(5)

    # Starting Tarsier
    tarsier_execution()

    finNSEMA.show()
    sys.exit(app.exec_())
