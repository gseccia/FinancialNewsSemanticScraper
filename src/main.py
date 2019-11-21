from scrapers.financial_web_scraper import Finviz_scraper
from scrapers.deep_scraping import make_request
from tripleizer import Tripleizer
from fuseki_wrapper import FusekiSparqlWrapper
from threading import Thread
import datetime
import time
import os
import json
from resources.gui.client_gui import Ui_finNSEMA
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import paralleldots

import traceback

debug_mode = True
TOKEN = "zmxvDWsLaMuo6cxA1ZuIhjaqw6vtNVc9OVB5RgHQWFw"
max_blocked_loops = 10


def DEBUG(x):
    if debug_mode:
        # ui.add_log_message(x)
        print(x)


def main_loop(sleep_time,fuseki):
    """Retrieve news and insert into database"""
    counter_news = 0
    scraper = Finviz_scraper.scraper_factory()
    tripleizer = Tripleizer()
    tripleizer.set_db_manager(fuseki)
    while True:
        try:
            # Retrieving fresh news

            news = scraper.autoretrieve_news()  # filename = "../resources/news_scraper_files/news_news.csv"

            # Filter only Bloomberg and Reuters news
            del_link = []
            for k,v in news.items():
                if v["source"] == "other":
                    del_link.append(k)
            for link in del_link:
                del news[link]

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

            DEBUG("INFO RETRIEVE " + str(news))

            ##########################################
            """ Da cancellare quando sarà in funzione
            news_retr = {}
            with open("../resources/news.tmp",mode="r") as f:
                news_retr = json.load(f)
                f.close()
            news_retr.update(news)
            with open("../resources/news.tmp",mode="w") as f:
                f.write(json.dumps(news_retr))
                f.close() """
            ##########################################

            # Generate and insert triples
            if len(news) != 0:
                DEBUG("Try to insert triples..")
                tripleizer.generate_insert(news_pool=news)
            else:
                DEBUG("No fresh news")
            # DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")

            ui.add_log_message("Acquisition at " + str(datetime.datetime.now()) + " SUCCESS")
            ui.news_counter_label.setText("News processed up to now: " + str(counter_news))
        except Exception as e:
            # DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
            ui.add_log_message("Acquisition at " + str(datetime.datetime.now()) + " FAILED")
            print("Exception " + repr(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
        time.sleep(sleep_time)


def tarsier_execution(tarsier_path):
    """ Start tarsier """
    DEBUG("Starting Tarsier..")
    os.startfile(tarsier_path + "tarsier.py")
    DEBUG("Tarsier is running!")


# Interaction function with GUI
def show_tarsier():
    """ Show Tarsier on broswer"""
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("localhost:8080")


def launch_clicked():
    """Run scraper"""
    update_thread = Thread(target=main_loop, args=(sleep_time,fuseki))
    update_thread.start()
    ui.launch_button.setText("Running")
    ui.launch_button.disconnect()


def config_clicked():
    """ Show Tarsier on broswer"""
    file_broswer = QtWidgets.QFileDialog()
    file_broswer.setVisible(True)
    if file_broswer.exec_():
        filenames = file_broswer.selectedFiles()
        try:
            load_configuration(filenames[0])
            ui.scrollAreaWidgetContents.appendPlainText("Load configuration completed")
        except:
            ui.scrollAreaWidgetContents.appendPlainText("Impossible load configuration file")


def load_configuration(filename="../resources/configuration/configuration.config"):
    """ Load the configuration file"""
    with open(filename, "r") as f:
        config_param = json.load(f)
        f.close()

    FUSEKI_PATH = config_param["fuseki_path"]
    TARSIER_PATH = config_param["tarsier_path"]
    SLEEP_TIME = config_param["news_update"]

    return FUSEKI_PATH, TARSIER_PATH, SLEEP_TIME


if __name__ == "__main__":
    # Load configuration params
    try:
        fuseki_path, tarsier_path, sleep_time = load_configuration()
        # RUN GUI
        app = QtWidgets.QApplication(sys.argv)
        finNSEMA = QtWidgets.QDialog()
        ui = Ui_finNSEMA()
        ui.setupUi(finNSEMA, show_tarsier, launch_clicked, config_clicked)

        # Starting Fuseki
        fuseki = FusekiSparqlWrapper()
        fuseki_pid = fuseki.start_fuseki(fuseki_location=fuseki_path)
        time.sleep(5)
        if not os.path.exists("../resources/scraper.dat"):
            # First Execution
            fuseki.load_ontology()
            time.sleep(1)

        # Starting Tarsier
        tarsier_execution(tarsier_path)

        # Init Paralleldots
        paralleldots.set_api_key(TOKEN)

        finNSEMA.show()
        app.exec_()

        # Closing Fuseki
        fuseki.kill_fuseki(fuseki_pid)
    except Exception as e:
        print(e)
