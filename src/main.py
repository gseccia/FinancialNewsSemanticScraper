from builtins import Exception
from scrapers.financial_web_scraper import Finviz_scraper
from scrapers.deep_scraping import make_request
from tripleizer import Tripleizer
from fuseki_wrapper import FusekiSparqlWrapper
from threading import Thread
import datetime
import time
import os
import json
import subprocess
from resources.gui.client_gui import Ui_finNSEMA
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import paralleldots

import traceback

debug_mode = True


def DEBUG(x):
    if debug_mode:
        # ui.add_log_message(x)
        print(x)


class Main:
    __instance = None
    rel_path = os.path.dirname(os.path.realpath(__file__))[:-3]

    def load_configuration(filename=os.path.join(rel_path,"resources/configuration/configuration.config")):
        """ Load the configuration file"""
        with open(filename, "r") as f:
            config_param = json.load(f)
            f.close()

        FUSEKI_PATH = config_param["fuseki_path"]
        TARSIER_PATH = config_param["tarsier_path"]
        SLEEP_TIME = config_param["news_update"]
        exe_path = config_param["browser_path"]
        token_dots = config_param["token_paralleldots"]
        try:
            FIRST_START = bool(config_param["first_start"])
        except KeyError:  # if there's no key
            FIRST_START = True

        print(Main.rel_path)
        if Main.__instance is None:
            Main.__instance = Main(FUSEKI_PATH, TARSIER_PATH, SLEEP_TIME, FIRST_START, exe_path,token_dots)
        else:
            #TODO Modified instance
            pass

        return Main.__instance

    def save_configuration(self):
        with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "w") as f:
            config = {"tarsier_path": self.tarsier_path, "fuseki_path": self.fuseki_path, "news_update": self.sleep_time,
                      "broswer_path": self.exe_path,"token_paralleldots":self.token_dots,"first_start":False}
            f.write(json.dumps(config))
            f.close()

    def __init__(self,fuseki_path,tarsier_path,sleep_time,is_first_start,exe_path,token_dots):
        self.fuseki_path = fuseki_path
        self.tarsier_path = tarsier_path
        self.sleep_time = sleep_time
        self.is_first_start = is_first_start
        self.exe_path = exe_path
        self.token_dots = token_dots

        # Starting Fuseki
        self.fuseki = FusekiSparqlWrapper()
        paralleldots.set_api_key(token_dots)

        # Init Tripleizer as a class attribute
        self.__tripleizer = None

        # GUI
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = Ui_finNSEMA()
        self.finNSEMA = QtWidgets.QDialog()
        self.ui.setupUi(self.finNSEMA, self.__show_tarsier, self.__launch_clicked, self.__config_clicked)

    def start(self):
        self.fuseki_pid = self.fuseki.start_fuseki(fuseki_location=self.fuseki_path)

        DEBUG("Starting Tarsier..")
        process = subprocess.Popen(['pythonw', self.tarsier_path + "tarsier.py"],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                                   )
        self.tarsier_pid = process.pid
        DEBUG("Tarsier is running!")

        if self.is_first_start:
            # First Execution
            self.fuseki.create_dataset_fuseki()
            self.fuseki.load_ontology()
            self.__tripleizer = Tripleizer(initialize=True)
            time.sleep(1)
            # Not anymore a first start...
            with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "r") as jsonFile:
                data = json.load(jsonFile)
            tmp = data["first_start"]
            data["first_start"] = False
            with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "w") as jsonFile:
                json.dump(data, jsonFile)
        else:
            self.__tripleizer = Tripleizer(initialize=False)
        self.__tripleizer.set_db_manager(self.fuseki)

        self.finNSEMA.show()
        self.app.exec_()

    def stop(self):
        import signal
        if hasattr(self,"fuseki_pid"):
            self.fuseki.kill_fuseki(self.fuseki_pid)
            print("Fuseki closed")
        if hasattr(self,"tarsier_pid"):
            os.kill(self.tarsier_pid, signal.SIGTERM)
            print("Tarsier closed")

    def __main_loop(self,max_blocked_loops=10):
        """Retrieve news and insert into database"""
        counter_news = 0
        scraper = Finviz_scraper.scraper_factory()
        while True:
            try:
                # Retrieving fresh news

                news = scraper.autoretrieve_news()  # filename = "../resources/news_scraper_files/news_news.csv"

                # Filter only Bloomberg and Reuters news
                del_link = []
                for k, v in news.items():
                    if v["source"] == "other":
                        del_link.append(k)
                for link in del_link:
                    del news[link]

                # Deep analysis of fresh news
                for link in news.keys():
                    more_info = make_request(link, self.exe_path)
                    blocked_loops = 0
                    while more_info is None:
                        more_info = make_request(link,self.exe_path)
                        blocked_loops += 1
                        if blocked_loops == max_blocked_loops:
                            self.ui.scrollAreaWidgetContents.appendPlainText("Captcha Not resolved!")
                            more_info = {}

                    # Update fresh news information
                    news[link].update(more_info)

                counter_news += len(news)

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
                    self.__tripleizer.generate_insert(news_pool=news)
                else:
                    DEBUG("No fresh news")
                # DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")

                self.ui.add_log_message("Acquisition at " + str(datetime.datetime.now()) + " SUCCESS")
                self.ui.news_counter_label.setText("News processed up to now: " + str(counter_news))
            except Exception as e:
                # DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
                self.ui.add_log_message("Acquisition at " + str(datetime.datetime.now()) + " FAILED")
                print("Exception " + repr(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                traceback.print_tb(exc_tb)
            time.sleep(self.sleep_time)

    # Interaction function with GUI
    def __show_tarsier(self):
        """ Show Tarsier on broswer"""
        from selenium import webdriver
        print(self.exe_path+"chromedriver.exe")
        driver = webdriver.Chrome(executable_path=self.exe_path+"chromedriver.exe")
        driver.get("localhost:8080")


    def __launch_clicked(self):
        """Run scraper"""
        update_thread = Thread(target=self.__main_loop, args=(self,))
        update_thread.start()
        self.ui.launch_button.setText("Running")
        self.ui.launch_button.disconnect()

    def __config_clicked(self):
        """ Show Tarsier on broswer"""
        file_broswer = QtWidgets.QFileDialog()
        file_broswer.setVisible(True)
        if file_broswer.exec_():
            filenames = file_broswer.selectedFiles()
            try:
                instance = Main.load_configuration(filenames[0])
                instance.save_configuration()
                self.ui.scrollAreaWidgetContents.appendPlainText("Load configuration completed")
            except Exception:
                self.ui.scrollAreaWidgetContents.appendPlainText("Impossible load configuration file")


if __name__ == "__main__":
    try:
        main = Main.load_configuration()
        try:
            main.start()
        except Exception as e:
            print("Exception during execution:",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
        finally:
            main.stop()
    except Exception as e:
        print("Exception in loading:",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        traceback.print_tb(exc_tb)
