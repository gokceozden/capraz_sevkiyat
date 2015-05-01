__author__ = 'robotes'

from receiving_door import ReceivingDoors
from shipping_doors import ShippingDoors

class Station(object):
    """
    Station for the goods to come in and go out.
    """
    def __init__(self):
        """
        Initialize the station by creating doors and types
        :return:
        """

        self.receiving_doors = []
        self.sending_doors = []

    def add_receiving_door(self):
        """
        creates a receiving door
        :return:
        """
        pass