import sys
import time
import bot

print("Shell car test: w/s/a/d/x, exit")
bot.stop()

try:
    while True:
        ch = sys.stdin.read(1)
        if not ch:
            continue
        ch = ch.lower()
        if ch == "w":
            print("forward")
            bot.forward()
        elif ch == "s":
            print("backward")
            bot.backward()
        elif ch == "a":
            print("left")
            bot.turn_left()
        elif ch == "d":
            print("right")
            bot.turn_right()
        elif ch == "x":
            print("stop")
            bot.stop()
        elif ch == "q":
            break
        time.sleep_ms(20)
finally:
    bot.stop()
    print("Stopped")
