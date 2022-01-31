#!/bin/bash


# DSLR TIMER ONLY for ASiair Pro uncommet next line
# mode="D"


cd /home/pi/web
[ x${mode} != "xD" ] && sudo ./main.py      1>/tmp/pwr.log 2>&1
[ x${mode} == "xD" ] && sudo ./main.py -d Y 1>/tmp/pwr.log 2>&1
