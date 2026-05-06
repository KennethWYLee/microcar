from machine import Pin, PWM

FREQUENCY = 1000

right_a = PWM(Pin(12))
right_b = PWM(Pin(13))
left_a = PWM(Pin(11))
left_b = PWM(Pin(10))

for pwm in (right_a, right_b, left_a, left_b):
    pwm.freq(FREQUENCY)

LEFT_POLARITY = -1
RIGHT_POLARITY = -1


def _duty(speed):
    speed = abs(speed)
    if speed <= 100:
        return int(speed / 100 * 65535)
    return min(65535, int(speed))


def _set_motor(a_pwm, b_pwm, value):
    if value > 0:
        a_pwm.duty_u16(_duty(value))
        b_pwm.duty_u16(0)
    elif value < 0:
        a_pwm.duty_u16(0)
        b_pwm.duty_u16(_duty(value))
    else:
        a_pwm.duty_u16(0)
        b_pwm.duty_u16(0)


def drive(left, right):
    _set_motor(left_a, left_b, left * LEFT_POLARITY)
    _set_motor(right_a, right_b, right * RIGHT_POLARITY)


def stop():
    drive(0, 0)


def forward(speed=40):
    drive(speed, speed)


def backward(speed=40):
    drive(-speed, -speed)


def turn_left(speed=40):
    drive(-speed, speed)


def turn_right(speed=40):
    drive(speed, -speed)


def forward_left(speed=40):
    drive(speed * 0.25, speed)


def forward_right(speed=40):
    drive(speed, speed * 0.25)


stop()
