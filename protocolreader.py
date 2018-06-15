import pandas as pd


class ProtocolReader:

    def __init__(self):
        pass

    def read_file(self, path):
        protocol_data = pd.read_excel(path)

        params_names = protocol_data['param_name']

        data_dict = dict()

        # add the titles as a separate list.
        titles = list()
        for param_key in protocol_data.keys():
            titles.append(param_key)

        # add the values for each parameter as a dictionary with attribute name as key and value as value.
        param_index = 0
        for param_name in params_names:
            data_dict[param_name] = dict()
            for param_key in protocol_data.keys():
                # if param_key != 'param_name':
                data_dict[param_name][param_key] = protocol_data[param_key][param_index]
            param_index += 1

        return [data_dict, titles]
