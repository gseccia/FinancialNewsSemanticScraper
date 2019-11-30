from gui.client_gui import Ui_finNSEMA
from PyQt5 import QtGui, QtWidgets
from main import Main
from gui.gen_query_specialized import QueryGUI
import traceback
from selenium import webdriver
import os


class ClientGUI(Ui_finNSEMA, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.__is_on = False
        try:
            self.__main = Main.load_configuration()
            print(self.__main.get_browser_path() + "chromedriver.exe")
            self._driver = None
        except Exception as e:
            print("Exception in loading:\n", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)

    def setupEvent(self):
        self.conf_button.clicked.connect(self.configure)
        self.query_button.clicked.connect(self.open_query_builder)
        self.vis_button.clicked.connect(self.visualize_data)
        self.launch_button.clicked.connect(self.start_stop_finNSEMA)

    def open_query_builder(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = QueryGUI()
        dialog.ui.setupUi(dialog)
        dialog.ui.setupEvent()
        dialog.exec_()
        dialog.show()

    def visualize_data(self):
        self._driver = webdriver.Chrome(executable_path=self.__main.get_browser_path() + "chromedriver.exe")
        self._driver.get("localhost:8080")

    def start_stop_finNSEMA(self):
        try:
            if not self.__is_on:
                self.update_log("System scraper starting...")
                self.__main.start_loop(logger_area=self.log_area, label=self.news_counter_label)
                self.launch_button.setIcon(QtGui.QIcon(QtGui.QPixmap("../../resources/gui/on_icon.png")))
                self.__is_on = not self.__is_on
                self.update_log("SUCCESS: Scraper is on")
            else:
                self.update_log("System scraper stopping...")
                self.__main.stop_loop()
                self.launch_button.setIcon(QtGui.QIcon(QtGui.QPixmap("../../resources/gui/off_icon.png")))
                self.__is_on = not self.__is_on
                self.update_log("SUCCESS: Scraper is off")
        except Exception as e:
            print(e)

    def update_log(self, s: str):
        self.log_area.append(s)

    def configure(self):
        self.anim.start()
        file_browser = QtWidgets.QFileDialog()
        file_browser.setVisible(True)
        if file_browser.exec_():
            filenames = file_browser.selectedFiles()
            try:
                instance = Main.load_configuration(filenames[0])
                instance.save_configuration()
                self.update_log("SUCCESS: Load configuration completed")
            except Exception:
                self.update_log("ERROR: impossible to load configuration file")

    def shutdown_finNSEMA(self):
        try:
            self.__main.stop_loop()
            print("Main loop closed")
        except Exception:  # If already turned off do nothing
            print("Main loop was already closed")
        try:
            self.__main.stop_daemons()
            print("Daemons closed")
        except Exception:
            print("Error in closing Fuseki and Tarsier daemons")

    def startup_finNSEMA_daemons(self):
        try:
            self.__main.start_daemons()
        except Exception as e:
            print("Error in starting Fuseki and Tarsier daemons:\n", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_tb(exc_tb)
            print(sys.exc_info())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = ClientGUI()
    ui.setupUi(dialog)
    dialog.show()
    ui.setupEvent()
    sys.exit(app.exec_())


