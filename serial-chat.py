# From "machine" library, only import classes: "UART", and "Pin"   |   UART is for serial communication   |   Pin lets you refer to GPIO pins such as GP8 and GP9
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

# Keep-alive timer
last_keep_alive = time.ticks_ms()
keep_alive_interval = 5000

# Keep checking for incoming serial data 
while True:
    if uart.any():

        # Read any available data from the other Pico
        data = uart.read()

        # Only print if something was actually received   | If something was recieved, also decode it when displaying
        if data is not None:
            print("Received:", data.decode("utf-8"))
    # Check if the local user typed a message
    if poll.poll(0):
        message = sys.stdin.readline().strip()

        if message:
            uart.write(message)
            print("You:", message)
            
            # Restart keep-alive timer after a real message is sent
            last_keep_alive = time.ticks_ms()

    # Send a keep-alive message every 5 seconds
    if time.ticks_diff(time.ticks_ms(), last_keep_alive) >= keep_alive_interval:

        current_time = time.localtime()

        keep_alive = (
            "KEEP ALIVE "
            # current_time[3] = hour
            + str(current_time[3]).zfill(2)
            + ":"
            # current_time[4] = minute
            + str(current_time[4]).zfill(2)
            + ":"
            # current_time[5] = second
            + str(current_time[5]).zfill(2)
        )

        uart.write(keep_alive)

        last_keep_alive = time.ticks_ms()
    # Prevent the loop from running too fast
    time.sleep_ms(50) 