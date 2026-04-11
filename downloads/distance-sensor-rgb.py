import time
from mango import RUS04
from mango import utils

# 主題 2：距離感測主程式
sensor = RUS04(sensor_pin=15, rgb_pin=14)
sensor.rgb_all((255, 0, 0))

for _ in range(500):
    dist = sensor.ping()
    print(f"distance = {dist} cm")

    if dist < 10:
        sensor.rgb_all(utils.COLOR_RED)
    elif 10 <= dist < 20:
        sensor.rgb_all(utils.COLOR_BLUE)
    else:
        sensor.rgb_all(utils.COLOR_GREEN)

    time.sleep(0.1)

sensor.rgb_close()
