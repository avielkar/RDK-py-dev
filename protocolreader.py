import pandas as pd

excel_file = 'D:\RDK-protocols\coherence.xlsx'

protocol_data = pd.read_excel(excel_file)

params_names = protocol_data['param_name']

data_dict = dict()
param_index = 0
for param_name in params_names:
    data_dict[param_name] = dict()
    for param_key in protocol_data.keys():
        if param_key != 'param_name':
            data_dict[param_name][param_key] = protocol_data[param_key][param_index]
    param_index += 1

