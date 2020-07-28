#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
import serial
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.ttk as ttk

import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import time
import datetime




import csv

def data_writer(time, consigne, temperature, temperature_max, puissance, coeff_proportionnel, coeff_integral, coeff_derive, proportionnel, integral, derive, file_name='eggsss.csv'):
    with open(file_name, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL) #
        spamwriter.writerow([time, consigne, temperature, temperature_max, puissance, coeff_proportionnel, coeff_integral, coeff_derive, proportionnel, integral, derive])
    csvfile.close()
    
def getValues(ser, puissance=0):
    
    if puissance > 124:
        puissance = 125
    if puissance <0 :                
        puissance = 0
    puissance = int(puissance //1)
    tkt =chr(puissance)
    ser.write(tkt.encode('ascii'))
    arduinoData = ser.readline().decode('ascii')
   
    return arduinoData
        

class CommunicationOven(threading.Thread):
    def __init__(self, tk_root):
#        partie communication (y->y)
        self.arret = False
        threading.Thread.__init__(self)
        
        self.real_temperaturee = 0

        self.arduino_I2C = serial.Serial('COM9', baudrate = 9600, timeout = 1)

        threading.Thread.__init__(self)
        self.arret = False
        self.tk_root = tk_root
        self.list_temperatures_ordered = []
        self.time = 0
        self.initial_time = time.perf_counter()
        self.output = 0
        self.erreur = 0
        self.order_temperature = 0
        self.erreur_liste = []
        self.temperature_iterator = 0


        self.proportional_error = self.erreur
        self.integral_error  = 0
        self.integral = 0
        self.derivative_error = 0

        self.proportional_coeff = 12#12
        self.intergral_coeff = 1200#20
        self.integral_time = 2000
        self.derivative_coeff = 20#200


        self.proportionnel = self.proportional_coeff * self.proportional_error
        self.integral = self.intergral_coeff * self.integral_error
        self.derive = self.derivative_coeff * self.derivative_error


        self.output = self.proportionnel
        self.erreur_moins_un = 0
        self.time_before = 0
        self.rectangle = 0
        self.rectangles_list = []
        self.minilist = [0,0]
        self.integral_somme = 0
        
        self.datetime_object = str(datetime.datetime.now())
        self.file_name = "Results/file_" + self.datetime_object[:10] + "_(" + self.datetime_object[11:13]+"_"+self.datetime_object[14:16]+"_"+self.datetime_object[17:19]+").csv"


        
        time.sleep(0.05)
        self.barPID = ttk.Progressbar(tk_root, orient="vertical", length=400,  mode='determinate')
#        data_writer("time", "order_temperature", "temperature", "tempéraure max_palier","puissance", "proportional_coeff", "coeff_integral", "derivative_coeff", "proportionnel", "integral", "derive", file_name=self.file_name )
#        
        
        self.timer_fixe = 120
        self.timer = self.timer_fixe 
        self.fidelite = 2
        self.order_temperature_respected = False
        self.temp_max_palier = 0
        self.list_temp_max_palier = []
        self.list_temp_maximum_palier = []
        self.minilist_temp_max_palier = []
        
        self.temperature_compensation = 0
        self.real_temperature_moins = 0
        self.start()
   
    def update_param(self, new_proportional_coeff, new_intergral_coeff, new_derivative_coeff):
        
        self.proportional_coeff = new_proportional_coeff
        self.intergral_coeff = new_intergral_coeff
        self.derivative_coeff = new_derivative_coeff
        
    
    def run(self ):
        for i in range (1000000000000):
            self.real_temperature = getValues(self.arduino_I2C, self.output)
            time.sleep(0.2)
            try:
                self.real_temperature = float(self.real_temperature )
            except:
                self.real_temperature  = 0
            
      
            
#            print(self.real_temperature) 

            self.time = time.perf_counter()-self.initial_time               # enregistrement du temps
            self.order_temperature = self.order_temperature   # + self.temperature_compensation   # accède à la order_temperature
            
            
                      
            try:
                self.real_temperature = float(self.real_temperature)  
            except:                                                         # 
                try:                                                        # 
                    self.real_temperature  = self.temperatures_liste[-1]       # à améliorer
                except:                                                     # 
                    self.real_temperature  =  20  
            if self.real_temperature == 0 :
                self.real_temperature = self.real_temperature_moins
                
            
            self.list_temp_max_palier.append(self.real_temperature )
            self.temp_max_palier = max(self.list_temp_max_palier)
            self.list_temp_maximum_palier.append(max(self.list_temp_max_palier))
            if len(self.list_temp_maximum_palier)>100 : 
                self.list_temp_maximum_palier = self.list_temp_maximum_palier[-100:]
            # partie proportionnel
            
            self.erreur = self.order_temperature - self.real_temperature
            self.proportional_error = self.erreur
            
             # partie proportionnel
            self.erreur = self.order_temperature - self.real_temperature
            self.proportionnel = 2 * self.proportional_error   # (y->y)self.proportional_coeff * self.proportional_error   #
            
            if self.proportionnel > 125 :
                self.proportionnel = 125 
            if self.proportionnel < -125 :
                self.proportionnel = -125
           
            self.rectangle = (self.erreur_moins_un + self.erreur) * (self.time - self.time_before) /2
            self.integral_somme = self.integral_somme + self.rectangle
            self.minilist = []
            self.minilist.append(self.time)             
            self.minilist.append(self.rectangle)
            self.minilist.append(self.erreur)
            
            self.rectangles_list.append(self.minilist)

            while self.rectangles_list[-1][0] - self.rectangles_list[0][0] > self.integral_time:                            #
                self.integral_somme = self.integral_somme - self.rectangles_list[0][1]
                del self.rectangles_list[0]
                   
            self.integral  = self.proportional_coeff *self.integral_somme/(self.intergral_coeff+0.000001)  
   
    
            if self.proportionnel + self.integral > 125 :
                self.integral_somme = (125 - self.proportionnel )*(self.intergral_coeff+0.000001) / self.proportional_coeff
            if self.proportionnel + self.integral < 0 :
                if self.proportionnel + self.integral < -125 :
                    self.integral_somme = (-125 - self.proportionnel )*(self.intergral_coeff+0.000001) / self.proportional_coeff


            #derived part
            if len(self.rectangles_list)>5:            
                self.derivative_error = (self.rectangles_list[-1][2] - self.rectangles_list[-4][2])/10
            else:            
                self.derivative_error = (self.rectangles_list[-1][2] - self.rectangles_list[0][2])/len(self.rectangles_list)
            self.derive =  self.proportional_coeff*self.derivative_coeff * self.derivative_error  
            
            if self.derive < -20:
                self.derive = -20
                
            if self.derive > 20:
                self.derive = 20
                
            
            
            #output part            
           
            #self.integral = self.intergral_coeff * self.integral_error                 # to delete
                                  #
            
            self.output = self.proportionnel# + self.integral + self.derive
            
            
            print("four : ordered, error, out =  ",self.order_temperature, self.erreur, self.output)
            
          
            self.erreur_moins_un = self.erreur



                
            self.time_before = self.time
            self.real_temperature_moins = self.real_temperature
            
            #Writing in a file
#            data_writer(self.time, self.order_temperature, self.real_temperature, 
#                        self.temp_max_palier, self.output, 
#                        self.proportional_coeff, self.intergral_coeff, 
#                        self.derivative_coeff, self.proportionnel, self.integral, 
#                        self.derive, file_name = self.file_name)
            
            
          
            # Gestion des compensations
            if len(self.list_temp_max_palier)>200: 
                if all(x == self.temp_max_palier for x in self.list_temp_maximum_palier[-500:]):
                    #self.temperature_compensation = (2*self.order_temperature/150)*100//100
                    if self.temperature_compensation < (2.5*self.order_temperature/300)*1000//1000 :
                        self.temperature_compensation = self.temperature_compensation + 0.1               
                else :
                    if self.temperature_compensation < 0:
                        self.temperature_compensation = self.temperature_compensation + 0.1           
            else :
                self.temperature_compensation = -(7-(2.5*self.order_temperature/300)*1000//1000)
                   
            if abs(self.real_temperature - (self.order_temperature - self.temperature_compensation)) < self.fidelite :
                if self.order_temperature_respected == False :
                    self.start_timer = self.time
                    self.order_temperature_respected = True    
                    
                self.timer = self.timer_fixe + self.start_timer - self.time
                if self.timer < 0 or self.timer == 0 :
                    self.tk_root.input_temperatures.cliquer_bouton_suivant()
                    
                    self.minilist_temp_max_palier.append(self.temp_max_palier)
                    self.temp_max_palier = 0                   
            else :
                self.order_temperature_respected = False
                self.timer  = self.timer_fixe 
            
            self.real_temperaturee = self.real_temperature   
            time.sleep(0.5)
 
    
    
    def stop(self):     
#        self.arduino_I2C.close()
        time.sleep(0.3)
#        self.arduino_I2C = serial.Serial('COM9', baudrate = 9600, timeout = 1)
        time.sleep(0.3)
#        self.arduino_I2C.close()
        self.arret=True
        
    def update_temperatures(self):
        
        
        self.list_temperatures_ordered = self.list_temperatures_ordered[1:-1]
        print(self.list_temperatures_ordered)
        print(type(self.list_temperatures_ordered))
        self.li = list(self.list_temperatures_ordered.split(", ")) 
        self.li = [float(x) for x in self.li]
        print(self.li)
        print(type(self.li))
        self.order_temperature = self.li[self.temperature_iterator]
        
    def next_temperature(self):
        self.temperature_iterator += 1
        self.order_temperature = self.li[self.temperature_iterator]
        
