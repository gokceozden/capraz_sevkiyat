__author__ = 'robotes'

from random import uniform


class Truck(object):
    """
    Base class for trucks. Inbound, outbound and compound trucks will be generated from this base class
    """
    def __init__(self, truck_data):
        """
        Initialize variables for all trucks types.
        :return:
        """
        self.loading_time = truck_data['loading_time']
        self.changeover_time = truck_data['changeover_time']
        self.alpha = truck_data['alpha']
        self.gamma = truck_data['gamma']
        self.tightness_factor = truck_data['tightness_factor']
        self.truck_number = truck_data['number']
        self.truck_name = truck_data['name']
        self.makespan_factor = truck_data['makespan_factor']

        self.two_gdj = 0

        self.mu = 0
        self.current_state = 0
        self.current_time = 0
        self.finish_time = 0
        self.next_action_time = 0
        self.product_per_truck = 0

    def calculate_twogd(self):
        """
        calculates upper limit for coming times
        :return:
        """
        self.two_gdj = (2 * self.mu * self.tightness_factor * self.product_per_truck) / (2 - self.tightness_factor * self.mu * self.makespan_factor)

    def next_state(self):
        self.current_state += 1


class InboundTruck(Truck):
    """
    inbound truck class
    """
    def __init__(self, truck_data, inbound_data):
        Truck.__init__(self, truck_data)
        self.truck_type = 0
        self.state_list = ('coming', 'waiting', 'start_deploy', 'deploying', 'done')

        self.arrival_time = inbound_data['arrival_time']
        self.arrival_time = inbound_data['arrival_time']
        self.mu = inbound_data['mu']
        self.product_per_truck = inbound_data['product_per_truck']

        self.inbound_gdj = 0
        self.door_number = 0
        self.receive_door = 0
        self.coming_goods = []

    def calculate_gdj(self):
        self.calculate_twogd()
        self.inbound_gdj = int(uniform(self.arrival_time, self.two_gdj))
        self.finish_time = self.inbound_gdj

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
    def __init__(self, truck_data, outbound_data):
        Truck.__init__(self, truck_data)
        self.truck_type = 1
        self.state_list = ('coming', 'waiting', 'start_loading', 'loading', 'going')
        self.going_goods = []
        self.finish_time = 0
        self.outbound_gdj = 0
        self.shipping_door = 0
        self.shipping_door_name = None
        self.arrival_time = outbound_data['arrival_time']
        self.mu = outbound_data['mu']
        self.product_per_truck = outbound_data['product_per_truck']

    def calculate_gdj(self):
        self.calculate_twogd()
        self.outbound_gdj = uniform(self.arrival_time, self.two_gdj)
        # hatali formul
        self.A = self.outbound_gdj + (self.mu - 1) * self.changeover_time + self.mu * self.product_per_truck * self.loading_time
        self.bounds = [self.A * self.alpha, self.A * self.gamma]
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
    def __init__(self, truck_data, compound_data):
        Truck.__init__(self, truck_data)
        self.truck_type = 2
        self.state_list = ('coming', 'waiting', 'start_deploy', 'deploying', 'transfering', 'waiting', 'start_loading', 'loading', 'going')
        self.coming_goods = []
        self.going_goods = []
        
        self.inbound_gdj = 0                
        self.outbound_gdj = 0
        self.finish_time = 0
        self.receiving_door = 0
        self.shipping_door = 0
        self.receiving_door_name = None
        self.shipping_door_name = None

        # compound truck data
        self.arrival_time = compound_data['arrival_time']
        self.mu = compound_data['mu']
        self.transfer_time = compound_data['transfer_time']
        self.inbound_product_per_truck = compound_data['inbound_product_per_truck']
        self.outbound_product_per_truck = compound_data['outbound_product_per_truck']

    def calculate_twogd(self):
        """
        calculates upper limit for coming times
        :return:
        """
        self.two_gdj = (2 * self.mu * self.tightness_factor * self.inbound_product_per_truck) / (2 - self.tightness_factor * self.mu * self.makespan_factor)

    def calculate_gdj(self):
        self.calculate_twogd()
        self.inbound_gdj = int(uniform(self.arrival_time, self.two_gdj))
        A = self.inbound_gdj + (self.mu - 1) * self.changeover_time + self.mu * self.inbound_product_per_truck * self.loading_time + self.transfer_time +(self.mu - 1) * self.changeover_time + self.mu * self.outbound_product_per_truck * self.loading_time
        self.bounds = [A * self.alpha, A*(self.alpha + self.gamma)]
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
            self.finish_time = self.current_time + self.transfer_time

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