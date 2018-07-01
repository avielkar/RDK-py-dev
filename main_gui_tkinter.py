# coding: utf-8
import os

import tkinter
import tkinter.ttk
from tkinter import Tk, Toplevel, Label
from tkinter import Label, Button, Entry
import tkinter.filedialog

from protocolreader import ProtocolReader
from controlloop import ControlLoop
import tkinter.messagebox
from threading import Thread
from experimentdata import ExperimentData


class MainGuiTkinter:

    def __init__(self):
        self.tkFileDialog = None
        self.protocol_reader = None  # type: ProtocolReader
        self.control_loop = None  # type: ControlLoop
        self.root = None  # type: Tk
        self.protocol_file_path = 'D:\RDK-protocols\coherence.xlsx'
        self.label_choose_folder = None  # type: Label
        self.btn_choose_folder = None  # type: Button
        self.protocol_root_dir = 'D:\RDK-protocols'  # type: object
        self.combobox_protocol_list = None  # type: Combobox
        self.btn_start_experiment = None  # type: Button
        self.dynamic_controls_dict = None  # type: Dict[Any, Any]
        self.parameters_attributes_dictionary = None  # type: Dict[Any,Any]
        self.label_num_of_repetitions = None  # type: Label
        self.label_num_of_trials = None  # type: Label
        self.label_backward_error_probability: Label
        self.label_forward_rightward_probability: Label
        self.entry_num_of_repetitions = None  # type: Entry
        self.entry_num_of_trials = None  # type: Entry
        self.control_loop_thread = None  # type: Thread
        self.currebt_gui_tooltip_window = None  # type: Toplevel

    def btn_choose_folder_clicked(self):
        self.protocol_root_dir = tkinter.filedialog.askdirectory()
        self.combo_box_protocol_update()

    def init_gui_controllers(self):
        # choose folder region.
        self.label_choose_folder = Label(master=self.root,
                                         text='Choose folder')
        self.label_choose_folder.pack()

        self.btn_choose_folder = Button(master=self.root,
                                        text='Choose Folder...',
                                        command=self.btn_choose_folder_clicked)
        self.btn_choose_folder.pack()

        # protocol list combobox region.
        self.combobox_protocol_list = tkinter.ttk.Combobox(master=self.root)
        self.combobox_protocol_list.bind("<<ComboboxSelected>>",
                                         self.combobox_protocols_item_selected)
        self.combo_box_protocol_update()
        self.combobox_protocol_list.pack()

        # start experiment button region.
        self.btn_start_experiment = Button(master=self.root,
                                           text='Start',
                                           command=self.btn_start_experiment_clicked)
        self.btn_start_experiment.place(relx=0.9,
                                        rely=0.0)

        # num of trials region.
        self.label_num_of_trials = Label(master=self.root,
                                         text='#Trials')
        self.label_num_of_trials.place(relx=0.8,
                                       rely=0.05)
        self.entry_num_of_trials = Entry(master=self.root)
        self.entry_num_of_trials.insert(0, 14)
        self.entry_num_of_trials.place(relx=0.85, rely=0.05)

        # num of repetitionns rehion.
        self.label_num_of_repetitions = Label(master=self.root,
                                              text='#repetitions')
        self.label_num_of_repetitions.place(relx=0.8,
                                            rely=0.1)
        self.entry_num_of_repetitions = Entry(master=self.root)
        self.entry_num_of_repetitions.insert(0, 1)
        self.entry_num_of_repetitions.place(relx=0.85, rely=0.1)

        # backword error probability region.
        self.label_backward_error_probability = Label(master=self.root,
                                                      text='#b.e.p')
        self.label_backward_error_probability.place(relx=0.8,
                                                    rely=0.15)
        self.entry_backward_error_probability = Entry(master=self.root)
        self.entry_backward_error_probability.insert(0, 1)
        self.entry_backward_error_probability.place(relx=0.85, rely=0.15)

        # forward rightward probability.
        self.label_forward_rightward_probability = Label(master=self.root,
                                                         text='#f.r.p')
        self.label_forward_rightward_probability.place(relx=0.8,
                                                       rely=0.2)
        self.entry_forward_rightward_probability = Entry(master=self.root)
        self.entry_forward_rightward_probability.insert(0, 1)
        self.entry_forward_rightward_probability.place(relx=0.85, rely=0.2)

    def btn_start_experiment_clicked(self):
        self.control_loop_thread = Thread(target=self.control_loop_function, args=())
        self.control_loop_thread.start()
        return

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
                                     name='label_' + key_param_name,
                                     text=key_param_name)
            param_label_name.place(relx=rel_x[0], rely=rel_y[0])
            self.dynamic_controls_dict['label_' + key_param_name] = param_label_name
            rel_x[0] += 0.1
            self.dynamic_controls_dict['label_' + key_param_name].bind('<Enter>', self.show_param_label_tooltip)
            self.dynamic_controls_dict['label_' + key_param_name].bind('<Leave>', self.hide_param_label_tooltip)

            for key_param_attribute in titles:
                if key_param_attribute == 'tool_tip' or \
                        key_param_attribute == 'param_name':
                    continue

                dynamic_entry_name = key_param_attribute + '_' + key_param_name
                if key_param_attribute == 'paramtype':
                    param_combobox = tkinter.ttk.Combobox(master=self.root,
                                                          name=dynamic_entry_name)
                    param_combobox['values'] = ['static', 'choice', 'constvec', 'acrosstair', 'withinstair']
                    param_combobox.place(relx=rel_x[0], rely=rel_y[0])
                    param_combobox.set(data_dict[key_param_name][key_param_attribute])
                    self.dynamic_controls_dict[dynamic_entry_name] = param_combobox
                    self.dynamic_controls_dict[dynamic_entry_name].bind('<<ComboboxSelected>>',
                                                                        self.on_dynamic_combobox_item_selected)
                else:
                    param_entry_value = Entry(master=self.root,
                                              name=dynamic_entry_name)
                    param_entry_value.insert(0, data_dict[key_param_name][key_param_attribute])
                    param_entry_value.place(relx=rel_x[0], rely=rel_y[0])
                    self.dynamic_controls_dict[dynamic_entry_name] = param_entry_value
                    self.dynamic_controls_dict[dynamic_entry_name].bind('<Leave>', self.on_dynamic_entry_leave)

                rel_x[0] += 0.1

            rel_x[0] = 0.0
            rel_y[0] += 0.04

        self.freeze_all_dynamic_entries_by_combobox_status()

    def delete_dynamic_controls(self):
        for control in self.dynamic_controls_dict.values():
            control.destroy()
        self.dynamic_controls_dict.clear()

    def update_dynamic_controls(self):
        self.delete_dynamic_controls()
        [excel_data_dict, titles] = self.protocol_reader.read_file(self.protocol_file_path)
        self.parameters_attributes_dictionary = excel_data_dict
        rel_x = [0.0]
        rel_y = [0.1]

        # for titles labels
        self.add_parameters_titles(titles, rel_x, rel_y)

        # for other attributes
        self.add_parameters_attributes(titles, excel_data_dict, rel_x, rel_y)

    def show_param_label_tooltip(self, event):
        label_name = event.widget._name
        param_name = label_name.split('_')[1]
        tool_tip_text = self.parameters_attributes_dictionary[param_name]['tool_tip']

        x = event.widget.winfo_rootx() + 25
        y = event.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.currebt_gui_tooltip_window = tkinter.Toplevel(event.widget)
        # Leaves only the label and removes the app window
        self.currebt_gui_tooltip_window.wm_overrideredirect(True)
        self.currebt_gui_tooltip_window.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.currebt_gui_tooltip_window, text=tool_tip_text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1)
        label.pack()
        pass

    def hide_param_label_tooltip(self, event):
        label_name = event.widget._name
        param_name = label_name.split('_')[1]
        self.currebt_gui_tooltip_window.destroy()
        pass

    def on_dynamic_combobox_item_selected(self, event):
        dynamic_entry_name = event.widget._name
        [key_param_attribute, key_param_name] = dynamic_entry_name.split('_')
        self.parameters_attributes_dictionary[key_param_name][key_param_attribute] = event.widget.get()
        param_status = event.widget.get()

        self.freeze_dynamic_entries_by_combobox_status(key_param_name, param_status)
        pass

    def on_dynamic_entry_leave(self, event):
        dynamic_entry_name = event.widget._name
        [key_param_attribute, key_param_name] = dynamic_entry_name.split('_')
        self.parameters_attributes_dictionary[key_param_name][key_param_attribute] = event.widget.get()
        pass

    def freeze_all_dynamic_entries_by_combobox_status(self):
        for key_param_name in self.parameters_attributes_dictionary.keys():
            self.freeze_dynamic_entries_by_combobox_status(key_param_name, self.dynamic_controls_dict[
                'paramtype_' + key_param_name].get())
        pass

    def freeze_dynamic_entries_by_combobox_status(self, key_param_name, status):
        if status == 'static':
            self.dynamic_controls_dict['value_' + key_param_name].config(state='normal')
            self.dynamic_controls_dict['minvalue_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['jumping_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['maxvalue_' + key_param_name].config(state='disabled')
        elif status == 'varying' or status == 'acrosstair' or status == 'withinstair':
            self.dynamic_controls_dict['value_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['minvalue_' + key_param_name].config(state='normal')
            self.dynamic_controls_dict['jumping_' + key_param_name].config(state='normal')
            self.dynamic_controls_dict['maxvalue_' + key_param_name].config(state='normal')
        pass

    def show_message_box(self, message):
        tkinter.messagebox.showinfo(message)
        pass

    def load(self):
        self.root = tkinter.Tk()
        self.root.geometry("1400x800")
        self.root.protocol('WM_DELETE_WINDOW', self.exit_window_clicked)

        self.control_loop = ControlLoop()

        self.init_gui_controllers()

        self.protocol_reader = ProtocolReader()
        self.protocol_reader.read_file(self.protocol_file_path)

        self.dynamic_controls_dict = {}

        tkinter.messagebox.showinfo('Hello python', 'Hello World')
        self.root.mainloop()

    def exit_window_clicked(self):
        # wait the current trial to be finished
        # and then close the window in the control loop.
        self.control_loop.exit_experiment = True
        if self.control_loop_thread is not None:
            self.control_loop_thread.join()
        self.root.destroy()
        pass

    def control_loop_function(self):
        experiment_data = ExperimentData(num_of_repetitions=int(self.entry_num_of_repetitions.get()),
                                         num_of_trials=int(self.entry_num_of_trials.get()),
                                         backward_error_probability=float(self.entry_backward_error_probability.get()),
                                         forward_rightward_probability=float(
                                             self.entry_forward_rightward_probability.get()))
        self.control_loop.start(attributes=self.parameters_attributes_dictionary,
                                experiment_data=experiment_data)
