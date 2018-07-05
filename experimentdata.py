class ExperimentData:
    num_of_repetitions = None  # type:int
    num_of_trials = None  # type:int
    backward_error_probability = None  # type:float
    forward_rightward_probability = None  # type:float
    enable_confidence_choice = None  # type:bool
    draw_fixation_point = None  # type:bool

    def __init__(self,
                 num_of_repetitions=None,
                 num_of_trials=None,
                 backward_error_probability=None,
                 forward_rightward_probability=None,
                 enable_confidence_choice=None,
                 draw_fixxation_point=None):
        self.num_of_repetitions = num_of_repetitions
        self.num_of_trials = num_of_trials
        self.backward_error_probability = backward_error_probability
        self.forward_rightward_probability = forward_rightward_probability
        self.enable_confidence_choice = enable_confidence_choice
        self.draw_fixation_point=draw_fixxation_point
        pass
