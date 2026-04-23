import time                # 用於 sleep
import blue                 # 匯入自訂 BLE 模組（blue.py）
import bot                 # 匯入馬達控制（bot.py）

print("Pico BLE 小車模式：等待 1/2/3/4/0 指令")

while True:
    buf = blue.read()       # 從藍牙 UART 讀取資料 （若無資料則 return None）
    if buf:
        data = blue.buf_to_text(buf).strip()   # 轉成字串並去除換行
        print("收到 BLE:", data)

        # 以下為指令對應動作
        if data == "1":
            bot.forward()      # 前進
        elif data == "2":
            bot.backward()     # 後退
        elif data == "3":
            bot.turn_left()    # 左轉
        elif data == "4":
            bot.turn_right()   # 右轉
        elif data == "0":
            bot.stop()         # 停止
