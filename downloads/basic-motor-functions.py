from machine import Pin

# Raspberry Pi Pico 小車基本動作函式

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)


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


def backward():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, -1)


def turn_left():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, 1)


def turn_right():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, -1)


stop()
