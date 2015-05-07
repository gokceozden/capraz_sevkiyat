__author__ = 'robotes'


class Truck(object):
    """
    Base class for trucks. Inbound, outbound and compound trucks will be generated from this base class
    """
    number_of_trucks = 0
    number_of_inbound_trucks = 0
    number_of_outbound_trucks = 0
    number_of_compound_trucks = 0

    def __init__(self, name):
        """
        Initialize variables for all trucks types.
        :return:
        """
        self.truck_number = number_of_trucks
        self.truck_name = name
        Truck.number_of_trucks = Truck.number_of_trucks +1




class InboundTruck(Truck):
    """
    inbound truck class
    """
    def __init__(self, name):
        super.__init__(self, name)
        self.state_list = {}
        Truck.number_of_inbound_trucks = Truck.number_of_inbound_trucks + 1


class OutboundTruck(Truck):
    """
    outbound truck class
    """
    def __init__(self, name):
        super.__init__(self)
        self.state_list = {}
        Truck.number_of_outbound_trucks = Truck.number_of_outbound_trucks + 1


class CompoundTruck(Truck):
    """
    comound truck class
    """
    def __init__(self, name):
        super.__init__(self)
        self.state_list = {}
        Truck.number_of_compound_trucks = Truck.number_of_compound_trucks + 1