from withinstair_decision_maker import *


class TrialMaker:
    def __init__(self):
        self._attributes = None  # type: Dict[Any, Any]
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self.trial_number = 0
        self.within_stair_decision_maker = None  # type: WithinStairDecisionMaker
        pass

    def current_trial(self):
        current_trial = self.within_stair_decision_maker.current_trial()

        # add the trial number to the current trial data
        self.trial_number += 1
        current_trial['Trial#'] = self.trial_number

        return current_trial

    def set_current_trial_response_correction(self, trial_correctness):
        self.within_stair_decision_maker.set_current_correctness(trial_correctness)

    def load_new_data(self,
                      attributes,
                      num_of_repetitions,
                      num_of_trials):
        self._attributes = attributes
        self._numOfTrials = num_of_trials
        self._numOfRepetitions = num_of_repetitions
        self.trial_number = 0
        experiment_type = self.check_experiment_type()
        if experiment_type == 'withinstair':
            self.within_stair_decision_maker = SimpleWithinstairDecisionMaker()
            self.within_stair_decision_maker.set_attributes(
                param_attributes=self._attributes,
                backword_error_probability=0.9,
                backword_rightword_probability=0.1)
        elif experiment_type == 'varying':
            pass
        elif experiment_type == 'statics':
            pass
        else:
            return False
        return True

    def get_trials_scala_values(self):
        return self.within_stair_decision_maker.get_within_stair_vector_values()

    def check_experiment_type(self):
        varying_type = sum(1 for param_name in self._attributes \
                           if self._attributes[param_name]['paramtype'] == 'varying')
        withinstair_type = sum(1 for param_name in self._attributes \
                               if self._attributes[param_name]['paramtype'] == 'withinstair')
        if varying_type == 0 and withinstair_type == 0:
            return 'statics'
        elif varying_type > 0 and withinstair_type > 0:
            return 'fault'
        elif varying_type > 0 and withinstair_type == 0:
            return 'varying'
        else:
            return 'withinstair'
