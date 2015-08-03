__author__ = 'robotes'

class ReceivingDoor(object):
    """
    Receiving doors of the station
    """
    def __init__(self,station, name):
        self.door_name = name
        self.type = 'Receiving'
        self.door_number = 0
        self.truck = 0
        self.truck_sequence = 0
        self.status = ['empty', 'deploying']
        self.status_number = 0
        self.good_list = []
        self.sequence = []
        self.station = station
        self.waiting_trucks = 0
        self.deploying_truck = None

    def set_truck_doors(self):
        for truck in self.sequence:
            truck.receiving_door = self
            truck.receiving_door_name = self.door_name

    def current_action(self):
        # self.print_state()
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.deploying()

    def next_state(self):
        self.status_number += 1

    def wait(self):
        pass

    def no_truck(self):
        if len(self.sequence) != 0:
            next_truck = self.sequence[0]
            self.deploying_truck = next_truck
            if next_truck.state_list[next_truck.current_state] == 'waiting':
                self.sequence[0].next_state()
                self.next_state()

    def deploy_goods(self, goods):
        self.station.add_goods(goods)
        self.status_number = 0
        self.sequence.pop(0)

    def deploying(self):
        #self.print_state()
        pass # wait for truck

    def print_state(self):
        print('door number: ', self.door_number, 'state: ', self.status[self.status_number])
