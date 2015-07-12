__author__ = 'mustafa'

#from solver import Solver
import itertools
import operator


class Tavlama(object):

    def __init__(self, model, temperature = 100, constant = 0.9, iteration_number = 100):
        self.model = model
        self.temperature = temperature
        self.temperature_constant = constant
        self.iteration_number = iteration_number
        self.current_sequence = {}
        self.best_seqeunce = {}
        self.previous_sequence = {}
        self.coming_trucks = {}
        self.sorted_coming_trucks = {}
        self.going_trucks = {}
        self.sorted_going_trucks = {}

        for truck in itertools.chain(self.model.inbound_trucks.values(), self.model.compound_trucks.values()):
            self.coming_trucks[truck.truck_name] = truck.inbound_gdj
            self.sorted_coming_trucks = sorted(self.coming_trucks.items(), key=operator.itemgetter(1))

        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            self.going_trucks[truck.truck_name] = truck.outbound_gdj
            self.sorted_going_trucks = sorted(self.going_trucks.items(), key=operator.itemgetter(1))

        for coming_doors in self.model.station.receiving_doors.keys():
            self.current_sequence[coming_doors] = []

        self.previous_sequence = self.current_sequence
        self.best_seqeunce = self.current_sequence

    def initialize_sequence(self):
        i = 0
        name = 'recv'
        for truck in self.sorted_coming_trucks:
            door_name = name + str(i)
            self.current_sequence[door_name].append(truck[0])
            i += 1
            if i>=len(self.current_sequence.keys()):
                i = 0

        print(self.current_sequence)
        self.previous_sequence = self.current_sequence
        self.best_seqeunce = self.current_sequence
        return self.current_sequence

    def calculate_next_sequence(self):
        pass

    def calculate_result(self):
        pass

