__author__ = 'mustafa'

import logging
import itertools
from src.solver import Solver
import random
import copy
import math
class Algorithms(object):
    """
    all the algorithms
    """
    def __init__(self):
        self.start_sequence_algorithms = {}
        self.next_sequence_algorithms = {}
        self.calculate_algorithms = {}

        self.temperature_reduction_rate = 0.9
        self.temperature = 100
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
        self.current_sequence['error'] = 0

        self.next_sequence = copy.deepcopy(self.current_sequence)
        self.solution_sequence = copy.deepcopy(self.current_sequence)
        self.best_sequence = copy.deepcopy(self.current_sequence)

    def set_algorithms(self, model):
        self.model = model

    def start(self):
        self.start_sequence_algorithms[self.start_algorithm]()

    def next(self):
        self.next_sequence_algorithms[self.next_algorithm]()

    def calculate(self):
        self.calculate_algorithms[self.calculate_algorithm]()

    def next_sequence(self):
        pass

    def start1(self):
        # do for outbound trucks too

        name = 'recv'
        self.init_sequence = [[] for i in range(self.model.number_of_receiving_doors)]

        unsorted_trucks = []
        # sort trucks
        for truck in itertools.chain(self.model.inbound_trucks.values(), self.model.compound_trucks.values()):
            truck_times = (truck.finish_time, truck.truck_name)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (time, truck) in sorted(unsorted_trucks)]

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

        # outbound
        self.init_sequence = [[] for i in range(self.model.number_of_shipping_doors)]
        unsorted_trucks = []
        # sort trucks
        for truck in self.model.outbound_trucks.values():
            truck_times = (truck.finish_time, truck.truck_name)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (time, truck) in sorted(unsorted_trucks)]
        for truck in self.model.compound_trucks.values():
            sorted_trucks.append(truck.truck_name)



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

        logging.info("Start sequence inbound: {0}".format(self.current_sequence['inbound']))
        logging.info("Start sequence outbound: {0}".format(self.current_sequence['outbound']))
        self.solution_sequence = copy.deepcopy(self.current_sequence)
        self.best_sequence = copy.deepcopy(self.current_sequence)

    def random1(self):
        """
        generates a random next sequence
        :return:
        """
        self.next_sequence = copy.deepcopy(self.current_sequence)

        truck_type = 'inbound'
        a, b = self.generate_random(truck_type)
        indexA = self.next_sequence[truck_type].index(a)
        indexB = self.next_sequence[truck_type].index(b)
        self.next_sequence[truck_type][indexA] = b
        self.next_sequence[truck_type][indexB] = a

        truck_type = 'outbound'
        a, b = self.generate_random(truck_type)
        indexA = self.next_sequence[truck_type].index(a)
        indexB = self.next_sequence[truck_type].index(b)
        self.next_sequence[truck_type][indexA] = b
        self.next_sequence[truck_type][indexB] = a
        self.next_sequence['error'] = 0

        logging.info("Random1 next sequence inbound: {0}".format(self.next_sequence['inbound']))
        logging.info("Random1 next sequence outbound: {0}".format(self.next_sequence['outbound']))
        self.solution_sequence = copy.deepcopy(self.next_sequence)

    def generate_random(self, truck_type):
        a = random.choice(self.current_sequence[truck_type])
        b = random.choice(self.current_sequence[truck_type])
        if a == b:
            a, b = self.generate_random(truck_type)
        if isinstance(a, int) and isinstance(b, int):
            a, b = self.generate_random(truck_type)
        return a, b

    def annealing1(self):
        # get next sequence
        # bir eksik var ????
        if self.solution_sequence['error'] < self.current_sequence['error']:
            self.current_sequence = copy.deepcopy(self.solution_sequence)
            if self.solution_sequence['error'] < self.best_sequence['error']:
                self.best_sequence = copy.deepcopy(self.current_sequence)
        else:
            p_accept = math.exp((self.current_sequence['error'] - self.solution_sequence['error']) / self.temperature)
            if p_accept >= random.random():
                self.current_sequence = copy.deepcopy(self.solution_sequence)


        self.temperature = self.temperature_reduction_rate * self.temperature

        self.previous_sequence = copy.deepcopy(self.current_sequence)
        self.solution_sequence = copy.deepcopy(self.current_sequence)

    def tabu1(self):
        pass

    def calculate_error1(self):
        """
        calculates error at the end of simulation
        :return:
        """
        pass