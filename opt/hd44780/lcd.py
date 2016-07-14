# !/usr/bin/env python
#############################

#
# initial release 27/4/2016
# Revision 27-04-2016
# jks

# Imports
import config
import RPi.GPIO as GPIO


# setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # using BCM GPIO counting
GPIO.setup(config.lcd_light, GPIO.OUT)

if GPIO.input(config.lcd_light) == GPIO.HIGH:
    # LED an
    print "LCD Backlight on"

if GPIO.input(config.lcd_light) == GPIO.LOW:
   # LED aus
   print "LCD Backlight off"
   #GPIO.output(config.lcd_light, GPIO.HIGH)
