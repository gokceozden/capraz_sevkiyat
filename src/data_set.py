class DataSet(object):
    inbound_mu = 0
    outbound_mu = 0
    product_per_inbound_truck = 0
    product_per_outbound_truck = 0

    
    def __init__(self, alpha, gamma, tightness_factor):
        self.alpha = alpha
        self.gamma = gamma
        self.tightnessFactor = tightness_factor
        self.makespan_factor = 0.1

        self.outbound_twoGD = 0
        self.inbound_twoGD = 0
        self.calculate_twoDG()
        

    def calculate_twoDG(self):

        self.outbound_twoGD = (2 * DataSet.outbound_mu * self.tightnessFactor * DataSet.product_per_outbound_truck)\
        / (2 - self.tightnessFactor * DataSet.outbound_mu * self.makespan_factor)

        self.inbound_twoGD = (2 * DataSet.inbound_mu * self.tightnessFactor * DataSet.product_per_inbound_truck)\
        / (2 - self.tightnessFactor * DataSet.inbound_mu * self.makespan_factor)