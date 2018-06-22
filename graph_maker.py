import matplotlib.pyplot as plot
import numpy as np


class GraphMaker:

    def __init__(self):
        self._x_values = None  # type: object
        self._y_values = None  # type: object
        pass

    def init_graph(self, scala_values):
        self._x_values = np.array(scala_values)
        self._y_values = np.zeros(len(self._x_values))
        fig, axes = plot.subplots(1, 1)
        axes.plot(self._x_values, self._y_values)
        plot.show()
        pass

    def update_graph(self, trial_data):
        pass
