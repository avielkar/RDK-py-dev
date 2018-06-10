from protocolreader import ProtocolReader

excel_path = 'D:\RDK-protocols\coherence.xlsx'

prot_reader = ProtocolReader()

data = prot_reader.read_file(excel_path)

data



