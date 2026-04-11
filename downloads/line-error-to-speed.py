from machine import Pin
import time

# Topic 4 bridge: turn line sensor values into speed difference
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 10000

last_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        error = previous_error

    return left_value, right_value, error


print("Topic 4 bridge")
print("Observe sensor values, error, and left/right speed")

while True:
    left_value, right_value, error = read_error(last_error)
    correction = KP * error
    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    print(
        "left =", left_value,
        "right =", right_value,
        "error =", error,
        "left_speed =", left_speed,
        "right_speed =", right_speed,
    )

    last_error = error
    time.sleep(0.1)
