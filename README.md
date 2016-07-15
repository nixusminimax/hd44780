# hd44780
drive your hd44780 lcd on a RPi witch squeezelite to show the actual playing Artist/Titel/Album/Genre

These Scripts are beeing used:

/etc/inid.d/
hd44780     The System V init script - sorry i dont like systemd


/opt/hd44780/
config.py 	The Configuration File to match your gpio/network/lcd width & high settings

hd44780.py 	The LCD script itself

lcd.py 	    A simple feedback Script for the backlight state.

wheel.py    Control your Player with a Mouse [<<] [|>] [>>] [volume up] [volume down]
