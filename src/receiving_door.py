__author__ = 'robotes'

class ReceivingDoor(object):
    """
    Receiving doors of the station
    """
    def __init__(self):
        self.door_number = 0
        self.truck_sequuence = 0
        self.status = ['empty', 'deploying', 'waiting']
        self.status_number = 0
        self.good_list = []
        self.sequence = []

    def current_action(self):
        print('door number: ', self.door_number, 'state: ', self.status[self.status_number])
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.deploy_goods()
        if self.status_number == 2:
            self.wait()

    def next_state(self):
        self.status_number = self.status_number + 1


    def wait(self):
        pass

    def no_truck(self):
        next_truck = self.sequence[0]
        if (next_truck.state_list[next_truck.current_state] == 'waiting'):
            print('door number:' , self.door_number, '  deploying')
            self.sequence[0].next_state()
            self.next_state()

    def deploy_goods(self):
        pass
