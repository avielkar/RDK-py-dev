import pandas as pd


class ProtocolWriter:
    def init(self):
        pass

    def write_file(self, path, data):
        excel_writer = pd.ExcelWriter(path + '.xlsx')

        excel_data = []
        for attribute_name in data['Coherence'].keys():
            column_data = [data[param_name][attribute_name] for param_name in data.keys()]
            columns_name = attribute_name
            excel_data.append((columns_name, column_data))

        df = pd.DataFrame.from_items(excel_data)
        df.to_excel(excel_writer,
                    index=False)
        excel_writer.save()

        pass
