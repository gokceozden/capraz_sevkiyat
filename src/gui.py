__author__ = 'Robotes'

import sys
from PySide.QtGui import *
from src.dataWindow import DataWindow
from src.solver import Solver
import cPickle

class MainWindow(QMainWindow):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Capraz Sevkiyat Projesi")
        self.setupComponents()

        self.model = Solver()

        # remember to add an icon for the application
        # self.setWindowIcon()

    def loadModel(self, file_name = 'deneme'):

        self.model = cPickle.load(file_name, open(file_name, 'rb'))

    def saveModel(self, file_name = 'deneme'):

        cPickle.dump(self.model,  open(file_name, 'wb'))


    def setupComponents(self):
        """
        Setup all the components, statusbar, menubar, toolbar
        :return:
        """

        self.setupStatusBar()
        self.setupMenuBar()
        self.setupButtons()
        self.setupLayout()

    def setupLayout(self):
        """
        Sets up the layout of the main window
        """
        self.mainGrid = QGridLayout()
        self.mainGrid.addWidget(self.dataButton, 0, 1)
        self.mainGrid.addWidget(self.loadButton, 0, 2)
        self.mainGrid.addWidget(self.saveButton, 2, 2)
        self.setLayout(self.mainGrid)


    def setupButtons(self):
        """
        Setting the buttons for the main windows
        :return:
        """

        self.dataButton = QPushButton('Set/Inspect Data', self)
        self.dataButton.adjustSize()
        self.dataButton.clicked.connect(self.showDataWindow)


        self.loadButton = QPushButton('Load Data', self)
        #self.loadButton.adjustSize()
        self.loadButton.clicked.connect(self.loadModel)

        self.saveButton = QPushButton('Save Data', self)
        #self.saveButton.adjustSize()
        self.saveButton.clicked.connect(self.saveModel)

    def showDataWindow(self):
        self.dataWindow = DataWindow()
        self.dataWindow.show()


    def setupStatusBar(self):

        self.mainStatusBar = QStatusBar()
        self.setStatusBar(self.mainStatusBar)
        self.mainStatusBar.showMessage('Ready')

    def setupMenuBar(self):
        self.setupActions()
        self.setupMenus()

    def setupActions(self):
        pass

    def setupMenus(self):
        pass

    def setupToolBar(self):
        pass


if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()


    mainWindow.show()
    #mainWindow.showMaximized()


    myApp.exec_()
    sys.exit(0)


