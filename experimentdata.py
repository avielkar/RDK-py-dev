class ExperimentData:
    num_of_repetitions = None  # type:int
    num_of_trials = None  # type:int
    backward_error_probability = None  # type:float
    forward_rightward_probability = None  # type:float
    enable_confidence_choice = None  # type:bool
    draw_fixation_point = None  # type:bool

    # todo: change all attributes to a list of dictionary.

    def __init__(self,
                 num_of_repetitions=None,
                 num_of_trials=None,
                 backward_error_probability=None,
                 forward_rightward_probability=None,
                 enable_confidence_choice=None,
                 draw_fixation_point=None):
        self.num_of_repetitions = num_of_repetitions
        self.num_of_trials = num_of_trials
        self.backward_error_probability = backward_error_probability
        self.forward_rightward_probability = forward_rightward_probability
        self.enable_confidence_choice = enable_confidence_choice
        self.draw_fixation_point = draw_fixation_point
        pass

    def to_string(self):
        return (
                'num_of_repetitions : {num_of_repetitions}' + '\r\n' +
                'num_of_trials : {num_of_trials}' + '\r\n' +
                'backward_error_probability : {backward_error_probability}' + '\r\n' +
                'forward_rightward_probability : {forward_rightward_probability}' + '\r\n' +
                'enable_confidence_choice : {enable_confidence_choice}' + '\r\n' +
                'draw_fixation_point : {draw_fixation_point}' + '\r\n'
        ).format(
            num_of_repetitions=self.num_of_repetitions,
            num_of_trials = self.num_of_trials,
            backward_error_probability = self.backward_error_probability,
            forward_rightward_probability = self.forward_rightward_probability,
            enable_confidence_choice = self.enable_confidence_choice,
            draw_fixation_point = self.draw_fixation_point
        )