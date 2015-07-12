__author__ = 'robotes'


from random import uniform

class Truck(object):
    """
    Base class for trucks. Inbound, outbound and compound trucks will be generated from this base class
    """
    number_of_trucks = 0
    number_of_inbound_trucks = 0
    number_of_outbound_trucks = 0
    number_of_compound_trucks = 0

    def __init__(self, name, type):
        """
        Initialize variables for all trucks types.
        :return:
        """
        self.truck_type = type
        self.truck_number = Truck.number_of_trucks
        self.truck_name = name
        Truck.number_of_trucks += Truck.number_of_trucks
        self.current_state = 0
        self.state_change_times = [5,10,30]
        self.loading_time = 0

    def next_state(self):
        self.current_state = self.current_state + 1


class InboundTruck(Truck):
    """
    inbound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'start_deploy', 'deploying', 'done')

        Truck.number_of_inbound_trucks += 1
        self.coming_goods = []
        self.inbound_gdj = 0
        self.door_number = 0
        self.current_time = 0
        self.finish_time = 0
        self.receive_door = 0
        self.receive_door_name = ''
        
    def current_action(self, current_time):

        self.current_time = current_time
        #self.print_state()
        if self.current_state == 0:
            self.coming()
        if self.current_state == 1:
            self.waiting()
        if self.current_state == 2:
            self.start_deploy()
        if self.current_state == 3:
            self.deploy_goods()
        if self.current_state == 4:
            self.leaving()
        
    def calculate_gdj(self, two_gdj, loading_time, changeover_time, alpha, gamma, tightness, arrival, outbound_mu):
        self.inbound_gdj = int(uniform(arrival[0], two_gdj))
        self.finish_time = self.inbound_gdj

    def start_deploy(self):
        total = 0
        for good in self.coming_goods:
            total += good.amount
        self.finish_time = int(self.current_time + total * self.loading_time)
        self.next_state()

    def deploy_goods(self):
        if self.current_time == self.finish_time:
            self.receiving_door.deploy_goods(self.coming_goods)
            self.next_state()

    def coming(self):
        if self.current_time == self.inbound_gdj:
            self.next_state()

    def leaving(self):
        pass
        
    def waiting(self):
        pass

    def print_state(self):
        print('truck name: ', self.truck_name, ' current_state: ' , self.state_list[self.current_state])

class OutboundTruck(Truck):
    """
    outbound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'start_loading', 'loading', 'going')
        Truck.number_of_outbound_trucks += 1
        self.going_goods = []
        self.finish_time = 0
        self.outbound_gdj = 0
        self.shipping_door = 0
        self.shipping_door_name = None

    def calculate_gdj(self, two_gdj, loading_time, changeover_time, alpha, gamma, tightness, arrival, outbound_mu):
        
        self.outbound_gdj = uniform(arrival[1], arrival[1] + two_gdj)
        self.A = self.outbound_gdj + (outbound_mu - 1) * loading_time + outbound_mu * changeover_time
        self.bounds = [self.A * alpha, self.A*(alpha + gamma)]
        self.finish_time = self.outbound_gdj

    def current_action(self, current_time):
        self.current_time = current_time
        if self.current_state == 0:
            self.coming()
        if self.current_state == 1:
            self.waiting()
        if self.current_state == 2:
            self.start_loading()
        if self.current_state == 3:
            self.loading_goods()
        if self.current_state == 4:
            self.leaving()

    def start_loading(self):
        total = 0
        for good in self.going_goods:
            total += good.amount
        self.finish_time = int(self.current_time + total * self.loading_time)
        self.next_state()

    def loading_goods(self):
        if self.current_time == self.finish_time:
            self.shipping_door.load_goods(self.going_goods)
            self.next_state()

    def coming(self):
        if self.current_time == int(self.outbound_gdj):
            self.next_state()

    def waiting(self):
        pass

    def leaving(self):
        pass


class CompoundTruck(Truck):
    """
    compound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'start_deploy', 'deploying', 'transfering', 'waiting', 'start_loading', 'loading', 'going')
        Truck.number_of_compound_trucks = Truck.number_of_compound_trucks + 1
        self.coming_goods = []
        self.going_goods = []
        
        self.inbound_gdj = 0                
        self.outbound_gdj = 0
        self.finish_time = 0
        self.receiviving_door = 0
        self.shipping_door = 0
        self.receiviving_door_name = None
        self.shipping_door_name = None

        self.changeover_time = 0

    def calculate_gdj(self, two_gdj, loading_time,  changeover_time, alpha, gamma, tightness, arrival, outbound_mu):
        self.outbound_gdj = uniform(arrival[1], arrival[1] + two_gdj)
        self.inbound_gdj = int(uniform(arrival[0], two_gdj))
        self.A = self.outbound_gdj + (outbound_mu - 1) * loading_time + outbound_mu * changeover_time
        self.bounds = [self.A * alpha, self.A*(alpha + gamma)]
        self.finish_time = self.inbound_gdj

    def current_action(self, current_time):
        #print('truck name: ', self.truck_name, ' current_state: ' , self.state_list[self.current_state])

        self.current_time = current_time
        print('state', self.current_state)
        if self.current_state == 0:
            self.coming()
        if self.current_state == 1:
            self.waiting_deploying()
        if self.current_state == 2:
            self.start_deploy()
        if self.current_state == 3:
            self.deploy_goods()
        if self.current_state == 4:
            self.transfering()
        if self.current_state == 5:
            self.waiting_loading()
        if self.current_state == 6:
            self.start_loading()
        if self.current_state == 7:
            self.loading_goods()
        if self.current_state == 8:
            self.leaving()

    def start_loading(self):
        total = 0
        for good in self.going_goods:
            total += good.amount
        self.finish_time = int(self.current_time + total * self.loading_time)
        self.next_state()

    def loading_goods(self):
        print('loading')
        print('time', self.finish_time)
        if self.current_time == self.finish_time:
            self.shipping_door.load_goods(self.going_goods)
            self.next_state()

    def start_deploy(self):
        total = 0
        for good in self.coming_goods:
            total += good.amount
        self.finish_time = int(self.current_time + total * self.loading_time)
        self.next_state()

    def deploy_goods(self):
        if self.current_time == self.finish_time:
            self.receiving_door.deploy_goods(self.coming_goods)
            self.next_state()
            self.finish_time = self.current_time + self.changeover_time

    def waiting_deploying(self):
        pass

    def coming(self):
        if self.current_time == self.inbound_gdj:
            self.next_state()

    def waiting_loading(self):
        pass

    def transfering(self):
        if self.current_time == self.finish_time:
            self.next_state()

    def leaving(self):
        pass