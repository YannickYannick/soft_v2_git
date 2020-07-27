#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:43:33 2020

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk

class GreenLight(ttk.Frame):   
    def __init__(self, parent, width, height, **kwargs):
        
        self._parent = parent
        self._width = width
        self._height = height
        
        super().__init__(self._parent, **kwargs)
        
        cnv = tk.Canvas(self, width=self._width, height=self._height)
        cnv.pack()
        
        cnv.create_oval((self._width/2)-(self._width/3),
                        (self._width/2)-(self._width/3), 
                        (self._width/2)+(self._width/3), 
                        (self._width/2)+(self._width/3), 
                        fill="green")
        
class RedLight(ttk.Frame):   
    def __init__(self, parent, width, height, **kwargs):
        
        self._parent = parent
        self._width = width
        self._height = height
        
        super().__init__(self._parent, **kwargs)
        
        cnv = tk.Canvas(self, width=self._width, height=self._height)
        cnv.pack()
        
        cnv.create_oval((self._width/2)-(self._width/3),
                        (self._width/2)-(self._width/3), 
                        (self._width/2)+(self._width/3), 
                        (self._width/2)+(self._width/3), 
                        fill="red")
        
        
        


            



test_gauge = tk.Tk()

test = GreenLight(test_gauge, 70, 70)
test.pack()
test1 = RedLight(test_gauge, 70, 70)
test1.pack()

test_gauge.mainloop()