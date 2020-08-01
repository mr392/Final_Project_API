from Calc.Calculator import Calculator
from Stats.Mean import mean
from Stats.Median import median
from Stats.Mode import mode
from Stats.Variance import variance
from Stats.Standard_Deviation import standard_deviation
from Stats.ZScore import zscore
from Stats.simple_sample import get_sample
from Stats.ConfidenceInterval import confidence_interval
from Stats.margin_of_error import margin_of_error
from Stats.Cohrans import sample
from Stats.sample_CI_width import sample_CI_width

from Stats.int_float_checker import check_for_number_parameters



class Statistics(Calculator):

    data = []

    def __init__(self):
        super().__init__()

    def get_mean(self, data):
        self.result = mean(data)
        return self.result

    def get_median(self, data):
        self.result = median(data)
        return self.result

    def get_mode(self, data):
        self.result = mode(data)
        return self.result

    def get_variance(self, data):
        self.result = variance(data)
        return self.result

    def get_standard_deviation(self, data):
        self.result = standard_deviation(data)
        return self.result

    def get_zscore(self, data):
        self.result = zscore(data)
        return self.result

    def get_simple_sample(self, data):
        sample_size = 6
        self.result = get_sample(data, sample_size)
        return self.result

    def get_confidence_interval (self, data):

        self.result = confidence_interval(data)
        return self.result

    def get_margin_of_error(self, crit_val, standard_error):
        self.result = margin_of_error(crit_val, standard_error)
        return self.result

    def get_cochrans_sample(self, n1, cl1, e1, p1):

        self.result = sample(n1, cl1, e1, p1)
        return self.result

    def get_sample_ci_width(self, confidence, width):

        check_for_number_parameters(confidence, width)


        self.result = sample_CI_width(confidence, width)
        return self.result