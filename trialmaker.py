class TrialMaker:
    def __init__(self):
        self._attributes = None  # type: Dict[Any, Any]
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self.trial_number = 0
        pass

    def current_trial(self, previous_decision_correction=False):
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

    def check_experiment_type(self):
        varying_type = 0
        withinstair_type = 0
        varying_type = sum(1 for param_name in self._attributes \
                           if self._attributes[param_name]['param_type'] == 'varying')
        withinstair_type = sum(1 for param_name in self._attributes \
                               if self._attributes[param_name]['param_type'] == 'withinstair')
        if varying_type == 0 and withinstair_type == 0:
            return 'statics'
        elif varying_type > 0 and withinstair_type > 0:
            return 'fault'
        elif varying_type > 0 and withinstair_type == 0:
            return 'varying'
        else:
            return 'withinstair'
