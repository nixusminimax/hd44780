#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#############################

import subprocess

##########################
# config file for hd44780.py
# jks 29/4/2015
# Feedback & Updates: http://forums.slimdevices.com/showthread.php?103577-Ank%FCndigung-Raspberry-amp-squeezelite-gt-hd44780-mit-deutschen-Umlauten-%28beta%29&p=816972#post816972

#########################


#Variables 2 modify: 
## The IP from your logitechmediaserver
## lms = '192.168.199.11'
##
## if you want squeezelite to find Logitech Media Server (lms):
## uncomment the following line.
## lms = subprocess.check_output("netstat |grep '3483'|cut -d ' ' -f21|cut -d':' -f1|tr -d '\n'", shell=True)
lms = subprocess.check_output("netstat |grep '3483'|cut -d ' ' -f21|cut -d':' -f1|tr -d '\n'", shell=True)

## The MAC Adress from your Raspberry
## You should set mac static eg. mac = '80:1f:02:f7:ca:fe'
## Since there are to many variants which mac is used
## (you can even use a fake mac for squeezelite session)
##
## I recommend for now "set it static and change the value 
## after changing sd card or the Wlanstick!"
## Otherwise the Display wont powered on or fetches the wrong information.
## 
## mac = 'ne:ed:mo:re:ca:fe'
mac = 'ch:an:ge:co:nf:ig'


## cliport is the port used by the commandlineinterface from lms
## If you didnt changed it: cliport = 9090 should be ok.
## if you unsure, look @ http://your.lms.server:9000/plugins/CLI/settings/basic.html?
cliport = 9090

## if raspberry should act as clock while not playing:
## For example:
## act_as_clock = 'forever' #means lcd Backlight is always on.
## act_as_clock = 300 #means lcd Backlight is switched off after 300 secs (=5min) not playing or powered off in the WEBUI.
## act_as_clock = '' #means lcd Backlight is switched off ASAP.
#act_as_clock = 'forever'
#act_as_clock = 30
#act_as_clock = ''
act_as_clock = 60

## want you see a counter on the last line from the lcd until the Display goes off?
## c0unter = 'y' # enables the counter
## c0unter = ''  # disable it
c0unter = 'y'


## GPIO <-> HD44780 LCD wiring
## using BCM GPIO counting
## change your wiring or the values
## or the values to your wiring.
## Its up to you ;-)
## But please check double !!!
lcd_RS = 7
lcd_E  = 8
lcd_data4 = 25
lcd_data5 = 24
lcd_data6 = 23
lcd_data7 = 18
lcd_light = 10

# HD44780 Specs
# since there are 10x1; 10x2; 16x2; 16x4; 20x2; 20x4; 40x2 and even 40x4 LCDs aviable
# change the values to match your setup
# i recommend  20x4 for best WAF experience ;-)

lcd_width = 20
lcd_lines = 4

##################
# dont change !
# These are the  default values
# for all the HD44780 controllers.
# If your LCD has only 2 rows the
# last 2 just wont be used in the
# main application.

lcd_line_1 = 0x80
lcd_line_2 = 0xC0
lcd_line_3 = 0x94
lcd_line_4 = 0xD4
lcd_chr = True
lcd_cmd = False
E_delay = 0.00005
E_pulse = 0.00005
