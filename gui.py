#!/usr/bin/python
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
        self.setGeometry(400,400,400,400)
        self.simulation = QGraphicsView()
        self.setCentralWidget(self.simulation)
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
        self.setupToolBar()
        self.setupLayout()

    def setupLayout(self):
        """
        Sets up the layout of the main window
        """

        self.mainGrid = QGridLayout()
        self.mainVBox = QVBoxLayout()
        self.mainGrid.addWidget(self.dataButton)
        self.setLayout(self.mainGrid)



    def setupButtons(self):
        """
        Setting the buttons for the main windows
        :return:
        """

        self.dataButton = QPushButton('Set/Inspect Data')
        self.dataButton.adjustSize()
        self.dataButton.clicked.connect(self.showDataWindow)


        self.loadButton = QPushButton('Load Data')
        #self.loadButton.adjustSize()
        self.loadButton.clicked.connect(self.loadModel)

        self.saveButton = QPushButton('Save Data')
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
        self.loadAction = QAction(QIcon('images/load.png'), '&Load', self,
                                   shortcut=QKeySequence.Open, statusTip = 'Load a saved data set', triggered = self.loadModel)

        self.saveAction = QAction(QIcon('images/save.png'), '&Save', self,
                                   shortcut=QKeySequence.Save, statusTip = 'Save data set', triggered = self.saveModel)

        self.dataAction = QAction(QIcon('images/save.png'), '&Data', self,
                                   shortcut=QKeySequence.New, statusTip = 'See data set', triggered = self.showDataWindow)




    def setupMenus(self):
        pass

    def setupToolBar(self):
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.loadAction)
        self.mainToolBar.addAction(self.saveAction)
        self.mainToolBar.addAction(self.dataAction)


if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()


    mainWindow.show()
    #mainWindow.showMaximized()


    myApp.exec_()
    sys.exit(0)


