# 檔案：bot.py
from machine import Pin, PWM
import time

FREQUENCY = 1000

# 根據您之前的測試修正的腳位
m1_a_pwm = PWM(Pin(13))
m1_b_pwm = PWM(Pin(12))
m2_a_pwm = PWM(Pin(10))
m2_b_pwm = PWM(Pin(11))

m1_a_pwm.freq(FREQUENCY)
m1_b_pwm.freq(FREQUENCY)
m2_a_pwm.freq(FREQUENCY)
m2_b_pwm.freq(FREQUENCY)

def stop():
    m1_a_pwm.duty_u16(0)
    m1_b_pwm.duty_u16(0)
    m2_a_pwm.duty_u16(0)
    m2_b_pwm.duty_u16(0)

def forward(speed):
    m1_a_pwm.duty_u16(speed)
    m1_b_pwm.duty_u16(0)
    m2_a_pwm.duty_u16(speed)
    m2_b_pwm.duty_u16(0)

def backward(speed):
    m1_a_pwm.duty_u16(0)
    m1_b_pwm.duty_u16(speed)
    m2_a_pwm.duty_u16(0)
    m2_b_pwm.duty_u16(speed)

def turn_left(speed):
    m1_a_pwm.duty_u16(speed)
    m1_b_pwm.duty_u16(0)
    m2_a_pwm.duty_u16(0)
    m2_b_pwm.duty_u16(speed)

def turn_right(speed):
    m1_a_pwm.duty_u16(0)
    m1_b_pwm.duty_u16(speed)
    m2_a_pwm.duty_u16(speed)
    m2_b_pwm.duty_u16(0)

# --- 斜向移動 (差速控制) ---
def forward_left(speed):
    # 左前：右輪快，左輪慢(20%)
    inner = int(speed * 0.2)
    m1_a_pwm.duty_u16(speed)
    m1_b_pwm.duty_u16(0)
    m2_a_pwm.duty_u16(inner)
    m2_b_pwm.duty_u16(0)

def forward_right(speed):
    # 右前：左輪快，右輪慢(20%)
    inner = int(speed * 0.2)
    m1_a_pwm.duty_u16(inner)
    m1_b_pwm.duty_u16(0)
    m2_a_pwm.duty_u16(speed)
    m2_b_pwm.duty_u16(0)