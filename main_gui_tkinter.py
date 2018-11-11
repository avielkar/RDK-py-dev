# coding: utf-8
import os

import tkinter
import tkinter.ttk
import win32api
import win32process
from tkinter import Tk, Toplevel, Label, Checkbutton, BooleanVar, Entry, Button
from tkinter import Label, Button, Entry
import tkinter.filedialog

from protocolreader import ProtocolReader
from protocolwriter import ProtocolWriter
from controlloop import ControlLoop
import tkinter.messagebox
from threading import Thread
from experimentdata import ExperimentData
from tkinter import BooleanVar
import queue


class MainGuiTkinter:

    def __init__(self, graph_maker_command_queue):
        self.tkFileDialog = None
        self.protocol_reader = None  # type: ProtocolReader
        self.protocol_writer = None  # type:ProtocolWriter
        self.control_loop = None  # type: ControlLoop
        self.root = None  # type: Tk
        self.protocol_file_path = 'D:\RDK-protocols\coherence.xlsx'
        self.label_choose_folder = None  # type: Label
        self.btn_choose_folder = None  # type: Button
        self.protocol_root_dir = 'D:\RDK-protocols'  # type: object
        self.combobox_protocol_list = None  # type: Combobox
        self.btn_start_experiment = None  # type: Button
        self.btn_stop_experiment = None  # type: Button
        self.dynamic_controls_dict = None  # type: Dict[Any, Any]
        self.parameters_attributes_dictionary = None  # type: Dict[Any,Any]
        self.label_num_of_repetitions = None  # type: Label
        self.label_num_of_trials = None  # type: Label
        self.label_backward_error_probability: Label
        self.label_forward_rightward_probability: Label
        self.entry_num_of_repetitions = None  # type: Entry
        self.entry_num_of_trials = None  # type: Entry
        self.control_loop_thread = None  # type: Thread
        self.current_gui_tooltip_window = None  # type: Toplevel
        self.checkbox_confidence_choice = None  # type:Checkbutton
        self.confidence_choice_value = None  # type: BooleanVar
        self.draw_fixation_point_value = None  # type:BooleanVar
        self.label_save_protocol_name = None  # type: Label
        self.entry_save_protocol_name = None  # type: Entry
        self.combobox_user_name_list = None  # type: Combobox
        self.label_user_name = None  # type: Label
        self.gui_queue = queue.Queue()
        self.control_loop_queue = queue.Queue()
        self.graph_maker_command_queue = graph_maker_command_queue
        self.btn_save_protocol = None  # type: Button
        self.label_screen_height_size = None  # type:Label
        self.label_screen_width_size = None  # type:Label
        self.entry_screen_width_size = None  # type: Button
        self.entry_screen_height_size = None  # type: Button

        win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_NORMAL)

    def btn_choose_folder_clicked(self):
        self.protocol_root_dir = tkinter.filedialog.askdirectory()
        self.combo_box_protocol_update()

    def init_gui_controllers(self):
        # screen size region.
        self.label_screen_width_size = Label(master=self.root,
                                             text='ScreenWidth (pixels)')
        self.label_screen_width_size.place(relx=0.0,
                                           rely=0.0)
        self.entry_screen_width_size = Entry(master=self.root)
        self.entry_screen_width_size.insert(0,1920)
        self.entry_screen_width_size.place(relx=0.09,
                                           rely=0.0)

        self.label_screen_height_size = Label(master=self.root,
                                              text='ScreenHeight (pixels)')
        self.label_screen_height_size.place(relx=0.0,
                                            rely=0.05)
        self.entry_screen_height_size = Entry(master=self.root)
        self.entry_screen_height_size.place(relx=0.09,
                                            rely=0.05)
        self.entry_screen_height_size.insert(0,1080)

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

        # save protocol region.
        self.btn_save_protocol = Button(master=self.root,
                                        text='Save Protocol',
                                        command=self.btn_save_protocol_clicked)
        self.btn_save_protocol.place(relx=0.6,
                                     rely=0.05)
        self.label_save_protocol_name = Label(master=self.root,
                                              text='New Protocol Name:')
        self.label_save_protocol_name.place(relx=0.6,
                                            rely=0.00)
        self.entry_save_protocol_name = Entry(master=self.root)
        self.entry_save_protocol_name.place(relx=0.7,
                                            rely=0.0)

        # start experiment button region.
        self.btn_start_experiment = Button(master=self.root,
                                           text='Start',
                                           command=self.btn_start_experiment_clicked)
        self.btn_start_experiment.place(relx=0.9,
                                        rely=0.0)

        # stop experiment button region.
        self.btn_stop_experiment = Button(master=self.root,
                                          text='Stop',
                                          command=self.btn_stop_experiment_clicked,
                                          state='disabled')
        self.btn_stop_experiment.place(relx=0.95,
                                       rely=0.0)

        # num of trials region.
        self.label_num_of_trials = Label(master=self.root,
                                         text='#Trials')
        self.label_num_of_trials.place(relx=0.8,
                                       rely=0.05)
        self.entry_num_of_trials = Entry(master=self.root)
        self.entry_num_of_trials.insert(0, 14)
        self.entry_num_of_trials.place(relx=0.85, rely=0.05)

        # num of repetitionns region.
        self.label_num_of_repetitions = Label(master=self.root,
                                              text='#repetitions')
        self.label_num_of_repetitions.place(relx=0.8,
                                            rely=0.1)
        self.entry_num_of_repetitions = Entry(master=self.root)
        self.entry_num_of_repetitions.insert(0, 1)
        self.entry_num_of_repetitions.place(relx=0.85, rely=0.1)

        # backword error probability region.
        self.label_backward_error_probability = Label(master=self.root,
                                                      text='#P.Down')
        self.label_backward_error_probability.place(relx=0.8,
                                                    rely=0.15)
        self.entry_backward_error_probability = Entry(master=self.root)
        self.entry_backward_error_probability.insert(0, 1)
        self.entry_backward_error_probability.place(relx=0.85, rely=0.15)

        # forward rightward probability.
        self.label_forward_rightward_probability = Label(master=self.root,
                                                         text='#P.Up')
        self.label_forward_rightward_probability.place(relx=0.8,
                                                       rely=0.2)
        self.entry_forward_rightward_probability = Entry(master=self.root)
        self.entry_forward_rightward_probability.insert(0, 1)
        self.entry_forward_rightward_probability.place(relx=0.85, rely=0.2)

        # checkbox confidence region.
        self.confidence_choice_value = BooleanVar()
        self.checkbox_confidence_choice = tkinter.Checkbutton(master=self.root,
                                                              text='Confidence Choice',
                                                              variable=self.confidence_choice_value)
        self.checkbox_confidence_choice.place(relx=0.7, rely=0.7)

        # draw_fixation_point region.
        self.draw_fixation_point_value = BooleanVar()
        self.checkbox_draw_fixation_point = tkinter.Checkbutton(master=self.root,
                                                                text='Draw F.P',
                                                                variable=self.draw_fixation_point_value)
        self.checkbox_draw_fixation_point.place(relx=0.7, rely=0.75)

        # user name region.
        self.label_user_name = Label(master=self.root, text='User Name:')
        self.label_user_name.place(relx=0.65, rely=0.1)

        self.combobox_user_name_list = tkinter.ttk.Combobox(master=self.root)
        self.combobox_user_name_list_initialize()
        self.combobox_user_name_list.place(relx=0.7, rely=0.1)

    def btn_start_experiment_clicked(self):
        if self.combobox_user_name_list.get() == '':
            tkinter.messagebox.showinfo('Error', 'Should choose user name !!!!')
        else:
            self.btn_start_experiment.config(state='disabled')
            self.btn_stop_experiment.config(state='norm')
            self.update_parameter_dictionary_according_to_gui()
            self.control_loop_function()
        return

    def btn_stop_experiment_clicked(self):
        # self.btn_start_experiment.config(state='normal')
        self.control_loop.stop_experiment = True

    def combo_box_protocol_update(self):
        if self.protocol_root_dir != '':
            self.combobox_protocol_list['values'] = [f for f in os.listdir(self.protocol_root_dir) if
                                                     f.endswith('.xlsx')]
        else:
            self.combobox_protocol_list['values'] = list()

    def combobox_protocols_item_selected(self, event_args):
        self.protocol_file_path = self.protocol_root_dir + '/' + self.combobox_protocol_list.get()
        self.update_dynamic_controls()

    def btn_save_protocol_clicked(self):
        self.update_parameter_dictionary_according_to_gui()
        if not self.protocol_writer.write_file(self.protocol_root_dir, self.entry_save_protocol_name.get(),
                                               self.parameters_attributes_dictionary):
            tkinter.messagebox.showinfo('Error', 'File name already exists in this directory')
        pass

    def add_parameters_titles(self, titles, rel_x, rel_y):
        for title in titles:
            if title != 'tool_tip':
                title_label = Label(master=self.root,
                                    text=title)
                title_label.place(relx=rel_x[0], rely=rel_y[0])
                rel_x[0] += 0.08

        rel_x[0] = 0.0
        rel_y[0] += 0.04

    def add_parameters_attributes(self, titles, data_dict, rel_x, rel_y):
        for key_param_name in data_dict:
            param_label_name = Label(master=self.root,
                                     name='label_' + key_param_name,
                                     text=key_param_name,
                                     width=14)
            param_label_name.place(relx=rel_x[0], rely=rel_y[0])
            self.dynamic_controls_dict['label_' + key_param_name] = param_label_name
            rel_x[0] += 0.08
            self.dynamic_controls_dict['label_' + key_param_name].bind('<Enter>', self.show_param_label_tooltip)
            self.dynamic_controls_dict['label_' + key_param_name].bind('<Leave>', self.hide_param_label_tooltip)

            for key_param_attribute in titles:
                if key_param_attribute == 'tool_tip' or \
                        key_param_attribute == 'param_name':
                    continue

                dynamic_entry_name = key_param_attribute + '_' + key_param_name
                if key_param_attribute == 'paramtype':
                    param_combobox = tkinter.ttk.Combobox(master=self.root,
                                                          name=dynamic_entry_name,
                                                          width=14)
                    param_combobox['values'] = ['static', 'choice', 'constvec', 'acrosstair', 'withinstair', 'const']
                    param_combobox.place(relx=rel_x[0], rely=rel_y[0])
                    param_combobox.set(data_dict[key_param_name][key_param_attribute])
                    self.dynamic_controls_dict[dynamic_entry_name] = param_combobox
                    self.dynamic_controls_dict[dynamic_entry_name].bind('<<ComboboxSelected>>',
                                                                        self.on_dynamic_combobox_item_selected)
                else:
                    param_entry_value = Entry(master=self.root,
                                              name=dynamic_entry_name,
                                              width=14)
                    param_entry_value.insert(0, data_dict[key_param_name][key_param_attribute])
                    param_entry_value.place(relx=rel_x[0], rely=rel_y[0])
                    self.dynamic_controls_dict[dynamic_entry_name] = param_entry_value
                    self.dynamic_controls_dict[dynamic_entry_name].bind('<Leave>', self.on_dynamic_entry_leave)

                rel_x[0] += 0.08

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
        self.current_gui_tooltip_window = tkinter.Toplevel(event.widget)
        # Leaves only the label and removes the app window
        self.current_gui_tooltip_window.wm_overrideredirect(True)
        self.current_gui_tooltip_window.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.current_gui_tooltip_window, text=tool_tip_text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1)
        label.pack()
        pass

    def hide_param_label_tooltip(self, event):
        label_name = event.widget._name
        param_name = label_name.split('_')[1]
        self.current_gui_tooltip_window.destroy()
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

    def update_parameter_dictionary_according_to_gui(self):
        for (dynamic_control_name, dynamic_control) in self.dynamic_controls_dict.items():
            if type(dynamic_control) == Entry:
                [key_param_attribute, key_param_name] = dynamic_control_name.split('_')
                self.parameters_attributes_dictionary[key_param_name][key_param_attribute] = dynamic_control.get()

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
        elif status == 'const':
            self.dynamic_controls_dict['value_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['minvalue_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['jumping_' + key_param_name].config(state='disabled')
            self.dynamic_controls_dict['maxvalue_' + key_param_name].config(state='disabled')
        pass

    def combobox_user_name_list_initialize(self):
        self.combobox_user_name_list['values'] = ['Orly', 'Avi',  'NoName']
        self.combobox_user_name_list.current(0)
        pass

    def show_message_box(self, message):
        tkinter.messagebox.showinfo(message)
        pass

    def load(self):
        self.root = tkinter.Tk()
        self.root.geometry("1400x800")
        self.root.protocol('WM_DELETE_WINDOW', self.exit_window_clicked)

        self.control_loop = ControlLoop(self.gui_queue,
                                        self.control_loop_queue,
                                        self.graph_maker_command_queue)

        self.init_gui_controllers()

        self.protocol_reader = ProtocolReader()
        self.protocol_reader.read_file(self.protocol_file_path)

        self.protocol_writer = ProtocolWriter()

        self.dynamic_controls_dict = {}

        tkinter.messagebox.showinfo('Hello python', 'Hello World')
        self.root.after(100, self.after_function)
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
                                             self.entry_forward_rightward_probability.get()),
                                         enable_confidence_choice=self.confidence_choice_value.get(),
                                         draw_fixation_point=self.draw_fixation_point_value.get(),
                                         user_running_experiment_name=self.combobox_user_name_list.get(),
                                         screen_width=self.entry_screen_width_size.get(),
                                         screen_height=self.entry_screen_height_size.get())
        command = 'start'
        command_data = (self.parameters_attributes_dictionary, experiment_data)
        data = (command, command_data)
        self.control_loop_queue.put(data)

    def after_function(self):
        # print('aaa')
        win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_LOWEST)
        while not self.gui_queue.empty():
            name_status = self.gui_queue.get()
            if name_status[0] == 'enable_start_btn':
                self.btn_start_experiment.config(state='disabled' if name_status[1] is False else 'normal')
                tkinter.messagebox.showinfo('Information', 'Experiment ended succesfully !!!!')
                self.combobox_user_name_list.set('')

        self.root.after(100, self.after_function)
        pass
