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
from src.solver import Solver
from src.show_data import ShowData

class MainWindow(QWidget):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QWidget.__init__(self)
        self.model = None
        self.setWindowTitle("Capraz Sevkiyat Projesi")
        self.setGeometry(400,400,400,400)

        self.set_buttons()
        self.set_layout()

        self.truck_image_list = {}
        self.truckDataWindow = None

        self.data = DataStore()
        self.model = None

    def set_buttons(self):
        self.new_data_set_button = QPushButton('New Data Set')
        self.load_data_set_button = QPushButton('Load Data Set')
        self.save_data_set_button = QPushButton('Save Data Set')

        self.truck_data_button = QPushButton('Truck Data')
        self.system_data_button = QPushButton('System Data')
        self.algorithm_data_button = QPushButton('Algorithm Data')

        self.generate_data_set_button = QPushButton('Generate Data Set')
        self.show_data_button = QPushButton('Show Data Set')
        self.print_gams_button = QPushButton('Print gams output')

        self.data_set_ready_button = QPushButton('Data Set Ready')

        self.solve_step_button = QPushButton('Solve Next Step')
        self.solve_iteration_button = QPushButton('Solve Next Iteration')
        self.solve_next_data_set_button = QPushButton('Solve Next Data Set')

        self.show_debug_logger_button = QPushButton('Show Debug Logger')
        self.show_logger_button = QPushButton('Show Logger')
        self.show_simulation_button = QPushButton('Show Simulation')

        self.new_data_set_button.clicked.connect(self.new_data_set)
        self.load_data_set_button.clicked.connect(self.load_data)
        self.save_data_set_button.clicked.connect(self.save_data)

        self.truck_data_button.clicked.connect(self.show_truck_data)
        self.system_data_button.clicked.connect(self.show_system_data)
        self.algorithm_data_button.clicked.connect(self.show_algorithm_data)

        self.generate_data_set_button.clicked.connect(self.generate_data_set)
        self.show_data_button.clicked.connect(self.show_data)
        self.print_gams_button.clicked.connect(self.print_gams)

        self.data_set_ready_button.clicked.connect(self.data_set_ready)

    def set_layout(self):
        self.data_set_layout = QGridLayout()
        self.data_set_layout.addWidget(self.new_data_set_button, 1 ,1)
        self.data_set_layout.addWidget(self.load_data_set_button, 1 ,2)
        self.data_set_layout.addWidget(self.save_data_set_button, 1 ,3)

        self.data_set_layout.addWidget(self.truck_data_button, 2 ,1)
        self.data_set_layout.addWidget(self.system_data_button, 2 ,2)
        self.data_set_layout.addWidget(self.algorithm_data_button, 2 ,3)

        self.data_set_layout.addWidget(self.generate_data_set_button, 3, 1)
        self.data_set_layout.addWidget(self.show_data_button, 3, 2)
        self.data_set_layout.addWidget(self.print_gams_button, 3, 3)

        self.data_set_layout.addWidget(self.data_set_ready_button, 4, 1)

        self.solver_layout = QGridLayout()
        self.solver_layout.addWidget(self.solve_step_button, 1, 1)
        self.solver_layout.addWidget(self.solve_iteration_button, 1, 2)
        self.solver_layout.addWidget(self.solve_next_data_set_button, 1, 3)

        self.interaction_layout = QGridLayout()
        self.interaction_layout.addWidget(self.show_logger_button, 1, 1)
        self.interaction_layout.addWidget(self.show_debug_logger_button, 1, 2)
        self.interaction_layout.addWidget(self.show_simulation_button, 1, 3)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.data_set_layout)
        self.layout.addLayout(self.solver_layout)
        self.layout.addLayout(self.interaction_layout)

        self.setLayout(self.layout)

    def new_data_set(self):
        """
        :return:
        """
        self.data = DataStore()

    def load_data(self):
        """
        loads prev saved data
        :return:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.data = pickle.load(open(file_name, 'rb'))

    def save_data(self):
        """
        saves current data
        :return:
        """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        pickle.dump(self.data,  open(file_name, 'wb'))

    def generate_data_set(self):
        # ask if sure

        self.data.arrival_times = []
        self.data.boundaries = []
        self.model = Solver(self.data)

        for i in range(len(self.data.data_set_list)):
            self.model.current_data_set = i
            self.model.set_data()

    def show_data(self):
        self.data_show = ShowData(self.data)
        self.data_show.exec_()

    def print_gams(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Open file', '/home')
        for i in range(len(self.data.data_set_list)):
            gams_writer(file_name + str(i), i, self.data )

    def show_truck_data(self):
        """
        shows data about the trucks
        :return:
        """
        self.truckDataWindow = TruckDataWindow(self.data)
        self.truckDataWindow.exec_()

    def show_system_data(self):
        """
        shows data set
        :return:
        """
        self.dataWindow = DataSetWindow(self.data)
        self.dataWindow.exec_()

    def show_algorithm_data(self):
        pass

    def data_set_ready(self):
        #enable solve buttons
        self.model = Solver(self.data)

    def init_simulation(self):
        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn, self.model)
        # self.setCentralWidget(self.simulation)

        #self.setup_simulation()

    def simulation_cycle(self):
        i = 0
        for inbound_trucks in self.model.inbound_trucks.values():
            truck_name = inbound_trucks.truck_name
            self.truck_image_list[truck_name] = self.scn.addPixmap(self.truckPixmap)
            self.truck_image_list[truck_name].scale(0.2,0.2)
            self.truck_image_list[truck_name].setPos(-600,i*100)
            i = i +1
        self.simulation.show()

if __name__ == '__main__':
    with open('capraz.log', 'w'):
        pass
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='capraz.log', level=logging.DEBUG)
    logging.info('Program Started')
    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    myApp.exec_()
    sys.exit(0)
