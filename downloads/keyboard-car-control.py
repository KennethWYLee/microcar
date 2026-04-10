from machine import Pin, PWM
import time

# 左右馬達
m1a = PWM(Pin(8))
m1b = PWM(Pin(9))
m2a = PWM(Pin(10))
m2b = PWM(Pin(11))

def stop():
    m1a.duty_u16(0)
    m1b.duty_u16(0)
    m2a.duty_u16(0)
    m2b.duty_u16(0)

def forward(speed=30):
    duty = int(speed / 100 * 65535)
    m1a.duty_u16(duty)
    m1b.duty_u16(0)
    m2a.duty_u16(duty)
    m2b.duty_u16(0)

def backward(speed=30):
    duty = int(speed / 100 * 65535)
    m1a.duty_u16(0)
    m1b.duty_u16(duty)
    m2a.duty_u16(0)
    m2b.duty_u16(duty)

def turn_left(speed=30):
    duty = int(speed / 100 * 65535)
    m1a.duty_u16(0)
    m1b.duty_u16(duty)
    m2a.duty_u16(duty)
    m2b.duty_u16(0)

def turn_right(speed=30):
    duty = int(speed / 100 * 65535)
    m1a.duty_u16(duty)
    m1b.duty_u16(0)
    m2a.duty_u16(0)
    m2b.duty_u16(duty)
