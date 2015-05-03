__author__ = 'robotes'


class Truck(object):
    """
    Base class for trucks. Inbound, outbound and compound trucks will be generated from this base class
    """


    def __init__(self):
        """
        Initialize variables for all trucks types.
        :return:
        """



class InboundTruck(Truck):
    """
    inbound truck class
    """
    def __init__(self):
        self.state_list = {}



class OutboundTruck(Truck):
    """
    outbound truck class
    """
    def __init__(self):
        self.state_list = {}



class CompoundTruck(Truck):
    """
    comound truck class
    """
    def __init__(self):
        self.state_list = {}
