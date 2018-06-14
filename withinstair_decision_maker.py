
class WithinStairDecisionMaker:
    backword_rightword_probability = None  # type: Integer
    backword_error_probability = None  # type: Integer
    attribute = None  # type: Any

    def __init__(self):
        pass


    def SetAttributes(self,
                      attribute,
                      backword_error_probability,
                      backword_rightword_probability):
        self.attribute = attribute
        self.backword_error_probability = backword_error_probability
        self.backword_rightword_probability = backword_rightword_probability
        pass

    def ResetDecision(self):
        pass

    def CurrentTrial(self):
        pass