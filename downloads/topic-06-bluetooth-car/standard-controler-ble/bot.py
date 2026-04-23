from machine import Pin     # 控制 GPIO
import time                 # 雖未使用，但可保留

# 小車馬達腳位（與你 USB 測試結果一致）
M1_A = Pin(12, Pin.OUT)     # 左馬達 A 相
M1_B = Pin(13, Pin.OUT)     # 左馬達 B 相
M2_A = Pin(10, Pin.OUT)     # 右馬達 A 相
M2_B = Pin(11, Pin.OUT)     # 右馬達 B 相

def stop():
    # 四個腳位都設成 0 → 馬達停止
    M1_A.value(0); M1_B.value(0)
    M2_A.value(0); M2_B.value(0)

def forward():
    # 左右兩個馬達都正轉
    M1_A.value(1); M1_B.value(0)
    M2_A.value(1); M2_B.value(0)

def backward():
    # 左右兩個馬達都反轉
    M1_A.value(0); M1_B.value(1)
    M2_A.value(0); M2_B.value(1)

def turn_left():
    # 左輪反轉 + 右輪前進 → 原地左轉
    M1_A.value(0); M1_B.value(1)
    M2_A.value(1); M2_B.value(0)

def turn_right():
    # 左輪前進 + 右輪反轉 → 原地右轉
    M1_A.value(1); M1_B.value(0)
    M2_A.value(0); M2_B.value(1)
