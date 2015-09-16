__author__ = 'robotes'
import logging
from src.good import Good
from copy import deepcopy

class ShippingDoor(object):
    """
    Shipping doors of the station
    """
    def __init__(self, station, name):
        self.station = station
        self.door_name = name
        self.trpe = 'Shipping'
        self.truck = None
        self.status = ['empty', 'loading']
        self.status_number = 0
        self.good_list = []
        self.sequence = []
        self.station = station
        self.waiting_trucks = 0
        self.loading_truck = None
        self.reserved_goods = {}

    def set_truck_doors(self):
        for truck in self.sequence:
            truck.shipping_door = self
            truck.shipping_door_name = self.door_name

    def current_action(self):
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.load()

    def next_state(self):
        self.status_number += 1

    def no_truck(self):
        if len(self.sequence) != 0:
            self.loading_truck = self.sequence[0]
            if self.loading_truck.state_list[self.loading_truck.current_state] == 'waiting_to_load':
                self.loading_truck.next_state()
                self.next_state()

    def check_goods(self):
        """
        check if enough in reserved goods
        :return:
        """
        logging.debug("---Check Goods")
        logging.debug("---Reserved goods:")
        for reserved_good in self.reserved_goods.values():
            for good in reserved_good:
                logging.debug("{0} : {1}".format(good.type, good.amount))

        logging.debug("---Station goods:")
        for station_good in self.station.station_goods.values():
            for good in station_good:
                logging.debug("{0} : {1}".format(good.type, good.amount))

        enough_goods = False
        for good in self.loading_truck.going_goods:
            total = 0
            if good.type in self.reserved_goods:
                enough_goods = True
                for reserved_good in self.reserved_goods[good.type]:
                    total += reserved_good.amount
                logging.debug("Total good in station {0}".format(total))
                logging.debug("Needed goods {0}".format(good.amount))
                if good.amount > total:
                    enough_goods = False
                logging.debug("Enough goods {0}".format(enough_goods))
        return enough_goods

    def reserve_goods(self, good_amounts):
        """
        reserve goods
        :param good_amounts:
        :return:
        """
        logging.debug("---Reserve Goods")
        for good_name, needed_good_amount in good_amounts.items():
            good_name = str(good_name)
            logging.debug("Good name: {0}".format(good_name))
            logging.debug("Needed amount: {0}".format(needed_good_amount))
            if good_name in self.station.station_goods.keys():
                logging.debug("Good in station: {0}".format(good_name))
                station_goods = self.station.station_goods[good_name]
                if good_name in self.reserved_goods.keys():
                    logging.debug("Good reserved: {0}".format(good_name))
                    for reserved_good in self.reserved_goods[good_name]:
                        needed_good_amount = needed_good_amount - reserved_good.amount
                logging.debug("needed amount {0}: {1}".format(good_name, needed_good_amount))
                if needed_good_amount == 0:
                    continue
                for station_good in station_goods:
                    if needed_good_amount == 0:
                        break
                    transfered_good_amount = 0
                    if station_good.amount > needed_good_amount:
                        station_good.amount = station_good.amount - needed_good_amount
                        needed_good_amount = 0
                        transfered_good_amount = needed_good_amount

                    elif station_good.amount == needed_good_amount:
                        del station_good
                        transfered_good_amount = needed_good_amount
                        needed_good_amount = 0

                    elif station_good.amount < needed_good_amount:
                        del station_good
                        transfered_good_amount = station_good.amount
                        needed_good_amount = needed_good_amount - station_good.amount

                    new_good = Good(good_name, transfered_good_amount)
                    if good_name in self.reserved_goods.keys():
                        self.reserved_goods[good_name].append(new_good)
                    else:
                        self.reserved_goods[good_name] = []
                        self.reserved_goods[good_name].append(new_good)

    def reserve_critical_goods(self, good_amounts):
        self.reserve_goods()
        if self.check_goods():
            return
        else:
            for good_name, needed_good_amount in good_amounts.items():
                if good_name in self.reserved_goods.keys():
                    for reserved_good in self.reserved_goods.values():
                        needed_good_amount = needed_good_amount - reserved_good.amount
                    if needed_good_amount == 0:
                        next()

                for shipping_door in self.station.shipping_doors:
                    if needed_good_amount == 0:
                        break
                    other_reserved_good = shipping_door.reserved_goods[good_name]
                    if other_reserved_good.amount > needed_good_amount:
                        other_reserved_good.amount = other_reserved_good.amount - needed_good_amount
                        needed_good_amount = 0
                        transfered_good_amount = needed_good_amount

                    elif other_reserved_good.amount == needed_good_amount:
                        del other_reserved_good
                        transfered_good_amount = needed_good_amount
                        needed_good_amount = 0

                    elif other_reserved_good.amount < needed_good_amount:
                        del other_reserved_good
                        transfered_good_amount = other_reserved_good.amount
                        needed_good_amount = needed_good_amount - other_reserved_good.amount

                new_good = Good(good_name, transfered_good_amount)
                if good_name in self.reserved_goods.keys():
                    self.reserved_goods[good_name].append(new_good)
                else:
                    self.reserved_goods[good_name] = []
                    self.reserved_goods[good_name].append(new_good)

    def load_goods(self):
        self.loading_truck.going_goods = deepcopy(self.reserved_goods)
        self.reserved_goods = {}
        self.status_number = 0
        self.sequence.pop(0)

    def load(self):
        pass # wait for truck


