#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:21:41 2020

tk frames and tk subframes related to the oven for the repeated flash 
experiment GUI

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk


class Laser(ttk.Frame):
    def __init__(self, container,main_app, **kwargs):
        super().__init__(container,**kwargs)
        
        self.main_app = main_app
   
        self.new_commands_list = ""
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
        
        self.title_label = ttk.Label(self, 
                                     text="LASER CONTROL",
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
        
        
        self.left_container = LeftContainer(sub_container)
        self.left_container.grid(row=0, column=0)
        
        
        self.right_container = RightContainer(sub_container, self)
        self.right_container.grid(row=0, column=1)
        
        
        for child in sub_container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]="Frame.TFrame"
        

        
class LeftContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0,1,2,3,4), weight=1)
        self.columnconfigure((1), weight=1)
        
        
        mode_label = ttk.Label(self, text="Mode : ")
        mode_label.grid(row=0, column=0)
        self.mode_value = tk.StringVar()
        mode = ttk.Combobox(self, 
                            textvariable=self.mode_value)
        mode["values"] = ("Burst", "Continued")
        mode.grid(row=0, column=1)
        
        
        repetition_rate_label = ttk.Label(self, text="Répétition Rate : ")
        repetition_rate_label.grid(row=1, column=0)
        self.repetition_rate_value = tk.StringVar()
        repetition_rate = ttk.Combobox(self, 
                                      textvariable=self.repetition_rate_value)
        repetition_rate["values"] = ("0", "1000","15000","20000","30000",)
        repetition_rate.grid(row=1, column=1)
        
        
        burst_label = ttk.Label(self, text="Burst Rate (kHz): ")
        burst_label.grid(row=2, column=0)
        self.burst_value = tk.StringVar()
        self.burst = ttk.Combobox(self, 
                             textvariable=self.burst_value)
        self.burst["values"] = ("0", "100", "200", "400", "800", "16700000")
        self.burst.grid(row=2, column=1)
        
        
        frequency_label = ttk.Label(self, text="Frequency (kHz): ")
        frequency_label.grid(row=3, column=0)
        self.frequency_value = tk.StringVar()
        frequency = ttk.Combobox(self, 
                                 textvariable=self.frequency_value)
        frequency["values"] = ("0", "3", "7", "10")
        frequency.grid(row=3, column=1)
        
        
        magnitude_label = ttk.Label(self, text="Magnitude (%): ")
        magnitude_label.grid(row=4, column=0)
        self.magnitude_value = tk.StringVar()
        magnitude = ttk.Combobox(self, 
                                 textvariable=self.magnitude_value)
        magnitude["values"] = ("0", "20", "50", "70", "100")
        magnitude.grid(row=4, column=1)
        
        
        for child in self.winfo_children():
            if isinstance(child, tk.ttk.Label) == True :
                child.grid_configure(sticky="W")
                child["style"]='Label.TLabel'
            if isinstance(child, tk.ttk.Combobox) == True :
                child.grid_configure(sticky="EW")
        
        
        self.data = []
        
    def get_data(self):
        self.data = [self.mode_value.get(),
                     self.repetition_rate_value.get(),
                     self.burst_value.get(),
                     self.frequency_value.get(),
                     self.magnitude_value.get()
                     ]
        return self.data
        
                
