__author__ = 'robotes'

from src.truck import *
import itertools
from src.station import *
from src.data_set import DataSet
from src.tavlama import Tavlama


class Solver(object):
    """
    Solver class contains everything needed for the solution and simulation.
    """

    def __init__(self):
        """
        Initialize trucks, the station and get ready to solve
        :return: nothing
        """
        self.data_name = 'unnamed'
        self.inbound_trucks = {}
        self.outbound_trucks = {}
        self.compound_trucks = {}
        self.goods = []
        self.number_of_goods = 0
        self.number_of_trucks = 0
        self.truck_dictionary = {'inbound': self.inbound_trucks,
                                 'outbound': self.outbound_trucks,
                                 'compound': self.compound_trucks
                                 }

        self.arrival_time = [0, 0]
        self.alpha = [0]
        self.gamma = [0]
        self.tightness_factor = [0]
        self.loading_time = 0
        self.changeover_time = 0
        self.makespan_factor = 0
        self.data_set = []
        self.inbound_mu = 0
        self.outbound_mu = 0
        self.number_of_shipping_doors = 0
        self.number_of_receiving_doors = 0
        self.product_per_inbound_truck = 0
        self.product_per_outbound_truck = 0
        self.station = Station()
        self.current_time = 0
        self.set_size = 0
        self.current_set = 0
        self.time_step = 1
        self.end_time = 10
        self.tavlama = None

    def init_data(self):
        self.calculate_product_per_truck()
        self.calculate_mu()
        self.create_data_set()
        self.calculate()
        self.create_sequence()

    def create_sequence(self):
        # i = 0
        # name = 'recv'

        self.station.clear_door_sequences()  # delete previous sequences

        self.tavlama = Tavlama(self)
        sequence = self.tavlama.initialize_sequence()

        # for coming_truck in itertools.chain(self.inbound_trucks.values(), self.compound_trucks.values()):
        #     door_name = name + str(i)
        #     i += 1
        #     self.station.receiving_doors[door_name].sequence.append(coming_truck)
        #     if i == len(self.station.receiving_doors):
        #         i = 0
        #

        for door_name, truck_names in sequence.iteritems():
            trucks = dict(self.inbound_trucks.items() + self.compound_trucks.items())
            for truck_name in truck_names:
                self.station.receiving_doors[door_name].sequence.append(trucks[truck_name])

        for doors in self.station.receiving_doors.values():
            doors.set_truck_doors()

        i = 0
        for going_trucks in itertools.chain(self.outbound_trucks.values(), self.compound_trucks.values()):
            door_name = 'ship' + str(i)
            i += 1
            self.station.shipping_doors[door_name].sequence.append(going_trucks)
            if i == len(self.station.shipping_doors):
                i = 0

        for doors in self.station.shipping_doors.values():
            doors.set_truck_doors()


    def create_data_set(self):
        self.calculate_mu()

        DataSet.inbound_mu = self.inbound_mu
        DataSet.outbound_mu = self.outbound_mu
        DataSet.product_per_inbound_truck = self.product_per_inbound_truck
        DataSet.product_per_outbound_truck = self.product_per_outbound_truck

        data_set = []
        for alpha in self.alpha:
            for gamma in self.gamma:
                for tightness in self.tightness_factor:
                    new_data_set = DataSet(alpha, gamma, tightness)
                    new_data_set.calculate_twoDG()
                    data_set.append(new_data_set)

        self.data_set = data_set
        self.set_size = len(self.data_set)

    def calculate(self):
        for coming_trucks in itertools.chain(self.inbound_trucks.values(), self.compound_trucks.values()):
            current_set = self.data_set[self.current_set]
            coming_trucks.calculate_gdj(current_set.inbound_twoGD, self.loading_time, self.changeover_time,
                                        current_set.alpha, current_set.gamma, self.tightness_factor, self.arrival_time,
                                        self.inbound_mu)
            coming_trucks.loading_time = self.loading_time

        for leaving_trucks in itertools.chain(self.outbound_trucks.values(), self.compound_trucks.values()):
            current_set = self.data_set[self.current_set]
            leaving_trucks.calculate_gdj(current_set.outbound_twoGD, self.loading_time, self.changeover_time,
                                        current_set.alpha, current_set.gamma, self.tightness_factor, self.arrival_time,
                                        self.outbound_mu)
            leaving_trucks.loading_time = self.loading_time

    def step(self):
        self.current_time += self.time_step
        print('current time: ', self.current_time)
        self.check_state_changers()

    def check_state_changers(self):

        for truck_types in self.truck_dictionary.values():
            for truck in truck_types.values():
                truck.current_action(self.current_time)

        for doors in itertools.chain(self.station.receiving_doors.values(), self.station.shipping_doors.values()):
            doors.current_action()

        self.station.check_states()

    # below are to set the system
    def calculate_mu(self):

        self.inbound_mu = (len(self.inbound_trucks) + len(self.compound_trucks)) / self.number_of_receiving_doors
        self.outbound_mu = (len(self.outbound_trucks) + len(self.compound_trucks)) / self.number_of_shipping_doors

        # changeover time
        for trucks in self.compound_trucks.values():
            trucks.changeover_time = self.changeover_time

    def calculate_product_per_truck(self):
        total_coming_goods = 0
        total_going_goods = 0

        for truck in itertools.chain(self.inbound_trucks.values(), self.compound_trucks.values()):
            for good in truck.coming_goods:
                total_coming_goods = total_coming_goods + good.amount

        for truck in itertools.chain(self.outbound_trucks.values(), self.compound_trucks.values()):
            for good in truck.going_goods:
                total_going_goods = total_going_goods + good.amount

        self.product_per_inbound_truck = total_coming_goods / (len(self.inbound_trucks) + len(self.compound_trucks))
        self.product_per_outbound_truck = total_going_goods / (len(self.outbound_trucks) + len(self.compound_trucks))

    def add_truck(self, type):
        """
        add a truck with given type
        :type self: object
        :param type: type of the truck
        :return: none
        """
        self.number_of_trucks += self.number_of_trucks
        if type == 'inbound':
            name = 'inbound' + str(len(self.inbound_trucks))
            new_truck = InboundTruck(name, type)

        if type == 'outbound':
            name = 'outbound' + str(len(self.outbound_trucks))
            new_truck = OutboundTruck(name, type)

        if type == 'compound':
            name = 'compound' + str(len(self.compound_trucks))
            new_truck = CompoundTruck(name, type)

        self.truck_dictionary[type][name] = new_truck

        return name

    def remove_truck(self, type):
        if type == 'inbound':
            name = 'inbound' + str(len(self.inbound_trucks) - 1)
            del self.truck_dictionary[type][name]

        if type == 'outbound':
            name = 'outbound' + str(len(self.outbound_trucks) - 1)
            del self.truck_dictionary[type][name]

        if type == 'compound':
            name = 'compound' + str(len(self.compound_trucks) - 1)
            del self.truck_dictionary[type][name]

        self.number_of_trucks -= self.number_of_trucks

    def add_good(self, type):
        """
        adds a good to the system
        :return:
        """
        self.goods.append(type)
