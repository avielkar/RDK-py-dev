import matplotlib.pyplot as plot
import numpy as np


class GraphMaker:

    def __init__(self):
        self._x_values = None  # type: list[int]
        self._y_values = None  # type: list[int]
        self._y_trials_count = None  # type: list[int]
        self._y_trials_right_response_count = None  # type: list[int]
        pass

    def init_graph(self, scala_values):
        self._x_values = scala_values.tolist()
        self._y_values = [0] * len(self._x_values)
        self._y_trials_count = [0] * len(self._x_values)
        self._y_trials_right_response_count = [0] * len(self._x_values)
        fig, axes = plot.subplots(1, 1)
        axes.scatter(np.array(self._x_values), np.array(self._y_values))
        axes.set_ybound(0.0, 1.0)
        fig.suptitle('Decision Graph')
        plot.show()
        pass

    def update_graph(self, trial_data):
        direction = trial_data['Coherence']
        response = trial_data['Response']
        direction_index = self._x_values.index(direction)
        self._y_trials_right_response_count[direction_index] = self._y_trials_right_response_count[direction_index] + 1 \
            if response == 'right' else self._y_trials_right_response_count[direction_index]
        self._y_trials_count[direction_index] += 1
        self._y_values[direction_index] = \
            self._y_trials_right_response_count[direction_index] / self._y_trials_count[direction_index]
        fig, axes = plot.subplots(1, 1)
        axes.scatter(np.array(self._x_values), np.array(self._y_values))
        axes.set_ybound(0.0, 1.0)
        fig.suptitle('Decision Graph')
        plot.show()
        pass
