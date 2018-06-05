from psychopy import gui

info = {
        'ExpVersion': 1.1,
        'Observer': 'jwp',
        'GratingOri': 45,
        'Group': ['Test', 'Control'],
        'DotsColor': [1.0, 1.0, 1.0],
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
dictDlg = gui.DlgFromDict(dictionary=info,
                          title="RDK",
                          fixed=['ExpVersion'])

if dictDlg.OK:
    print(info)
else:
    print('User Cancelled')

keyWait = input('Press key to quit')
dictDlg.Close()
