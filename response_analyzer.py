# coding: utf-8

class ResponseAnalyzer:
    def __init__(self):
        pass

    def analyze_response(self, trial_data):
        current_direction = float(trial_data['Direction'])
        response = trial_data['Response']

        if 90 > current_direction > -90 and response == 'right':
            return True
        elif 90 > current_direction > -90 and response == 'left':
            return False
        elif 270 > current_direction > 90 and response == 'right':
            return False
        elif 270 > current_direction < 90 and response == 'left':
            return True

        return False

    def reset_analyzer(self):
        pass
