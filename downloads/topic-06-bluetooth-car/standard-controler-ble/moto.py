# main.py -- Pico 小車：最簡易硬體測試版（用 w/s/a/d/x 控制）
from machine import Pin          # 從 MicroPython 匯入 Pin 類別，用來控制 GPIO 腳位
import sys                       # 匯入 sys，用來讀取 USB 輸入
import time                      # 匯入 time，用來做延遲

# ===== 馬達腳位設定（依你的接線） =====
M1_A = Pin(12, Pin.OUT)          # 馬達1 的 A 相，輸出腳
M1_B = Pin(13, Pin.OUT)          # 馬達1 的 B 相，輸出腳
M2_A = Pin(10, Pin.OUT)          # 馬達2 的 A 相，輸出腳
M2_B = Pin(11, Pin.OUT)          # 馬達2 的 B 相，輸出腳

LED = Pin(25, Pin.OUT)           # Pico 板載 LED（GP25）

# 控制一個馬達的方向
def _set_motor(pin_a, pin_b, v):
    """v: -1 = 反轉, 0 = 停止, 1 = 正轉"""
    if v > 0:                    # 正轉
        pin_a.value(1)
        pin_b.value(0)
    elif v < 0:                  # 反轉
        pin_a.value(0)
        pin_b.value(1)
    else:                        # 停止
        pin_a.value(0)
        pin_b.value(0)

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
    _set_motor(M1_A, M1_B, -1)   # 左輪後退
    _set_motor(M2_A, M2_B, 1)    # 右輪前進

def turn_right():
    _set_motor(M1_A, M1_B, 1)    # 左輪前進
    _set_motor(M2_A, M2_B, -1)   # 右輪後退

print("Pico 小車測試：請在 Thonny Shell 輸入 w/s/a/d/x")
print("w=前進, s=後退, a=左轉, d=右轉, x=停止")

stop_all()                      # 啟動時先停止
LED.off()

while True:
    ch = sys.stdin.read(1)      # 從 USB 讀 1 個字元（阻塞）
    if not ch:
        continue                # 若沒讀到就繼續等

    ch = ch.lower()             # 轉小寫，避免大小寫問題

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

    LED.toggle()                # 收到任何指令就閃一下 LED
    time.sleep(0.1)
