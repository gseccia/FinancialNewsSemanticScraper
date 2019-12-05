from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsProxyWidget, QDialog,
                             QGraphicsPixmapItem, QGraphicsScene, QLabel, QGraphicsItem, QWidget)
from PyQt5.QtGui import QPainter, QPixmap, QMovie
from PyQt5.QtCore import (QObject, QPointF, Qt,
                          QTimer, pyqtProperty, QSequentialAnimationGroup,
                          QRect, QSize)

class SemantiCat(QWidget):

    def __init__(self):
        super().__init__()
        # Define a QLabel
        self.l = QLabel(self)
        self.icon_size = 64
        self.l.setFixedSize(self.icon_size, self.icon_size)
        # Define the gif
        self.movie = QMovie("../../resources/gui/semantigif_slow.gif")
        size = QSize(self.icon_size, self.icon_size)
        self.movie.setScaledSize(size)
        # Start the gif
        QTimer().singleShot(3000, self.movie.start)
        # Put the gif into the QLabel
        self.l.setMovie(self.movie)

        self.l.show()
        self.setWindowOpacity(1)  # show the widget
        self.setStyleSheet("background-color: rgba(0,0,0,0)")

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)