import pandas as pd
import os


class ProtocolWriter:
    def init(self):
        pass

    def write_file(self, dir_path, file_name, data):
        if file_name + '.xlsx' in os.listdir(dir_path):
            return False

        excel_writer = pd.ExcelWriter(dir_path + '/' + file_name + '.xlsx')

        excel_data = []
        for attribute_name in data[list(data.keys())[0]].keys():
            column_data = [data[param_name][attribute_name] for param_name in data.keys()]
            columns_name = attribute_name
            excel_data.append((columns_name, column_data))

        df = pd.DataFrame.from_items(excel_data)
        df.to_excel(excel_writer,
                    index=False)
        excel_writer.save()

        return True
        pass
