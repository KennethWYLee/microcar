from machine import Pin

# Raspberry Pi Pico 小車基本動作函式

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

RIGHT_SIGN = 1
LEFT_SIGN = 1


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


def backward():
    drive(-1, -1)


def turn_left():
    drive(-1, 1)


def turn_right():
    drive(1, -1)


stop()
