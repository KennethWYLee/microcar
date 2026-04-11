import time
from mango import RUS04

# 主題 2：感測器操控暖身程式

sensor = RUS04(sensor_pin=15, rgb_pin=14)

sensor.rgb_all((255, 0, 0))
time.sleep(1)

sensor.rgb_all((0, 255, 0))
time.sleep(1)

sensor.rgb_all((0, 0, 255))
time.sleep(1)

sensor.rgb_close()
