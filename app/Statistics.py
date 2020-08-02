from Calculator import Calculator
from Mean import mean




class Statistics(Calculator):

    data = []

    def __init__(self):
        super().__init__()

    def get_mean(self, data):
        self.result = mean(data)
        return self.result




        self.result = sample_CI_width(confidence, width)
        return self.result