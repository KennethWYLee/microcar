import time
from mango import RUS04
from mango import utils

# 初始化超音波距離感測器與 RGB LED
sensor = RUS04(sensor_pin=15, rgb_pin=14)
sensor.rgb_all((255, 0, 0))

# 重複量測 500 次
for i in range(500):
    dist = sensor.ping()
    print(f'distance = {dist} cm')

    if dist < 10:
        sensor.rgb_all(utils.COLOR_RED)
    elif 10 <= dist < 20:
        sensor.rgb_all(utils.COLOR_BLUE)
    else:
        sensor.rgb_all(utils.COLOR_GREEN)

    time.sleep(0.1)  # 100 毫秒

# 關閉感測器
sensor.rgb_close()
