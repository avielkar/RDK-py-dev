from withinstair_decision_maker import *
from experimentdata import ExperimentData


class TrialMaker:
    def __init__(self):
        self._attributes = None  # type: Dict[Any, Any]
        self._experiment_data = None  # type: ExperimentData
        self.trial_number = 0
        self.decision_maker = None  # type: DecisionMaker
        self.experiment_type = None  # type:str
        pass

    def current_trial(self):
        current_trial = self.decision_maker.current_trial()

        # add the trial number to the current trial data
        self.trial_number += 1
        current_trial['Trial#'] = self.trial_number

        self.convert_current_trial_attributes_to_their_types(current_trial=current_trial)

        return current_trial

    def convert_current_trial_attributes_to_their_types(self, current_trial):
        current_trial['Direction'] = int(current_trial['Direction'])
        current_trial['NumberOfDots'] = int(current_trial['NumberOfDots'])
        current_trial['FieldSize'] = float(current_trial['FieldSize'])
        current_trial['DotLife'] = int(current_trial['DotLife'])
        current_trial['Speed'] = float(current_trial['Speed'])
        current_trial['Coherence'] = float(current_trial['Coherence'])
        current_trial['RenderTime'] = float(current_trial['RenderTime'])
        current_trial['RenderFrequency'] = float(current_trial['RenderFrequency'])
        current_trial['ResponseTime'] = float(current_trial['ResponseTime'])
        current_trial['ConfidenceResponseTime'] = float(current_trial['ConfidenceResponseTime'])
        current_trial['PostTrialTime'] = float(current_trial['PostTrialTime'])
        pass

    def set_current_trial_response_correction(self, trial_correctness):
        self.decision_maker.set_current_correctness(trial_correctness)

    def load_new_data(self,
                      attributes,
                      experiment_data):
        self._attributes = attributes
        self.experiment_data = experiment_data
        self.trial_number = 0
        self.experiment_type = self.check_experiment_type()
        if self.experiment_type == 'withinstair':
            self.decision_maker = SimpleWithinStairDecisionMaker()
            self.decision_maker.set_attributes(
                param_attributes=self._attributes,
                experiment_data=experiment_data)
        elif self.experiment_type == 'varying':
            pass
        elif self.experiment_type == 'statics':
            pass
        else:
            return False
        return True

    def get_trials_scala_values(self):
        return self.decision_maker.get_vector_values()

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
