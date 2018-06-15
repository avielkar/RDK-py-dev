import random
import numpy


class WithinStairDecisionMaker:
    def __init__(self):
        self.backword_rightword_probability = None  # type: Integer
        self.backword_error_probability = None  # type: Integer
        self.param_attributes = None  # type: Anys
        self.within_stair_vector_positive = None  # type: list
        self.within_stair_vector_negative = None  # type: list
        self.within_stair_negative_vector_index = 0
        self.within_stair_positive_vector_index = 0
        pass

    def set_attributes(self,
                       param_attributes,
                       backword_error_probability,
                       backword_rightword_probability):
        self.param_attributes = param_attributes
        self.backword_error_probability = backword_error_probability
        self.backword_rightword_probability = backword_rightword_probability
        self.reset_within_maker()
        self.create_within_stair_vector()
        pass

    def reset_within_maker(self):
        within_stair_vector = self.create_within_stair_vector()
        self.within_stair_vector_positive = [value for value in within_stair_vector if value > 0]
        self.within_stair_vector_negative = [value for value in within_stair_vector if value < 0]
        self.within_stair_negative_vector_index = 0
        self.within_stair_positive_vector_index = 0
        pass

    def create_within_stair_vector(self):
        within_stair_low_val = self.param_attributes['min_value']
        within_stair_high_value = self.param_attributes['max_value']
        within_stair_jumping = self.param_attributes['jumping']
        within_vector = numpy.arange(float(within_stair_low_val),
                              float(within_stair_high_value),
                              float(within_stair_jumping))
        return within_vector

    def current_trial(self, previous_decision_correction):
        right_trial = True if random.randint(0, 1) == 0 else False

        if len(self.within_stair_vector_positive) == 0 and len(self.within_stair_vector_negative) > 0:
            right_trial = False
        elif len(self.within_stair_vector_positive) > 0 and len(self.within_stair_vector_negative) == 0:
            right_trial = True

        if right_trial:
            if previous_decision_correction:
                self.within_stair_positive_vector_index = self.within_stair_positive_vector_index + 1 \
                    if self.within_stair_positive_vector_index < len(self.within_stair_vector_positive) \
                    else self.within_stair_positive_vector_index
            else:
                self.within_stair_positive_vector_index = self.within_stair_positive_vector_index \
                    if self.within_stair_positive_vector_index == 0 \
                    else self.within_stair_positive_vector_index - 1

            return self.within_stair_vector_positive[self.within_stair_positive_vector_index]
        else:
            if previous_decision_correction:
                self.within_stair_negative_vector_index = self.within_stair_negative_vector_index + 1 \
                    if self.within_stair_negative_vector_index < len(self.within_stair_vector_negative) - 1 \
                    else self.within_stair_negative_vector_index
            else:
                self.within_stair_negative_vector_index = self.within_stair_negative_vector_index \
                    if self.within_stair_negative_vector_index == 0 \
                    else self.within_stair_negative_vector_index - 1

            return self.within_stair_vector_negative[self.within_stair_negative_vector_index]
