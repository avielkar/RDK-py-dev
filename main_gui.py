from psychopy import gui

info = {'Observer':'jwp',
        'GratingOri':45,
        'ExpVersion': 1.1,
        'Group': ['Test', 'Control'],
        }
dictDlg = gui.DlgFromDict(dictionary=info,
                          title="RDK",
                          fixed=['ExpVersion'])

if dictDlg.OK:
    print(info)
else:
    print('User Cancelled')

dictDlg.show()

keyWait = input('Press key to quit')
dictDlg.Close()
