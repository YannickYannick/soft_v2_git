# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 14:59:26 2020

@author: yannb
"""

import time
import pyvisa
rm = pyvisa.ResourceManager()
device = rm.list_resources()
print(device)
inst = rm.open_resource(device[0])
inst.query("*IDN?")

inst.query("OUTPUT ON")