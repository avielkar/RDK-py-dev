import pandas as pd

class ProtocolWriter:
    def init(self):
        pass

    def write_file(self , path , data):
        excel_writer = pd.ExcelWriter('D:\RDK-protocols\coherence123.xlsx')
        protocol_data_frame = pd.DataFrame.from_dict(data)
        protocol_data_frame.to_excel(excel_writer)
        excel_writer.save()
        pass

