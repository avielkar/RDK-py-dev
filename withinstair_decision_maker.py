class WithinStairDecisionMaker:
    def __init__(self):
        self.backword_rightword_probability = None  # type: Integer
        self.backword_error_probability = None  # type: Integer
        self.param_attributes = None  # type: Anys
        pass

    def set_attributes(self,
                       param_attributes,
                       backword_error_probability,
                       backword_rightword_probability):
        self.param_attributes = param_attributes
        self.backword_error_probability = backword_error_probability
        self.backword_rightword_probability = backword_rightword_probability
        pass

    def reset_decision(self):
        pass

    def create_within_stair_vector(self):
        within_stair_low_val = self.param_attributes['min_value']
        within_stair_high_value = self.param_attributes['max_value']
        within_stair_jumping = self.param_attributes['jumping']
        within_vector = range(within_stair_low_val,
                              within_stair_high_value,
                              within_stair_jumping)
        return within_vector

    def current_trial(self, previous_decision_correction):
        pass
