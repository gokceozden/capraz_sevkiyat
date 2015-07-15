__author__ = 'robotes'

from src.truck import *
from src.station import *
from src.tavlama import Tavlama
from src.data_store import DataStore
from collections import OrderedDict

class Solver(object):
    """
    Solver class contains everything needed for the solution and simulation.
    """

    def __init__(self, data = DataStore()):
        """
        Initialize trucks, the station and get ready to solve
        :return: nothing
        """
        self.data = data
        self.inbound_trucks = OrderedDict()
        self.outbound_trucks = OrderedDict()
        self.compound_trucks = OrderedDict()
        self.inbound_data = {}
        self.outbound_data = {}
        self.compound_data = {}
        self.truck_data = {}
        self.number_of_goods = self.data.number_of_goods
        self.number_of_trucks = self.data.number_of_inbound_trucks + self.data.number_of_outbound_trucks + self.data.number_of_compound_trucks
        self.number_of_coming_trucks = self.data.number_of_inbound_trucks + self.data.number_of_compound_trucks
        self.number_of_going_trucks = self.data.number_of_outbound_trucks + self.data.number_of_compound_trucks
        self.truck_dictionary = {'inbound': self.inbound_trucks,
                                 'outbound': self.outbound_trucks,
                                 'compound': self.compound_trucks
                                 }

        self.number_of_shipping_doors = self.data.number_of_shipping_doors
        self.number_of_receiving_doors = self.data.number_of_receiving_doors

        self.alpha = 0
        self.gamma = 0
        self.tightness_factor = 0
        self.inbound_mu = 0
        self.outbound_mu = 0
        self.product_per_inbound_truck = 0
        self.product_per_outbound_truck = 0

        # calculate data
        self.calculate_mu()
        self.calculate_product_per_truck()

        self.inbound_data['arrival_time'] = self.data.inbound_arrival_time
        self.inbound_data['inbound_mu'] = self.inbound_mu

        self.outbound_data['arrival_time'] = self.data.outbound_arrival_time
        self.outbound_data['outbound_mu'] = self.outbound_mu

        self.compound_data['arrival_time'] = self.data.inbound_arrival_time
        self.compound_data['inbound_mu'] = self.inbound_mu
        self.compound_data['outbound_mu'] = self.outbound_mu

        self.truck_data['loading_time'] = self.data.loading_time
        self.truck_data['changeover_time'] = self.data.changeover_time
        self.truck_data['makespan_factor'] = self.data.makespan_factor # not used anthwere!!
        self.truck_data['alpha'] = self.alpha
        self.truck_data['gamma'] = self.gamma
        self.truck_data['tightness_factor'] = self.tightness_factor

        self.create_trucks()
        # init model solution
        #self.station = Station()
        self.current_time = 0
        self.time_step = 1

    def calculate_mu(self):
        """
        calculates the mu values for coming and going trucks
        :return:
        """
        self.inbound_mu = self.number_of_coming_trucks / self.data.number_of_receiving_doors
        self.outbound_mu = self.number_of_going_trucks / self.data.number_of_shipping_doors

    def calculate_product_per_truck(self):
        """
        calculates products per truck
        :return:
        """
        total_coming_goods = 0
        total_going_goods = 0

        for amount in  itertools.chain(self.data.inbound_goods, self.data.compound_coming_goods):
            total_coming_goods += sum(amount)

        for amount in itertools.chain(self.data.outbound_goods, self.data.compound_going_goods):
            total_going_goods += sum(amount)

        self.product_per_inbound_truck = total_coming_goods / self.number_of_coming_trucks
        self.product_per_outbound_truck = total_going_goods / self.number_of_going_trucks

    def set_data(self, data_set):
        """
        sets alpha gamma and tightness factor values
        :return:
        """
        self.alpha = data_set[0]
        self.gamma = data_set[1]
        self.tightness_factor = data_set[2]

    def create_trucks(self):
        """
        creates trucks for the given values
        :return:
        """
        for i in range(self.data.number_of_inbound_trucks):
            self.truck_data['number'] = i
            name = 'inbound' + str(i)
            self.inbound_trucks[name] = InboundTruck(self.truck_data, self.inbound_data)

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

    def next_step(self):
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
