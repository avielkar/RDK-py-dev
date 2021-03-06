import win32api
import win32process

import matplotlib.pyplot as pyplot
import numpy as np
import queue
import time


class GraphMaker:

    def __init__(self):
        self._x_values = None  # type: list[int]
        self._y_values = None  # type: list[int]
        self._y_trials_count = None  # type: list[int]
        self._y_trials_correct_response_count = None  # type: list[int]
        win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_LOWEST)
        pass

    def init_graph(self, scala_values):
        self._x_values = scala_values.tolist()
        self._y_values = [0] * len(self._x_values)
        self._y_trials_count = [0] * len(self._x_values)
        self._y_trials_correct_response_count = [0] * len(self._x_values)

        pyplot.ion()
        pyplot.plot(np.array(self._x_values), np.array(self._y_values), 'ro')
        pyplot.axis([self._x_values[0], \
                     self._x_values[len(self._x_values) - 1], \
                     0.0, \
                     1.0])
        pyplot.xlabel('Coherence')
        pyplot.ylabel('Correctness')
        pyplot.draw()
        pyplot.show()
        pyplot.pause(1)
        pass

    def reset_graph(self
                    , scala_values):
        self._x_values = scala_values.tolist()
        self._y_values = [0] * len(self._x_values)
        self._y_trials_count = [0] * len(self._x_values)
        self._y_trials_correct_response_count = [0] * len(self._x_values)

        pyplot.axis([self._x_values[0], \
                     self._x_values[len(self._x_values) - 1], \
                     0.0, \
                     1.0])
        pyplot.clf()
        pyplot.xlabel('Coherence')
        pyplot.ylabel('Correctness')
        pyplot.draw()
        pyplot.pause(1)
        pass

    def update_graph(self, trial_data):
        direction = trial_data['Coherence']
        response_correctness = trial_data['ResponseCorrectness']
        direction_index = self._x_values.index(direction)
        self._y_trials_correct_response_count[direction_index] = self._y_trials_correct_response_count[
                                                                     direction_index] + 1 \
            if response_correctness else self._y_trials_correct_response_count[direction_index]
        self._y_trials_count[direction_index] += 1
        self._y_values[direction_index] = \
            float(self._y_trials_correct_response_count[direction_index]) / self._y_trials_count[direction_index]

        pyplot.clf()
        pyplot.xlabel('Coherence')
        pyplot.ylabel('Correctness')
        pyplot.plot(np.array(self._x_values), np.array(self._y_values), 'ro')
        pyplot.draw()
        pyplot.pause(1)
        pass

    def listening_function_thread(self , control_loop_queue):
        win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_LOWEST)
        while True:
            if not control_loop_queue.empty():
                (command_function , command_data) = control_loop_queue.get()
                if command_function == 'update_graph':
                    self.update_graph(command_data)
                elif command_function == 'reset_graph':
                    self.reset_graph(command_data)
                elif command_function == 'init_graph':
                    self.init_graph(command_data)
            pyplot.pause(0.1)
            time.sleep(0.5)
        pass
