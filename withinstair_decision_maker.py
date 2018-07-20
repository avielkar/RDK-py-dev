import numpy
from experimentdata import ExperimentData
from decision_maker import DecisionMaker


class WithinStairDecisionMaker(DecisionMaker):

    def __init__(self):
        self.within_stair_vector = None  # type: list
        self.within_stair_attribute = None  # type: Any
        pass

    def set_attributes(self,
                       param_attributes,
                       experiment_data):
        self.param_attributes = param_attributes
        self.experiment_data = experiment_data
        self.reset_maker()
        pass

    def get_vector_values(self):
        return self.within_stair_vector

    def reset_maker(self):
        pass

    def create_within_stair_vector(self):
        self.within_stair_attribute = self.param_attributes \
            [list(
                filter(lambda x: self.param_attributes[x]['paramtype'] == 'withinstair', self.param_attributes.keys()))[
                0]]
        self.static_parameters_attributes = (
            list(filter(lambda attributes: attributes['paramtype'] == 'static' or attributes['paramtype'] == 'const', self.param_attributes.values())))
        within_stair_low_val = self.within_stair_attribute['minvalue']
        within_stair_high_value = self.within_stair_attribute['maxvalue']
        within_stair_jumping = self.within_stair_attribute['jumping']
        within_vector = numpy.arange(float(within_stair_low_val),
                                     float(within_stair_high_value),
                                     float(within_stair_jumping))
        return within_vector

    def current_trial(self):
        pass


class ComplexWithinStairDecisionMaker(WithinStairDecisionMaker):

    def __init__(self):
        self.within_stair_negative_vector_index = 0
        self.within_stair_positive_vector_index = 0
        self.last_trial_direction = None  # type: 'left' , 'right' or 'none'
        self.last_trial_correction_right = None  # type: bool
        self.last_trial_correction_left = None  # type: bool
        pass

    def reset_maker(self):
        self.within_stair_vector = self.create_within_stair_vector()
        self.within_stair_negative_vector_index = len(self.within_stair_vector) - 1
        self.within_stair_positive_vector_index = len(self.within_stair_vector) - 1
        self.last_trial_correction_right = False
        self.last_trial_correction_left = False
        self.last_trial_direction = 'none'
        pass

    def set_current_correctness(self, trial_correctness):
        if 0 < self.current_trial_attributes['Direction'] < 180:
            self.last_trial_correction_right = trial_correctness
        else:
            self.last_trial_correction_left = trial_correctness

    def current_trial(self):
        right_trial = True if numpy.random.random_integers(low=0, high=1) == 0 else False

        if right_trial:
            if not self.last_trial_correction_right:
                self.within_stair_positive_vector_index = self.within_stair_positive_vector_index + 1 \
                    if self.within_stair_positive_vector_index < len(self.within_stair_vector) - 1 \
                    else self.within_stair_positive_vector_index
            else:
                self.within_stair_positive_vector_index = self.within_stair_positive_vector_index \
                    if self.within_stair_positive_vector_index == 0 \
                    else self.within_stair_positive_vector_index - 1

            current_withinstair_value = self.within_stair_vector[self.within_stair_positive_vector_index]
        else:
            if not self.last_trial_correction_left:
                self.within_stair_negative_vector_index = self.within_stair_negative_vector_index + 1 \
                    if self.within_stair_negative_vector_index < len(self.within_stair_vector) - 1 \
                    else self.within_stair_negative_vector_index
            else:
                self.within_stair_negative_vector_index = self.within_stair_negative_vector_index \
                    if self.within_stair_negative_vector_index == 0 \
                    else self.within_stair_negative_vector_index - 1
            current_withinstair_value = self.within_stair_vector[self.within_stair_negative_vector_index]

        current_trial_data = dict()
        for param_attributes in self.static_parameters_attributes:
            current_trial_data[param_attributes['param_name']] = param_attributes['value']
        current_trial_data[self.within_stair_attribute['param_name']] = current_withinstair_value
        current_trial_data['Direction'] = current_trial_data['Direction'] if right_trial \
            else -current_trial_data['Direction']
        self.current_trial_attributes = current_trial_data

        return current_trial_data


class SimpleWithinStairDecisionMaker(WithinStairDecisionMaker):
    def __init__(self):
        self.within_stair_vector_index = 0
        self.last_trial_correction = None  # type: bool
        pass

    def reset_maker(self):
        self.within_stair_vector = self.create_within_stair_vector()
        self.within_stair_vector_index = len(self.within_stair_vector) - 1
        self.last_trial_correction = False
        pass

    def set_current_correctness(self, trial_correctness):
        self.last_trial_correction = trial_correctness

    def current_trial(self):
        right_trial = True if numpy.random.random_integers(low=0, high=1) == 0 else False

        if not self.last_trial_correction:
            if numpy.random.binomial(size=1, n=1, p=self.experiment_data.backward_error_probability)[0] == 1:
                self.within_stair_vector_index = self.within_stair_vector_index + 1 \
                    if self.within_stair_vector_index < len(self.within_stair_vector) - 1 \
                    else self.within_stair_vector_index
        else:
            if numpy.random.binomial(size=1, n=1, p=self.experiment_data.forward_rightward_probability)[0] == 1:
                self.within_stair_vector_index = self.within_stair_vector_index \
                    if self.within_stair_vector_index == 0 \
                    else self.within_stair_vector_index - 1

        current_withinstair_value = self.within_stair_vector[self.within_stair_vector_index]

        current_trial_data = dict()
        for param_attributes in self.static_parameters_attributes:
            current_trial_data[param_attributes['param_name']] = param_attributes['value']
        current_trial_data[self.within_stair_attribute['param_name']] = current_withinstair_value
        current_trial_data['Direction'] = current_trial_data['Direction'] if right_trial \
            else - float(current_trial_data['Direction'])
        self.current_trial_attributes = current_trial_data

        return current_trial_data
