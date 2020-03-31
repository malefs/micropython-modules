# Source: https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/experiment-4-i2c

import machine
import sys
import utime

#################################################################
# Parameters and Global Variables

# Pin Definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
repl_led = machine.Pin(5, machine.Pin.OUT)
sda_pin = machine.Pin(21)
scl_pin = machine.Pin(22)

# Create and I2C object out of our SDA and SCL pin objects
i2c = machine.I2C(sda=sda_pin, scl=scl_pin)

# TMP102 address on the I2C bus (set by manufacturer)
tmp102_addr = 0x48

# TMP102 register addresses
reg_temp = 0x00
reg_config = 0x01

#################################################################
# Functions

# Calculate the 2's complement of a number
def twos_comp(val, bits):
    if (val & (1 << (bits -1))) !=0:
        val = val - (1 << bits)
    return val

# Read temperature registers and calculate Celsius
def read_temp():

    # Read temperature registers
    val = i2c.readfrom_mem(tmp102_addr, reg_temp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    # Covert to 2's complement (temperatures can be negative)
    temp_c = twos_comp(temp_c, 12)

    # Convert registers value to temperature (C)
    temp_c = temp_c * 0.0625

    return temp_c

# Initialize communications with the TMP102
def init():

    # Read CONFIG register (2 bytes) and convert to integer list
    val = i2c.readfrom_mem(tmp102_addr, reg_config, 2)
    print("Old CONFIG:", val)
    val = list(val)

    # Set to 4Hz sampling (CR1, CR0 = 0b10)
    val[1] = val[1] & 0b00111111
    val[1] = val[1] | (0b10 << 6)

    # Write 4Hz sampling back to CONFIG
    i2c.writeto_mem(tmp102_addr, reg_config, bytearray(val))

    # Check that new config is in place
    val = i2c.readfrom_mem(tmp102_addr, reg_config, 2)
    print("New CONFIG:", val)

#################################################################
# Main script

# Initialize Communications with TMP102
init()

# Print out temperature every second
while True:

    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL")
        repl_led.value(1)
        sys.exit()

    # Read temperature and print it to the console
    celsius    = read_temp()
    fahrenheit = (celsius * 9/5) + 32

    celsius    = round(celsius, 2)
    fahrenheit = round(fahrenheit, 2)

    celsius    = "{:.2f}".format(celsius) + "C"
    fahrenheit = "{:.2f}".format(fahrenheit) + "F"

    print(celsius, fahrenheit)
    utime.sleep(1)

