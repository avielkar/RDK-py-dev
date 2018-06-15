# coding: utf-8
from psychopy import visual, event, core

import time


class Renderer:

    def __init__(self):
        self._my_win = None
        self._attributes_dict = {
            'Units': None,
            'Color': dict(r=1, g=1, b=1),
            'Direction': 270,
            'NumberOfDots': 500,
            'FieldShape': 'circle',
            'FieldPosition': dict(x=0.0, y=0),
            'FieldSize': 1,
            'DotLife': 5,  # number of frames for each dot to be drawn
            'SignalDots': 'same',
            # are the signal dots the 'same' on each frame? (see Scase et al)
            'NoiseDots': 'direction',
            # do the noise dots follow random- 'walk', 'direction', or 'position'
            'Speed': 0.01,
            'Coherence': 0.9,
            'RenderTime': 1,
            'RenderFrequency': 60
        }
        self.data = None  # type: List{(,)}
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

    def render(self, data):
        self.data = data
        dot_patch = visual.DotStim(win=self._my_win,
                                   units=eval(self._attributes_dict['Units']),
                                   color=list([eval(self._attributes_dict['Color'])['r'],
                                               eval(self._attributes_dict['Color'])['g'],
                                               eval(self._attributes_dict['Color'])['b'],
                                               ]),
                                   dir=self._attributes_dict['Direction'],
                                   nDots=self._attributes_dict['NumberOfDots'],
                                   fieldShape=self._attributes_dict['FieldShape'],
                                   fieldPos=[eval(self._attributes_dict['FieldPosition'])['x'],
                                             eval(self._attributes_dict['FieldPosition'])['y']],
                                   fieldSize=self._attributes_dict['FieldSize'],
                                   dotLife=self._attributes_dict['DotLife'],
                                   # number of frames for each dot to be drawn
                                   signalDots=self._attributes_dict['SignalDots'],
                                   # are the signal dots the 'same' on each frame? (see Scase et al)
                                   noiseDots=self._attributes_dict['NoiseDots'],
                                   # do the noise dots follow random- 'walk', 'direction', or 'position'
                                   speed=self._attributes_dict['Speed'],
                                   coherence=self._attributes_dict['Coherence'])

        message = visual.TextStim(win=self._my_win,
                                  text='Hit Q to quit',
                                  pos=(0, -0.5))

        start_time = time.time()
        while time.time() - start_time < self._attributes_dict['RenderTime']:
            dot_patch.draw()
            message.draw()
            self._my_win.flip()  # redraw the buffer
            time.sleep((1 / self._attributes_dict['RenderFrequency']))
        time.sleep(2)
