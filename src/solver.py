__author__ = 'robotes'

from src.truck import *
import itertools
from src.station import *
from src.data_set import DataSet

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

        self.arrival_time = [0,0]


        
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

        self.time_step = 1

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
                    new_data_set = DataSet(alpha,gamma,tightness)
                    new_data_set.calculate_twoDG()
                    data_set.append(new_data_set)

        
        self.data_set = data_set
        self.end_time = 50

        
    def init_simulation(self):


        self.calculate_product_per_truck()
        self.calculate_mu()
        self.create_data_set()
        
        for data_set in self.data_set:
            for trucks in itertools.chain(self.inbound_trucks.values(), self.outbound_trucks.values(), self.compound_trucks.values()):
                trucks.calculate_gdj(data_set.outbound_twoGD, self.loading_time, data_set.alpha, data_set.gamma, data_set.tightnessFactor, self.arrival_time)

        while(self.current_time < self.end_time):
            self.step()


    def calculate(self):

        pass
                
    def step(self):

        self.current_time = self.current_time + self.time_step
        self.check_state_changers()

    def check_state_changers(self):
            
        for truck_types in self.truck_dictionary.values():
            for truck in truck_types.values():
                if self.current_time in truck.state_change_times:
                    print('next state', self.current_time)
                    truck.next_state()
        
    def calculate_mu(self):

        self.inbound_mu = (len(self.inbound_trucks) + len(self.compound_trucks)) / self.number_of_receiving_doors
        self.outbound_mu = (len(self.outbound_trucks) + len(self.compound_trucks)) / self.number_of_shipping_doors
        
        
    def calculate_product_per_truck(self):

        total_coming_goods = 0
        total_going_goods = 0
        
        for truck in itertools.chain(self.inbound_trucks.values(), self.compound_trucks.values()):
            for good in truck.coming_goods.values():
                total_coming_goods = total_coming_goods + good.amount
                
                
        for truck in itertools.chain(self.outbound_trucks.values(), self.compound_trucks.values()):
            for good in truck.going_goods.values():
                total_going_goods = total_going_goods + good.amount


        self.product_per_inbound_truck = total_coming_goods / (len(self.inbound_trucks) + len(self.compound_trucks))
        self.product_per_outbound_truck = total_going_goods / (len(self.outbound_trucks) + len(self.compound_trucks))

        print('productpertruck', self.product_per_outbound_truck)
        
        
    def add_truck(self, type):
        """
        add a truck with given type
        :param type: type of the truck
        :return: none
        """
        self.number_of_trucks = self.number_of_trucks + 1
        if(type == 'inbound'):
            name = 'inbound' + str(len(self.inbound_trucks))
            new_truck = InboundTruck(name, type)

        if(type == 'outbound'):
            name = 'outbound' + str(len(self.outbound_trucks))
            new_truck = OutboundTruck(name, type)

        if(type == 'compound'):
            name = 'compound' + str(len(self.compound_trucks))
            new_truck = CompoundTruck(name, type)


        self.truck_dictionary[type][name] = new_truck
        return name

    def remove_truck(self, type):
        if(type == 'inbound'):
            name = 'inbound' + str(len(self.inbound_trucks) - 1)
            del self.truck_dictionary[type][name]

        if(type == 'outbound'):
            name = 'outbound' + str(len(self.outbound_trucks) - 1)
            del self.truck_dictionary[type][name]

        if(type == 'compound'):
            name = 'compound' + str(len(self.compound_trucks) - 1)
            del self.truck_dictionary[type][name]


        self.number_of_trucks = self.number_of_trucks - 1


    def add_good(self, type):
        """
        adds a good to the system
        :return:
        """
        self.goods.append(type)
