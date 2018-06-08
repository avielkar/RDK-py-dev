from psychopy import visual, event, core

import time


class Renderer:

    def __init__(self):
        self._my_win = None
        self._attributes_dict = {
            'units': None,
            'color': (1.0, 1.0, 1.0),
            'dir': 270,
            'nDots': 500,
            'fieldShape': 'circle',
            'fieldPos': (0.0, 0.0),
            'fieldSize': 1,
            'dotLife': 5,  # number of frames for each dot to be drawn
            'signalDots': 'same',
            # are the signal dots the 'same' on each frame? (see Scase et al)
            'noiseDots': 'direction',
            # do the noise dots follow random- 'walk', 'direction', or 'position'
            'speed': 0.01,
            'coherence': 0.9
        }
        pass

    def init_window(self):
        self._my_win = visual.Window((600, 600),
                                     allowGUI=False,
                                     bitsMode=None,
                                     units='norm',
                                     winType='pyglet')

    def set_attributes(self, attributes_dict):
        self._attributes_dict = attributes_dict

    def set_attribute(self, name, value):
        self._attributes_dict[name] = value

    def render_trial(self):
        dot_patch = visual.DotStim(win=self._my_win,
                                   units=self._attributes_dict['units'],
                                   color=self._attributes_dict['color'],
                                   dir=self._attributes_dict['dir'],
                                   nDots=self._attributes_dict['nDots'],
                                   fieldShape=self._attributes_dict['fieldShape'],
                                   fieldPos=self._attributes_dict['fieldPos'],
                                   fieldSize=self._attributes_dict['fieldSize'],
                                   dotLife=self._attributes_dict['dotLife'],
                                   # number of frames for each dot to be drawn
                                   signalDots=self._attributes_dict['signalDots'],
                                   # are the signal dots the 'same' on each frame? (see Scase et al)
                                   noiseDots=self._attributes_dict['noiseDots'],
                                   # do the noise dots follow random- 'walk', 'direction', or 'position'
                                   speed=self._attributes_dict['speed'],
                                   coherence=self._attributes_dict['coherence'])

        message = visual.TextStim(win=self._my_win,
                                  text='Hit Q to quit',
                                  pos=(0, -0.5))

        start_time = time.time()
        while time.time() - start_time < 1:
            dot_patch.draw()
            message.draw()
            self._my_win.flip()  # redraw the buffer
            time.sleep((50 / 1000))
