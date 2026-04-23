# import mangoblock                 # 原 MangoBlock 套件（實際未使用）
# import board                      # MangoBlock 板定義（未使用）
import time                       # 延遲用
from machine import Pin, UART, Timer  # UART 用於 BLE

# 初始化 BLE UART：UART0 (TX=GP0, RX=GP1)
ble = UART(0, baudrate = 115200, tx = Pin(0), rx = Pin(1))

# BLE UUID 設定命令（為 MangoBlock 模組專用 AT 指令）
sv_cmd_uuid = b'AT+U0'+"FFA0" + '\r\n'
tx_cmd_uuid = b'AT+U1'+"FFA1" + '\r\n'
rx_cmd_uuid = b'AT+U2'+"FFA2" + '\r\n'
no_cmd_uuid = b'AT+U3'+"FFA3" + '\r\n'

def send(txt):
    ble.write(txt)               # 傳送資料至 BLE 模組

def read():
    if ble.any():                # 若有收到資料
        buf = ble.read()         # 讀取 bytes
        return buf
    return None                  # 無資料回傳 None

def buf_to_text(buf):
    data = buf.decode('utf-8').strip()  # 將 bytes 轉字串並去空白
    return data

# 更新 BLE 的 UUID（通常只需一次，不常用）
def update_uuid():
    send(sv_cmd_uuid)
    time.sleep(1)
    send(tx_cmd_uuid)
    time.sleep(1)
    send(rx_cmd_uuid)
    time.sleep(1)
    send(no_cmd_uuid)
    time.sleep(1)

# 更新 BLE 廣播名稱
def update_ble_name(name):
    data = b'AT+BM'+name+'\r\n'  # MangoBlock 名稱設定格式
    send(data)
    time.sleep(1)
