import time

try:
    import blue as ble
except ImportError:
    import ble

import bot

print("Pico BLE car ready: 1/2/3/4/8/9/0")

SPEED_LOW = 18000
SPEED_MID = 38000
SPEED_HIGH = 65535
IDLE_TIMEOUT_MS = 1000

current_speed = SPEED_MID
last_cmd = "0"
last_rx = time.ticks_ms()
bot.stop()


def execute_move(cmd, speed):
    if cmd == "1":
        bot.forward(speed)
    elif cmd == "2":
        bot.backward(speed)
    elif cmd == "3":
        bot.turn_left(speed)
    elif cmd == "4":
        bot.turn_right(speed)
    elif cmd == "8":
        bot.forward_left(speed)
    elif cmd == "9":
        bot.forward_right(speed)
    elif cmd == "0":
        bot.stop()


try:
    while True:
        buf = ble.read()
        now = time.ticks_ms()

        if buf:
            data = ble.buf_to_text(buf).strip()
            last_rx = now
            print("Cmd:", data, "Speed:", current_speed)

            if data in ["0", "1", "2", "3", "4", "8", "9"]:
                last_cmd = data
                execute_move(data, current_speed)
            elif data in ["5", "6", "7"]:
                if data == "5":
                    current_speed = SPEED_LOW
                elif data == "6":
                    current_speed = SPEED_MID
                elif data == "7":
                    current_speed = SPEED_HIGH
                execute_move(last_cmd, current_speed)

        elif last_cmd != "0" and time.ticks_diff(now, last_rx) > IDLE_TIMEOUT_MS:
            print("BLE timeout: stop")
            last_cmd = "0"
            bot.stop()

        time.sleep_ms(20)
except KeyboardInterrupt:
    bot.stop()
    print("Stopped")
