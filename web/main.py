#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   main.py  my ASi-pwr-borad  
#
#   Version 1.0
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

import os
import glob 
import time
import logging 
import argparse
import math
import sys 
import trace 
import threading 
import mysqm
import sqmrrd
import time 

from bottle import Bottle, route, run, template, static_file, get, post, request


views_path ='views' 

pkg_path = os.path.split(os.path.abspath(__file__))
print pkg_path
#views_path = os.path.join(pkg_path, 'views')



# default settings

WEB_HOST = '0.0.0.0'
WEB_PORT = 8080

daemon_exit_flag = False
lock_serial_port = False

debug = True

parser = argparse.ArgumentParser(description='myASi-pwr'
                                'A simple web application to manage ASI-PWR-board')

parser.add_argument('--port', '-P', type=int, default=WEB_PORT,
                    help='web server port (default: %d)' % WEB_PORT)
parser.add_argument('--host', '-H', default=WEB_HOST,
                    help='bind web server to this interface (default: %s)' % WEB_HOST)
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print more messages')
parser.add_argument('--logfile', '-l', help='log file name')

args = parser.parse_args()

logging.debug("command line arguments: " + str(vars(args)))


app = Bottle()
logging.info('using Bottle as standalone server')

#
serial_port = args.com


# 
#  Define sqm Thread daemon
#
class pwrThread(threading.Thread):
  def __init__(self, name): 
    threading.Thread.__init__(self) 
    self.name = name
    daemon_exit_flag = False
  
  def run(self): 
    print "Thread Starting" + self.name
    sqm_daemon(self.name)
    print "Thread Stop" + self.name

  def stop(self): 
    daemon_exit_flag = True

def sqm_daemon(threadName): 
    daemon_exit_flag = False
    while not daemon_exit_flag:
      try:         
        if  myrrd.sqm.open_ser :
            if not  myrrd.lock_serial : 
                myrrd.read_sqm_current_data()
                time.sleep(15)
            else:   
                if myrrd.debug :
                     print "sqm_daemon() serial port is lock"
                     time.sleep(1)
 
        else:
            if myrrd.debug :
                print "sqm_daemon() wiat serial port open" 
                time.sleep(1)
      except:
        print "sqm_daemon() Serial port error"
        myrrd.sqm.open_ser = False
        myrrd.lock_serial = False
    threadName.exit()
     

#
# Init my class defaut is com open and debug off
#
sqm = mysqm.MySQM(port=serial_port,debug=debug) 
#
# Init MySQMMrrd class
#
myrrd = sqmrrd.MySQMrrd(port=serial_port, database=rrd_database, debug=debug )

if  not os.path.exists(rrd_database) :
    print "Create new rrd database"
    myrrd.create_database()
else : 
    print "Use old rrd database"


print "SQM daemon starting"  
mydaemon = sqmThread(sqm_daemon)
mydaemon.start()
print "OK"


#
# Web pages rendering
#
def init_page():
    return template( os.path.join(views_path, 'init.tpl'),
                     ports =  ports,
                     port = 'none'
                   )

#
# Main page
#
def main_page():
    return template( os.path.join(views_path, 'main.tpl'), 
                        port1  = '%03d' % myrrd.mpsas, 
                        port2  = '%03d' % myrrd.dmpsas,
                        port3  = '%03d' % myrrd.ir,
                        port4  = '%03d' % myrrd.vis, 
                    )
                    


def config_page():
    def _on_off(c):
        if (c == 1 ):
            return 'On'
        else:
            return 'Off'
    
    def _yes_no(c):
        if (c == 'Y'):
            return 'Yes'
        else: 
            return 'No'
    while myrrd.lock_serial :
        if debug :
            print "config_page() serial is lock"
            time.sleep(1)
    myrrd.lock_serial = True
    s = sqm.read_config().split(',')
    myrrd.lock_serial = False
    m_offset = float(s[1].split('m')[0])
    t_offest = float(s[2].split('C')[0])
    tc       = s[3].split(':')[1]
    oled     = int(s[5][0:1])
    dimmer   = int(s[5][1:2])
    contras  = int(s[6].split(':')[1])
    return template( os.path.join(views_path, 'config.tpl'),
                        moffset  = m_offset,
                        moffset_s  = '%6.2f' % m_offset,
                        toffset  =  t_offest,
                        toffset_s  = '%5.1f' % t_offest,
                        tc       = _yes_no(tc),
                        oled     = _on_off(oled),
                        dimmer   = _on_off(dimmer),
                        contras  = '%d' % contras
                    )

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
         return template( os.path.join(views_path, 'wait.tpl'))
        return main_page()
    return init_page()

@app.route('/main', method='POST') 
def do_main():
    form_id=request.forms.get('id')
    print form_id
    if form_id == 'port1':
        oled_off = int(request.forms.get('sled'))
        

@app.route('/DSLRtimer')
def info():
    """info page"""
    return info_page()

@app.route('/DSLRtimer', method='POST')
def do_info():
    """info page"""
    form_id=request.forms.get('id')
    if form_id == 'contras':
        sqm.set_oled_contras(int(request.forms.get('scontras')))
    return info_page()

 
@app.route('/config')
def config():
   """config page"""	
   return config_page()

 
@app.route('/config', method='POST')
def do_config():
    """config page"""
    form_id=request.forms.get('id')
    return config_page()


###############################################################################
# Startup standalone server
###############################################################################

def main():
    """Start autostart profile if any"""
    run(app, host=args.host, port=args.port, quiet=args.verbose)
    logging.info("Exiting")


if __name__ == '__init__' or __name__ == '__main__':
    main()

