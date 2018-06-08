from psychopy import visual, event, core

import time

class CntrlLoop:
    def __init__(self , numOfTrials):
        self._numOfTrials = numOfTrials
        pass

    def Start(self):
        myWin = visual.Window((600, 600),
                              allowGUI=False,
                              bitsMode=None,
                              units='norm',
                              winType='pyglet')

        for trialNum in range(self._numOfTrials):
            dotPatch = visual.DotStim(win=myWin,
                                      units=None,
                                      color=(1.0, 1.0, 1.0),
                                      dir=270,
                                      nDots=500,
                                      fieldShape='circle',
                                      fieldPos=(0.0, 0.0),
                                      fieldSize=1,
                                      dotLife=5,  # number of frames for each dot to be drawn
                                      signalDots='same',
                                      # are the signal dots the 'same' on each frame? (see Scase et al)
                                      noiseDots='direction',
                                      # do the noise dots follow random- 'walk', 'direction', or 'position'
                                      speed=0.01,
                                      coherence=0.9)

            message = visual.TextStim(win=myWin,
                                      text='Hit Q to quit',
                                      pos=(0, -0.5))
            start_time = time.time()

            while time.time() - start_time < 1:
                dotPatch.draw()
                message.draw()
                myWin.flip()  # redraw the buffer
                time.sleep((50/1000))

            time.sleep(2)
