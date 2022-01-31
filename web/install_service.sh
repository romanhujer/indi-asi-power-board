#!/bin/bash


sudo cp pwrweb.service /lib/systemd/system/

sudo systemctl enable pwrweb

sudo systemctl start  pwrweb




