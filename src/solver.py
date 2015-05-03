__author__ = 'robotes'

from truck import *

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

        truck = 5

        # add the created truck to the dictionary
        self.truck_dictionary[type].append(truck)
