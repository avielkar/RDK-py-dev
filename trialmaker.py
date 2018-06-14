class TrialMaker:
    def __init__(self):
        self._attributes = None  # type: Dict[Any, Any]
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self.trial_number = 0
        pass

    def current_trial(self):
        pass

    def load_new_data(self,
                      attributes,
                      num_of_repetitions,
                      num_of_trials):
        self._attributes = attributes
        self._numOfTrials = num_of_trials
        self._numOfRepetitions = num_of_repetitions
        self.trial_number = 0
        pass
