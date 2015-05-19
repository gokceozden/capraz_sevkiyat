#!/usr/bin/python
__author__ = 'Robotes'

import sys
from PySide.QtGui import *
from src.dataWindow import DataWindow
from src.solver import Solver
import cPickle

class GraphView(QGraphicsView):
    def __init__(self, scn, model = Solver()):
        QGraphicsView.__init__(self, scn)
        self.model = model

    def mouseDoubleClickEvent(self, *args, **kwargs):
        
        print(self.model.truck_dictionary['inbound']['inbound0'].coming_goods[0].amount)


class MainWindow(QMainWindow):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.model = Solver()
        self.setWindowTitle("Capraz Sevkiyat Projesi")
        self.setGeometry(400,400,400,400)

        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn, self.model)
        self.setCentralWidget(self.simulation)
        self.setupComponents()


        self.setup_simulation()
        self.truck_image_list = {}

        # remember to add an icon for the application
        # self.setWindowIcon()


    def setup_simulation(self):

        self.truckPixmap = QPixmap("images/truck.png")
        # self.truck1 = self.scn.addPixmap(self.truckPixmap)
        # self.truck2 = self.scn.addPixmap(self.truckPixmap)
        # self.truck1.scale(0.2,0.2)
        # self.truck1.setPos(100,800)
        # self.truck2.scale(0.2,0.2)
        # self.truck2.setPos(800,800)

        self.scn.addRect(0,250,500,500)
        self.scn.addLine(-400,0,-400,900)
        self.scn.addLine(800,0,800,900)

        self.simulation.show()






    def simulation_cycle(self):
        i = 0
        for inbound_trucks in self.model.inbound_trucks.values():
            truck_name = inbound_trucks.truck_name
            self.truck_image_list[truck_name] = self.scn.addPixmap(self.truckPixmap)
            self.truck_image_list[truck_name].scale(0.2,0.2)
            self.truck_image_list[truck_name].setPos(-600,i*100)
            i = i +1
        self.simulation.show()

    def loadModel(self, file_name = 'deneme'):

        self.model = cPickle.load(file_name, open(file_name, 'rb'))

    def saveModel(self, file_name = 'deneme'):
        print(self.model.truck_dictionary['inbound']['inbound0'].coming_goods[0].amount)
        self.simulation_cycle()
        #cPickle.dump(self.model,  open(file_name, 'wb'))


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
        self.dataWindow = DataWindow(self.model)
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


    #mainWindow.show()
    mainWindow.showMaximized()


    myApp.exec_()
    sys.exit(0)


