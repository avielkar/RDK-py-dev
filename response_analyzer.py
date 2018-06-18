# coding: utf-8

class ResponseAnalyzer:
    def __init__(self):
        pass

    def analyze_response(self, trial_data, response):
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
