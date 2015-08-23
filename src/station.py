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
        self.not_ready_goods = {}
        self.station_goods = {}

    def add_receiving_door(self):
        """
        creates a receiving door
        :return:
        """
        name = 'recv' + str(len(self.receiving_doors))
        door = ReceivingDoor(self, name)
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
        door = ShippingDoor(self, name)
        self.shipping_doors[name] = door

    def remove_shipping_door(self):
        """
        removes a receiving door from the station
        :return:
        """
        name = 'ship' + str(len(self.shipping_doors)-1)
        del self.shipping_doors[name]

    def check_states(self):
        for doors in itertools.chain(self.receiving_doors.values()):
            if doors.good_list:
                self.add_goods(doors.good_list)

    def add_goods(self, goods):
        for good in goods:
            if good.type in self.not_ready_goods.keys():
                self.not_ready_goods[good.type].append(good)
            else:
                self.not_ready_goods[good.type] = []
                self.not_ready_goods[good.type].append(good)
        print(self.not_ready_goods)

    def transfer_goods(self, good_type):
        """
        transfer goods inside the station
        :param good_tyoe:
        :return:
        """
        # problem with all the goods transfering at the same time
        self.station_goods[good_type].append(self.not_ready_goods.pop(good_type))

    def remove_goods(self, goods):
        for good in goods:
            max_item = None
            moved_good = 0
            error = good.amount - moved_good
            while error > 0 :
                for items in self.station_goods[good.type]:
                    next_item = items
                    if max_item is None or max_item.amount < next_item.amount:
                        max_item = next_item
                if max_item < error:
                    moved_good += max_item
                    max_item.amount = 0
                elif max_item >= error:
                    moved_good += error
                    max_item.amount -= error
                error = good.amount - moved_good