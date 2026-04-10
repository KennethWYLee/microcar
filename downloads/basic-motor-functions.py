# main.py  -- Pico 小車：最簡易硬體測試版（用 w/s/a/d/x 控制）
from machine import Pin
import sys
import time

# ===== 馬達腳位（依你的接線） =====
M1_A = Pin(12, Pin.OUT)   # 馬達 1 A
M1_B = Pin(13, Pin.OUT)   # 馬達 1 B
M2_A = Pin(10, Pin.OUT)   # 馬達 2 A
M2_B = Pin(11, Pin.OUT)   # 馬達 2 B

LED = Pin(25, Pin.OUT)    # 板載 LED

def _set_motor(pin_a, pin_b, v):
    """v: -1(反轉), 0(停), 1(正轉)"""
    if v > 0:
        pin_a.value(1); pin_b.value(0)
    elif v < 0:
        pin_a.value(0); pin_b.value(1)
    else:
        pin_a.value(0); pin_b.value(0)

def stop_all():
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

print("Pico 小車測試：請在 Thonny Shell 輸入 w/s/a/d/x")
print("w=前進, s=後退, a=左轉, d=右轉, x=停止")

stop_all()
LED.off()

while True:
    ch = sys.stdin.read(1)  # 從 USB 讀字元
    if not ch:
        continue

    ch = ch.lower()

    if ch == 'w':
        print("前進")
        forward()
    elif ch == 's':
        print("後退")
        backward()
    elif ch == 'a':
        print("左轉")
        turn_left()
    elif ch == 'd':
        print("右轉")
        turn_right()
    elif ch == 'x':
        print("停止")
        stop_all()
    else:
        print("未知指令:", ch)

    LED.toggle()
    time.sleep(0.1)
