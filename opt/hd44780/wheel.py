import config
from evdev import InputDevice
from select import select
import socket
import subprocess
import sys
import telnetlib
import time

## mousedetection
my_mouse = subprocess.check_output("grep 'mouse' /proc/bus/input/devices |cut -d ' ' -f3 |tr '\r\n' ' ' ", shell=True)
my_mouse = my_mouse.replace(" ", "")

if my_mouse == '':
   print "no mouse detected"
   sys.exit(0)

dev = evdev.InputDevice('/dev/input/' + (my_mouse))


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

def lms_set_value(mac,set,value):
    tn = telnetlib.Telnet(config.lms, config.cliport)
    print (config.mac + " " + set + " " + value + " \n")
    tn.write(config.mac + " " + set + " " + value + " \n")
    tn.write("exit\n")    
    

while True:
       info = ['mixer volume']
       for question in info:
               if not lms_unaviable():
                  r,w,x = select([dev], [], [])       
                  answer = lms_feedback(config.mac,question)
                  for event in dev.read():
                      #Wheel spinning
                      if event.code == 8:
                         vol = int(answer)
                         #Volume Down
                         if event.value == -1: 
                             if vol >= 80:
                                vol = vol - 2
                             elif vol >= 50:
                                vol = vol - 10
                                   
                             if vol != 0:
                                vol = vol -5
                             new_vol = str(vol)                             
                             lms_set_value(config.mac,'mixer volume',new_vol) 
                         ##Volume Up
                         elif event.value == 1:
                             if vol <= 50:
                                vol = vol +10
                             elif vol <= 80:
                                vol = vol +5
                             elif vol != 100:
                                vol = vol + 1
                             new_vol = str(vol)
                             lms_set_value(config.mac,'mixer volume',new_vol)
                                                                               
                      #Left Button pressed
                      elif event.code == 272 and event.value == 1:
                           lms_set_value(config.mac,'playlist index','-1')
                      #Right Button pressed       
                      elif event.code == 273 and event.value == 1:
                           lms_set_value(config.mac,'playlist index','+1')
                      # Mouse Wheel pressed
                      elif event.code == 274 and event.value == 1:
                           lms_set_value(config.mac,'pause', '')
                           #prevent to pause and unpause when the wheel is pressed a long time
                           time.sleep (2)                                                     
                             
