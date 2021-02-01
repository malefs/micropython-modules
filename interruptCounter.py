# Source: https://techtutorialsx.com/2017/10/07/esp32-micropython-timer-interrupts/

from machine import Timer

count = 0

def handleInterrupt(timer):
  global count
  count += 1

# ESP32 has four hardware timers to choose from (0 through 3)
timer = Timer(0)

# period in milliseconds
timer.init(period=1000, mode=Timer.PERIODIC, callback=handleInterrupt)

# From REPL: import interruptCounter
# Watch the variable increment from the REPL with: print(interruptCounter.count)
# Stop with: interruptCounter.timer.deinit()

