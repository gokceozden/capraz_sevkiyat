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
from src.logger_output import LogData
import itertools
from src.algorithms import Algorithms

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

        self.current_iteration = 1
        self.iteration_limit = 100
        self.current_data_set = 0

        self.algorithms = None

        self.solution_choice = None

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

        self.data_set_number = QSpinBox()
        self.data_set_number.setMinimum(0)

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

        self.show_logger_button.clicked.connect(self.show_data)

        self.solve_next_data_set_button.clicked.connect(self.data_set_button)
        self.solve_iteration_button.clicked.connect(self.iteration_button)
        self.solve_step_button.clicked.connect(self.step_button)
        self.data_set_number.valueChanged.connect(self.set_data_set_number)

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
        self.solver_layout.addWidget(self.data_set_number, 1, 4)

        self.interaction_layout = QGridLayout()
        self.interaction_layout.addWidget(self.show_logger_button, 1, 1)
        self.interaction_layout.addWidget(self.show_debug_logger_button, 1, 2)
        self.interaction_layout.addWidget(self.show_simulation_button, 1, 3)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.data_set_layout)
        self.layout.addLayout(self.solver_layout)
        self.layout.addLayout(self.interaction_layout)

        self.setLayout(self.layout)
        self.pause_bool = False

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
        self.algorithms = Algorithms()
        self.model = Solver(self.data)
        self.model.current_data_set = self.current_data_set
        self.model.load_data_set()
        self.algorithms.set_algorithms(self.model)
        self.current_iteration = 1
        self.iteration_limit = 100

    def show_data(self):
        self.logger = LogData()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(self.logger)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
        self.logger.show()
        logging.info('Logger Started')

    def data_set_button(self):
        self.solution_choice = 'data_set'
        self.solution_type_choice()
        self.solve_dataset()

    def iteration_button(self):
        self.solution_choice = 'iteration'
        self.solution_type_choice()
        self.solve_dataset()

    def step_button(self):
        self.solution_choice = 'step'
        self.solution_type_choice()
        self.solve_dataset()

    def set_data_set_number(self):
        self.current_data_set = self.data_set_number.value()

    def solve_dataset(self):
        """
        solves one data set
        :return:
        """
        logging.info('Data Set Number: {0}'.format(self.current_data_set))
        self.model.current_data_set = self.current_data_set
        if self.data_set_bool:
            #print('one_set')1
            if self.current_iteration == 1 and self.model.current_time == 0:
                self.model.load_data_set()
            self.solve_iteration()

            if self.current_data_set == len(self.data.data_set_list):
            #    print('finish')
                self.current_iteration = 1
                self.current_data_set = 0
                self.trial_time = 0
        else:
            while self.current_data_set < len(self.data.data_set_list):
                if self.pause_bool:
                    break
                self.model.load_data_set()
                self.solve_iteration()
            #   print(self.current_data_set)
            self.current_data_set = 0

    def solve_iteration(self):
        """
        solves one iteration
        :return:
        """
        if self.iteration_bool:
            #print('one_iteration')
            if self.model.current_time == 0:

                if self.current_iteration == 1:
                    print('start')
                    self.algorithms.start()
                    self.model.set_sequence(self.algorithms.solution_sequence)
                    self.solve_whole_step()
                    self.algorithms.next()
                    self.model.set_sequence(self.algorithms.solution_sequence)
                else:
                    self.algorithms.next()
                    self.model.set_sequence(self.algorithms.solution_sequence)
                self.print_simulation_data()
            self.solve_step()

            if self.current_iteration == self.iteration_limit:
                self.current_data_set += 1
                self.current_iteration = 1
        else:
            while self.current_iteration < self.iteration_limit:
                if self.pause_bool:
                    break

                self.print_simulation_data()
                if self.model.current_time == 0:
                    if self.current_iteration == 1:
                        self.algorithms.start()
                    else:
                        self.algorithms.next()
                    self.model.set_sequence(self.algorithms.solution_sequence)
                # next sequence
                self.solve_step()
            #print(self.current_iteration)
            self.current_iteration = 1
            #print('whole_iteration')

    def solve_step(self):
        if self.step_bool:
            self.solve_one_step()
        else:
            self.solve_whole_step()

    def solve_whole_step(self):
        """
        solves one iterations
        :return:
        """
        while not self.model.finish:
            if self.model.current_time > 800:

                break
            if self.pause_bool:
                break
            self.model.next_step()

            #finished
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            truck.calculate_error()

        #add reset
        self.model.finish = False
        self.algorithms.solution_sequence['error'] = self.add_errors()
        self.model.reset_trucks()
        if self.current_iteration > 1:
            self.algorithms.calculate()
        self.current_iteration += 1
        #self.print_results()

    def solve_one_step(self):
        """
        goes one time step forward
        :return:
        """

        self.model.next_step()
#        self.simulation.update_image()

        if self.model.finish:
            #finished
            for truck in self.model.outbound_trucks.values():
                truck.calculate_error()
            self.model.reset_trucks()
            # add reset
            self.add_errors()
            #self.print_results()
            self.current_iteration += 1
            self.model.finish = False
            self.algorithms.solution_sequence['error'] = self.add_errors()
            self.algorithms.calculate()

    def add_errors(self):
        """
        adds absolute values of the errors

        :return:
        """
        total_error = 0
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            total_error += abs(truck.error)
        logging.info("Error: {0}\n".format(total_error))
        return total_error

    def simulation_cycle(self):
        i = 0
        for inbound_trucks in self.model.inbound_trucks.values():
            truck_name = inbound_trucks.truck_name
            self.truck_image_list[truck_name] = self.scn.addPixmap(self.truckPixmap)
            self.truck_image_list[truck_name].scale(0.2,0.2)
            self.truck_image_list[truck_name].setPos(-600,i*100)
            i = i +1
        self.simulation.show()

    def solution_type_choice(self):
        """
        update bools for the choosen solution type
        :return:
        """

        if self.solution_choice == 'solve':
            self.solve_bool = True
            self.data_set_bool = False
            self.iteration_bool = False
            self.step_bool = False

        elif self.solution_choice == 'data_set':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = False
            self.step_bool = False
            self.data_set_ready()

        elif self.solution_choice == 'iteration':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = True
            self.step_bool = False

        elif self.solution_choice == 'step':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = True
            self.step_bool = True

    def print_simulation_data(self):
        logging.info("Iteration Number: {0}\n".format(self.current_iteration))
        logging.info("Inbound Sequence: {0}\n".format(self.algorithms.solution_sequence['inbound']))
        logging.info("Outbound Sequence: {0}\n".format(self.algorithms.solution_sequence['outbound']))



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
