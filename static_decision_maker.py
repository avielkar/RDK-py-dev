import numpy
from decision_maker import DecisionMaker


class StaticDecisionMaker(DecisionMaker):

    def __init__(self):
        self.experiment_data = None  # type: ExperimentData
        self.param_attributes = None  # type: Dict[Any, Any]
        self.static_parameters_attributes = None  # type: List[Any]
        self.within_stair_vector = None  # type: list
        self.within_stair_attribute = None  # type: Any
        pass

    def set_attributes(self,
                       param_attributes,
                       experiment_data):
        self.param_attributes = param_attributes
        self.experiment_data = experiment_data
        self.reset_within_maker()
        pass

    def get_within_stair_vector_values(self):
        return self.within_stair_vector

    def reset_within_maker(self):
        pass

    def create_within_stair_vector(self):
        self.within_stair_attribute = self.param_attributes \
            [list(
                filter(lambda x: self.param_attributes[x]['paramtype'] == 'withinstair', self.param_attributes.keys()))[
                0]]
        self.static_parameters_attributes = (
            list(filter(lambda attributes: attributes['paramtype'] == 'static' or attributes['paramtype'] == 'const',
                        self.param_attributes.values())))
        within_stair_low_val = self.within_stair_attribute['minvalue']
        within_stair_high_value = self.within_stair_attribute['maxvalue']
        within_stair_jumping = self.within_stair_attribute['jumping']
        within_vector = numpy.arange(float(within_stair_low_val),
                                     float(within_stair_high_value),
                                     float(within_stair_jumping))
        return within_vector

    def set_current_correctness(self, trial_correctness):
        pass

    def current_trial(self):
        pass
