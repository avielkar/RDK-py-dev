# coding: utf-8
from Tkinter import Label, Button

import os
import tkinter
import ttk
from tkinter import Tk
from tkinter import Label, Button
import tkFileDialog

from protocolreader import ProtocolReader
import tkMessageBox


class MainGuiTkinter:

    def __init__(self):
        self.tkFileDialog = None
        self.protocol_reader = None  # type: ProtocolReader
        self.root = None  # type: Tk
        self.protocol_file_path = 'D:\RDK-protocols\coherence.xlsx'
        self.label_choose_folder = None  # type: Label
        self.btn_choose_folder = None  # type: Button
        self.protocol_root_dir = 'D:\RDK-protocols'  # type: object

    def btn_choose_folder_clicked(self):
        self.protocol_root_dir = tkFileDialog.askdirectory()

    def init_gui_controllers(self):
        self.label_choose_folder = Label(master=self.root,
                                         text='Choose folder')
        self.label_choose_folder.pack()

        self.btn_choose_folder = Button(master=self.root,
                                        text='Choose Folder...',
                                        command=self.btn_choose_folder_clicked)
        self.btn_choose_folder.pack()

        combobox_protocol_list = ttk.Combobox(master=self.root)
        combobox_protocol_list['values'] = [f for f in os.listdir(self.protocol_root_dir) if f.split('.')[1] == 'xlsx']
        combobox_protocol_list.pack()

    def load(self):
        self.root = tkinter.Tk()

        self.init_gui_controllers()

        self.protocol_reader = ProtocolReader()
        self.protocol_reader.read_file(self.protocol_file_path)

        tkMessageBox.showinfo('Hello python', 'Hello World')
        self.root.mainloop()
