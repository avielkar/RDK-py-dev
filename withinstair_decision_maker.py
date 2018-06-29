import numpy


class WithinStairDecisionMaker:
    def __init__(self):
        self.backword_rightword_probability = None  # type: Integer
        self.backword_error_probability = None  # type: Integer
        self.param_attributes = None  # type: Dict[Any, Any]
        self.static_parameters_attributes = None  # type: List[Any]
        self.within_stair_vector = None  # type: list
        self.within_stair_attribute = None  # type: Any
        self.current_trial_attributes = None  # Dict[string, Any]
        pass


class ComplexWithinStairDecisionMaker(WithinStairDecisionMaker):

    def __init__(self):
        self.within_stair_negative_vector_index = 0
        self.within_stair_positive_vector_index = 0
        self.last_trial_direction = None  # type: 'left' , 'right' or 'none'
        self.last_trial_correction_right = None  # type: bool
        self.last_trial_correction_left = None  # type: bool
        pass

    def set_attributes(self,
                       param_attributes,
                       backword_error_probability,
                       backword_rightword_probability):
        self.param_attributes = param_attributes
        self.backword_error_probability = backword_error_probability
        self.backword_rightword_probability = backword_rightword_probability
        self.reset_within_maker()
        pass

    def get_within_stair_vector_values(self):
        return self.within_stair_vector

    def reset_within_maker(self):
        self.within_stair_vector = self.create_within_stair_vector()
        self.within_stair_negative_vector_index = len(self.within_stair_vector) - 1
        self.within_stair_positive_vector_index = len(self.within_stair_vector) - 1
        self.last_trial_correction_right = False
        self.last_trial_correction_left = False
        self.last_trial_direction = 'none'
        pass

    def create_within_stair_vector(self):

        self.within_stair_attribute = self.param_attributes \
            [list(
                filter(lambda x: self.param_attributes[x]['paramtype'] == 'withinstair', self.param_attributes.keys()))[
                0]]
        self.static_parameters_attributes = (
            list(filter(lambda attributes: attributes['paramtype'] == 'static', self.param_attributes.values())))
        within_stair_low_val = self.within_stair_attribute['minvalue']
        within_stair_high_value = self.within_stair_attribute['maxvalue']
        within_stair_jumping = self.within_stair_attribute['jumping']
        within_vector = numpy.arange(float(within_stair_low_val),
                                     float(within_stair_high_value),
                                     float(within_stair_jumping))
        return within_vector

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


class SimpleWithinstairDecisionMaker:
    def __init__(self):
        self.backword_rightword_probability = None  # type: Integer
        self.backword_error_probability = None  # type: Integer
        self.param_attributes = None  # type: Dict[Any, Any]
        self.static_parameters_attributes = None  # type: List[Any]
        self.within_stair_vector = None  # type: list
        self.within_stair_negative_vector_index = 0
        self.within_stair_positive_vector_index = 0
        self.within_stair_attribute = None  # type: Any
        self.last_trial_direction = None  # type: 'left' , 'right' or 'none'
        self.last_trial_correction_right = None  # type: bool
        self.last_trial_correction_left = None  # type: bool
        self.current_trial_attributes = None  # Dict[string, Any]
        pass
