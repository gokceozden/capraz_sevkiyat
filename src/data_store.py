__author__ = 'mustafa'

class DataStore(object):
    """
    Stores all the data from the user
    """
    def __init__(self):
        """
        init all the variables from the user
        :return:
        """
        # truck related data
        self.number_of_inbound_trucks = 0
        self.number_of_outbound_trucks = 0
        self.number_of_compound_trucks = 0
        self.number_of_receiving_doors = 0
        self.number_of_shipping_doors = 0
        self.number_of_goods = 0
        self.inbound_goods = []
        self.outbound_goods = []
        self.compound_coming_goods = []
        self.compound_going_goods = []
        self.compound_goods = [self.compound_coming_goods, self.compound_going_goods]
        self.goods = [self.inbound_goods, self.outbound_goods, self.compound_goods]

        # data set
        self.loading_time = 0
        self.changeover_time = 0
        self.makespan_factor = 0
        self.inbound_arrival_time = 0
        self.outbound_arrival_time = 0
        self.number_of_gammas = 0
        self.gamma_values = [0]
        self.number_of_alphas = 0
        self.alpha_values = [0]
        self.number_of_tghtness_factors = 0
        self.tightness_factors = [0]

        # sequence
        self.sequence_receiving_doors = []
        self.sequence_shipping_doors = []
        self.sequence = [self.sequence_receiving_doors, self.sequence_shipping_doors]

    def calculate_truck_data(self):
        """
        create lists and names
        :return:
        """

    def create_data_set(self):
        """
        creates data set for alpha gamma and tightness factor values
        :return:
        """
        pass