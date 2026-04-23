from machine import Pin
import time

# Raspberry Pi Pico microcar motor calibration
# Course pin map:
#   right motor M1 = GP12 / GP13
#   left motor M2  = GP11 / GP10

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

# If one side moves backward during the forward test, change 1 to -1.
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


tests = [
    ("right wheel forward", 0, 1),
    ("left wheel forward", 1, 0),
    ("car forward", 1, 1),
    ("car backward", -1, -1),
    ("turn left in place", -1, 1),
    ("turn right in place", 1, -1),
]

print("Motor calibration start")
print("If a direction is wrong, press Ctrl+C and edit RIGHT_SIGN or LEFT_SIGN.")

for label, left, right in tests:
    print(label)
    drive(left, right)
    time.sleep(1.2)
    stop()
    time.sleep(0.8)

print("Motor calibration done")
stop()
