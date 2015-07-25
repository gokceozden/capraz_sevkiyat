__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *
from src.algorithms import Algorithms

class ChooseAlgo(QDialog):
    """
    screen to choose algorithms
    """
    def __init__(self):
        """
        choose solution algorithms and set configurations
        :param algorithms:
        :return:
        """
        QDialog.__init__(self)

        self.setWindowTitle("Choose Algorithms")

        self.start_algo = ''
        self.next_algo = ''
        self.calculate_algo = ''
        self.algo = Algorithms()
        self.iteration_number = 0

        # cobo boxes
        self.start_label = QLabel('Start Algorithm')
        self.start_algo_combo = QComboBox()
        self.start_algo_combo.addItems(self.algo.start_sequence_algorithms.keys())

        self.next_label = QLabel('Next Algorithm')
        self.next_algo_combo = QComboBox()
        self.next_algo_combo.addItems(self.algo.next_sequence_algorithms.keys())

        self.calculate_label = QLabel('Calculate Algorithm')
        self.calculate_algo_combo = QComboBox()
        self.calculate_algo_combo.addItems(self.algo.calculate_algorithms.keys())

        # config data
        self.iteration_number_label = QLabel('Number of Iterations')
        self.iteration_number_edit = QLineEdit('0')

        # layout
        self.dataForm = QFormLayout()
        self.dataForm.addRow(self.start_label, self.start_algo_combo)
        self.dataForm.addRow(self.next_label, self.next_algo_combo)
        self.dataForm.addRow(self.calculate_label, self.calculate_algo_combo)
        self.dataForm.addRow(self.iteration_number_label, self.iteration_number_edit)

        self.setLayout(self.dataForm)

    def save_data(self):
        pass
        self.iteration_number = int(self.iteration_number_edit.text())
        #self.algo.calculate_algorithm = self.calculate_algo_c


