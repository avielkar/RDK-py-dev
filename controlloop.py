# coding: utf-8
from psychopy import visual, event, core

import time
from renderer import Renderer


class ControlLoop:
    def __init__(self):
        self._numOfTrials = None  # type: Integer
        self._renderer = Renderer()
        self._attributes = None  # type: Dict[Any, Any]
        pass

    def start(self, attributes, num_of_trials):
        self._renderer.init_window()

        self._attributes = attributes

        self._numOfTrials = num_of_trials

        self._renderer.set_attributes(self._attributes)

        for trialNum in range(self._numOfTrials):
            self._renderer.render()
