__author__ = 'mustafa'

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
        self.time_bool = False
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

        self.play_button.setDisabled(True)
        self.stop_button.setDisabled(True)
        self.pause_button.setDisabled(True)

        self.play_button.clicked.connect(self.start_button)

        # setup layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.infoText, 1, 1, 1)
        self.layout.addWidget(self.simulation, 1, 2)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.play_button)
        self.h_layout.addWidget(self.stop_button)
        self.h_layout.addWidget(self.pause_button)
        self.layout.addLayout(self.h_layout, 2, 1)

        # self.layout.addWidget(self.simulation, 1, 2)
        self.setLayout(self.layout)
        self.model = None
        self.data = DataStore()
        self.current_iteration = 1
        self.iteration_limit = 0
        self.current_data_set = 0
        self.data_string = ''
        self.algorithms = Algorithms()
        self.algo_screen = ChooseAlgo()

    def init_solution(self, data=DataStore()):
        """
        Starts solution for a data set
        :param data: data store
        :return:
        """
        self.play_button.setDisabled(False)
        self.stop_button.setDisabled(False)
        self.pause_button.setDisabled(False)

        self.data = data
        self.model = Solver(self.data)
        self.simulation.init_image(self.model)
        self.print_start_data()
        numbers = {'inbound': self.data.number_of_inbound_trucks, 'outbound': self.data.number_of_outbound_trucks,
                   'compound': self.data.number_of_compound_trucks, 'receive': self.data.number_of_receiving_doors,
                   'shipping': self.data.number_of_shipping_doors}
        self.algorithms.set_algorithms(self.model)
        self.model.set_data(0)
        # self.simulation.init_image(self.model)

    def choose_algorithm(self):
        """
        choose and algorithm
        :return:
        """
        self.algo_screen.exec_()
        self.iteration_limit = self.algo_screen.iteration_number
        #get algorithm

    def solve(self):
        """
        solves all of the data sets
        :return:
        """
        pass

    def solve_dataset(self):
        """
        solves one data set
        :return:
        """
        pass

    def solve_iteration(self):
        """
        solves one iteration
        :return:
        """
        if self.current_iteration == 1:
            self.algorithms.start()
        # until finish step forward
        solved_itration = False
        self.model.set_sequence(self.algorithms.current_sequence)
        while not solved_itration:
            solved_itration = self.solve_step()

    def solve_step(self):
        """
        goes one time step forward
        :return:
        """
        self.model.next_step()
        self.status_bar.showMessage(str(self.model.current_time))
        print('time', self.model.current_time)
        self.simulation.update_image()
        if self.model.urrent_time == 50:
            print('true')
            return True
        return False

    def start_button(self):
        """
        does a solution depending and the solution type
        :return:
        """
        self.solution_list[self.solution_type]()

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
        self.data_string += "Iteration Number:"
        # time
        # data set number
        # error value
        # sequence
        self.infoText.setText(self.data_string)


