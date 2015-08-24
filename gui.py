#!/usr/bin/python
__author__ = 'Robotes'

import os
import logging
import sys
from PySide.QtGui import *
from src.truckDataWindow import TruckDataWindow
from src.solver import Solver
from src.data_set_window import *
import pickle
from src.data_store import DataStore
from src.graphview import GraphView
from src.tavlama import Tavlama
from src.greeting_screen import Greeting
from src.general_info import GeneralInfo
from src.data_writer import gams_writer

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
        self.newAction = QAction(QIcon('images/new.png'), '&New', self, shortcut = QKeySequence.New, statusTip = "New data set", triggered = self.newModel)
        self.loadAction = QAction(QIcon('images/load.png'), '&Load', self,
                                   shortcut=QKeySequence.Open, statusTip = 'Load a saved data set', triggered = self.load_data)

        self.saveAction = QAction(QIcon('images/save.png'), '&Save', self, shortcut=QKeySequence.Save, statusTip = 'Save data set', triggered = self.save_model)

        self.printAction = QAction(QIcon('images/print.png'), '&Print', self, shortcut=QKeySequence.Print, )
        # setup buttons

        # setup toolbar
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.newAction)
        self.mainToolBar.addAction(self.loadAction)
        self.mainToolBar.addAction(self.saveAction)

        # setup layout
        self.general_info = GeneralInfo(self.mainStatusBar)
        self.setCentralWidget(self.general_info)

        # empty objects
        self.truck_image_list = {}
        self.truckDataWindow = None

        # set algoruthms
        # self.tavlama = Tavlama()
        self.data_set_number = 0
        self.data_set = []

        self.simulation_on = False
        self.data = DataStore()
        self.greeting = Greeting()
        self.data_screen = None

    def greet(self):
        """
        starts a new window sequence to gather information about the system and solution
        :return:
        """
        i = self.greeting.exec_()
        if i == 1:
            self.new_model()
        elif i == 0:
            self.load_data()

    def newModel(self):
        """

        :return:
        """
        self.data = DataStore()
        self.show_truck_data()
        self.show_data()
        self.general_info.print_start_data()
        self.general_info.init_solution(self.data)

    def load_data(self):
        """
        loads prev saved data
        :return:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.data = pickle.load(open(file_name, 'rb'))
        self.show_truck_data()
        self.show_data()
        self.general_info.init_solution(self.data)
        self.general_info.print_start_data()

    def save_model(self):
        """
        saves current data
        :return:
        """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        pickle.dump(self.data,  open(file_name, 'wb'))

    def show_truck_data(self):
        """
        shows data about the trucks
        :return:
        """
        self.truckDataWindow = TruckDataWindow(self.data)
        self.truckDataWindow.exec_()

    def show_data(self):
        """
        shows data set
        :return:
        """
        self.dataWindow = DataSetWindow(self.data)
        self.dataWindow.exec_()

    def init_simulation(self):
        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn, self.model)
        # self.setCentralWidget(self.simulation)

        #self.setup_simulation()

    def showDataSet(self):
        self.model.init_iteration(0)
        self.simulation.update_image()

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

if __name__ == '__main__':
    with open('capraz.log', 'w'):
        pass
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='capraz.log', level=logging.DEBUG)
    logging.info('Program Started')
    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    myApp.exec_()
    sys.exit(0)
