#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import serial
import serial.tools.list_ports

import time
import threading   
import tkinter as tk



    
class CommunicationLaser(threading.Thread):
    def __init__(self, master):
        threading.Thread.__init__(self)
        
        self.master = master
        self.new_commands_list = []
        
#        self.serial_laser = serial.Serial('COM6', baudrate = 9600, 
#                            bytesize = 8, parity = 'N', stopbits = 1, 
#                            xonxoff = 0, timeout = 5)
        
        self.laser_properties = {"self.state":0, "self.mode":0, "self.current_mode" : 0, "self.burst_rate" : 0, "self.repetition_rate" : 0, "self.burst_rate" : 0, "self.current_intensity_p":0, "self.light":0}
        self.laser_commands = {"self.state":"STA=", "self.mode":"QM=", "self.current_mode" : "CM=", "self.burst_rate" : "generateur", "self.repetition_rate" : "RR=", "self.burst_rate" : "BR=", "self.power_intensity":"P=", "self.current_intensity_p":"CIP=", "self.light":"L="}
        self.laser_properties_before = self.laser_properties
#        print(self.serial_laser.write(b'>=1;?STA;'))
#        self.laser_properties["self.state"] = self.serial_laser.readline() #enlever certaines infos
#        self.serial_laser.write(b'CM=1;QM=0;BR=0;RR=0;CIP=0;L=0;') 
        

   
        
        self.update_val  = 0
        self.start()
 
        
    def run(self):
        for i in range(2000):
         
            time.sleep(1)  
            
    def update(self):
        str_cons = ""
        
        self.a = self.serial_laser.readline()
        print (self.a )
        print("update")
    def consigne (self):       
        print("consigne_laser = ", self.new_commands_list)
        self.serial_laser.write(bytes(self.new_commands_list, encoding="ascii"))
        print("self.real_state = ",  self.serial_laser.readline() )
        
        self.serial_laser.write(b'?BR;?RR;?CIP;?L;')
        print("self.real_state = ",  self.serial_laser.readline() )
#        
        pass
#    def switch_light (self):   
#        if :
#        else =
        
class ApplicationLaser(threading.Thread):
    
    def __init__(self, main_windows):    
        threading.Thread.__init__(self)
        
        self.main_windows = main_windows
        self.communication_laser = CommunicationLaser(self)
        self.reglage_1 = ""
        
      
        self.start()
        
    def run(self):
        for i in range(60):
            self.reglage_1 = 0
            time.sleep(1)
        
        
    def update(self):
        
        self.communication_laser.update()  
