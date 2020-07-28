#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:22:24 2020

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Sample(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
        

        self.title_label = ttk.Label(self, 
                                     text="SAMPLE PARAMETRES",
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
        
        
        left_container = LeftContainer(sub_container)
        left_container.grid(row=0, column=0)
        
        
        right_container = RightContainer(sub_container)
        right_container.grid(row=0, column=1)
        
        
        for child in sub_container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]='Frame.TFrame'
            #child["padding"]=10
        

        
class LeftContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0,1,2), weight=1)
        self.rowconfigure((3), weight=3)
        self.columnconfigure((1), weight=1)
        
        
        material_label = ttk.Label(self, text="Material : ")
        material_label.grid(row=0, column=0)
        material_value = tk.StringVar()
        material = ttk.Combobox(self, 
                                textvariable=material_value
                                )
        material["values"] = ("Burst", "Continued")
        material.grid(row=0, column=1)
        
        
        sample_name_label = ttk.Label(self, text="Sample Name : ")
        sample_name_label.grid(row=1, column=0)
        sample_name_value = tk.StringVar()
        sample_name = ttk.Combobox(self, 
                                   textvariable=sample_name_value
                                   )
        sample_name["values"] = ("Burst", "Continued")
        sample_name.grid(row=1, column=1)
        
        
        sample_width_label = ttk.Label(self, text="Sample Width : ")
        sample_width_label.grid(row=2, column=0)
        sample_width_value = tk.StringVar()
        sample_width = ttk.Combobox(self, 
                                   textvariable=sample_width_value
                                   )
        sample_width["values"] = ("Burst", "Continued")
        sample_width.grid(row=2, column=1)
        
        text_box_value = tk.StringVar()
        text_box= ttk.Entry(self, 
                            textvariable=text_box_value)
        text_box.grid(row=3, column=0, columnspan=2, 
                      padx=5, pady=5,
                      sticky="NESW"
                      )
        
        for child in self.winfo_children():
            if isinstance(child, tk.ttk.Label) == True :
                child.grid_configure(sticky="W")
                child["style"]='Label.TLabel'
            if isinstance(child, tk.ttk.Combobox) == True :
                child.grid_configure(sticky="EW")
                #child["style"]='Label.TFrame'
        
class RightContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        
        
        dialogue_box_container= ttk.LabelFrame(self, 
                                               padding=10, 
                                               text="Dialogue Box",
                                               style="Label.TLabelframe"
                                               )
        dialogue_box_container.grid(row=0, column=0,
                                    sticky="NSEW"
                                    )        
        dialogue_value = tk.StringVar()
        dialogue_box = ttk.Label(dialogue_box_container, 
                                 textvariable=dialogue_value,
                                 style="Label.TLabel"
                                 )
        dialogue_box.grid(row=0, column=0)
        
        
        logo_image = Image.open("./assets/logo.png").resize((65, 40))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(self, 
                               image=logo_photo, 
                               padding=10,
                               style="Label.TLabel"
                               )
        logo_label.grid(column=0, row=1)
        logo_label.image = logo_photo
        
        
