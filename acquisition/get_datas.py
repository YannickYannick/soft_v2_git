#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 17:39:00 2020

@author: melinapannier
"""
# dans l'entete, à coté du bouton run global, mettre un parametre 
# pr remplir le nom de fichier et indiquer le chemin de stockage
#apl la fonction save data qd on clique sur la bouton run global
#faire une liste dans tous les fichiers qui recupere les données en attribut 
#des classes necessaires, les instancier dans app.py et les passer en argument 
#de cette fonction appelée dans app.py par le bouton run
#(reunir toutes les datas continues dans une meme liste results_dat pour la lisibilité)
#apl

import datetime

def save_data(filename, operator, oven_dat, oscillo_dat, laser_dat, sample_dat):

    today_date = datetime.date.today()

    backup = open(f"{filename}.txt", "w")

    backup.write(f"operator : {operator} \n")
    backup.write(f"date : {today_date} \n")
    backup.write("--------------- Oven ---------------\n")
    backup.write(f"rise rate (C°/min): {oven_dat[4]}\n")
    backup.write(f"accuracy (°C): {oven_dat[5]} \n")
    backup.write(f"annealing time (s) : {oven_dat[6]}\n")
    backup.write(f"entry mode : {oven_dat[0]}\n")
    backup.write(f"min. temperature (°C): {oven_dat[2]}\n")
    backup.write(f"max.temperature (°C): {oven_dat[3]} \n")
    backup.write(f"number of point : {oven_dat[1]}\n")
    backup.write("target temperatures (°C): \n")
    backup.write("----------- Oscilloscope -----------\n")
    backup.write(f"selected picoscope : {oscillo_dat[2]}\n")
    backup.write(f"time scale (ns/DIV): {oscillo_dat[1]}\n")
    backup.write(f"number of averages : {oscillo_dat[0]} \n")
    backup.write("--------------- Laser ---------------\n")
    backup.write(f"mode : {laser_dat[0]}\n")
    backup.write(f"repetition rate : {laser_dat[1]} \n")
    backup.write(f"pulse (kHz) : {laser_dat[2]} \n")
    backup.write(f"frequency (kHz) : {laser_dat[3]} \n")
    backup.write(f"magnitude (%) : {laser_dat[4]} \n")
    backup.write("----------- Sample Parameters -----------\n")
    backup.write(f"material : {sample_dat[0]} \n")
    backup.write(f"sample name : {sample_dat[1]} \n")
    backup.write(f"sample width (mm): {sample_dat[2]} \n \n \n")

    backup.write("time ; setpoint ; temperature ; power ; repetition rate ; pulse rate ; frequency ; magnitude ; y  \n")

    backup.close()

def save_results(filename, results_data) :

    backup = open(f"{filename}.txt", "a")

    backup.write(f"{results_data[0]} ; setpoint ; temperature ; power ; repetition rate ; pulse rate ; frequency ; magnitude ; y  \n")

    backup.close() 