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
        axes.scatter(self._x_values, self._y_values)
        axes.set_ybound(0.0, 1.0)
        fig.suptitle('Decision Graph')
        plot.show()
        pass

    def update_graph(self, trial_data):
        pass
