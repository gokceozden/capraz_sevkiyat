__author__ = 'robotes'

from receiving_door import ReceivingDoor
from shipping_doors import ShippingDoor

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


        door = ReceivingDoor()



    def add_shipping_door(self):
        """
        creates a shipping door
        :return:
        """

        door = ShippingDoor()

