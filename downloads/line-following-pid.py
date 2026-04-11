from machine import Pin, PWM
import time

# Topic 5: simplified PID line following
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0
# This is a teaching version for two digital sensors.

FREQUENCY = 1000
BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 9500
KI = 900
KD = 4200
INTEGRAL_LIMIT = 4.0

RIGHT_FORWARD = PWM(Pin(13))
RIGHT_BACKWARD = PWM(Pin(12))
LEFT_FORWARD = PWM(Pin(10))
LEFT_BACKWARD = PWM(Pin(11))

for motor in (RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD):
    motor.freq(FREQUENCY)

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

last_error = 0.0
sum_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def clamp_integral(value):
    if value > INTEGRAL_LIMIT:
        return INTEGRAL_LIMIT
    if value < -INTEGRAL_LIMIT:
        return -INTEGRAL_LIMIT
    return value


def stop():
    RIGHT_FORWARD.duty_u16(0)
    RIGHT_BACKWARD.duty_u16(0)
    LEFT_FORWARD.duty_u16(0)
    LEFT_BACKWARD.duty_u16(0)


def drive_forward(left_speed, right_speed):
    LEFT_FORWARD.duty_u16(left_speed)
    LEFT_BACKWARD.duty_u16(0)
    RIGHT_FORWARD.duty_u16(right_speed)
    RIGHT_BACKWARD.duty_u16(0)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        if previous_error > 0:
            error = 1.5
        elif previous_error < 0:
            error = -1.5
        else:
            error = 0.0

    return left_value, right_value, error


print("PID line following")
print("correction = KP * error + KI * sum_error + KD * derivative")

while True:
    left_value, right_value, error = read_error(last_error)
    derivative = error - last_error
    sum_error = clamp_integral(sum_error + error)

    correction = KP * error + KI * sum_error + KD * derivative

    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    if left_value == 0 and right_value == 0 and last_error == 0:
        stop()
        print("stop", left_value, right_value, "error =", error)
    else:
        drive_forward(left_speed, right_speed)
        print(
            "left =", left_value,
            "right =", right_value,
            "error =", error,
            "sum_error =", round(sum_error, 2),
            "left_speed =", left_speed,
            "right_speed =", right_speed,
        )

    last_error = error
    time.sleep(0.03)
