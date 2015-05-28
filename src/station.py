__author__ = 'robotes'

from src.receiving_door import ReceivingDoor
from src.shipping_doors import ShippingDoor
import itertools

class Station(object):
    """
    Station for the goods to come in and go out.
    """
    def __init__(self):
        """
        Initialize the station by creating doors and types
        :return:
      """

        self.receiving_doors = {}
        self.shipping_doors = {}


    def add_receiving_door(self):
        """
        creates a receiving door
        :return:
        """
        
        name = 'recv' + str(len(self.receiving_doors))
        door = ReceivingDoor()
        self.receiving_doors[name] = door

    def clear_door_sequences(self):
        for doors in itertools.chain(self.receiving_doors.values(), self.shipping_doors.values()):
            doors.sequence = []

    def remove_receiving_door(self):
        """
        removes a receiving door from the station
        :return:
        """
        name = 'recv' + str(len(self.receiving_doors)-1)
        del self.receiving_doors[name]


    def add_shipping_door(self):
        """
        creates a shipping door
        :return:
        """
        name = 'ship' + str(len(self.shipping_doors))
        door = ShippingDoor()
        self.shipping_doors[name] = door

    def remove_shipping_door(self):
        """
        removes a receiving door from the station
        :return:
        """
        name = 'ship' + str(len(self.shipping_doors)-1)
        del self.shipping_doors[name]
