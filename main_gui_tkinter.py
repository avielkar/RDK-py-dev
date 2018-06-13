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

    def add_parameters_titles(self, titles, rel_x, rel_y):
        for title in titles:
            if title != 'tool_tip':
                title_label = Label(master=self.root,
                                    text=title)
                title_label.place(relx=rel_x[0], rely=rel_y[0])
                rel_x[0] += 0.1

        rel_x[0] = 0.0
        rel_y[0] += 0.04

    def add_parameters_attributes(self, titles, data_dict, rel_x, rel_y):
        for key_param_name in data_dict:
            param_label_name = Label(master=self.root,
                                     text=key_param_name)
            param_label_name.place(relx=rel_x[0], rely=rel_y[0])
            self.dynamic_controls_dict['label_' + key_param_name] = param_label_name
            rel_x[0] += 0.1

            for key_param_attribute in titles:
                if key_param_attribute == 'tool_tip' or \
                        key_param_attribute == 'param_name':
                    continue

                if key_param_attribute == 'param_type':
                    param_combobox = ttk.Combobox(master=self.root)
                    param_combobox['values'] = ['static', 'choice', 'constvec', 'acrosstair', 'withinstair']
                    param_combobox.place(relx=rel_x[0], rely=rel_y[0])
                    param_combobox.set(data_dict[key_param_name][key_param_attribute])
                    self.dynamic_controls_dict[key_param_attribute + '_' + key_param_name] = param_combobox
                else:
                    param_entry_value = Entry(master=self.root)
                    param_entry_value.insert(0, data_dict[key_param_name][key_param_attribute])
                    param_entry_value.place(relx=rel_x[0], rely=rel_y[0])
                    self.dynamic_controls_dict[key_param_attribute + '_' + key_param_name] = param_entry_value

                rel_x[0] += 0.1

            rel_x[0] = 0.0
            rel_y[0] += 0.04

    def delete_dynamic_controls(self):
        for control in self.dynamic_controls_dict.values():
            control.destroy()
        self.dynamic_controls_dict.clear()

    def update_dynamic_controls(self):
        self.delete_dynamic_controls()
        [excel_data_dict, titles] = self.protocol_reader.read_file(self.protocol_file_path)
        rel_x = [0.0]
        rel_y = [0.1]

        # for titles labels
        self.add_parameters_titles(titles, rel_x, rel_y)

        # for other attributes
        self.add_parameters_attributes(titles, excel_data_dict, rel_x, rel_y)

    def load(self):
        self.root = tkinter.Tk()
        self.root.geometry("1400x800")

        self.init_gui_controllers()

        self.protocol_reader = ProtocolReader()
        self.protocol_reader.read_file(self.protocol_file_path)

        self.dynamic_controls_dict = {}

        tkMessageBox.showinfo('Hello python', 'Hello World')
        self.root.mainloop()