class RightContainer(ttk.Frame):
    def __init__(self, container, laser_frame, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        
        self.laser_frame = laser_frame
        # self.laser_properties = self.laser_frame.main_app.communication_laser.laser_properties.copy() #{"self.state":0, "self.mode":0, "self.current_mode" : 0, "self.pulse_rate" : 0, "self.repetition_rate" : 0, "self.burst_rate" : 0, "self.current_intensity_p":0, "self.light":0}
        # self.laser_properties = self.laser_frame.main_app.communication_laser.laser_properties.copy() #{"self.state":0, "self.mode":0, "self.current_mode" : 0, "self.burst_rate" : 0, "self.repetition_rate" : 0, "self.burst_rate" : 0, "self.current_intensity_p":0, "self.light":0}
        # self.laser_commands = self.laser_frame.main_app.communication_laser.laser_commands.copy()
        
        
        dialogue_box_container= ttk.LabelFrame(self, 
                                               padding=10, 
                                               text="Dialogue Box",
                                               style="Label.TLabelframe"
                                               )
        dialogue_box_container.grid(row=0, column=0,
                                    columnspan=2,
                                    sticky="NSEW"
                                    )        
        dialogue_value = tk.StringVar()
        dialogue_box = ttk.Label(dialogue_box_container, 
                                 textvariable=dialogue_value,
                                 style="Label.TLabel"
                                 )
        dialogue_box.grid(row=0, column=0)
        
        
        validation_button = ttk.Button(self, 
                                 text="Validate", 
                                 padding=10, 
                                 style="Button.TButton",
                                 #command = self.validate
                                 )
        validation_button.grid(row=1, column=0)
        
        
        self.pause_button = ttk.Button(self, 
                                 text="Pause", 
                                 padding=10, 
                                 style="Button.TButton",
                                 command=self.pause
                                 )
        self.pause_button.grid(row=1, column=1)
        
        self.play_button = ttk.Button(self, 
                                 text="Play", 
                                 padding=10, 
                                 style="Button.TButton",
                                 command=self.play
                                 )
        self.play_button.grid(row=1, column=1)
        
    
        
    def pause(self):
        self.play_button.tkraise()
        
    def play(self):
        self.pause_button.tkraise()
        
        
    # def mode(self, i): # peut-être interessant si on veut utiliser les 9 modes du laser (y->m)
    #     switcher={"Burst":'4', "Continued":'1'}
    #     return switcher.get(i,"Invalid day of week")
    
#     def validate(self): # Bouton gris tant que tous les champs ne sont pas remplis (y->m)
#         # désactive les autres champs pendant 6 secondes (y->m) 
#         self.state = self.laser_frame.left_container.mode.get()   
#         self.state = self.mode(self.state)
        
#         self.laser_properties["self.state"] = self.laser_frame.main_app.communication_laser.laser_properties["self.state"]
#         self.laser_properties["self.mode"] = self.state
#         self.laser_properties["self.current_mode"] = 0 # voir si ce mode est compatible avec burst et continuous (y->y)
#         self.laser_properties["self.pulse_rate"] = self.laser_frame.left_container.pulse.get() 
#         self.aa = self.laser_frame.left_container.repetition_rate.get() 
#         self.laser_properties["self.burst_rate"] = self.laser_frame.left_container.burst.get() 
#         self.aa = self.laser_frame.left_container.repetition_rate_value.get() 
#         self.laser_properties["self.repetition_rate"] = self.aa
#         self.laser_properties["self.burst_rate"] = 0
#         self.laser_properties["self.current_intensity_p"] = self.laser_frame.left_container.magnitude_value.get() 
#         self.laser_properties["self.light"] = 0 #bouton play/pause
        
#         print(self.laser_properties)
#         for key,value in self.laser_properties.items():
       
#             print (1,self.laser_properties[key])
#             print(2,self.laser_frame.main_app.communication_laser.laser_properties[key])
#             if self.laser_properties[key] != self.laser_frame.main_app.communication_laser.laser_properties[key]:
#                 print(key,self.laser_properties[key])
#                 self.laser_frame.new_commands_list += self.laser_commands[key] + self.laser_properties[key] + ";"
#                 self.laser_frame.main_app.communication_laser.new_commands_list = self.laser_frame.new_commands_list
#                 self.laser_frame.main_app.communication_laser.laser_properties[key] = self.laser_properties[key]
#         self.laser_frame.main_app.communication_laser.new_commands_list = self.laser_frame.new_commands_list
#         self.laser_frame.main_app.communication_laser.consigne()
        
#         #consigne & consigne_before = elles servent à rien ces assignations, c'est juste pour ne pas se perdre (y->m)
        
#         self.consigne = self.laser_properties
#         self.consigne_before = self.laser_frame.main_app.communication_laser.laser_properties


# #        


# #        for x_values, y_values in zip(self.consigne.items(), self.consigne_before.items()):       
# #            if x_values == y_values:
# #                print(1,x_values)
# #                print(2,y_values)
# #                pass
# #            else:
# #                print(3,x_values)
# #                print(4,y_values)
# #                self.laser_frame.new_commands_list += str(x_values)
#         print ("new_commands_list =",self.laser_frame.new_commands_list)

#         self.laser_frame.new_commands_list = ''


# #        self.laser_frame.main_app.communication_laser.laser_properties = self.laser_properties
             
                
# #        self.consigne_before = self.consigne
