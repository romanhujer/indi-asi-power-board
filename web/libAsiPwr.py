#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   libAsiPwr.py   RPi ASi-Power borad 
#
#   Copyright (c) 2019 Roman Hujer   http://hujer.net
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,ss
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Description:
#
#  Wiring diagram a PCB  on https://easyeda.com/hujer.roman/rpi-asi-power-clone
#

import sys      
import os
import logging
import time

import RPi.GPIO as GPIO



class  ASiPWR:
    """ASiPWR"""  
    port1 = 12
    port2 = 13
    port3 = 26
    port4 = 18
    DSLR = 21

    dslr_count = 10 
    dslr_exptime = 30
    dslr_wait = 5
    _c_exptime = 0
    _c_count = 0
    _c_wain = 0
    _r_dslr = False

    
    BUZZER = 19
    LED = 20
    _led_on = False

    _p1_cfg = 100
    _p2_cfg = 100
    _p3_cfg = 100
    _p4_cfg = 100
    _power_cycle = 1000
    
    _p1_on = False
    _p2_on = False
    _p3_on = False
    _p4_on = False
    _first_dslr_run = True;
  

    def __init__(self, debug=False ) :
       """__init__"""  
#       GPIO.setwarnings(debug)
       GPIO.setwarnings(False) 
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(self.port1, GPIO.OUT)
       GPIO.setup(self.port2, GPIO.OUT)
       GPIO.setup(self.port3, GPIO.OUT)
       GPIO.setup(self.port4, GPIO.OUT)
       GPIO.setup(self.DSLR, GPIO.OUT)
       GPIO.setup(self.BUZZER, GPIO.OUT)
       GPIO.setup(self.LED, GPIO.OUT)
       self.debug = debug 

# Port On
    def PortON(self, port=LED):
       """PortON"""  
       GPIO.output(port,GPIO.HIGH)

# Port Off
    def PortOFF(self,port=LED):
       """PortOFF"""  
       GPIO.output(port,GPIO.LOW)

#  All PWR ON
    def AllPwrON(self):
       """AllPwrON"""  
       self.PortON(self.port1)
       self.PortON(self.port2)
       self.PortON(self.port3)
       self.PortON(self.port4)
# All PWR OFF    
    def AllPwrOFF(self):
       """AllPwrOFF"""  
       self.PortOFF(self.port1)
       self.PortOFF(self.port2)
       self.PortOFF(self.port3)
       self.PortOFF(self.port4)

    def LedChgStat(self,st=2):
        """LedChngStat"""  
        if st == 0 :
                self.PortOFF(self.LED) 
                self._led_on = False
        elif st ==1 :
                 self.PortON(self.LED)
                 self._led_on = True
        else:
                 if self._led_on :
                    self.PortOFF(self.LED)
                    self._led_on = False
                 else:
                    self.PortON(self.LED)
                    self._led_on = True 
                    
    def beep(self,t_long=5,hertz=500):
        """beep"""  
        _t = int ((1./hertz) * 5000)
        _buzzer = False
        _init_sec = int(time.time() * 10 + 0.5)
        while (int(time.time() * 10 ) -_init_sec) < t_long :
            if _buzzer :
                self.PortOFF(self.BUZZER)
                _buzzer = False
            else:
                self.PortON(self.BUZZER)
                _buzzer = True
            _init_t = int(time.time() * 10000)
            while ( int(time.time() * 10000) - _init_t) < _t:  
                continue
        self.PortOFF(self.BUZZER)

    def power_cycle(self, debug=False):
        """power cycle"""  
        self.read_cfg()
        p1_load = self._p1_cfg
        p2_load = self._p2_cfg
        p3_load = self._p3_cfg
        p4_load = self._p4_cfg
        cycle_t = self._power_cycle
        if debug: 
            print "L1 %03d" % p1_load
            print "L2 %03d" % p2_load
            print "L3 %03d" % p3_load
            print "L4 %03d" % p4_load
            print "C2 %06d" % cycle_t
        sleep_t = cycle_t / 200000.
        init_ms = int(time.time() * 1000)
        end_time = init_ms + cycle_t - 1
        p1_end_t = init_ms + (cycle_t * p1_load / 100)
        p2_end_t = init_ms + (cycle_t * p2_load / 100)
        p3_end_t = init_ms + (cycle_t * p3_load / 100)
        p4_end_t = init_ms + (cycle_t * p4_load / 100)
        if p1_load > 0 :
            self.PortON(self.port1)
        else:     
            self.PortOFF(self.port1)
        if p2_load > 0 :
            self.PortON(self.port2)
        else:
            self.PortOFF(self.port2)
        if p3_load > 0 :
            self.PortON(self.port3)
        else:
            self.PortOFF(self.port3)
        if p4_load > 0 :
            self.PortON(self.port4)
        else:
            self.PortOFF(self.port4)
        c_time = int(time.time() * 1000)
        while c_time < end_time:
            if c_time > p1_end_t :
               self.PortOFF(self.port1)
            if c_time > p2_end_t :
               self.PortOFF(self.port2)
            if c_time > p3_end_t :
               self.PortOFF(self.port3)
            if c_time > p4_end_t :
               self.PortOFF(self.port4) 
            time.sleep(sleep_t)   
            c_time = int(time.time() * 1000) 
        if p1_load < 100 :
           self.PortOFF(self.port1)
        if p2_load < 100 :
           self.PortOFF(self.port2)
        if p3_load < 100 :
           self.PortOFF(self.port3)
        if p4_load < 100 :          
           self.PortOFF(self.port4)
        self.LedChgStat(2)

    def write_cfg(self,cfg='/home/pi/.asi_pwr.cfg'):
        """write_cfg"""  
        c = ( 'P1:'  + '%03d' % self._p1_cfg +
              ',P2:' + '%03d' % self._p2_cfg +
              ',P3:' + '%03d' % self._p3_cfg +
              ',P4:' + '%03d' % self._p4_cfg +
              ',PC:' + '%04d' % self._power_cycle +
              '\n')
        with open(cfg, 'w') as f:
            f.write(c)        
   
    def read_cfg(self,cfg='/home/pi/.asi_pwr.cfg'):
        """read_cfg"""  
        f = open(cfg, "r")
        s = f.read().split(',')
        self._p1_cfg = int(s[0].split(':') [1])
        self._p2_cfg = int(s[1].split(':') [1])
        self._p3_cfg = int(s[2].split(':') [1])
        self._p4_cfg = int(s[3].split(':') [1])
        

    def shut_start(self):
        """shut_start"""
        GPIO.output(self.DSLR, GPIO.HIGH)
    
    def shut_stop(self):
        """"shut_stop"""
        GPIO.output(self.DSLR, GPIO.LOW)


    def dslr_timer_start(self):
        """dslr_timer_start"""
        self._c_count = self.dslr_count
        while (self._c_count > 0 )  and self._r_dslr :
            self._c_count -= 1
            self._c_exptime = self.dslr_exptime 
            self._c_wait =  self.dslr_wait
            self.shut_start()
            while (self._c_exptime > 0) and self._r_dslr :
                self._c_exptime -= 1
                time.sleep(1)
            self.shut_stop()
            while (self._c_wait > 0)  and self._r_dslr :
                self._c_wait -= 1
                time.sleep(1)
            self.beep(1)
        self._r_dslr = False


    def dslr_timer_stop(self):
        """dslr_timer_stop"""
        self._c_count = 0
        self._c_exptime = 0
        self._c_wait = 0
        self._r_dslr = False

