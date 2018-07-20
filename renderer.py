# coding: utf-8

from psychopy import visual, monitors

from experimentdata import ExperimentData

import time


class Renderer:
    is_initialized = False

    def __init__(self):
        self._my_win = None
        self.is_initialized = False
        self._attributes_dict = {
            'Units': 'deg',
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
        self.data = None  # type: Dict[String, Any]
        self.experiment_data = None  # type: ExperimentData
        pass

    def init_window(self, units, distance2screen):
        my_monitor = monitors.Monitor(name='testMonitor',
                                      distance=distance2screen)

        self._my_win = visual.Window(size=(800, 800),
                                     monitor=my_monitor,
                                     color='black',
                                     fullscr=False,
                                     allowGUI=False,
                                     bitsMode=None,
                                     units=units,
                                     winType='pygame')
        self.is_initialized = True

    def close(self):
        self._my_win.close()

    # todo: remove the attributes_dict - it is not necessary , also remove the experiment_data and transfer it via
    # the render function.
    def set_attributes(self, attributes_dict, experiment_data):
        self._attributes_dict = attributes_dict
        self.experiment_data = experiment_data

    def render(self, data):
        self.data = data
        dot_patch = visual.WrappingDotStim(win=self._my_win,
                                           units=self.data['Units'],
                                           color=list([eval(self.data['Color'])[0],
                                                       eval(self.data['Color'])[1],
                                                       eval(self.data['Color'])[2],
                                                       ]),
                                           dir=self.convert_to_psycho_direction(self.data['Direction']),
                                           nDots=self.data['NumberOfDots'],
                                           fieldShape=self.data['FieldShape'],
                                           fieldPos=[eval(self.data['FieldPosition'])[0],
                                                     eval(self.data['FieldPosition'])[1]],
                                           fieldSize=self.data['FieldSize'],
                                           dotLife=self.data['DotLife'],
                                           # number of frames for each dot to be drawn
                                           signalDots=self.data['SignalDots'],
                                           # are the signal dots the 'same' on each frame? (see Scase et al)
                                           noiseDots=self.data['NoiseDots'],
                                           # do the noise dots follow random- 'walk', 'direction', or 'position'
                                           speed=self.data['Speed'],
                                           coherence=self.data['Coherence'])

        message = visual.TextStim(win=self._my_win,
                                  text='Hit Q to quit',
                                  pos=(0, -0.5))

        if self.experiment_data.draw_fixation_point:
            fixation_point_stim = visual.Circle(win=self._my_win,
                                                radius=0.01,
                                                edges=32,
                                                pos=[0, 0],
                                                lineColor=[0, 1, 0],
                                                fillColor=[0, 1, 0])

        start_time = time.time()
        while time.time() - start_time < self.data['RenderTime']:
            dot_patch.draw()
            if self.experiment_data.draw_fixation_point:
                fixation_point_stim.draw()
            message.draw()
            self._my_win.flip()  # redraw the buffer
            time.sleep((1 / self.data['RenderFrequency']))

    def convert_to_psycho_direction(self, direction):
        if 90 >= direction >= 0:
            return 90 - direction
        elif 180 >= direction > 90:
            return -direction + 90
        elif -90 <= direction <= 0:
            return 90 - direction
        elif -180 <= direction < -90:
            return -direction - 270

    def clean_screen(self):
        self._my_win.flip()

    def add_text_to_screen(self, text):
        message = visual.TextStim(win=self._my_win,
                                  text=text,
                                  pos=(0, 0),
                                  height=0.06)
        message.draw()

        self._my_win.flip(clearBuffer=False)
