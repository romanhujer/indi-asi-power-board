#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   main.py  my ASi-pwr-borad  
#
#   Version 1.0
#
#   Copyright (c) 2022 Roman Hujer   http://hujer.net
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

import os
import glob 
import time
import logging 
import argparse
import math
import sys 
import trace 
import threading 
import libAsiPwr
import time 

from bottle import Bottle, route, run, template, static_file, get, post, request


views_path ='views' 

pkg_path = os.path.split(os.path.abspath(__file__))

# default settings

WEB_HOST = '0.0.0.0'
WEB_PORT = 80
CFG_FILE = '/home/pi/.asi_pwr.cfg'

debug = True

parser = argparse.ArgumentParser(description='myASi-pwr'
                                'A simple web application to manage ASI-PWR-board')
parser.add_argument('--port', '-P', type=int, default=WEB_PORT,
                    help='web server port (default: %d)' % WEB_PORT)
parser.add_argument('--host', '-H', default=WEB_HOST,
                    help='bind web server to this interface (default: %s)' % WEB_HOST)
parser.add_argument('--config', '-c', default=CFG_FILE,
                    help='config file (default %s)' % CFG_FILE)
parser.add_argument('--dslr', '-d', default='N',
                   help='DSLR timer only [Y|N](default N)')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print more messages')
parser.add_argument('--logfile', '-l', help='log file name')

args = parser.parse_args()

logging.debug("command line arguments: " + str(vars(args)))


app = Bottle()
logging.info('using Bottle as standalone server')

#
cfg_file = args.config


#
# Init my libAsiPwr class 
#
pwr = libAsiPwr.ASiPWR(debug=debug)


# 
#  Define sqm Thread daemon
#
class pwr_Thread(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 

    def run(self): 
        print "PWR Thread Starting"
        pwr.beep(4)
        while True :
            pwr.power_cycle()
        print "PWR Thread Stop"


class DSLR_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "DSLR Thred Starting"
        pwr.dslr_timer_stop()
        while True :
            if pwr._r_dslr :
                pwr.dslr_timer_start()
                pwr.beep(4)
            time.sleep(1)
        print "DSLR Thred Stop"


#
# Init 
#
if args.dslr == 'N'  :
    if  not os.path.exists(cfg_file): 
        print "Create new cfg_file: " + cfg_file
        pwr.write_cfg(cfg=cfg_file)
    else : 
        print "Used cfg_file: " + cfg_file
        pwr.read_cfg(cfg=cfg_file)
    main_daemon = pwr_Thread() 
    main_daemon.start()


dslr_daemon = DSLR_Thread()
dslr_daemon.start()


#
# Web pages rendering
#

#
# Main page
#
def main_page():
    pwr.read_cfg(cfg=cfg_file)
    return template( os.path.join(views_path, 'main.tpl'),
        pt1 = '%3d' % pwr._p1_cfg,
        pt2 = '%3d' % pwr._p2_cfg,
        pt3 = '%3d' % pwr._p3_cfg,
        pt4 = '%3d' % pwr._p4_cfg,
        ckl = '%4d' % pwr._power_cycle )



@app.route('/static/<path:path>')
def callback(path):
    """Serve static files"""
    return static_file(path, root=views_path)

@app.route('/favicon.ico', method='GET')
def get_favicon():
    """Favicon"""
    return static_file('favicon.ico', root=views_path)


@app.route('/')
@app.route('/main')
def main(): 
    """main page"""
    if args.dslr == 'Y'   :
        return dslr_page()
    return main_page()            
 

@app.route('/main', method='POST') 
def do_main():
   """do main"""
   form_id=request.forms.get('id')
   if form_id == 'p1': 
      pwr._p1_cfg = int(request.forms.get('npt1'))
   if form_id == 'p2':
      pwr._p2_cfg = int(request.forms.get('npt2'))
   if form_id == 'p3':
      pwr._p3_cfg = int(request.forms.get('npt3'))
   if form_id == 'p4':
      pwr._p4_cfg = int(request.forms.get('npt4'))
   pwr.write_cfg(cfg=cfg_file)
   return main_page()

#
# DSLR tiner page
#
def dslr_page():
    return template(os.path.join(views_path, 'dslr.tpl'),
        exptime = pwr.dslr_exptime,
        wait = pwr.dslr_wait,
        count = pwr.dslr_count,
        i_exptime =  pwr.dslr_exptime - pwr._c_exptime,
        i_wait = pwr.dslr_wait - pwr._c_wait,
        i_count = pwr.dslr_count - pwr._c_count,
        running = pwr._r_dslr,
        dslr = args.dslr 
        )

@app.route('/dslr')
def dslr():
    return dslr_page()

@app.route('/dslr', method='POST')
def do_dslr():
    form_id=request.forms.get('id')
    if form_id == 'timer' :
        pwr.dslr_count = int(request.forms.get('icount'))
        pwr.dslr_exptime = int( request.forms.get('iexptime'))
        pwr.dslr_wait = int(request.forms.get('iwait'))
        pwr._r_dslr = True
    if form_id == 'stop' : 
        pwr.dslr_timer_stop()
    return dslr_page()   


###############################################################################
# Startup standalone server
###############################################################################

def main():
    """Start autostart profile if any"""
    run(app, host=args.host, port=args.port, quiet=args.verbose)
    logging.info("Exiting")


if __name__ == '__init__' or __name__ == '__main__':
    main()

