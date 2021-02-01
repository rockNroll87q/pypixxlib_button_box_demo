#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Button box threading.

Author: Michele Svanera
Aug. 2019

    Code version 1.0

"""


################################################################################################################
## Imports 

from __future__ import division 
from __future__ import print_function

import threading
import numpy as np
from datetime import datetime as dt

from pypixxlib._libdpx import DPxOpen, DPxSelectDevice, DPxSetMarker, \
   DPxUpdateRegCache, DPxGetMarker, DPxEnableDinDebounce, DPxGetDinValue, \
   DPxSetDinLog, DPxStartDinLog, DPxGetDinStatus, DPxReadDinLog


################################################################################################################
## Paths and Constants

# Button box
Button_coding = [-1,-2,-3,-4,-5]              #red,yellow,green,blue,white(i.e. trigger)
IsMRI = 0


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
        DPxEnableDinDebounce()                      # Filter out button bounce
        self.local_status = DPxSetDinLog()          # Configure logging with default values
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
#        print("Starting " + self.name)
        
        initial_values = DPxGetDinValue()
        
#        print('Initial digital input states = ' + "{0:016b}".format(initial_values) + " (int=%d)".format(initial_values))

        while(True):
            DPxUpdateRegCache()
            DPxGetDinStatus(self.local_status)
            
            if self.local_status['newLogFrames'] > 0 :           #Something happened
                data_list = DPxReadDinLog(self.local_status)
                self.button_state = self.updateStateButton(self.button_state,data_list)
                
#                print(self.button_state)

            if(self.stopped()):
                break
                
#        print("Exiting " + self.name)
        
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

   
    
