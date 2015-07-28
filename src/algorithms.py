__author__ = 'mustafa'

import itertools
from src.solver import Solver
import random

class Algorithms(object):
    """
    all the algorithms
    """
    def __init__(self):
        self.start_sequence_algorithms = {}
        self.next_sequence_algorithms = {}
        self.calculate_algorithms = {}

        self.model = None

        self.start_sequence_algorithms['start1'] = self.start1

        self.next_sequence_algorithms['random1'] = self.random1

        self.calculate_algorithms['annealing1'] = self.annealing1
        self.calculate_algorithms['tabu1'] = self.tabu1

        # choosen algorithms
        self.start_algorithm = 'start1'
        self.next_algorithm = 'random1'
        self.calculate_algorithm = 'annealing1'

        # sequences
        self.start_sequence = []
        self.current_sequence = {}
        self.current_sequence['inbound'] = []
        self.current_sequence['outbound'] = []
        self.previous_sequence = {}
        self.next_sequence = {}
        self.best_sequence = {}

    def set_algorithms(self, model):
        self.model = model

    def start(self):
        self.start_sequence_algorithms[self.start_algorithm]()

    def next(self):
        self.next_sequence_algorithms[self.next_algorithm]()

    def calculate(self):
        self.calculate_sequence_algorithms[self.calculate_algorithm]()

    def next_sequence(self):
        pass

    def start1(self):
        # do for outbound trucks too
        name = 'recv'
        self.init_sequence = [[] for i in range(self.model.number_of_receiving_doors)]

        unsorted_trucks = []
        # sort trucks
        for truck in itertools.chain(self.model.inbound_trucks.values(), self.model.compound_trucks.values()):
            truck_times = (truck.truck_name, truck.finish_time)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (truck, time) in sorted(unsorted_trucks)]
        i = 0
        for truck in sorted_trucks:
            self.init_sequence[i].append(truck)
            i += 1
            if i == self.model.number_of_receiving_doors:
                i = 0

        i = 0
        for items in self.init_sequence:
            self.current_sequence['inbound'].extend(items)
            self.current_sequence['inbound'].extend([i])
            i += 1

        self.current_sequence['inbound'].pop()

        # outboun
        self.init_sequence = [[] for i in range(self.model.number_of_shipping_doors)]
        unsorted_trucks = []
        # sort trucks
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            truck_times = (truck.truck_name, truck.finish_time)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (truck, time) in sorted(unsorted_trucks)]
        i = 0
        for truck in sorted_trucks:
            self.init_sequence[i].append(truck)
            i += 1
            if i == self.model.number_of_shipping_doors:
                i = 0

        i = 0
        for items in self.init_sequence:
            self.current_sequence['outbound'].extend(items)
            self.current_sequence['outbound'].extend([i])
            i += 1

        self.current_sequence['outbound'].pop()
        print(self.current_sequence)


        self.previous_sequence = self.current_sequence
        self.best_sequence = self.current_sequence

    def random1(self):
        """
        generates a random next sequence
        :return:
        """
        a, b = self.generate_random()
        indexA = self.current_sequence.index(a)
        indexB = self.current_sequence.index(b)
        self.current_sequence[indexA] = b
        self.current_sequence[indexB] = a

    def generate_random(self):
        a = random.choice(self.current_sequence)
        b = random.choice(self.current_sequence)
        if a == b:
            a, b = self.generate_random()
        if isinstance(a, int) and isinstance(b, int):
            a, b = self.generate_random()
        return (a, b)

    def annealing1(self):
        pass

    def tabu1(self):
        pass

    def calculate_error1(self):
        """
        calculates error at the end of simulation
        :return:
        """
        pass