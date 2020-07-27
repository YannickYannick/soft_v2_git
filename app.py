#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:20:56 2020

Main tk window for the repeated flash experiment GUI

@author: melinapannier
"""

import tkinter as tk
from tkinter import ttk
from frames import Oven, Oscilloscope, Sample, Laser
import acquisition.get_datas
# from communication.pico9000 import CommunicationPicoscope
# from communication.laser import CommunicationLaser
# from communication.oven import CommunicationOven

COLOR_LIGHT_BACKGROUND = "#D3E2F1"
COLOR_DARK_BACKGROUND = "#2e3f4f"
COLOR_TITLE = "#2e3f4f"
COLOR_ACTIVE_BACKGROUND = "#86C0F5"
COLOR_PRESSED_BACKGROUND = "#4390D5"

class RepeatedFlashExperiment(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      
        self.title("Repeated Flash Experiment")
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
        
        
                
        
        header = ttk.Frame(self, 
                           padding=10, 
                           style="Frame.TFrame",
                           )
        header.grid(row=0, column=0, 
                       sticky="NSEW")
        header.columnconfigure((1,3,5,6), weight=1)
        
        
        operator_label = ttk.Label(header, 
                                   text="Operator : ",
                                   style="Label.TLabel"
                                   )
        operator_label.grid(row=0, column=0,
                            sticky="NSW"
                            )
        
        self.operator_value = tk.StringVar()
        operator_input = ttk.Entry(header, 
                                   textvariable=self.operator_value,
                                   #style="Label.TLabel"
                                   )
        operator_input.grid(row=0, column=1,
                            sticky="NSEW"
                            )
        
        
        file_name_label = ttk.Label(header, 
                                   text="File Name : ",
                                   style="Label.TLabel"
                                   )
        file_name_label.grid(row=0, column=2,
                            sticky="NSW"
                            )
        
        self.file_name_value = tk.StringVar(value='kgflquf')
        file_name_input = ttk.Entry(header, 
                                   textvariable=self.file_name_value,
                                   #style="Label.TLabel"
                                   )
        file_name_input.grid(row=0, column=3,
                            sticky="NSEW"
                            )
        
        
        directory_label = ttk.Label(header, 
                                   text="File Name : ",
                                   style="Label.TLabel"
                                   )
        directory_label.grid(row=0, column=4,
                            sticky="NSW"
                            )
        
        self.directory_value = tk.StringVar(value='dir')
        directory_input = ttk.Entry(header, 
                                   textvariable=self.directory_value,
                                   #style="Label.TLabel"
                                   )
        directory_input.grid(row=0, column=5,
                            sticky="NSEW"
                            )
        
        
        run_button = ttk.Button(header, 
                                text="Run Experiment", 
                                style="Button.TButton", 
                                command=self.run
                                )
        run_button.grid(row=0, column=6,
                        sticky="NSEW"
                        )
        
        
        
        
        
        container = ttk.Frame(self, 
                              padding=10, 
                              style="MainContainer.TFrame",
                              )
        container.grid(row=1, column=0, 
                       sticky="NSEW")
        container.rowconfigure((0,1), weight=1)
        container.columnconfigure((0,1), weight=1)
        
        #self.communication_oven = CommunicationOven(self)
        self.oven_frame = Oven(container, self)   
        self.oven_frame.grid(row=0, column=0)
        
        #self.communication_picoscope = CommunicationPicoscope(self)
        self.oscilloscope_frame = Oscilloscope(container, self)   
        self.oscilloscope_frame.grid(row=0, column=1)
        
        # self.communication_laser = CommunicationLaser(self)
        self.laser_frame = Laser(container, self) 
        self.laser_frame.grid(row=1, column=0)
        
        
        self.sample_frame = Sample(container)  
        self.sample_frame.grid(row=1, column=1)
        

        for child in container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]='Frame.TFrame'
            child["padding"]=10
            
        self.time = 0
            
    #     self.protocol('WM_DELETE_WINDOW',  self.close_window)
        
    # def close_window(self):
    #     self.communication_oven.arduino_I2C.close()
        
    #     self.destroy()
    
    
    def timer(self):
        self.time += 1
        print(self.time)
        self._timer= self.after(1000, self.timer)
        
        
    def get_results(self):        
        """time ; setpoint ; temperature ; power ; repetition rate ; pulse rate ; frequency ; magnitude ; y  \n"""
        # temperature = self.communication_oven.real_temperaturee
        # power = self.communication_oven.
        # repetition_rate = self.communication_laser.
        # pulse_rate = self.communication_laser.
        # frequency = self.communication_laser.frequency
        # magnitude = self.communication_laser.
        # y = self.communication_picoscope
        time = self.time
        results_data = [time]
        return results_data
    
    def write_results(self):
        file_name = self. file_name_value.get()
        acquisition.get_datas.save_results(file_name, self.get_results())
        self.after(1000, self.write_results)
        
    def run(self):
        oven_data = self.oven_frame.get_data()
        oscilloscope_data = self.oscilloscope_frame.right_container.get_data()
        laser_data = self.laser_frame.left_container.get_data()
        sample_data = self.sample_frame.left_container.get_data()
        
        file_name = self. file_name_value.get()
        operator = self.operator_value.get()
        
        acquisition.get_datas.save_data(file_name, operator, oven_data, oscilloscope_data, laser_data, sample_data)
        
        self.timer()
        self.write_results()
        

    
   
app = RepeatedFlashExperiment()


style = ttk.Style()
style.theme_use("clam")

style.configure("MainContainer.TFrame", 
                background=COLOR_DARK_BACKGROUND
                )
style.configure("Frame.TFrame", 
                background=COLOR_LIGHT_BACKGROUND
                )
style.configure("Title.TLabel", 
                foreground=COLOR_TITLE, 
                background=COLOR_LIGHT_BACKGROUND, 
                font="Helvetica 20 bold"
                )
style.configure("Label.TLabel", 
                background=COLOR_LIGHT_BACKGROUND
                )
style.configure("LabelCurrentTemperature.TLabel", 
                background='red'
                )
style.configure("LabelTemperature.TLabel", 
                background='white'
                )
style.configure("Label.TLabelframe.Label", 
                background=COLOR_LIGHT_BACKGROUND,
                foreground=COLOR_DARK_BACKGROUND
                )
style.configure("Label.TLabelframe", 
                background=COLOR_LIGHT_BACKGROUND,
                labeloutside=False,
                labelmargins=10
                )
style.configure("Radiobutton.TRadiobutton", 
                background=COLOR_LIGHT_BACKGROUND
                )
style.configure("Button.TButton",
                background=COLOR_LIGHT_BACKGROUND,
                foreground=COLOR_DARK_BACKGROUND,
                font="Helvetica 14 bold"
                )
style.map("Button.TButton",
          background=[('pressed', COLOR_PRESSED_BACKGROUND), 
                      ('active', COLOR_ACTIVE_BACKGROUND)]
          )
style.configure("Checkbutton.TCheckbutton",
                background=COLOR_LIGHT_BACKGROUND,
                )

app.mainloop()

