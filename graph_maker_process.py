from graph_maker import GraphMaker


class GraphMakerProcess:
    def __init__(self):
        self.graph_maker = GraphMaker()
        self.graph_maker.listening_function_thread()
