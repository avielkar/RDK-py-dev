import matplotlib.pyplot as pyplot
import numpy as np


class GraphMaker:

    def __init__(self):
        self._x_values = None  # type: list[int]
        self._y_values = None  # type: list[int]
        self._y_trials_count = None  # type: list[int]
        self._y_trials_correct_response_count = None  # type: list[int]
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
        pyplot.pause(0.01)
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
        pyplot.pause(0.01)
        pass
