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
print pkg_path
#views_path = os.path.join(pkg_path, 'views')



# default settings

WEB_HOST = '0.0.0.0'
WEB_PORT = 80
CFG_FILE = '/home/pi/.asi_pwr.cfg'

daemon_exit_flag = False
lock_serial_port = False

debug = True

parser = argparse.ArgumentParser(description='myASi-pwr'
                                'A simple web application to manage ASI-PWR-board')
parser.add_argument('--port', '-P', type=int, default=WEB_PORT,
                    help='web server port (default: %d)' % WEB_PORT)
parser.add_argument('--host', '-H', default=WEB_HOST,
                    help='bind web server to this interface (default: %s)' % WEB_HOST)
parser.add_argument('--config', '-c', default=CFG_FILE,
                    help='config file (default %s)' % CFG_FILE)
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
#  Define sqm Thread daemon
#
class pwrThread(threading.Thread):
  def __init__(self, name): 
    threading.Thread.__init__(self) 
    self.name = name
    daemon_exit_flag = False
  
  def run(self): 
    print "Thread Starting: " + self.name
    pwr_daemon(self.name)
    print "Thread Stop: " + self.name

  def stop(self): 
    daemon_exit_flag = True

def pwr_daemon(threadName): 
    daemon_exit_flag = False
    pwr.beep(4)
    while not daemon_exit_flag:
        pwr.power_cycle()
    threadName.exit()
     

#
# Init my class defaut is com open and debug off
#
pwr = libAsiPwr.ASiPWR(debug=debug)

#
# Init class
#

if  not os.path.exists(cfg_file): 
    print "Create new cfg_file: " + cfg_file
    pwr.write_cfg(cfg=cfg_file)
else : 
    print "Use old cfg_file: " + cfg_file
    pwr.read_cfg(cfg=cfg_file)


print "PWR demon starting"  
mydaemon = pwrThread('pwrD') 
mydaemon.start()
print "OK"


#
# Web pages rendering
#

#
# Main page
#
def main_page():
    pwr.read_cfg(cfg=cfg_file)
    return template( os.path.join(views_path, 'main.tpl'),
        pt1 = '%03d' % pwr._p1_cfg,
        pt2 = '%03d' % pwr._p2_cfg,
        pt3 = '%03d' % pwr._p3_cfg,
        pt4 = '%03d' % pwr._p4_cfg,
        ckl = '%04d' % pwr._power_cycle )

#
# Web pages routing 
#

@app.route('/static/<path:path>')
def callback(path):
    """Serve static files"""
    return static_file(path, root=views_path)

@app.route('/favicon.ico', method='GET')
def get_favicon():
    """Serve favicon"""
    return static_file('favicon.ico', root=views_path)


@app.route('/')
@app.route('/main')
def main(): 
   """main page"""
   return main_page()            
 

@app.route('/main', method='POST') 
def do_main():
   """do main"""
   form_id=request.forms.get('id')
   print "Form ID:" + form_id
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



###############################################################################
# Startup standalone server
###############################################################################

def main():
    """Start autostart profile if any"""
    run(app, host=args.host, port=args.port, quiet=args.verbose)
    logging.info("Exiting")


if __name__ == '__init__' or __name__ == '__main__':
    main()

