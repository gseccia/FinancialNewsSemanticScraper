from gui.main_GUI import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def location_on_the_screen(t):
    screen = QDesktopWidget().screenGeometry()
    widget = t.geometry()
    x = screen.width() - widget.width()
    y = screen.height() - widget.height()
    t.move(x/2, y/2)


if __name__ == "__main__":
    import sys, time, os

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # suppress Tensorflow warnings version 1.14
    import tensorflow as tf
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    app = QApplication(sys.argv)

    DEFAULT_STYLE = """
    QProgressBar{
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        font-size: 18px;
    }

    QProgressBar::chunk {
        background-color: lightblue;
        width: 10px;
        margin: 1px;
    }
    """


    # Create and display the splash screen

    # splash_pix = QPixmap('../ball.png')

    pixmap = QPixmap('../../resources/gui/background.png')
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)
    splash.setFixedSize(300, 300)
    # splash.setWindowOpacity(1)  # show the widget
    splash.setStyleSheet(DEFAULT_STYLE)

    # splash = QSplashScreen(splash_pix)
    movie = QMovie('../../resources/gui/semantigif.gif')
    lab = QLabel()
    icon_size = 250
    lab.setFixedSize(icon_size,icon_size)
    lab.setParent(splash)
    lab.setStyleSheet("background-color: transparent;")
    lab.setGeometry(splash.width()/2-lab.width()/2,splash.height()/2-lab.height()/2-40, icon_size, icon_size)
    movie.setScaledSize(QSize(icon_size, icon_size))
    movie.start()
    lab.setMovie(movie)
    # QTimer.singleShot(2000, lambda: movie.start())


    # adding progress bar
    progressBar = QProgressBar(splash)
    progressBar.setMaximum(50)
    progressBar.setGeometry(splash.width()/2-200/2, 230, 200, 20)

    # splash.setMask(splash_pix.mask())
    location_on_the_screen(splash)
    splash.show()
    splash.showMessage("<h1><font size=20 color='white'>Loading...</font></h1>", Qt.AlignBottom | Qt.AlignCenter, Qt.black)


    for i in range(1, 51):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    # Simulate something that takes time
    # time.sleep(1)

    form = MainWindow()
    form.show()
    splash.finish(form)
    sys.exit(app.exec_())