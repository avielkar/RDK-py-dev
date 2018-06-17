# coding: utf-8
from typing import BinaryIO
import datetime


class SaveDataMaker:

    def __init__(self):
        self.directory_path = 'D:\RDK-SavedData'
        self.current_saved_file_name = ''
        self.current_saved_file = None  # type: BinaryIO
        pass

    def create_new_data_file(self):
        self.current_saved_file_name = '{date:%Y-%m-%d %H:%M:%S}.txt' \
            .format(date=datetime.datetime.now())
        self.current_saved_file = open(self.directory_path + self.current_saved_file_name, 'rw')
        pass

    def save_trial_data_to_file(self, trial_data):
        for (key, value) in trial_data.items():
            self.current_saved_file.write('{key} : {value}\n'.format(key=key, value=value))
        pass

    def close_data_file(self):
        self.current_saved_file.close()
