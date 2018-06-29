class ExperimentData:
    backward_error_probability = None  # type:int
    forward_rightward_probability = None  # type:int

    def __init__(self,
                 backward_error_probability=None,
                 forward_rightward_probability=None):
        self.backward_error_probability = backward_error_probability
        self.forward_rightward_probability = forward_rightward_probability
        pass
