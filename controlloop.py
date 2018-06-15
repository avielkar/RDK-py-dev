# coding: utf-8

import time
from renderer import Renderer
from trialmaker import TrialMaker
import psychopy.event


class ControlLoop:

    def __init__(self):
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self._renderer = Renderer()
        self._attributes = None  # type: Dict[Any, Any]
        self._trial_maker = TrialMaker()
        self.current_trial_data = None  # type: Dict[String, Any]

    pass

    def start(self, attributes, num_of_trials, num_of_repetitions):
        self._renderer.init_window()

        self._attributes = attributes

        self._numOfRepetitions = num_of_repetitions

        self._numOfTrials = num_of_trials

        self._renderer.set_attributes(self._attributes)

        self._trial_maker.load_new_data(attributes=self._attributes,
                                        num_of_repetitions=self._numOfRepetitions,
                                        num_of_trials=self._numOfTrials)

        for trialNum in range(self._numOfTrials):
            self.current_trial_data = self._trial_maker.current_trial(True)

            self.wait_start_key_response()

            self._renderer.render(self.current_trial_data)

            self.response_time_stage()

            self.post_trial_stage()

    def wait_start_key_response(self):
        print self.current_trial_data

        self._renderer.add_text_to_screen('Press space to start the trial')

        keys = psychopy.event.waitKeys(maxWait=float('inf'),
                                       keyList=['space'])

    def response_time_stage(self):
        keys = psychopy.event.waitKeys(maxWait=self.current_trial_data['ResponseTime'],
                                       keyList=['left', 'right'])
        if keys:
            print ('pressed {key}'.format(key=keys[0]))
        else:
            print 'no response'

    def post_trial_stage(self):
        self._renderer.clean_screen()
        time.sleep(self.current_trial_data['PostTrialTime'])


