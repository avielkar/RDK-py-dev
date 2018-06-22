# coding: utf-8

import time
from threading import Thread
from renderer import Renderer
from trialmaker import TrialMaker
from save_data_maker import SaveDataMaker
from response_analyzer import ResponseAnalyzer
from graph_maker import GraphMaker
import psychopy.event


class ControlLoop:

    def __init__(self):
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self._renderer = Renderer()
        self._attributes = None  # type: Dict[Any, Any]
        self._trial_maker = TrialMaker()
        self._save_data_maker = SaveDataMaker()
        self._current_trial_data = None  # type: Dict[String, Any]
        self._response_analyzer = ResponseAnalyzer()
        self._graph_maker = GraphMaker()
    pass

    def start(self, attributes, num_of_trials, num_of_repetitions):
        self._renderer.init_window()

        self._attributes = attributes

        self._numOfRepetitions = num_of_repetitions

        self._numOfTrials = num_of_trials

        self._renderer.set_attributes(self._attributes)

        self._response_analyzer.reset_analyzer()

        self._trial_maker.load_new_data(attributes=self._attributes,
                                        num_of_repetitions=self._numOfRepetitions,
                                        num_of_trials=self._numOfTrials)

        self._graph_maker.init_graph(self.trialmaker.get_trials_scala_values())

        self._save_data_maker.create_new_data_file()

        for trialNum in range(self._numOfTrials):
            self._current_trial_data = self._trial_maker.current_trial()

            self.wait_start_key_response()

            self._renderer.render(self._current_trial_data)

            self.response_time_stage()

            self.post_trial_stage()

    def wait_start_key_response(self):
        print self._current_trial_data

        self._renderer.add_text_to_screen('Press space to start the trial')

        keys = psychopy.event.waitKeys(maxWait=float('inf'),
                                       keyList=['space'])

    def response_time_stage(self):
        keys = psychopy.event.waitKeys(maxWait=self._current_trial_data['ResponseTime'],
                                       keyList=['left', 'right'])
        if keys:
            print ('pressed {key}'.format(key=keys[0]))
            self._current_trial_data['Response'] = keys[0]
        else:
            self._current_trial_data['Response'] = 'none'
            print 'no response'

    def post_trial_stage(self):
        # todo: check how to tahe the screen clean to the post_trial_stage_thread.
        self._renderer.clean_screen()
        thread_sleep = Thread(target=self.sleep_function,
                              args=(self._current_trial_data['PostTrialTime'],))
        thread_post_trial_stage = Thread(target=self.post_trial_stage_thread,
                                         args=())

        thread_post_trial_stage.start()
        thread_sleep.start()

        thread_post_trial_stage.join()
        thread_sleep.join()

    def post_trial_stage_thread(self):
        trial_correction = self._response_analyzer.analyze_response(self._current_trial_data)
        self._trial_maker.set_current_trial_response_correction(trial_correction)
        self._save_data_maker.save_trial_data_to_file(self._current_trial_data)

    def sleep_function(self, sleep_time_seconds):
        time.sleep(sleep_time_seconds)
