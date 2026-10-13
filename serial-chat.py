# From "machine" library, only import moduals "UART", and "Pin"   |   UART is for serial communication   |   Pin lets you refer to GPIO pins such as GP8 and GP9
from machine import UART, Pin
import time
import sys
import select

# Set up UART channel 1 for serial communication.
# Use GP8 to send data, GP9 to receive data, at 9600 baud.
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Use 8 data bits, no parity bit, and 1 stop bit.
uart.init(bits=8, parity=None, stop=1)

# Watch for keyboard input without stopping the whole program
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# Keep checking for incoming serial data 
while True:
    if uart.any():

        # Read any available data from the other Pico
        data = uart.read()

        # Only print if something was actually received
        if data is not None:
            print("Received:", data)
    # Check if the local user typed a message
    if poll.poll(0):
        message = sys.stdin.readline().strip()

        if message:
            uart.write(message)
            print("You:", message)
            