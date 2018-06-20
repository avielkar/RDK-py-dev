# coding: utf-8

class ResponseAnalyzer:
    def __init__(self):
        self._first_trial = True
        pass

    def analyze_response(self, trial_data, response):
        # if it is the firat trial there is no past to look for.....
        if self._first_trial:
            self._first_trial = False
            return False

        current_direction = float(trial_data['Direction'])
        if 180 > current_direction > 0 and response == 'right':
            return True
        elif 180 > current_direction > 0 and response == 'left':
            return False
        elif 180 > current_direction and response == 'right':
            return False
        elif 180 < current_direction and response == 'left':
            return True

        return False

    def reset_analyzer(self):
        self._first_trial = True

