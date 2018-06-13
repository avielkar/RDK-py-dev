# coding: utf-8
import os
import tkinter
import ttk
from tkinter import Tk
from tkinter import Label, Button, Entry
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
        self.combobox_protocol_list = None  # type: Combobox
        self.dynamic_controls_dict = None  # type: Dict[Any, Any]

    def btn_choose_folder_clicked(self):
        self.protocol_root_dir = tkFileDialog.askdirectory()
        self.combo_box_protocol_update()

    def init_gui_controllers(self):
        self.label_choose_folder = Label(master=self.root,
                                         text='Choose folder')
        self.label_choose_folder.pack()

        self.btn_choose_folder = Button(master=self.root,
                                        text='Choose Folder...',
                                        command=self.btn_choose_folder_clicked)
        self.btn_choose_folder.pack()

        self.combobox_protocol_list = ttk.Combobox(master=self.root)
        self.combobox_protocol_list.bind("<<ComboboxSelected>>",
                                         self.combobox_protocols_item_selected)
        self.combo_box_protocol_update()
        self.combobox_protocol_list.pack()

    def combo_box_protocol_update(self):
        self.combobox_protocol_list['values'] = [f for f in os.listdir(self.protocol_root_dir) if
                                                 f.endswith('.xlsx')]

    def combobox_protocols_item_selected(self, event_args):
        self.protocol_file_path = self.protocol_root_dir + '/' + self.combobox_protocol_list.get()
        self.update_dynamic_controls()

    def update_dynamic_controls(self):
        excel_data_dict = self.protocol_reader.read_file(self.protocol_file_path)
        rel_x = 0.0
        rel_y = 0.0
        for key_param_name in excel_data_dict:
            param_label_name = Label(master=self.root,
                                     text=key_param_name)
            param_label_name.place(relx=rel_x, rely=rel_y)
            self.dynamic_controls_dict['label_' + key_param_name] = param_label_name
            rel_x += 0.1

            for key_param_attribute in excel_data_dict[key_param_name]:
                param_entry_value = Entry(master=self.root)
                param_entry_value.insert(0, excel_data_dict[key_param_name][key_param_attribute])
                param_entry_value.place(relx=rel_x, rely=rel_y)
                rel_x += 0.05

            rel_x = 0.0
            rel_y += 0.04

    def load(self):
        self.root = tkinter.Tk()
        self.root.geometry("1400x800")

        self.init_gui_controllers()

        self.protocol_reader = ProtocolReader()
        self.protocol_reader.read_file(self.protocol_file_path)

        self.dynamic_controls_dict = {}

        tkMessageBox.showinfo('Hello python', 'Hello World')
        self.root.mainloop()
