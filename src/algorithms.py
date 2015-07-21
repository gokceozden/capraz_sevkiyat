__author__ = 'mustafa'

class Algorithms(object):
    """
    all the algorithms
    """
    def __init__(self):
        self.start_sequence_algorithms = {}
        self.next_sequence_algorithms = {}
        self.calculate_algorithms = {}

        self.start_sequence_algorithms['start1'] = self.start1

        self.next_sequence_algorithms['random1'] = self.random1

        self.calculate_algorithms['annealing1'] = self.annealing1
        self.calculate_algorithms['tabu1'] = self.tabu1

        # choosen algorithms
        self.start_algorithm = ''
        self.next_algorithm = ''
        self.calculate_algorithm = ''

        # sequences
        self.start_sequence = []
        self.current_sequence = []
        self.previous_sequence = []
        self.next_sequence = []
        self.best_sequence = []

    def start(self):
        self.start_sequence_algorithms[self.start_algorithm]

    def next(self):
        self.next_sequence_algorithms[self.next_algorithm]

    def calculate(self):
        self.calculate_sequence_algorithms[self.calculate_algorithm]

    def next_sequence(self):
        pass

    def start1(self):
        pass

    def random1(self):
        pass

    def annealing1(self):
        pass

    def tabu1(self):
        pass

