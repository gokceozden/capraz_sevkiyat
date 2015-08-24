__author__ = 'mustafa'

import itertools
from PySide.QtGui import *
from PySide.QtCore import *
from src.graphview import GraphView
from src.solver import Solver
from src.data_store import DataStore
from src.algorithm_screen import ChooseAlgo
from src.algorithms import Algorithms

class GeneralInfo(QWidget):
    """
    General information screen in main gui
    """
    def __init__(self, status_bar):
        """
        init text screen for info
        :return:
        """
        QWidget.__init__(self)
        self.data = None
        self.infoText = QTextEdit()
        self.infoText.setReadOnly(True)
        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn)

        self.status_bar = status_bar
        # solution types
        self.solution_list = {}
        self.solution_list['iteration'] = self.solve_iteration
        self.solution_list['step'] = self.solve_step
        self.solution_list['data_set'] = self.solve_dataset
        self.solution_list['solve'] = self.solve

        self.solution_type = 'iteration'

        # cycle booleans
        self.solve_bool = False
        self.step_bool = False
        self.iteration_bool = False
        self.data_set_bool = False
        self.pause_bool = False

        # buttons
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

        self.pause_button = QPushButton("Pause")
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        self.solution_type_combo = QComboBox()
        self.solution_type_combo.addItems(self.solution_list.keys())

        self.play_button.setDisabled(True)
        self.stop_button.setDisabled(True)
        self.pause_button.setDisabled(True)
        self.solution_type_combo.setDisabled(True)

        self.play_button.clicked.connect(self.solve)
        self.pause_button.clicked.connect(self.pause)

        # setup layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.infoText, 1, 1, 1)
        self.layout.addWidget(self.simulation, 1, 2)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.play_button)
        self.h_layout.addWidget(self.stop_button)
        self.h_layout.addWidget(self.pause_button)
        self.h_layout.addWidget(self.solution_type_combo)
        self.layout.addLayout(self.h_layout, 2, 1)

        # self.layout.addWidget(self.simulation, 1, 2)
        self.setLayout(self.layout)
        self.model = None
        self.data = DataStore()
        self.current_iteration = 1
        self.iteration_limit = 100
        self.current_data_set = 0
        self.data_string = ''
        self.algorithms = Algorithms()
        self.algo_screen = ChooseAlgo()

        self.trial_time = 0

    def init_solution(self, data=DataStore()):
        """
        Starts solution for a data set
        :param data: data store
        :return:
        """
        self.play_button.setDisabled(False)
        self.stop_button.setDisabled(False)
        self.pause_button.setDisabled(False)
        self.solution_type_combo.setDisabled(False)

        self.data = data
        self.model = Solver(self.data)
        self.simulation.init_image(self.model)
        self.print_start_data()
        numbers = {'inbound': self.data.number_of_inbound_trucks, 'outbound': self.data.number_of_outbound_trucks,
                   'compound': self.data.number_of_compound_trucks, 'receive': self.data.number_of_receiving_doors,
                   'shipping': self.data.number_of_shipping_doors}
        self.algorithms.set_algorithms(self.model)
        self.model.set_data(0)

    def solution_type_choice(self):
        """
        update bools for the choosen solution type
        :return:
        """
        choice = self.solution_type_combo.currentText()
        if choice == 'solve':
            self.solve_bool = True
            self.data_set_bool = False
            self.iteration_bool = False
            self.step_bool = False

        elif choice == 'data_set':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = False
            self.step_bool = False

        elif choice == 'iteration':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = True
            self.step_bool = False

        elif choice == 'step':
            self.solve_bool = True
            self.data_set_bool = True
            self.iteration_bool = True
            self.step_bool = True

    def choose_algorithm(self):
        """
        choose and algorithm
        :return:
        """
        self.algo_screen.exec_()
        self.iteration_limit = self.algo_screen.iteration_number
        #get algorithm

    def pause(self):
        self.pause_bool = True

    def solve(self):
        """
        solves all of the data sets
        :return:
        """
        self.pause_bool = False
        self.solution_type_choice()
        # print('solve')
        self.solve_dataset()

    def solve_dataset(self):
        """
        solves one data set
        :return:
        """
        if self.data_set_bool:
            #print('one_set')1
            if self.current_iteration == 1 and self.model.current_time == 0:
                self.model.set_data(self.current_data_set)
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
                self.model.set_data(self.current_data_set)
                self.solve_iteration()
                self.current_data_set += 1
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
                        self.algorithms.next_sequence()
                    self.model.set_sequence(self.algorithms.solution_sequence)
                # next sequence
                self.solve_step()
                self.current_iteration += 1
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
            if self.pause_bool:
                break
            self.model.next_step()

            #finished
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            truck.calculate_error()

        #add reset
        self.model.finish = False
        self.current_iteration += 1
        self.algorithms.current_sequence['error'] = self.add_errors()
        self.model.reset_trucks()
        #self.print_results()

    def solve_one_step(self):
        """
        goes one time step forward
        :return:
        """

        self.model.next_step()
        self.simulation.update_image()

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
            self.algorithms.current_sequence['error'] = self.add_errors()

    def add_errors(self):
        """
        adds absolute values of the errors

        :return:
        """
        total_error = 0
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            total_error += abs(truck.error)
        print('total error', total_error)
        return total_error

    def print_start_data(self):
        """
        prints the configuration info one time
        :return:
        """
        self.infoText.clear()
        self.data_string = ''
        self.data_string += "Number of inbound Trucks: {0}\n".format(self.data.number_of_inbound_trucks)
        self.data_string += "Number of outbound Trucks: {0}\n".format(self.data.number_of_outbound_trucks)
        self.data_string += "Number of compound Trucks: {0}\n".format(self.data.number_of_compound_trucks)
        self.data_string += "Number of receiving doors: {0}\n".format(self.data.number_of_receiving_doors)
        self.data_string += "Number of shipping doors: {0}\n".format(self.data.number_of_shipping_doors)
        #
        # data set
        self.infoText.setText(self.data_string)

    def step_time(self):
        pass

    def next_iteration(self):
        """
        increase iteration if limit not reached
        :return:
        """
        if self.current_iteration < self.iteration_limit:
            self.current_iteration += 1
        else:
            self.current_iteration = 0
            self.next_data_set()

    def next_data_set(self):
        pass

    def print_simulation_data(self):
        self.infoText.clear()
        self.data_string = ''
        self.data_string += "Iteration Number: {0}\n".format(self.current_iteration)
        self.data_string += "Inbound Sequence: {0}\n".format(self.algorithms.solution_sequence['inbound'])
        self.data_string += "Outbound Sequence: {0}\n".format(self.algorithms.solution_sequence['outbound'])
        # time
        # data set number
        # error value
        # sequence
        self.infoText.setText(self.data_string)

    def print_results(self):
        self.infoText.clear()
        for truck in self.model.outbound_trucks.values():
            print('bounds', truck.bounds)
            print('error', truck.error)
            print('finish', truck.finish_time)

