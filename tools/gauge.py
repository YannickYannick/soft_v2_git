#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:43:33 2020

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk

class Gauge(ttk.Frame):   
    def __init__(self, parent, width, height, min_value, max_value, divisions,
                 label, units, bg, **kwargs):
        
        # self.rowconfigure((0), weight=1)
        # self.columnconfigure((0), weight=1)
        
        self._parent = parent
        
        super().__init__(self._parent, **kwargs)
        
    
        self._width = width
        self._height = height
        self._min_value = min_value
        self._max_value = max_value
        self._divisions = divisions
        self._label = label
        self._units = units
        self._bg = bg
        
        self._value = self._min_value
        
        
        self._canvas = tk.Canvas(self, width=self._width, height=self._height,
                                 bg=self._bg, bd=0, highlightthickness=0)
        self._canvas.grid(row=0, column=0, sticky='NEWS')
        self._drawgauge()
        
        
        
    def _drawgauge(self):
        
        self._canvas.delete('all')
        
        max_angle = 180
        value_as_percent = ((self._value - self._min_value) 
                            / (self._max_value - self._min_value))
        value = float(max_angle * value_as_percent)
        
        # main
        for i in range(self._divisions):
            extent = (max_angle / self._divisions)
            start = (0 + i * extent)
            rate = (i+1)/(self._divisions+1)
            if rate < 0.2:
                bg_color = '#FF4200'
            elif rate <= 0.40:
                bg_color = '#FF6D3A'
            elif rate <= 0.50:
                bg_color = '#FF906A'
            elif rate <= 0.80:
                bg_color = '#FFAE92'
            else:
                bg_color = '#FFCEBC'

            self._canvas.create_arc(
                self._height/6, 
                self._height * 0.15,
                self._width-(self._height/6), 
                self._height * 1.8,
                start=start, 
                extent=extent, 
                width=3,
                fill=bg_color, 
                outline='white',
            )
        
        # hide center    
        self._canvas.create_arc(
            (self._height/6)*2.5, 
            self._height * 0.15 * 2.7,
            self._width - (self._height/6) * 2.5, 
            self._height * 1.8,
            start=0, 
            extent=max_angle, 
            width=3,
            outline='white',
            fill=self._bg
            )
         
        # needle
        self._canvas.create_arc(
            self._height/6-10, 
            self._height * 0.15-10,
            self._width-(self._height/6)+10, 
            self._height * 1.9,
            start=0, 
            extent=180-value, 
            width=4,
            #fill=bg_color, 
            outline='black',
            )

        # hide needle
        self._canvas.create_arc(
            self._height/6-10, 
            self._height * 0.15-10,
            self._width-(self._height/6)+10, 
            self._height * 1.9,
            start=0, 
            extent=max_angle, 
            width=6,
            outline=self._bg,
            )
        
        # base needle
        self._canvas.create_arc(
            self._height*0.8, 
            self._height*0.92 ,
            self._width-(self._height*0.8), 
            self._height * 1.9,
            start=0, 
            extent=max_angle, 
            width=2,
            outline='grey',
            fill=self._bg
            )
        
        # hide additional arcs outline
        self._canvas.create_rectangle(
            (self._height/59)*2.5,
            self._height*0.985,
            self._width - (self._height/59) * 2.5, 
            self._height*1.2,
            outline='red',
            fill=self._bg,
            width=0
            )
        
        # display lowest value
        value_text = '{}'.format(self._min_value)
        self._canvas.create_text(
            self._width * 0.05, self._height*0.95 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display second value
        value_text = '{}'.format(round(((self._max_value-self._min_value)/5)*1))
        self._canvas.create_text(
            self._width * 0.12, self._height*0.48 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display third value
        value_text = '{}'.format(round(((self._max_value-self._min_value)/5)*2))
        self._canvas.create_text(
            self._width * 0.35, self._height*0.15 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display third value
        value_text = '{}'.format(round(((self._max_value-self._min_value)/5)*3))
        self._canvas.create_text(
            self._width * 0.65, self._height*0.15 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display fifth value
        value_text = '{}'.format(round(((self._max_value-self._min_value)/5)*4))
        self._canvas.create_text(
            self._width * 0.88, self._height*0.48 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display highest value
        value_text = '{}'.format(self._max_value)
        self._canvas.create_text(
            self._width * 0.96, self._height*0.95 ,
            font=('Helvetica', 11), text=value_text, fill='black')
        
        # display legende
        value_text = '{} {}'.format(self._label, self._units )
        self._canvas.create_text(
            self._width * 0.5, self._height*0.8 ,
            font=('Helvetica bold', 12), text=value_text, fill='#2e3f4f')
        
    
    def set_value(self, value):
        self._value = value
        if self._min_value * 1.02 < value < self._max_value * 0.98:
            self._drawgauge()     # refresh all

            



# test_gauge = tk.Tk()

# gauge = Gauge(
# test_gauge,
# width=200, 
# height=100,
# min_value=0,
# max_value=1200,
# # label='Current Temperature',
# # unit='°C',
# divisions=5,
# bg="#D3E2F1"
# )
# gauge.grid(column=0, row=0, sticky ="NESW") 
# #gauge.set_value(600)

# test_gauge.mainloop()