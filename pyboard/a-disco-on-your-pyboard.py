# http://docs.micropython.org/en/latest/pyboard/tutorial/leds.html#a-disco-on-your-pyboard
#
# "import pyb" is called in boot.py
#
# screen /dev/ttyACM0

# There are 4 built-in LED's
leds = [pyb.LED(i) for i in range(1,5)]
for l in leds:
    l.off()

n = 0
try:
   while True:
      # The % sign is a modulus operator that keeps n between 0 and 3
      n = (n + 1) % 4
      leds[n].toggle()
      pyb.delay(50)

# If you hit Ctrl-C to stop the script, this turns off all the LED's
finally:
    for l in leds:
        l.off()
