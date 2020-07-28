#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:40:24 2020

tk frames and tk subframes related to the oscilloscope for the repeated flash 
experiment GUI

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk

import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from communication.pico9000 import CommunicationPicoscope


import numpy as np


class Oscilloscope(ttk.Frame):
    def __init__(self, container, main_frame, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
    
        self.main_frame = main_frame
        self.update_val  = 0
        
        self.title_label = ttk.Label(self, 
                                     text="OSCILLOSCOPE CONTROL",
                                     style="Title.TLabel"
                                     )
        self.title_label.grid(row=0, column=0, sticky="W")
        
        
        sub_container = ttk.Frame(self,
                                   padding=10,
                                   style='Frame.TFrame'
                                   )
        sub_container.grid(row=1, column=0, sticky="NSEW")       
        sub_container.rowconfigure((0), weight=1)
        sub_container.columnconfigure((0,1), weight=1)
        
        
        left_container = LeftContainer(sub_container, self)
        left_container.grid(row=0, column=0)
        
        
        self.right_container = RightContainer(sub_container, self)
        self.right_container.grid(row=0, column=1)

        
        for child in sub_container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]='Frame.TFrame'
            #child["padding"]=10
        

class LeftContainer(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        
        self.controller = controller
        
        height = 1.5 * 2
        width = 1.5 * 3

        self.fig = Figure(figsize=(width, height), dpi=100)

        
        
        canvas = FigureCanvasTkAgg(self.fig, master=self) 
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        
        self.fig.ani = animation.FuncAnimation(self.fig, self.get_data, interval=100)
        
    def get_data(self, *args):
        self.fig.add_subplot(111).clear()
        x = range(512)
        y = self.controller.main_frame.communication_picoscope.data
        self.fig.add_subplot(111).plot(x, y)
        return y 
        
        
        
class RightContainer(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        
        self.controller = controller
        
        
        dialogue_box_container= ttk.LabelFrame(self, 
                                               padding=10, 
                                               text="Dialogue Box",
                                               style="Label.TLabelframe"
                                               )
        dialogue_box_container.grid(row=0, column=0)        
        dialogue_value = tk.StringVar()
        dialogue_box = ttk.Label(dialogue_box_container, 
                                 textvariable=dialogue_value,
                                 style="Label.TLabel"
                                 )
        dialogue_box.grid(row=0, column=0)
        
        
        self.oscilloscope_selection = tk.StringVar()
        oscillo1 = ttk.Radiobutton(
            self, 
            text="Picoscope 2204A", 
            variable=self.oscilloscope_selection, 
            value="pico1",
            style="Radiobutton.TRadiobutton",
            command = self.picoscope_2000)

        oscillo1.grid(column=0, row=1)
        
        oscillo2 = ttk.Radiobutton(
            self, 
            text="Picoscope 9000", 
            variable=self.oscilloscope_selection, 
            value="pico2",
            style="Radiobutton.TRadiobutton",
            command = self.picoscope_9000)

        oscillo2.grid(column=0, row=2)
        
        
        
        spinbox_container= ttk.Frame(self, padding=10, 
                                     style="Frame.TFrame")
        spinbox_container.grid(row=3, column=0)
        spinbox_container.rowconfigure((0,1,2,3), weight=1)
        spinbox_container.columnconfigure((0,1), weight=1)
        
        
        time_scale_label = ttk.Label(spinbox_container, text="Time Scale", 
                                     style="Label.TLabel")
        time_scale_label.grid(column=0, row=0)
               
        self.time_scale_value = tk.StringVar()
        time_scale_input = ttk.Spinbox(
            spinbox_container,
            from_=0,
            to=120,
            increment=1,
            justify="center",
            textvariable=self.time_scale_value,
            width=10,
        )
        time_scale_input.grid(column=1, row=0, sticky="NESW")
        time_scale_input.bind('<KeyRelease>',self.entry_in_timespinbox)
        
        self.average_state = tk.IntVar()
        average_checkbutton = ttk.Checkbutton(spinbox_container, 
                                  text="Average", 
                                  style="Checkbutton.TCheckbutton",
                                  variable=self.average_state
                                  ) 
        average_checkbutton.grid(column=0, row=1)
        
        
        self.average_value = tk.IntVar()
        self.average_value_str = tk.StringVar()
        self.average_value_before = tk.StringVar(value=0)
        average_display = ttk.Label(spinbox_container, 
                                    textvariable=self.average_value_str, 
                                    ) 
        average_display.grid(column=1, row=1)
        
        average_scale = ttk.Scale(self, 
                                  orient="horizontal", 
                                  from_=0, 
                                  to=10000, 
                                  variable = self.average_value
                                  )
        average_scale.grid(row=4, column=0)
        average_scale.bind('<Motion>',self.motion_in_scale)
        
#        self.reglage_1 = self.controller.main_frame.communication_picoscope.picoscope_properties["self.average"] 
       
        for child in spinbox_container.winfo_children():
            child.grid_configure(padx=5, pady=5,
                                 sticky="NSEW")
            
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5,
                                 sticky="NSEW")

    def picoscope_9000(self):
        print("initializing picoscope_9000")
        self.controller.main_frame.communication_picoscope.initialisation_picoscope_9001 += 10
        print("variable = ok")
        self.controller.main_frame.communication_picoscope.initialisation_picoscope_9000()
        
    def picoscope_2000(self):
        print("initializing picoscope_2000")
        self.controller.main_frame.communication_picoscope.initialisation_picoscope_2000()

    def motion_in_scale(self,event):
        if self.average_state.get() == 1 :
            received_average = self.average_value.get()
            self.average_value_str.set(str(received_average))
            self.controller.main_frame.communication_picoscope.picoscope_properties["self.average"]=received_average
     
        
    def entry_in_timespinbox(self,event):
        received_time_scale = self.time_scale_value.get()
        self.update_val  = 1
        self.controller.main_frame.communication_picoscope.picoscope_properties["self.time_scale"]=received_time_scale #passer la commande à comm Oscillo

        
    def get_data(self):
        self.data = [self.average_value.get(),
                     self.time_scale_value.get(),
                     self.oscilloscope_selection.get()
                     ]
        return self.data
