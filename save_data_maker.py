# coding: utf-8
import datetime
from experimentdata import ExperimentData
import scipy.io as sio


class SaveDataMaker:

    def __init__(self):
        self.directory_path = 'D:\RDK-SavedData\\'
        self.current_saved_file_name = ''
        self.current_saved_file = None  # type: BinaryIO
        pass

    def create_new_data_file(self):
        self.current_saved_file_name = '{date:%Y-%m-%d %H_%M_%S}.txt' \
            .format(date=datetime.datetime.now())
        self.current_saved_file = open(self.directory_path + self.current_saved_file_name, 'w', buffering=1)
        pass

    def save_trial_data_to_file(self, trial_data, experiment_data):
        # add the trial number as the first line.
        self.current_saved_file.write('Trial# {trial_number}\r\n'.format(trial_number=trial_data['Trial#']))

        # loop over all keys and values.
        for (key, value) in trial_data.items():
            if key != 'Trial#':
                self.current_saved_file.write('{key} : {value}\r\n'.format(key=key, value=value))

        # loop over all experiment_data
        self.current_saved_file.write(experiment_data.to_string())

        # new line for spacing with the next trial data.
        self.current_saved_file.write('\r\n')

        saved_trial_dic = {'trial data': trial_data,
                           'experiment_data': experiment_data}
        with open(self.directory_path + self.current_saved_file_name, 'ab') as f:
            sio.savemat(f, {'trial_' + trial_data['Trial#']: saved_trial_dic})
        pass

    def close_data_file(self):
        self.current_saved_file.close()
