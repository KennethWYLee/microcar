from machine import Pin
import time

# Topic 3: line following intro
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def stop():
    _set_motor(M1_A, M1_B, 0)
    _set_motor(M2_A, M2_B, 0)


def forward():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, 1)


def turn_left():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, 1)


def turn_right():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, -1)


print("Line following intro")
print("left black + right black  -> forward")
print("left black + right white  -> turn left")
print("left white + right black  -> turn right")
print("left white + right white  -> stop")

while True:
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        forward()
        print("forward", left_value, right_value)
    elif left_value == 1 and right_value == 0:
        turn_left()
        print("left", left_value, right_value)
    elif left_value == 0 and right_value == 1:
        turn_right()
        print("right", left_value, right_value)
    else:
        stop()
        print("stop", left_value, right_value)

    time.sleep(0.05)
