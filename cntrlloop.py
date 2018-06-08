from psychopy import visual, event, core

import time
from renderer import Renderer

class CntrlLoop:
    def __init__(self , num_of_trials , attributes):
        self._numOfTrials = num_of_trials
        self._renderer = Renderer()
        self._attributes = attributes
        pass

    def start(self):
        self._renderer.init_window()
        self._renderer.set_attributes(self._attributes)
        for trialNum in range(self._numOfTrials):
            self._renderer.render()
