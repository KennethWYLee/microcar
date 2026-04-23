import blue        # 匯入您的 blue.py
import time

print("======== 開始更改晶片設定 ========")

# 1. 修改廣播名稱
new_name = "PicoCarKenneth2"
print(f"1. 正在將名稱改為: {new_name}")
blue.update_ble_name(new_name)
time.sleep(1)  # 等待寫入

# 2. 修改 UUID (這是之前缺少的步驟)
# 根據您的 blue.py，這會將 UUID 設定為 FFA0
print("2. 正在修改 Service UUID 為 FFA0...")
blue.update_uuid() 
time.sleep(1)

print("==================================")
print("✅ 指令皆已發送！")
print("⚠️ 關鍵步驟：請現在「拔掉 USB 線」")
print("⚠️ 等待 3 秒後再重新插上，設定才會生效！")