#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:25:38 2018

@author: Michele Svanera
@mail: Michele.Svanera@glasgow.ac.uk
"""

################################################################################################################
## Imports 

from __future__ import division
from __future__ import print_function

from datetime import datetime as dt
import numpy as np
import threading, itertools
import time

from pypixxlib._libdpx import DPxOpen, DPxSelectDevice, DPxSetMarker, \
   DPxUpdateRegCache, DPxGetMarker, DPxEnableDinDebounce, DPxGetDinValue, \
   DPxSetDinLog, DPxStartDinLog, DPxGetDinStatus, DPxReadDinLog

from psychopy import event, core, visual


################################################################################################################
## Paths and Constants

Initial_code = 16777200
Button_coding = [-1,-2,-3,-4,-5]              #red,yellow,green,blue,white(i.e. trigger)
IsMRI = 0                                   #MRI inverses the bit polarities


################################################################################################################
## Functions

class buttonBoxThread(threading.Thread):
    def __init__(self, thread_id, name):           
        threading.Thread.__init__(self)
        
        self.stimulus_onset_time = 0
        self.local_status = 0
        self.mask = 0x0000 if IsMRI == 0  else 0x001f
        
        # Open comunication with Vpixx
        DPxOpen()
        
        #Select the correct device
        DPxSelectDevice('PROPixxCtrl')
        DPxSetMarker()
        self.stimulus_onset_time = DPxGetMarker()
        DPxEnableDinDebounce()              # Filter out button bounce
        self.local_status = DPxSetDinLog()        # Configure logging with default values
        DPxStartDinLog()
        DPxUpdateRegCache()

        # Thread infos        
        self.thread_id = thread_id
        self.name = name
        
        # Every button has: its value {0,1} and time when it changed (as datetime)
        self.button_state = {'time': np.array([dt.now()]*5), 'state': np.zeros((5,),dtype=np.int8)}
        self.button_state['state'][-1] = 1
        self.scanner_trigger = False
        self._stop_event = threading.Event()
        
    def run(self):
        print("Starting " + self.name)
        
        initial_values = DPxGetDinValue()
        
        print('Initial digital input states = ' + "{0:016b}".format(initial_values) + " (int=%d)".format(initial_values))

        while(True):
            DPxUpdateRegCache()
            DPxGetDinStatus(self.local_status)
            
            if self.local_status['newLogFrames'] > 0 :           #Something happened
                data_list = DPxReadDinLog(self.local_status)
                self.button_state = self.updateStateButton(self.button_state,data_list)
                
                print(self.button_state)

            if(self.stopped()):
                break
                
        print("Exiting " + self.name)
        
    def stop(self):        
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    # Take in input a state and check what is changed
    def updateStateButton(self,button_state,data_list):   
        
        for j in range(len(data_list)):
            j_value = bin(data_list[j][1] ^ self.mask)
            
            # Check every button
            for i_button in range(len(button_state['state'])):
                i_button_detected_value = int(j_value[Button_coding[i_button]])
                if(i_button_detected_value != button_state['state'][i_button]):
                    button_state['state'][i_button] = i_button_detected_value
                    button_state['time'][i_button] = dt.now()

        return button_state
    

################################################################################################################
## Main

# Create and start new threads
thread1 = buttonBoxThread(1, "bottom box check")
thread1.start()
print(thread1.button_state)

win = visual.Window([800, 800], monitor='testMonitor')

button_red = visual.Circle(win=win,radius=0.1,
            fillColor='red',lineColor='red',pos=(0.5,0))
button_yellow = visual.Circle(win=win,radius=0.1,
            fillColor='yellow',lineColor='yellow',pos=(0,0.5))
button_green = visual.Circle(win=win,radius=0.1,
            fillColor='green',lineColor='green',pos=(-0.5,0))
button_blue = visual.Circle(win=win,radius=0.1,
            fillColor='blue',lineColor='blue',pos=(0,-0.5))
button_white = visual.Circle(win=win,radius=0.1,
            fillColor='white',lineColor='white',pos=(0,0))

while not event.getKeys():
    
    button_state = thread1.button_state
    scanner_trigger = thread1.scanner_trigger
    button_state = button_state['state']
    
    if(button_state[0]==1):
        button_red.draw()
    if(button_state[1]==1):
        button_yellow.draw()
    if(button_state[2]==1):
        button_green.draw()
    if(button_state[3]==1):
        button_blue.draw()
    if(button_state[4]==0):
        button_white.draw()
    win.flip()

thread1.stop()
win.close()
core.quit()

