from main_gui_tkinter import MainGuiTkinter
from graph_maker import GraphMaker
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    graph_maker_command_queue = multiprocessing.Queue()
    graph_maker = GraphMaker()
    graph_maker_process = multiprocessing.Process(target=graph_maker.listening_function_thread,
                                                       args=(graph_maker_command_queue,))
    graph_maker_process.start()

    main_gui = MainGuiTkinter(graph_maker_command_queue)

    main_gui.load()
