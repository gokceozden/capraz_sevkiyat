class DataSet(object):

    def __init__(self, alpha, gamma, tightnessFactor):
        self.alpha = alpha
        self.gamma = gamma
        self.tightnessFactor = tightnessFactor

        self.outbound_twoGD = 0
        self.inbound_twoGD = 0
        