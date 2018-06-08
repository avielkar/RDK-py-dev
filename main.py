# coding: utf-8
from psychopy import visual, event, core
from cntrlloop import CntrlLoop

info = {
    'ExpVersion': 1.1,
    'Units': None,
    'Color': [1.0, 1.0, 1.0],
    'Direction': 270,
    'NumberOfDots': 500,
    'FieldShape': 'circle',
    'FieldPosition': [0.0, 0.0],
    'FieldSize': 1,
    'DotLife': 5,
    'SignalDots': 'same',
    'NoiseDots': 'direction',
    'Speed': 0.01,
    'Coherence': 0.9,
    'RenderTime': 1,
    'RenderFrequency': 60
}
cntrlLoop = CntrlLoop(num_of_trials=12, attributes=info)
cntrlLoop.start()
