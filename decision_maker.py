from abc import abstractmethod

import numpy
from experimentdata import ExperimentData


class DecisionMaker:

    def __init__(self):
        self.experiment_data = None  # type: ExperimentData
        self.param_attributes = None  # type: Dict[Any, Any]
        self.static_parameters_attributes = None  # type: List[Any]
        pass

    def set_attributes(self,
                       param_attributes,
                       experiment_data):
        self.param_attributes = param_attributes
        self.experiment_data = experiment_data
        self.reset_maker()
        pass

    @abstractmethod
    def get_vector_values(self):
        return self.within_stair_vector

    def reset_within_maker(self):
        pass

    @abstractmethod
    def current_trial(self):
        pass

    @abstractmethod
    def reset_maker(self):
        pass

    @abstractmethod
    def set_current_correctness(self, trial_correctness):
        pass

    @abstractmethod
    def current_trial(self):
        pass
