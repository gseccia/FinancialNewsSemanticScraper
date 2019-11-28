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

    @staticmethod
    def load_configuration():
        return Main.__load_configuration()

    @staticmethod
    def __load_configuration():
        """ Proxy """
        return Main()

    def __change_configuration(self,filename=os.path.join(rel_path,"resources/configuration/configuration.config")):
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

        # print(Main.rel_path)

        self.__init__(FUSEKI_PATH, TARSIER_PATH, SLEEP_TIME, FIRST_START, exe_path,token_dots)

    def save_configuration(self):
        if self.__is_proxy:
            self.__change_configuration()
        with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "w") as f:
            config = {"tarsier_path": self.tarsier_path, "fuseki_path": self.fuseki_path, "news_update": self.sleep_time,
                      "broswer_path": self.__exe_path,"token_paralleldots":self.token_dots,"first_start":False}
            f.write(json.dumps(config))
            f.close()

    def __init__(self,fuseki_path=None,tarsier_path=None,sleep_time=None,is_first_start=None,exe_path=None,token_dots=None):

        self.fuseki_path = fuseki_path
        self.tarsier_path = tarsier_path
        self.sleep_time = sleep_time
        self.__is_first_start = is_first_start
        self.__exe_path = exe_path
        self.token_dots = token_dots

        if fuseki_path is None:
            # Class attributes initialized only ones in proxy
            self.__is_active = True

            # daemons processes
            self.__fuseki_pid = None
            self.__tarsier_process = None
            self.__scraper_thread = None
            self.__tripleizer = None
            self.fuseki = None
            print("Main proxy initialized successfully")
            self.__is_proxy = True

        else:
            # This must be done ony when real instance must be used
            # Starting Fuseki
            self.fuseki = FusekiSparqlWrapper()
            paralleldots.set_api_key(token_dots)
            self.__is_proxy = False
            print("Main configuration properly changed")


    def get_browser_path(self) -> str:
        if self.__is_proxy:
            self.__change_configuration()
        return self.__exe_path

    def start_daemons(self):
        if self.__is_proxy:
            self.__change_configuration()
        self.__fuseki_pid = self.fuseki.start_fuseki(fuseki_location=self.fuseki_path)

        DEBUG("Starting Tarsier...")
        process = subprocess.Popen(['pythonw', self.tarsier_path + "tarsier.py"],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                                   )
        self.__tarsier_process = process
        DEBUG("Tarsier is running!")

        if self.__is_first_start:
            # First Execution
            self.fuseki.create_dataset_fuseki()
            self.fuseki.load_ontology()
            self.__tripleizer = Tripleizer(initialize=True)
            time.sleep(1)
            # Not anymore a first start...
            with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "r") as jsonFile:
                data = json.load(jsonFile)
            data["first_start"] = False
            with open(os.path.join(Main.rel_path,"resources/configuration/configuration.config"), "w") as jsonFile:
                json.dump(data, jsonFile)
        else:
            self.__tripleizer = Tripleizer(initialize=False)
        self.__tripleizer.set_db_manager(self.fuseki)

    def stop_daemons(self):
        # if self.__is_proxy:
        #     self.__change_configuration()
        if self.__fuseki_pid is not None:
            self.fuseki.kill_fuseki(self.__fuseki_pid)
            print("Fuseki closed")
        try:
            if self.__tarsier_process is not None:
                self.__tarsier_process.kill()
                print("Tarsier closed")
        except Exception as e:
            print("Tarsier exc: ", e)
            print(sys.exc_info())

    def start_loop(self, logger_area, label):
        if self.__is_proxy:
            self.__change_configuration()
        # launch scraping engine
        self.__is_active = True
        self.__scraper_thread = Thread(target=self.loop, args=(logger_area, label))
        self.__scraper_thread.start()

    def stop_loop(self):
        # if self.__is_proxy:
        #     self.__change_configuration()
        self.__is_active = False

    def loop(self, logger_area, label, max_blocked_loops=10):
        if self.__is_proxy:
            self.__change_configuration()
        """Retrieve news and insert into database"""
        counter_news = 0
        scraper = Finviz_scraper.scraper_factory()
        while self.__is_active:
            try:
                #  Retrieving fresh news

                news = scraper.autoretrieve_news()

                # Filter only Bloomberg and Reuters news
                del_link = []
                for k, v in news.items():
                    if v["source"] == "other":
                        del_link.append(k)
                for link in del_link:
                    del news[link]

                # Deep analysis of fresh news
                for link in news.keys():
                    more_info = make_request(link, self.__exe_path,verbose=True)
                    blocked_loops = 0
                    while more_info is None:
                        more_info = make_request(link,self.__exe_path,verbose=True)
                        blocked_loops += 1
                        if blocked_loops == max_blocked_loops:
                            logger_area.append("ERROR: Captcha not resolved!")
                            more_info = {}
                    # Update fresh news information
                    news[link].update(more_info)

                counter_news += len(news)

                DEBUG("INFO RETRIEVE " + str(news))

                # Generate and insert triples
                if len(news) != 0:
                     DEBUG("Try to insert triples..")
                     self.__tripleizer.generate_insert(news_pool=news)
                else:
                     DEBUG("No fresh news")
                # DEBUG("Acquisition at "+str(datetime.datetime.now())+" SUCCESS")
                if len(news) == 0:
                    logger_area.append("NO FRESH NEWS: Acquisition at " + str(datetime.datetime.now()))
                else:
                    logger_area.append("SUCCESS: Acquisition at " + str(datetime.datetime.now()))
                    label.setText("News processed up to now: " + str(counter_news))
            except Exception as e:
                # DEBUG("Acquisition at "+str(datetime.datetime.now())+" FAILED")
                logger_area.append("ERROR: Acquisition at " + str(datetime.datetime.now()))
                print("Exception " + repr(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                traceback.print_tb(exc_tb)
            time.sleep(self.sleep_time)
        else:
            print("Scraper loop is now down... :c")

if __name__ == "__main__":
    try:
        main = Main.load_configuration()
        try:
            main.start_daemons()
        except Exception as e:
            print("Exception during execution:",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
        finally:
            main.stop_daemons()
    except Exception as e:
        print("Exception in loading:",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        traceback.print_tb(exc_tb)
