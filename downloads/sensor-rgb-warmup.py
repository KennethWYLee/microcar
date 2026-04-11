import time
from mango import RUS04

# 主題 2：感測器的操控
# 先用最簡單的方式確認感測器模組與 RGB LED 可以正常工作

sensor = RUS04(sensor_pin=15, rgb_pin=14)

# 依序顯示紅、綠、藍三種顏色
sensor.rgb_all((255, 0, 0))
time.sleep(1)

sensor.rgb_all((0, 255, 0))
time.sleep(1)

sensor.rgb_all((0, 0, 255))
time.sleep(1)

# 結束前關閉 RGB LED
sensor.rgb_close()
