# 檔案：rcbot.py
import time
import blue
import bot

print("Pico BLE Ready")

# --- 速度參數 ---
SPEED_LOW  = 18000
SPEED_MID  = 38000
SPEED_HIGH = 65535

current_speed = SPEED_MID
last_cmd = "0"  # [新增] 用來記憶目前車子的動作狀態

# 定義一個 helper 函式，用來執行動作
def execute_move(cmd, speed):
    if cmd == "1": bot.forward(speed)
    elif cmd == "2": bot.backward(speed)
    elif cmd == "3": bot.turn_left(speed)
    elif cmd == "4": bot.turn_right(speed)
    elif cmd == "8": bot.forward_left(speed)   # 斜向
    elif cmd == "9": bot.forward_right(speed)  # 斜向
    elif cmd == "0": bot.stop()

while True:
    buf = blue.read()
    if buf:
        data = blue.buf_to_text(buf).strip()
        print(f"Cmd: {data} | Speed: {current_speed}")

        # --- 情況 A：收到方向指令 ---
        if data in ["0", "1", "2", "3", "4", "8", "9"]:
            last_cmd = data  # 記住這個動作
            execute_move(data, current_speed)
        
        # --- 情況 B：收到變速指令 ---
        elif data in ["5", "6", "7"]:
            # 1. 更新速度變數
            if data == "5": current_speed = SPEED_LOW
            elif data == "6": current_speed = SPEED_MID
            elif data == "7": current_speed = SPEED_HIGH
            
            # 2. [關鍵] 立刻用新速度重新執行「上一個動作」
            # 這樣車子就會在移動中直接改變速度，不用停下來
            print(f">> 即時變速: {current_speed}")
            execute_move(last_cmd, current_speed)