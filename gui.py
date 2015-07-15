#!/usr/bin/python
__author__ = 'Robotes'

import sys
from PySide.QtGui import *
from src.truckDataWindow import TruckDataWindow
from src.solver import Solver
from src.data_set_window import *
import pickle
from src.data_store import DataStore
from src.graphview import GraphView
from src.tavlama import Tavlama

class MainWindow(QMainWindow):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.model = None
        self.setWindowTitle("Capraz Sevkiyat Projesi")
        self.setGeometry(400,400,400,400)

        # setup status bar
        self.mainStatusBar = QStatusBar()
        self.setStatusBar(self.mainStatusBar)
        self.mainStatusBar.showMessage('Ready')

        ### setup menu bar
        # setup actions
        self.newAction = QAction(QIcon('images/new.png'), '&New', self, shortcut = QKeySequence.New, statusTip = "New data set", triggered = self.new_model)
        self.loadAction = QAction(QIcon('images/load.png'), '&Load', self,
                                   shortcut=QKeySequence.Open, statusTip = 'Load a saved data set', triggered = self.load_data)

        self.saveAction = QAction(QIcon('images/save.png'), '&Save', self, shortcut=QKeySequence.Save, statusTip = 'Save data set', triggered = self.save_model)

        self.truckDataAction = QAction(QIcon('images/truck.png'), '&Truck Data', self,
                                   shortcut=QKeySequence.New, statusTip = 'See truck data set', triggered = self.show_truck_data)

        self.dataAction = QAction(QIcon('images/data.png'), '&Data', self, shortcut=QKeySequence.New, statusTip = 'Set data set', triggered = self.show_data)

        self.showDataAction = QAction(QIcon('images/data.png'), '&Show Data', self, statusTip = "See Data Set", triggered = self.showDataSet)

        self.stepAction = QAction(QIcon('images/step.png'), 'Step forward', self, statusTip = 'One step in simulation', triggered = self.stepForward)

        # setup buttons
        self.dataButton = QPushButton('Set/Inspect Data')
        self.dataButton.adjustSize()
        self.dataButton.clicked.connect(self.show_truck_data)
        self.loadButton = QPushButton('Load Data')
        self.loadButton.clicked.connect(self.load_data)

        self.saveButton = QPushButton('Save Data')
        self.saveButton.clicked.connect(self.save_model)

        # setup toolbar
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.newAction)
        self.mainToolBar.addAction(self.loadAction)
        self.mainToolBar.addAction(self.saveAction)
        self.mainToolBar.addAction(self.truckDataAction)
        self.mainToolBar.addAction(self.dataAction)
        self.mainToolBar.addAction(self.showDataAction)
        self.mainToolBar.addAction(self.stepAction)

        # setup layout
        self.mainGrid = QGridLayout()
        self.mainVBox = QVBoxLayout()
        self.mainGrid.addWidget(self.dataButton)
        self.setLayout(self.mainGrid)

        # empty objects
        self.scn = None
        self.simulation = None
        self.truck_image_list = {}
        self.truckDataWindow = None

        # set algoruthms
#        self.tavlama = Tavlama()
        self.data_set_number = 0
        self.data_set = []

        self.simulation_on = False
        self.data = DataStore()

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.data = pickle.load(open(file_name, 'rb'))

    def save_model(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        pickle.dump(self.data,  open(file_name, 'wb'))

    def show_truck_data(self):
        self.truckDataWindow = TruckDataWindow(self.data)
        self.truckDataWindow.show()
#        self.scn.clear()
#        self.simulation.init_image()

    def show_data(self):
        self.dataWindow = DataSetWindow(self.data)
        self.dataWindow.show()

    def new_model(self):
        msgBox = QMessageBox()
        msgBox.setText('Would you like to save the old data')
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()

        if ret == QMessageBox.Save:
            self.save_model()
        elif ret == QMessageBox.Cancel:
            pass

        self.data = DataStore()
        self.scn.clear()

    def init_simulation(self):
        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn, self.model)
        # self.setCentralWidget(self.simulation)

        #self.setup_simulation()

    def setup_simulation(self):

        self.simulation.init_image()
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

    def stepForward(self):
        self.model = Solver(self.data)
#        self.model.set_data(self.data_set[self.data_set_number])
        # self.model.step()
        # self.statusBar().showMessage(str(self.model.current_time))
        # self.simulation.update_image()

    def create_data_set(self):
        for alpha in self.data.alpha_values:
            for gamma in self.data.gamma_values:
                for tightness in self.data.inbound_goods:
                    self.data_set.append((alpha, gamma, tightness))


    def showDataSet(self):
        self.model.init_iteration(0)
        self.simulation.update_image()

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    myApp.exec_()
    sys.exit(0)
