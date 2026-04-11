from machine import Pin
import time

# Raspberry Pi Pico 小車 1 hr Boot Camp
# 在 Thonny Shell 輸入 w / a / s / d / x 後按 Enter

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)
LED = Pin(25, Pin.OUT)


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


print("Raspberry Pi Pico 小車 Boot Camp")
print("請在 Thonny Shell 輸入 w / a / s / d / x 後按 Enter")
print("w=前進 s=後退 a=左轉 d=右轉 x=停止")

stop()
LED.off()

while True:
    command = input("Command (w/a/s/d/x): ").strip().lower()

    if command == "w":
        print("前進")
        forward()
    elif command == "s":
        print("後退")
        backward()
    elif command == "a":
        print("左轉")
        turn_left()
    elif command == "d":
        print("右轉")
        turn_right()
    else:
        print("停止")
        stop()

    LED.toggle()
    time.sleep(0.05)
