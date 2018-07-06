from graph_maker import GraphMaker


class GraphMakerProcess:
    def __init__(self , graph_maker_command_queue):
        self.graph_maker = GraphMaker()
        self.graph_maker.listening_function_thread(graph_maker_command_queue)
