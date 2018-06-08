# coding: utf-8
from psychopy import gui

info = {
    'ExpVersion': 1.1,
    'Units': 'None',
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
    'Coherence': 0.9
}

tipDictionary = {
    'ExpVersion': 'The experiment version.',
    'units': 'None, norm, cm, deg or pix',
    'DotsColor': 'The dots color [red , green , blue].',
    'Direction': 'Direction of the signal dots (degrees).',
    'NumberOfDots': 'Number of dots to be generated.',
    'FieldShape': 'Defines the shape of the field in which the dots appear. For a circular field the nDots '
                  'represents the average number of dots per frame, but on each frame this may vary a little.',
    'FieldPosition': 'Specifying the location of the centre of the stimulus [x,y].',
    'FieldSize': 'Specifying the diameter of the field (Sizes can be negative and can extend beyond the window).',
    'DotLife': 'Number of frames each dot lives for (-1=infinite).',
    'SignalDots': 'If ‘same’ then the signal and noise dots are constant. If different then the choice of which \
                        is signal and which is noise gets randomised on each frame. This corresponds to Scase et al’s \
                        (1996) categories of RDK.',
    'NoiseDots': 'Determines the behaviour of the noise dots, taken directly from Scase et al’s (1996) \
                        categories. For ‘position’, noise dots take a random position every frame. For ‘direction’ \
                        noise dots follow a random, but constant direction. For ‘walk’ noise dots vary their direction \
                        every frame, but keep a constant speed.',
    'Speed': 'Speed of the dots (in units per frame).',
    'Coherence': 'Change the coherence (%) of the DotStim. This will be rounded \
                        according to the number of dots in the stimulus'
}

dictDlg = gui.DlgFromDict(dictionary=info,
                          title="RDK",
                          fixed=['ExpVersion'],
                          tip=tipDictionary,
                          sort_keys=False)

if dictDlg.OK:
    print(info)
else:
    print('User Cancelled')

keyWait = input('Press key to quit')
dictDlg.Close()
