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
    def __init__(self):
        """
        init text screen for info
        :return:
        """
        QWidget.__init__(self)
        self.data = None
        self.infoText = QTextEdit()
        self.infoText.setReadOnly(True)
        # self.scn = QGraphicsScene()
        # self.simulation = GraphView(self.scn, self.data)

        self.layout = QGridLayout()
        self.layout.addWidget(self.infoText, 1, 1)

        # cycle booleans
        self.time_bool = False
        self.iteration_bool = False
        self.data_set_bool = False
        self.pause_bool = False

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

    def start_solution(self, data=DataStore()):
        """
        Starts solution for a data set
        :param data: data store
        :return:
        """
        self.data = data
        self.model = Solver(self.data)
        self.print_start_data()

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
        pass

    def solve_step(self):
        """
        goes one time step forward
        :return:
        """
        pass

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


