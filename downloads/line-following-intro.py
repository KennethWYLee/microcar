from machine import Pin
import time

# Topic 3: line following intro
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

RIGHT_SIGN = 1
LEFT_SIGN = 1

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


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


def forward():
    drive(1, 1)


def turn_left():
    drive(-1, 1)


def turn_right():
    drive(1, -1)


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
