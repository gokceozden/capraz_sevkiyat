__author__ = 'Robotes'

import sys
from PySide.QtGui import *

class MainWindow(QMainWindow):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Capraz Sevkiyat Projesi")


if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()


    myApp.exec_()
    sys.exit(0)


