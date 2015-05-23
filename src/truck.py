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
        self.coming_goods = {}

        self.inbound_gdj = 0

    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        self.inbound_gdj = uniform(arrival[0], two_gdj)
        print('inbound ', self.inbound_gdj)

class OutboundTruck(Truck):
    """
    outbound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'filling', 'going')
        Truck.number_of_outbound_trucks = Truck.number_of_outbound_trucks + 1
        self.going_goods = {}

        self.outbound_gdj = 0
        
    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        self.outbound_gdj = uniform(arrival[1], two_gdj)
        print('outbound ', self.outbound_gdj)


class CompoundTruck(Truck):
    """
    comound truck class
    """
    def __init__(self, name, type):
        Truck.__init__(self, name, type)
        self.state_list = ('coming', 'waiting', 'dumping', 'transfering', 'waiting', 'fillinf', 'done')
        Truck.number_of_compound_trucks = Truck.number_of_compound_trucks + 1
        self.coming_goods = {}
        self.going_goods = {}
        
        self.inbound_gdj = 0                
        self.outbound_gdj = 0

    def calculate_gdj(self, two_gdj, loading_time, alpha, gamma, tightness, arrival):
        
        print('arrival', two_gdj )
        self.outbound_gdj = uniform(arrival[1], two_gdj)
        self.inbound_gdj = uniform(arrival[0], two_gdj)
        
        print('cinbound ', self.inbound_gdj)
        print('coutbound ', self.outbound_gdj)