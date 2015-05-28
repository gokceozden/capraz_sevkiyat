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
        Truck.number_of_trucks = Truck.number_of_trucks +1
        self.current_state = 0
        self.state_change_times = [5,10,30]
        
    def next_state(self):
        self.current_state = self.current_state + 1
    

class InboundTruck(Truck):
    """
    inbound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'dumping', 'done')

        Truck.number_of_inbound_trucks = Truck.number_of_inbound_trucks + 1
        self.coming_goods = []

        self.inbound_gdj = 0
        self.door_number = 0
        self.item_loading_counter = 0
        
    def current_action(self):
        if (self.current_state == 0):
            self.coming()
        if (self.current_state == 1):
            self.waiting()
        if (self.current_state == 2):
            self.deploy_goods()
        if (self.current_state == 3):
            self.leaving()
        
    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        self.inbound_gdj = uniform(arrival[0], two_gdj)
        print('inbound ', self.inbound_gdj)

    def deploy_goods(self, loading_time, time_step):
        print("deploying")

    def coming(self):
        print('waiting')

    def leaving(self):
        print("leaving")
        
    def waiting(self):
        print("waiting")
        


class OutboundTruck(Truck):
    """
    outbound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'filling', 'going')
        Truck.number_of_outbound_trucks = Truck.number_of_outbound_trucks + 1
        self.going_goods = []

        self.outbound_gdj = 0
        
    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        self.outbound_gdj = uniform(arrival[1], arrival[1] + two_gdj)
        print('outbound ', self.outbound_gdj)

    def current_action(self):
        if (self.current_state == 0):
            self.coming()
        if (self.current_state == 1):
            self.waiting()
        if (self.current_state == 2):
            self.loading_goods()
        if (self.current_state == 3):
            self.leaving()

        
    def loading_goods(self):
        pass

    def coming(self):
        pass

    def waiting(self):
        pass

    def leaving(self):
        pass


class CompoundTruck(Truck):
    """
    comound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'dumping', 'transfering', 'waiting', 'fillinf', 'done')
        Truck.number_of_compound_trucks = Truck.number_of_compound_trucks + 1
        self.coming_goods = []
        self.going_goods = []
        
        self.inbound_gdj = 0                
        self.outbound_gdj = 0

    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        print('arrival', two_gdj )
        self.outbound_gdj = uniform(arrival[1], arrival[1] + two_gdj)
        self.inbound_gdj = uniform(arrival[0], two_gdj)
        
        print('cinbound ', self.inbound_gdj)
        print('coutbound ', self.outbound_gdj)


    def current_action(self):
        if (self.current_state == 0):
            self.coming()
        if (self.current_state == 1):
            self.waiting_deploying()
        if (self.current_state == 2):
            self.deploy_goods()
        if (self.current_state == 3):
            self.transfering()
        if (self.current_state == 4):
            self.waiting_loading()
        if (self.current_state == 5):
            self.loading_goods()
        if (self.current_state == 6):
            self.leaving()

    def deploy_goods(self):
        pass

    def waiting_deploying(self):
        pass

    def loading_goods(self):
        pass

    def coming(self):
        pass

    def waiting_loading(self):
        pass

    def transfering(self):
        pass

    def leaving(self):
        pass