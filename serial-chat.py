# From "machine" library, only import moduals "UART", and "Pin"   |   UART is for serial communication   |   Pin lets you refer to GPIO pins such as GP8 and GP9
from machine import UART, Pin
import time
import sys
import select

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)
