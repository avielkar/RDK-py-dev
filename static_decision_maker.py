import numpy
from decision_maker import DecisionMaker


class StaticDecisionMaker(DecisionMaker):

    def __init__(self):
        pass

    def set_attributes(self,
                       param_attributes,
                       experiment_data):
        self.param_attributes = param_attributes
        self.experiment_data = experiment_data
        self.reset_maker()
        pass

    def get_vector_values(self):
        return self.param_attributes['Coherence']['value']

    def reset_maker(self):
        pass

    def set_current_correctness(self, trial_correctness):
        pass

    def current_trial(self):
        pass
