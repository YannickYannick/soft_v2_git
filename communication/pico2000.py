#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from picoscope import ps2000a
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
from picoscope import ps2000
# from picoscope import ps2000a
import pylab as plt
import time

#pico9000
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import tkinter as tk



import win32com.client
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import pythoncom




#import widgets_picoscope

class CommunicationPicoscope(threading.Thread):
    def __init__(self, master):
        threading.Thread.__init__(self)
        self.picoscope_properties = {"self.average":0, "self.time_scale":0}
        
        
        self.master = master
#        self.strdata = [1,2,3,4,5]
#        self.data = [1,2,3,4,5]
## comment deletting
#        ############ MODEL #############
#        self.COMRCW = win32com.client.Dispatch("PicoScope9000.COMRC") # create COM object   
#        self.COMRCW.ExecCommand("Gui:Control:Invisible")
#        self.COMRCW.ExecCommand("Header Off")
#        
#        self.COMRCW.ExecCommand(" ACQuire:CH1:MODE AVGSTAB")
#        self.picoscope_properties["self.average"] = self.COMRCW.ExecCommand("ACQuire:CH1:NAVG?")
#        self.picoscope_properties["self.time_scale"] = self.COMRCW.ExecCommand("TB:ScaleA?") 
#
#        
#          # Set up measurements
#        self.COMRCW.ExecCommand("TB:ScaleA? 1m")  
#        self.COMRCW.ExecCommand("Meas:Display:Param")
#        self.COMRCW.ExecCommand("Meas:DisplSrc:Ch1")
#        self.COMRCW.ExecCommand("Meas:Mode:Single")
#        self.COMRCW.ExecCommand("Meas:Ch1:XParam:Freq 1")
#        self.COMRCW.ExecCommand("Meas:Ch1:XParam:Rise 1")
#        self.COMRCW.ExecCommand("Meas:Ch1:YParam:Max 1")
#        self.COMRCW.ExecCommand("Meas:Ch1:YParam:Min 1")
#        self.COMRCW.ExecCommand("Meas:Ch1:YParam:PP 1")
#        self.COMRCW.ExecCommand("Trig:Mode Trig")
#        self.COMRCW.ExecCommand("Trig:Source? Direct")
#        
#        
        self.data = range(512)
#        self.update_val  = 0
#        self.average_before = self.picoscope_properties["self.average"] # nouvelle variable -> ctrl+f : déclenchement lors d'un changement de valeur
#        self.time_scale_before =  self.picoscope_properties["self.average"]
        
        
        print("Attempting to open Picoscope 2000...")

        
        
       


        self.start()

    
    def run(self):
        for i in range(10):
            self.ps.runBlock()
            self.ps.waitReady()
            
            self.ps.runBlock()
            self.ps.waitReady()
            self.dataa = self.ps.getDataV('A', self.nSamples, returnOverflow=False)
            self.data = self.dataa[:512]
#            print(self.dataa)
#            
#            pythoncom.CoInitialize()
#            self.COMRCW = win32com.client.Dispatch("PicoScope9000.COMRC")
#            
            
            #déclenchement lors d'un changement de valeur
#            if self.average_before != self.picoscope_properties["self.average"] :               
#
#                           
#                #niveau 3
#                self.command = "ACQuire:CH1:NAVG " + str(self.picoscope_properties["self.average"])
#                self.COMRCW.ExecCommand(self.command) #update time scale
#                self.average_before = self.picoscope_properties["self.average"]
#                
#                
#            if self.time_scale_before != self.picoscope_properties["self.time_scale"] :                    
#                                         
#                #niveau 3
#                self.command = "TB:ScaleA? " + self.picoscope_properties["self.time_scale"] + "n"
#                self.COMRCW.ExecCommand(self.command) #update time scale                           
#                self.time_scale_before = self.picoscope_properties["self.time_scale"]
#                
#            self.strdata = self.COMRCW.ExecCommand("Wfm:Data?")
#            self.strdata = str(self.strdata)
#            self.strdata = self.strdata.split(',')
#            self.strdata = np.asarray(self.strdata)   
#            self.data = self.strdata.astype(np.float)
            
        
            time.sleep(1) #1 second = un peu lent
        
        self.ps.stop()
        self.ps.close()
            
 
        






  
  
