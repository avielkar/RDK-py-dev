# coding: utf-8
from psychopy import visual, event, core
from controlloop import ControlLoop

info = {
    'ExpVersion': 1.1,
    'Units': None,
    'Color': dict(r=1, g=1, b=1),
    'Direction': 270,
    'NumberOfDots': 500,
    'FieldShape': 'circle',
    'FieldPosition': dict(x=0.0, y=0),
    'FieldSize': 1,
    'DotLife': 5,
    'SignalDots': 'same',
    'NoiseDots': 'direction',
    'Speed': 0.01,
    'Coherence': 0.9,
    'RenderTime': 1,
    'RenderFrequency': 60
}
cntrlLoop = ControlLoop(num_of_trials=12, attributes=info)
cntrlLoop.start()
