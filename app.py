#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:20:56 2020

Main tk window for the repeated flash experiment GUI

@author: melinapannier
"""

import tkinter as tk
from tkinter import ttk
from frames import OvenSeparate, Oscilloscope, Sample #,Laser
from communication.pico9000 import CommunicationPicoscope
from communication.laser import CommunicationLaser
from communication.oven import CommunicationOven

COLOR_LIGHT_BACKGROUND = "#D3E2F1"
COLOR_DARK_BACKGROUND = "#2e3f4f"
COLOR_TITLE = "#2e3f4f"
COLOR_ACTIVE_BACKGROUND = "#86C0F5"
COLOR_PRESSED_BACKGROUND = "#4390D5"

class RepeatedFlashExperiment(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      
        self.title("Repeated Flash Experiment")
        
        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)
        
        
        
        container = ttk.Frame(self, 
                              padding=10, 
                              style="MainContainer.TFrame",
                              )
        container.grid(row=0, column=0, 
                       sticky="NSEW")
        container.rowconfigure((0,1), weight=1)
        container.columnconfigure((0,1), weight=1)
        
        self.communication_oven = CommunicationOven(self)
        oven_frame = OvenSeparate(container, self)   
        oven_frame.grid(row=0, column=0)
        
        self.communication_picoscope = CommunicationPicoscope(self)
        oscilloscope_frame = Oscilloscope(container, self)   
        oscilloscope_frame.grid(row=0, column=1)
        
        # self.communication_laser = CommunicationLaser(self)
        # laser_frame = Laser(container, self) 
        # laser_frame.grid(row=1, column=0)
        
        
        sample_frame = Sample(container)  
        sample_frame.grid(row=1, column=1)
        

        for child in container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]='Frame.TFrame'
            child["padding"]=10
            
        self.protocol('WM_DELETE_WINDOW',  self.close_window)
        
    def close_window(self):
        self.communication_oven.arduino_I2C.close()
        
        self.destroy()
   
    
   
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

