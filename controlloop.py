# coding: utf-8

import time
from threading import Thread
from renderer import Renderer
from trialmaker import TrialMaker
from save_data_maker import SaveDataMaker
from response_analyzer import ResponseAnalyzer
from graph_maker import GraphMaker
import tkinter.messagebox
import psychopy.event
import pygame
from pygame.locals import *
from experimentdata import ExperimentData
import queue
import multiprocessing


class ControlLoop:
    exit_experiment = None  # type:bool

    def __init__(self, gui_queue, control_loop_queue, graph_maker_queue):
        self._numOfTrials = None  # type: Integer
        self._numOfRepetitions = None  # type: Integer
        self.experiment_data: None  # type: ExperimentData
        self._renderer = Renderer()
        self._attributes = None  # type: Dict[Any, Any]
        self._trial_maker = TrialMaker()
        self._save_data_maker = SaveDataMaker()
        self._current_trial_data = None  # type: Dict[String, Any]
        self._response_analyzer = ResponseAnalyzer()
        self._graph_maker = GraphMaker()
        self.exit_experiment = False
        self.gui_queue = gui_queue  # type:queue.Queue
        self.control_loop_commands_queue = control_loop_queue  # type: queue.Queue
        self.graph_maker_command_queue = graph_maker_queue  # type: multiprocessing.Queue
        self.main_loop_thread = Thread(target=self.listening_function,
                                       args=())
        self.main_loop_thread.start()

    def start(self, attributes, experiment_data):
        self._attributes = attributes

        self.experiment_data = experiment_data

        self._renderer.set_attributes(self._attributes, self.experiment_data)

        self._response_analyzer.reset_analyzer()

        self._trial_maker.load_new_data(attributes=self._attributes,
                                        experiment_data=self.experiment_data)

        self._save_data_maker.create_new_data_file(experiment_data.user_running_experiment_name)

        if not self._renderer.is_initialized:
            self._renderer.init_window(units=self._current_trial_data['Units'],
                                       distance2screen=self._current_trial_data['Distance2Screen'])
            self.graph_maker_command_queue.put(('init_graph', self._trial_maker.get_trials_scala_values()))
        else:
            self.graph_maker_command_queue.put(('reset_graph', self._trial_maker.get_trials_scala_values()))            # self._graph_maker.reset_graph(self._trial_maker.get_trials_scala_values())

        for trialNum in range(self.experiment_data.num_of_trials):
            if self.exit_experiment:
                break

            self._current_trial_data = self._trial_maker.current_trial()

            self.wait_start_key_response()

            self._renderer.render(self._current_trial_data)

            self.response_time_stage()

            if self.experiment_data.enable_confidence_choice and \
                    self._current_trial_data['Response'] != 'none':
                self.confidence_response_time_stage()

            self.post_trial_stage()

        # todo: check why it is causing here a stucking problem.
        # tkinter.messagebox.showinfo('info', 'End of the experiment!')

        self._save_data_maker.close_data_file()
        self.gui_queue.put(('enable_start_btn', True))

    def wait_start_key_response(self):
        print(self._current_trial_data)

        self._renderer.add_text_to_screen('Press space to start the trial')
        print('waiting to start response...')

        pygame.event.clear()
        event = pygame.event.poll()
        while (event.type != KEYDOWN and event.type != KEYUP) or event.key != K_SPACE:
            event = pygame.event.poll()

    def response_time_stage(self):
        response = 'none'
        pygame.event.clear()
        print('waiting to response...')

        start_time = time.time()
        while time.time() - start_time < self._current_trial_data['ResponseTime']:
            event = pygame.event.poll()
            if ((event.type == KEYDOWN or event.type == KEYUP) \
                    and (event.key == K_LEFT or event.key == K_RIGHT)):
                response = 'left' if event.key == K_LEFT else 'right'
                break
            time.sleep(0.001)

        if response is not 'none':
            print('pressed {key}'.format(key=response))
        else:
            print('no response')

        self._current_trial_data['Response'] = response

    def confidence_response_time_stage(self):
        response = 'none'
        pygame.event.clear()
        print('waiting to confidence response...')

        start_time = time.time()
        while time.time() - start_time < self._current_trial_data['ConfidenceResponseTime']:
            event = pygame.event.poll()
            if ((event.type == KEYDOWN or event.type == KEYUP) \
                    and (event.key == K_UP or event.key == K_DOWN)):
                response = 'up' if event.key == K_UP else 'down'
                break
            time.sleep(0.001)

        if response is not 'none':
            print('pressed {key}'.format(key=response))
        else:
            print('no response')

        self._current_trial_data['ConfidenceResponse'] = response

    def post_trial_stage(self):
        # todo: check how to add the screen clean to the post_trial_stage_thread.
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
        self._current_trial_data['ResponseCorrectness'] = trial_correction
        self._trial_maker.set_current_trial_response_correction(trial_correction)
        self._save_data_maker.save_trial_data_to_file(self._current_trial_data, self.experiment_data)
        self.graph_maker_command_queue.put(('update_graph', self._current_trial_data))

    def sleep_function(self, sleep_time_seconds):
        time.sleep(sleep_time_seconds)

    def listening_function(self):
        while not self.exit_experiment:
            if not self.control_loop_commands_queue.empty():
                (command, data) = self.control_loop_commands_queue.get()
                if command == 'start':
                    (attributes, experiment_data) = data
                    self.start(attributes=attributes,
                               experiment_data=experiment_data)
            time.sleep(0.1)
