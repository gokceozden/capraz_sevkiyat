__author__ = 'mustafa'

from data_set import DataSet

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
        self.transfer_time = 0
        self.good_transfer_time = 0
        self.inbound_arrival_time = 0
        self.outbound_arrival_time = 0
        self.number_of_gammas = 0
        self.gamma_values = [0]
        self.number_of_alphas = 0
        self.alpha_values = [0]
        self.number_of_tghtness_factors = 0
        self.tightness_factors = [0]

        # dataset
        self.outbound_twoGD = 0
        self.inbound_twoGD = 0
        self.alpha = 0
        self.gamma  = 0
        self.tightness_factor = 0

        self.data_set_list = []

        # sequence
        self.sequence_receiving_doors = []
        self.sequence_shipping_doors = []
        self.sequence = [self.sequence_receiving_doors, self.sequence_shipping_doors]
        self.data_set_number = 0

        # gdj values
        self.inbound_twogdj = 0
        self.outbound_twogdj = 0

    def calculate_truck_data(self):
        """
        create lists and names
        :return:
        """
        pass

    def create_data_set(self):
        """
        creates data set for alpha gamma and tightness factor values
        :return:
        """
        for alpha in self.alpha_values:
            for gamma in self.gamma_values:
                for tightness in self.tightness_factors:
                    self.data_set_list.append((alpha, gamma, tightness))

    def setup_data_set(self, data_set_number):
        """
        sets the current data set to the given number
        :param data_set_number:
        :return:
        """
        self.data_set_number = data_set_number
        self.alpha, self.gamma, self.tightness_factor = self.data_set_list[data_set_number]
