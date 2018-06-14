
class WithinStairDecisionMaker:
    backword_rightword_probability = None  # type: Integer
    backword_error_probability = None  # type: Integer
    attribute = None  # type: Any

    def __init__(self):
        pass


    def set_attributes(self,
                       attribute,
                       backword_error_probability,
                       backword_rightword_probability):
        self.attribute = attribute
        self.backword_error_probability = backword_error_probability
        self.backword_rightword_probability = backword_rightword_probability
        pass

    def reset_decision(self):
        pass

    def create_within_stair_vector(self):
        within_stair_low_val = attribute
        within_stair_high_value=0
        within_stair_jumping = 0

    def current_trial(self , previous_decision_correction):

        pass