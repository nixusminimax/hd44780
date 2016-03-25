# !/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#############################

# Working Beta
# initial release 29/4/2015
# Revision 15-01-2016
# jks

# Imports
import config
import sys
reload(sys)
sys.setdefaultencoding('iso-8859-1')
import subprocess
import telnetlib                                        
from time import sleep 
import time
import textwrap
import RPi.GPIO as GPIO
from uuid import getnode as get_mac
import unicodedata
import signal
import socket

#Variables 2 modify:
#change the values in the config.py

if config.mac == 'ch:an:ge:co:nf:ig':
   print "please update /opt/hd44780/config.py to match your setup"
   print "have fun and report errors to:"
   exit

################################################
###  Heres comes the main programm code      ###
###  please backup before changing here.     ###
################################################

# Variables 4 runtime (ALL MODE)
album = ''
albumA = ''
albumB = ''
artist = ''
artistA = ''
artistB = ''
title = ''  
genre = ''  
power = 'off'
wait = 2
error = 0

# Variables 4 runtime (2 Rows only)
if config.lcd_lines == 2:
   show_artist = 'A'

GPIO.setmode(GPIO.BCM) # using BCM GPIO counting
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(config.lcd_E, GPIO.OUT)
GPIO.setup(config.lcd_RS, GPIO.OUT)
GPIO.setup(config.lcd_data4, GPIO.OUT)
GPIO.setup(config.lcd_data5, GPIO.OUT)
GPIO.setup(config.lcd_data6, GPIO.OUT)
GPIO.setup(config.lcd_data7, GPIO.OUT)
GPIO.setup(config.lcd_light, GPIO.OUT)

# HD44780 send
def lcd_byte(bits, mode):
    GPIO.output(config.lcd_RS, mode)
    GPIO.output(config.lcd_data4, False)
    GPIO.output(config.lcd_data5, False)
    GPIO.output(config.lcd_data6, False)
    GPIO.output(config.lcd_data7, False)
    if bits&0x10==0x10:
      GPIO.output(config.lcd_data4, True)
    if bits&0x20==0x20:
      GPIO.output(config.lcd_data5, True)
    if bits&0x40==0x40:
      GPIO.output(config.lcd_data6, True)
    if bits&0x80==0x80:
      GPIO.output(config.lcd_data7, True)
    time.sleep(config.E_delay)
    GPIO.output(config.lcd_E, True)
    time.sleep(config.E_pulse)
    GPIO.output(config.lcd_E, False)
    time.sleep(config.E_delay)
    GPIO.output(config.lcd_data4, False)
    GPIO.output(config.lcd_data5, False)
    GPIO.output(config.lcd_data6, False)
    GPIO.output(config.lcd_data7, False)
    if bits&0x01==0x01:
      GPIO.output(config.lcd_data4, True)
    if bits&0x02==0x02:
      GPIO.output(config.lcd_data5, True)
    if bits&0x04==0x04:
      GPIO.output(config.lcd_data6, True)
    if bits&0x08==0x08:
      GPIO.output(config.lcd_data7, True)
    time.sleep(config.E_delay)
    GPIO.output(config.lcd_E, True)
    time.sleep(config.E_pulse)
    GPIO.output(config.lcd_E, False)
    time.sleep(config.E_delay)

# HD44780 write lines
def lcd(lcd_line,text):
    if lcd_line == 1:
        lcd_byte(config.lcd_line_1, config.lcd_cmd)
    if lcd_line == 2:
        lcd_byte(config.lcd_line_2, config.lcd_cmd)
    if lcd_line == 3:
        lcd_byte(config.lcd_line_3, config.lcd_cmd)
    if lcd_line == 4:
        lcd_byte(config.lcd_line_4, config.lcd_cmd)
          
    message = text.ljust(config.lcd_width," ")
    for i in range(config.lcd_width):
        lcd_byte(ord(message[i]),config.lcd_chr)
        
