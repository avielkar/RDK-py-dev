from psychopy import visual, event, core

import time

class CntrlLoop:
    def __init__(self , numOfTrials):
        self._numOfTrials = numOfTrials
        pass

    def start(self):
        for trialNum in range(self._numOfTrials):
            start_time = time.time()

            time.sleep(2)
