__author__ = 'robotes'

from src.truck import *
import itertools
from src.station import *

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
        
        self.alpha = [0]
        self.gamma = [0]
        self.loading_time = 0
        self.changeover_time = 0
        self.makespan_factor = 0


        self.inbound_mu = 0
        self.outbound_mu = 0
        
        self.number_of_shipping_doors = 0
        self.number_of_receiving_doors = 0

        self.product_per_inbound_truck = 0
        self.product_per_outbound_truck = 0

        self.station = Station()


    def calculate_mu(self):
            
        self.inbound_mu = (len(self.inbound_truck) + len(self.compound_truck)) / self.number_of_receiving_doors
        self.outbound_mu = (len(self.outbound_truck) + len(self.compound_truck)) / self.number_of_shipping_doors
        
        
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


        # create a truck with given type

        # add the created truck to the dictionary


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
