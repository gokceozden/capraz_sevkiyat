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
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.deploy_goods()
        if self.status_number == 2:
            self.wait()


    def wait(self):
        print("waiting")

    def no_truck(self):
        print("empty")

    def deploy_goods(self):
        print("doploying")

