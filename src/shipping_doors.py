__author__ = 'robotes'

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

    def set_truck_doors(self):
        for truck in self.sequence:
            truck.shipping_door = self
            truck.shipping_door_name = self.door_name

    def current_action(self):
        # self.print_state()
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.load()

    def next_state(self):
        self.status_number += 1

    def no_truck(self):
        # self.print_state()
        if len(self.sequence) != 0:
            next_truck = self.sequence[0]
            self.loading_truck = next_truck
            if next_truck.state_list[next_truck.current_state] == 'waiting':
                if self.check_goods():
                    self.sequence[0].next_state()
                    self.next_state()

    def check_goods(self):
        enough_goods = False
        for good in self.loading_truck.going_goods:
            total = 0
            if good.type in self.station.station_goods:
                enough_goods = True
                for station_good in self.station.station_goods[good.type]:
                    total += station_good.amount
                if good.amount > total:
                    enough_goods = False
        return enough_goods

    def load_goods(self, goods):
        self.station.remove_goods(goods)
        self.status_number = 0
        self.sequence.pop(0)

    def load(self):
        pass # wait for truck

    def print_state(self):
        print('shippin door number: ', self.door_name, 'state: ', self.status[self.status_number])

