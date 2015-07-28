__author__ = 'robotes'

from src.truck import *
from src.station import *
from src.tavlama import Tavlama
from src.data_store import DataStore
from collections import OrderedDict
from src.good import Good

class Solver(object):
    """
    Solver class contains everything needed for the solution and simulation.
    """

    def __init__(self, data=DataStore()):
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
        self.number_of_inbound_trucks = self.data.number_of_inbound_trucks
        self.number_of_outbound_trucks = self.data.number_of_outbound_trucks
        self.number_of_compound_trucks = self.data.number_of_compound_trucks
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

        # create trucks
        self.inbound_data['arrival_time'] = self.data.inbound_arrival_time
        self.inbound_data['mu'] = self.inbound_mu
        self.inbound_data['product_per_truck'] = self.product_per_inbound_truck

        self.outbound_data['arrival_time'] = self.data.outbound_arrival_time
        self.outbound_data['mu'] = self.outbound_mu
        self.outbound_data['product_per_truck'] = self.product_per_outbound_truck

        self.compound_data['arrival_time'] = self.data.inbound_arrival_time
        self.compound_data['mu'] = self.inbound_mu
        self.compound_data['transfer_time'] = self.data.transfer_time
        self.compound_data['inbound_product_per_truck'] = self.product_per_inbound_truck
        self.compound_data['outbound_product_per_truck'] = self.product_per_outbound_truck

        self.truck_data['loading_time'] = self.data.loading_time
        self.truck_data['changeover_time'] = self.data.changeover_time
        self.truck_data['makespan_factor'] = self.data.makespan_factor # not used anthwere!!
        self.truck_data['alpha'] = self.alpha
        self.truck_data['gamma'] = self.gamma
        self.truck_data['tightness_factor'] = self.tightness_factor

        self.station = Station()
        self.create_trucks()

        # init model solution
        self.current_time = 0
        self.time_step = 1

    def calculate_mu(self):
        """
        calculates the mu values for coming and going trucks
        :return:
        """
        self.inbound_mu = float(self.number_of_coming_trucks / self.data.number_of_receiving_doors)
        self.outbound_mu = float(self.number_of_going_trucks / self.data.number_of_shipping_doors)

    def calculate_product_per_truck(self):
        """
        calculates products per truck
        :return:
        """
        total_coming_goods = 0
        total_going_goods = 0

        for amount in itertools.chain(self.data.inbound_goods, self.data.compound_coming_goods):
            total_coming_goods += sum(amount)

        for amount in itertools.chain(self.data.outbound_goods, self.data.compound_going_goods):
            total_going_goods += sum(amount)

        self.product_per_inbound_truck = total_coming_goods / self.number_of_coming_trucks
        self.product_per_outbound_truck = total_going_goods / self.number_of_going_trucks

    def create_trucks(self):
        """
        creates trucks for the given values
        :return:
        """
        for i in range(self.data.number_of_inbound_trucks):
            self.truck_data['number'] = i
            name = 'inbound' + str(i)
            self.truck_data['name'] = name
            self.inbound_trucks[name] = InboundTruck(self.truck_data, self.inbound_data)
            coming_goods = self.data.inbound_goods[i]
            for k, amount in enumerate(coming_goods):
                new_good = Good(k, amount)
                self.inbound_trucks[name].coming_goods.append(new_good)

        for i in range(self.data.number_of_outbound_trucks):
            self.truck_data['number'] = i
            name = 'outbound' + str(i)
            self.truck_data['name'] = name
            self.outbound_trucks[name] = OutboundTruck(self.truck_data, self.outbound_data)
            going_goods = self.data.outbound_goods[i]
            for k, amount in enumerate(going_goods):
                new_good = Good(k, amount)
                self.outbound_trucks[name].going_goods.append(new_good)

        for i in range(self.data.number_of_compound_trucks):
            self.truck_data['number'] = i
            name = 'compound' + str(i)
            self.truck_data['name'] = name
            self.compound_trucks[name] = CompoundTruck(self.truck_data, self.compound_data)
            coming_goods = self.data.compound_coming_goods[i]
            going_goods = self.data.compound_going_goods[i]
            for k, amount in enumerate(coming_goods):
                print('amount', amount)
                new_good = Good(k, amount)
                self.compound_trucks[name].coming_goods.append(new_good)
            for k, amount in enumerate(going_goods):
                new_good = Good(k, amount)
                self.compound_trucks[name].going_goods.append(new_good)


        # add doors
        for i in range(self.data.number_of_receiving_doors):
            self.station.add_receiving_door()

        for i in range(self.data.number_of_shipping_doors):
            self.station.add_shipping_door()


    def set_data(self, data_set_number):
        """
        sets alpha gamma, tightness factor and twogd values
        :return:
        """
        self.data.setup_data_set(data_set_number)

        for truck in self.inbound_trucks.values():
            truck.alpha = self.data.alpha
            truck.gamma = self.data.gamma
            truck.tightness_factor = float(self.data.tightness_factor)
            truck.calculate_gdj()

        for truck in self.outbound_trucks.values():
            truck.alpha = self.data.alpha
            truck.gamma = self.data.gamma
            truck.tightness_factor = float(self.data.tightness_factor)
            truck.calculate_gdj()

        for truck in self.compound_trucks.values():
            truck.alpha = self.data.alpha
            truck.gamma = self.data.gamma
            truck.tightness_factor = float(self.data.tightness_factor)
            truck.calculate_gdj()

    def set_sequence(self, sequence):
        """
        sets sequence to trucks and doors
        :param sequence:
        :return:
        """
        self.current_sequence = sequence['inbound']
        self.door_sequences = []
        prev_index = 0

        for door_number in range(self.number_of_receiving_doors - 1):
            current_index = self.current_sequence.index(door_number)
            door_sequence = self.current_sequence[prev_index:current_index]
            self.door_sequences.append(door_sequence)
        self.door_sequences.append(self.current_sequence[prev_index:])

        for i, door_sequence in enumerate(self.door_sequences):
            door_name = 'recv' + str(i)
            print('door_sequence', door_sequence)
            for trucks in door_sequence:
                if trucks in self.inbound_trucks:
                    print('truck', trucks)
                    self.inbound_trucks[trucks].receiving_door_name = door_name
                    self.station.receiving_doors[door_name].sequence.append(self.inbound_trucks[trucks])
                if trucks in self.compound_trucks:
                    self.compound_trucks[trucks].receiving_door_name = door_name
                    self.station.receiving_doors[door_name].sequence.append(self.compound_trucks[trucks])

        for door_number in range(self.number_of_shipping_doors - 1):
            current_index = self.current_sequence.index(door_number)
            door_sequence = self.current_sequence[prev_index:current_index]
            self.door_sequences.append(door_sequence)
        self.door_sequences.append(self.current_sequence[prev_index:])

        for i, door_sequence in enumerate(self.door_sequences):
            door_name = 'ship' + str(i)
            print('door_sequence', door_sequence)
            for trucks in door_sequence:
                if trucks in self.inbound_trucks:
                    print('truck', trucks)
                    self.inbound_trucks[trucks].receiving_door_name = door_name
                    self.station.receiving_doors[door_name].sequence.append(self.inbound_trucks[trucks])
                if trucks in self.compound_trucks:
                    self.compound_trucks[trucks].receiving_door_name = door_name
                    self.station.receiving_doors[door_name].sequence.append(self.compound_trucks[trucks])

            #prev_index = current_index + 1
        #
        # self.door_sequences.append(self.current_sequence[prev_index:])
        # print(self.door_sequences)
        # i = 0
        # name = 'recv'

        # self.station.clear_door_sequences()  # delete previous sequences
        #
        # self.tavlama = Tavlama(self)
        # sequence = self.tavlama.initialize_sequence()
        #
        # # for coming_truck in itertools.chain(self.inbound_trucks.values(), self.compound_trucks.values()):
        # #     door_name = name + str(i)
        # #     i += 1
        # #     self.station.receiving_doors[door_name].sequence.append(coming_truck)
        # #     if i == len(self.station.receiving_doors):
        # #         i = 0
        # #
        # for door_name, truck_names in sequence.iteritems():
        #     trucks = dict(self.inbound_trucks.items() + self.compound_trucks.items())
        #     for truck_name in truck_names:
        #         self.station.receiving_doors[door_name].sequence.append(trucks[truck_name])
        #
        # for doors in self.station.receiving_doors.values():
        #     doors.set_truck_doors()
        #
        # i = 0
        # for going_trucks in itertools.chain(self.outbound_trucks.values(), self.compound_trucks.values()):
        #     door_name = 'ship' + str(i)
        #     i += 1
        #     self.station.shipping_doors[door_name].sequence.append(going_trucks)
        #     if i == len(self.station.shipping_doors):
        #         i = 0
        #
        # for doors in self.station.shipping_doors.values():
        #     doors.set_truck_doors()

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