# HD44780 init and clear
def lcd_init():
    lcd_byte(0x33,config.lcd_cmd)
    lcd_byte(0x32,config.lcd_cmd)
    lcd_byte(0x28,config.lcd_cmd)
    lcd_byte(0x0C,config.lcd_cmd)
    lcd_byte(0x06,config.lcd_cmd)
    lcd_byte(0x01,config.lcd_cmd)
    GPIO.output(10,True)
        
# HD44780 clear Display
def lcd_cls(speed):
    for line in range(1,config.lcd_lines+1):
        lcd(line,'')
        if speed == 'slow':
           sleep(.5)
        if speed == 'fast':
           sleep(0.3)
        if speed == 'fast':
           sleep(0.3)      
    sleep(1)
                
# HD44780 Backlight on/off
def lcd_backlight(what):
    GPIO.output(config.lcd_light, what)
   
## systemstuff
def handler(signum, frame):
    lcd_cls('fast')
    message = 'Shutting down...'
    points = 13
    while points < len(message)+1: 
       lcd(1,message[:points])
       sleep(1)
       points = points +1
    lcd_cls('fast')
    sys.exit()

## Textstuff
def center_text (Display_Lines,text):
    if config.lcd_width == 16:               
       centered = ("{0:^16}".format(text))
       return centered
    if config.lcd_width == 20:             
       centered = ("{0:^20}".format(text))
       return centered
    
## Logitechmediaserverstuff
def lms_unaviable():  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((config.lms,config.cliport))
    return result
    
def lms_feedback(mac,question):
    tn = telnetlib.Telnet(config.lms, config.cliport)    
    tn.write(config.mac + " " + question + " ?\n")
    tn.write("exit\n")
    answer = tn.read_all()
    answer = answer.split("\n")[0]
    answer = answer.replace('%3A',':')
    answer = answer.replace(mac+" "+question+' ','')
    result = answer.replace(mac+" "+question,'')
    return result                                                    


###main
signal.signal(signal.SIGTERM, handler)    
lcd_init()
sleep (2)
lcd_cls('fast')
sleep (1)
lcd_init()

if lms_unaviable() and config.lcd_lines == 2:   
   lcd(1,'No Connection')
   lcd(2,'need help!')
   sleep(5)
   lcd(1,'LMS IS OFFLINE')                        

if lms_unaviable() and config.lcd_lines == 4:
        lcd(1,time.strftime("     %d.%m.%Y"))
        lcd(2,time.strftime("       %H:%M")) 
        lcd(3,'   searching LMS')
        lcd(4,'need support!')
        sleep(5)                                          
        lcd(1,'  '+config.myIP)
        lcd(3,'LMS IS OFFLINE')
print [config.lms]                
    
if not lms_unaviable() and config.lcd_lines == 4:
         lcd(1,time.strftime("     %d.%m.%Y"))
         lcd(2,time.strftime("       %H:%M"))
         lcd(3,'    connected to:')
         lcd(4,'   '+config.lms)
         sleep (1)
sleep (10)
lcd_cls('fast')
lcd_init()

if not lms_unaviable():
   error = 0
                         
