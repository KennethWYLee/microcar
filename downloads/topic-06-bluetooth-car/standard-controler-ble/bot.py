from machine import Pin

# GP12/GP13 = right motor, GP11/GP10 = left motor
right_a = Pin(12, Pin.OUT)
right_b = Pin(13, Pin.OUT)
left_a = Pin(11, Pin.OUT)
left_b = Pin(10, Pin.OUT)

LEFT_POLARITY = -1
RIGHT_POLARITY = -1


def _set_motor(pin_a, pin_b, value):
    if value > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif value < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(left_a, left_b, left * LEFT_POLARITY)
    _set_motor(right_a, right_b, right * RIGHT_POLARITY)


def stop():
    drive(0, 0)


def forward(speed=None):
    drive(1, 1)


def backward(speed=None):
    drive(-1, -1)


def turn_left(speed=None):
    drive(-1, 1)


def turn_right(speed=None):
    drive(1, -1)


def forward_left(speed=None):
    drive(0.3, 1)


def forward_right(speed=None):
    drive(1, 0.3)


stop()
