from machine import Pin
import time

# Topic 3 warm-up: read two line sensor values
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

print("Line sensor warm-up")
print("black = 1, white = 0")

while True:
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    print("left =", left_value, "right =", right_value)
    time.sleep(0.1)