try:
  while True:
    info = ['power', 'mode', 'time', 'artist', 'album', 'title', 'genre']
    for question in info:
        if not lms_unaviable():
           error = 0             
        else:
           if config.lcd_lines == 4:
              lcd(1,' \377 \377 \377\377\377 \377   \377\377\377')
              lcd(2,' \377 \377 \377__ \377   \377  \377')
              lcd(3,' \377=\377 \377   \377   \377\377\377') 
              lcd(4,' \377 \377 \377\377\377 \377\377\377 \377')
              sleep(3)
              lcd_cls('fast')
           
           lcd(1,' Connection Lost')
           lcd(2,config.lms)   
           sleep (2)
           lcd_backlight(False)
           sleep (1)
           lcd_backlight(True)
           error = error +1
           print error
           if error > 11:
              print error
              subprocess.call(['service hd44780 check_connection'], shell=True)
           if error > 10:
              print "should start here"
              subprocess.call(['sudo service hd44780 restart'], shell=True) 
           break
        answer = lms_feedback(config.mac,question)
                        
        if question == 'time':
           if answer == "0":
              power = 'off'
              break
        if question == 'mode':
           if answer != 'play':
              if answer == '%3F':
                 answer = 'check mac setting'
              answer = answer.upper()
              answer = 'Player: '+answer
              answer = center_text(config.lcd_width,answer)
              if config.lcd_lines == 2:
                 lcd(1,answer)
                 lcd(2,time.strftime("%d.%m.%Y  %H:%M"))
              else:
                 lcd(1,answer)
                 lcd(2,time.strftime("     %d.%m.%Y"))
                 lcd(3,time.strftime("       %H:%M")) 
                 lcd(4,'')
              sleep (3)
              break                
        if question == 'power':
           if answer == '1':
              #if config.lcd_lines == 4:
                 #lcd(4,' ')
              lcd_backlight(True)
              
           power = 'on'
           if answer == '':
              answer == '0'
           if answer == '0':
              answer = "Player offline"
              answer = center_text(config.lcd_width,answer)
              power = 'off'
              backlight_state = GPIO.input(config.lcd_light)
              
              ##act as clock:
              if config.act_as_clock != '' and type(config.act_as_clock) == int:
                 lcd(1,'') 
              else:
                 if config.lcd_lines == 2:
                    lcd(1,time.strftime("   %d.%m.%Y"))
                    lcd(2,time.strftime("      %H:%M"))
                 else:
                    lcd(1,answer)
                    lcd(2,time.strftime("     %d.%m.%Y"))
                    lcd(3,time.strftime("       %H:%M"))
                    lcd(4,'')
              
              if config.act_as_clock == 'forever':
                 break
              ###countdowncode          
              if backlight_state:
                 if config.act_as_clock != '' and type(config.act_as_clock) == int:
                    if not lms_unaviable():
                       modestate_now = lms_feedback(config.mac,'mode')
                       for counter in range(config.act_as_clock,1,-1):
                           counter = str(counter)
                           countdown = 'offline in ' +counter
                           countdown = center_text(config.lcd_width,countdown)
                           if config.lcd_lines == 2:
                              lcd(1,time.strftime(" %d.%M %H:%M"))
                              if config.c0unter == '':
                                 lcd(2,countdown)
                           else:
                              lcd(2,time.strftime("     %d.%m.%Y"))
                              lcd(3,time.strftime("       %H:%M"))
                              if config.c0unter == '':
                                 lcd(4,countdown)
                           if not lms_unaviable():
                              if modestate_now != lms_feedback(config.mac,'mode'):
                                 break
                           else:
                                 break                                 
                           sleep (.9)                         
                       if modestate_now == lms_feedback(config.mac,'mode'):
                           lcd_cls('fast')
                           lcd_backlight(False)
                           break
                 else:
                           lcd_backlight(False)
                           lcd_cls('fast')
                           break
              else:  
                    break
                    
        if question != 'power' and power != 'off':
           answer = answer.replace('~','-')
           answer = answer.replace('%20',' ')
           answer = answer.replace('%22','"')
           answer = answer.replace('%23','#')
           answer = answer.replace('%24', '\44')
           answer = answer.replace('%25', '\45')
           answer = answer.replace('%26','&')
           answer = answer.replace('%2B','+')
           answer = answer.replace('%2C','\54')
           answer = answer.replace('%2F','\57')
           answer = answer.replace('%3A','\72')
           answer = answer.replace('%3B', '\73')
           answer = answer.replace('%3C', '\74')
           answer = answer.replace('%3D', '\75')
           answer = answer.replace('%3E','\76')
           answer = answer.replace('%3F', '\77')
           answer = answer.replace('%5B','\133')
           answer = answer.replace('%5D','\135')
           answer = answer.replace('%5E','\136')        
           answer = answer.replace('%60','\47')
           answer = answer.replace("%C2%A5","'") 
           answer = answer.replace('%C2%A7', ' ')
           answer = answer.replace('%C3%A4', '\341')
           answer = answer.replace('%C3%A8', 'e')
           answer = answer.replace('%C3%A9', 'e')
           answer = answer.replace('%C3%AA', 'e')
           answer = answer.replace('%C3%AF', 'i')
           answer = answer.replace('%C3%B3','o')
           answer = answer.replace('%C3%84', '\341')
           answer = answer.replace('%C3%9F', '\342')
           answer = answer.replace('%C3%B1', '\356')
           answer = answer.replace('%C3%B6', '\357')
           answer = answer.replace('%C3%BB', 'u')
           answer = answer.replace('%C3%96', '\357')
           answer = answer.replace('%C3%9C', '\365')
           answer = answer.replace('%C3%BC', '\365')                     
           answer = answer.replace('%CC%81', '\27')
           answer = answer.replace('%CC%83', '')
           answer = answer.replace('%E2%80%B2','\47')
           answer = center_text(config.lcd_width,answer)
                                                 
           if question == 'artist':
              artistA = ''
              artistB = ''
              if len(answer.strip()) > config.lcd_width:
                 artist = textwrap.fill(answer, width=config.lcd_width)
                 artistA = artist.split('\n')[-0]
                 artistA = center_text(config.lcd_width,artistA)
                 artistB = artist.split('\n')[1]
                 artistB = center_text(config.lcd_width,artistB)
                 if config.lcd_lines == 4:
                    lcd(1,artistA)
                    lcd(2,artistB)
                    ## For better viewing (on the LCD NOT the code)
                    ## i decided to move the code for 2 rows 
                    ## to the title section.        
              else:   
                 artist = answer            
                 lcd(1,artist)
                 
           elif question == "title":
              title = answer
              if len(answer.strip()) > config.lcd_width:
                 answer = " " * config.lcd_width + answer + " "
                 slow = 0.25
                 for i in range(len(answer) + 1):
                     scroll = answer[i:i+config.lcd_width]
                     if i == config.lcd_width:
                        slow = 0.4
                     if config.lcd_lines == 2:
                        if artistA != '':
                           if slow == 0.25:
                              show_artist == 'A'
                              lcd(1,artistA)   
                           else:
                              lcd(1,artistB)                                                                                                               
                        lcd(2,scroll)
                     if config.lcd_lines == 4 and artistB == '':
                        lcd(2,scroll)
                     elif config.lcd_lines == 4 and artistB != '':
                        lcd(3,scroll)         
                     time.sleep(slow)
              else:
                     if config.lcd_lines == 2:
                        if artistA != '':
                           if show_artist == 'A':
                              lcd(1,artistA)
                              show_artist = 'B'
                           else:
                              lcd(1,artistB)
                              show_artist = 'A'                           
                        lcd(2,title)
                     if config.lcd_lines == 4 and artistB == '':
                        lcd(2,title)
                     if config.lcd_lines == 4 and artistB != '':
                        lcd(3,title)                           
           
           elif question == "album" and config.lcd_lines == 4:           
              albumA = ''
              albumB = ''
              if len(answer) > config.lcd_width:
                 album = textwrap.fill(answer, width=config.lcd_width)
                 albumA = album.split('\n')[-0]
                 albumA = center_text(config.lcd_width,albumA)
                 albumB = album.split('\n')[1]
                 albumB = center_text(config.lcd_width,albumB)
                 
                 if artistB == '':
                    lcd(3,albumA)
                    lcd(4,albumB)
                 if artistB != '':
                    lcd(4,albumA)
              
              if len(answer) <= config.lcd_width:
                 album = center_text(config.lcd_width,answer)
                 if artistB == '':
                    lcd(3,album)
                 else: 
                    lcd(4,album)     
           elif question == "genre" and config.lcd_lines == 4:
                genre = center_text(config.lcd_width,answer)   
                if artistB == '' and albumB == '':
                   lcd(4,genre)         
    sleep (wait)
      
except KeyboardInterrupt:
       lcd_cls('fast')
       lcd_backlight(False)
       
