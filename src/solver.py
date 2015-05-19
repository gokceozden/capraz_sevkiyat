__author__ = 'robotes'

from src.truck import *

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
