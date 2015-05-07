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
        self.inbound_trucks = []
        self.outbound_trucks = []
        self.compound_trucks = []
        self.goods = []
        self.number_of_goods = 0

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

        # create a truck with given type

        # add the created truck to the dictionary
        self.truck_dictionary[type].append(truck)

    def add_good(self, type):
        """
        adds a good to the system
        :return:
        """
        self.goods.append(type)
