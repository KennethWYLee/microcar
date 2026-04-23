# 01 入門延伸 Cases：平台、LED、按鈕與狀態控制

本篇延伸原教材第 1-30 頁，目標是讓學生從最小的硬體控制開始，逐步建立「輸出、輸入、判斷、狀態」的概念。所有案例都以 Raspberry Pi Pico / MicroPython 的 `machine.Pin` 為核心，並配合芒果機器人主板常用腳位。

參考資料：

- MicroPython `machine.Pin`：https://docs.micropython.org/en/latest/library/machine.Pin.html
- Raspberry Pi Pico Python SDK：https://datasheets.raspberrypi.com/pico/sdk/pico_python_sdk.pdf
- Raspberry Pi Pico MicroPython examples：https://github.com/raspberrypi/pico-micropython-examples
- MicroPython RP2 quick reference：https://docs.micropython.org/en/latest/rp2/quickref.html

## Case 1：內建 LED 閃爍

### 1. 要做的主題

讓 Pico 內建 LED 以固定節奏亮、滅，建立數位輸出的第一個概念。

### 2. 分階段逐步教學

**階段 A：認識輸出腳位**

LED 是輸出裝置，程式要先把腳位設定成 `Pin.OUT`。

**階段 B：讓 LED 亮與滅**

使用 `on()` 與 `off()` 控制高低電位。

**階段 C：加入時間**

使用 `time.sleep()` 讓亮滅可以被眼睛看見。

**階段 D：加入無限迴圈**

使用 `while True` 讓動作持續發生。

### 3. 完整程式碼

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

### 4. 最終成果展現

執行後，內建 LED 每 1 秒亮一次、每 1 秒滅一次，形成穩定閃爍。

### 5. 應用題與解答

**題目：** 請修改程式，讓 LED 快速閃 3 次後休息 2 秒，然後重複。

**解答：**

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

while True:
    for i in range(3):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)

    time.sleep(2)
```

## Case 2：LED 訊號節奏設計

### 1. 要做的主題

用陣列設計 LED 閃爍節奏，讓學生理解「資料可以控制行為」。

### 2. 分階段逐步教學

**階段 A：把閃爍時間放進陣列**

例如 `[0.1, 0.1, 0.5]` 代表短、短、長。

**階段 B：用 `for` 讀取節奏**

每次讀一個時間值，讓 LED 亮同樣長度。

**階段 C：加入休息時間**

每個節奏播放完後，讓 LED 停一小段。

**階段 D：形成重複訊號**

使用 `while True` 讓節奏不斷重複。

### 3. 完整程式碼

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

pattern = [0.15, 0.15, 0.15, 0.6]

while True:
    for duration in pattern:
        led.on()
        time.sleep(duration)
        led.off()
        time.sleep(0.15)

    time.sleep(1)
```

### 4. 最終成果展現

LED 會依照「短、短、短、長」的節奏閃爍。這可以當成小車待機或警示訊號。

### 5. 應用題與解答

**題目：** 設計一個「啟動倒數」燈號：先慢閃 3 次，再快速閃 5 次。

**解答：**

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

while True:
    for i in range(3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

    for i in range(5):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

    time.sleep(2)
```

## Case 3：按鈕即時控制 LED

### 1. 要做的主題

讀取板載按鈕，按下時 LED 亮，放開時 LED 滅。

### 2. 分階段逐步教學

**階段 A：宣告輸入與輸出**

LED 是輸出，按鈕是輸入。

**階段 B：讀取按鈕值**

用 `btn.value()` 讀取 `0` 或 `1`。

**階段 C：用判斷式控制 LED**

如果按鈕值等於啟動值，就讓 LED 亮。

**階段 D：印出按鈕值**

先觀察按下與放開的數字，確認硬體邏輯。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

while True:
    value = btn.value()
    print("button =", value)

    if value == BUTTON_ACTIVE:
        led.on()
    else:
        led.off()

    time.sleep(0.1)
```

如果你的按鈕按下時讀到 `0`，把這行改成：

```python
BUTTON_ACTIVE = 0
```

### 4. 最終成果展現

按住按鈕時 LED 亮，放開按鈕時 LED 滅。學生可直接看到輸入如何影響輸出。

### 5. 應用題與解答

**題目：** 修改程式，讓按下按鈕時 LED 滅，放開時 LED 亮。

**解答：**

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

while True:
    if btn.value() == BUTTON_ACTIVE:
        led.off()
    else:
        led.on()

    time.sleep(0.1)
```

## Case 4：按鈕切換 LED 狀態

### 1. 要做的主題

讓按鈕從「按住才亮」變成「按一下切換一次狀態」。這是小車啟動/停止控制的基礎。

### 2. 分階段逐步教學

**階段 A：建立狀態變數**

用 `led_state` 記錄 LED 目前該亮或該滅。

**階段 B：偵測按下事件**

按鈕從沒按到按下時，才切換狀態。

**階段 C：加入防彈跳**

按鈕是機械開關，按下瞬間可能跳動，要加短暫延遲。

**階段 D：等待放開**

避免長按時連續切換多次。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

led_state = False

while True:
    if btn.value() == BUTTON_ACTIVE:
        led_state = not led_state

        if led_state:
            led.on()
        else:
            led.off()

        time.sleep_ms(250)

        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)

    time.sleep_ms(20)
```

### 4. 最終成果展現

按一下按鈕，LED 亮；再按一下，LED 滅。這種寫法可以直接延伸成「按一下啟動小車，再按一下停止」。

### 5. 應用題與解答

**題目：** 改成「LED 亮的時候慢閃，LED 關閉狀態時完全不亮」。

**解答：**

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

running = False
last_blink = time.ticks_ms()
led_level = False

while True:
    if btn.value() == BUTTON_ACTIVE:
        running = not running
        time.sleep_ms(250)
        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)

    if running:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) >= 500:
            led_level = not led_level
            led.value(1 if led_level else 0)
            last_blink = now
    else:
        led.off()

    time.sleep_ms(20)
```

## Case 5：短按與長按判斷

### 1. 要做的主題

判斷學生是短按還是長按按鈕。短按可用於切換模式，長按可用於重置或停止。

### 2. 分階段逐步教學

**階段 A：記錄按下時間**

按下時用 `time.ticks_ms()` 記錄起點。

**階段 B：等待放開**

按住期間持續等待。

**階段 C：計算按住多久**

使用 `time.ticks_diff()` 計算時間差。

**階段 D：根據時間決定動作**

短按切換 LED，長按快速閃爍 3 次。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1
LONG_PRESS_MS = 1000

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

led_state = False

def blink(times, delay_ms):
    for i in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

while True:
    if btn.value() == BUTTON_ACTIVE:
        start = time.ticks_ms()

        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)

        duration = time.ticks_diff(time.ticks_ms(), start)
        print("press ms =", duration)

        if duration >= LONG_PRESS_MS:
            blink(3, 120)
            led_state = False
        else:
            led_state = not led_state
            led.value(1 if led_state else 0)

        time.sleep_ms(200)

    time.sleep_ms(20)
```

### 4. 最終成果展現

短按按鈕會切換 LED 亮滅；長按超過 1 秒會快速閃 3 次並關閉 LED。這可延伸為小車的「短按啟動、長按緊急停止」。

### 5. 應用題與解答

**題目：** 將長按門檻改成 2 秒，並讓長按後 LED 長亮 2 秒再熄滅。

**解答：**

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1
LONG_PRESS_MS = 2000

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

while True:
    if btn.value() == BUTTON_ACTIVE:
        start = time.ticks_ms()

        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)

        duration = time.ticks_diff(time.ticks_ms(), start)

        if duration >= LONG_PRESS_MS:
            led.on()
            time.sleep(2)
            led.off()
        else:
            led.toggle()

        time.sleep_ms(200)
```

## Case 6：小車啟動前狀態燈

### 1. 要做的主題

設計小車啟動前的狀態控制：待機慢閃、按下後進入啟動狀態、再按一次回待機。

### 2. 分階段逐步教學

**階段 A：建立 `running` 狀態**

`False` 代表待機，`True` 代表啟動。

**階段 B：待機時慢閃**

讓學生理解非阻塞式計時，不要一直卡在 `sleep()`。

**階段 C：啟動時 LED 長亮**

代表小車可以開始進入下一階段任務。

**階段 D：按鈕切換狀態**

此架構可直接移植到避障車或循跡車。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

running = False
blink_on = False
last_blink = time.ticks_ms()

def wait_button_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

while True:
    if btn.value() == BUTTON_ACTIVE:
        running = not running
        print("running =", running)
        time.sleep_ms(250)
        wait_button_release()

    if running:
        led.on()
    else:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) >= 700:
            blink_on = not blink_on
            led.value(1 if blink_on else 0)
            last_blink = now

    time.sleep_ms(20)
```

## Case 7：按鈕中斷計數器

### 1. 要做的主題

使用 `Pin.irq()` 建立按鈕中斷，讓程式不需要一直卡在等待按鈕，也能在按下時記錄事件。

### 2. 分階段逐步教學

**階段 A：理解輪詢與中斷**

輪詢是程式一直問「按了嗎？」；中斷是按鈕事件發生時通知程式。

**階段 B：建立中斷處理函式**

中斷函式中不要做太複雜的工作，只設定旗標或計數。

**階段 C：加入簡單防彈跳**

用 `time.ticks_ms()` 避免一次按下被算成很多次。

**階段 D：主迴圈處理結果**

主迴圈看到按鈕次數改變後，再更新 LED。

### 3. 完整程式碼

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

press_count = 0
last_irq_time = 0

def button_irq(pin):
    global press_count, last_irq_time
    now = time.ticks_ms()
    if time.ticks_diff(now, last_irq_time) > 250:
        press_count += 1
        last_irq_time = now

btn.irq(trigger=Pin.IRQ_RISING, handler=button_irq)

last_count = -1

while True:
    if press_count != last_count:
        print("press count =", press_count)
        led.value(press_count % 2)
        last_count = press_count

    time.sleep_ms(50)
```

### 4. 最終成果展現

每按一次按鈕，Shell 會顯示累積次數；奇數次 LED 亮，偶數次 LED 滅。

### 5. 應用題與解答

**題目：** 改成每按滿 5 次，LED 快閃 5 下，然後重新計數。

**解答：**

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

press_count = 0
last_irq_time = 0
flash_request = False

def button_irq(pin):
    global press_count, last_irq_time, flash_request
    now = time.ticks_ms()
    if time.ticks_diff(now, last_irq_time) > 250:
        press_count += 1
        last_irq_time = now
        if press_count >= 5:
            flash_request = True

btn.irq(trigger=Pin.IRQ_RISING, handler=button_irq)

while True:
    if flash_request:
        flash_request = False
        press_count = 0
        for i in range(5):
            led.on()
            time.sleep_ms(120)
            led.off()
            time.sleep_ms(120)

    time.sleep_ms(50)
```

## Case 8：非阻塞式待機燈與按鈕模式

### 1. 要做的主題

讓 LED 持續慢閃，同時還能立即偵測按鈕，建立非阻塞式程式設計概念。

### 2. 分階段逐步教學

**階段 A：避免長時間 `sleep()`**

長時間 `sleep()` 會讓程式暫時無法處理按鈕。

**階段 B：使用 `ticks_ms()`**

用目前時間和上次閃爍時間相減，判斷是否該切換 LED。

**階段 C：建立模式**

`mode = 0` 慢閃，`mode = 1` 長亮，`mode = 2` 快閃。

**階段 D：按鈕切換模式**

每按一次切換到下一個模式。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

mode = 0
led_on = False
last_blink = time.ticks_ms()

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

while True:
    if btn.value() == BUTTON_ACTIVE:
        mode = (mode + 1) % 3
        print("mode =", mode)
        time.sleep_ms(250)
        wait_release()

    now = time.ticks_ms()

    if mode == 0:
        interval = 700
        if time.ticks_diff(now, last_blink) >= interval:
            led_on = not led_on
            led.value(1 if led_on else 0)
            last_blink = now
    elif mode == 1:
        led.on()
    else:
        interval = 120
        if time.ticks_diff(now, last_blink) >= interval:
            led_on = not led_on
            led.value(1 if led_on else 0)
            last_blink = now

    time.sleep_ms(20)
```

### 4. 最終成果展現

按鈕可以在慢閃、長亮、快閃三種模式中切換，且 LED 閃爍時按鈕仍能被即時讀取。

### 5. 應用題與解答

**題目：** 加入第 4 種模式 `mode = 3`，讓 LED 完全關閉。

**解答：**

```python
# 將切換改成 4 種模式
mode = (mode + 1) % 4

# 在主迴圈中加入：
if mode == 3:
    led.off()
```

完整版本：

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)
mode = 0
led_on = False
last_blink = time.ticks_ms()

while True:
    if btn.value() == BUTTON_ACTIVE:
        mode = (mode + 1) % 4
        time.sleep_ms(250)
        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)

    now = time.ticks_ms()

    if mode == 0 and time.ticks_diff(now, last_blink) >= 700:
        led_on = not led_on
        led.value(led_on)
        last_blink = now
    elif mode == 1:
        led.on()
    elif mode == 2 and time.ticks_diff(now, last_blink) >= 120:
        led_on = not led_on
        led.value(led_on)
        last_blink = now
    elif mode == 3:
        led.off()

    time.sleep_ms(20)
```

## Case 9：Shell 指令控制 LED

### 1. 要做的主題

透過 Thonny Shell 輸入文字指令，控制 LED 開、關、閃爍，讓學生理解「命令式控制」。

### 2. 分階段逐步教學

**階段 A：使用 `input()`**

從 Shell 讀取使用者輸入。

**階段 B：判斷文字命令**

例如 `on`、`off`、`blink`、`quit`。

**階段 C：呼叫對應動作**

將命令轉成 LED 行為。

**階段 D：建立可互動測試工具**

未來可擴充成馬達或感測器測試命令。

### 3. 完整程式碼

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

def blink(times=3):
    for i in range(times):
        led.on()
        time.sleep_ms(200)
        led.off()
        time.sleep_ms(200)

while True:
    cmd = input("command(on/off/blink/quit): ").strip().lower()

    if cmd == "on":
        led.on()
        print("LED on")
    elif cmd == "off":
        led.off()
        print("LED off")
    elif cmd == "blink":
        blink(3)
    elif cmd == "quit":
        led.off()
        print("bye")
        break
    else:
        print("unknown command")
```

### 4. 最終成果展現

學生可以在 Shell 輸入 `on`、`off`、`blink` 控制 LED。這可作為硬體測試台的雛形。

### 5. 應用題與解答

**題目：** 新增 `blink5` 指令，讓 LED 閃 5 次。

**解答：**

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

def blink(times=3):
    for i in range(times):
        led.on()
        time.sleep_ms(200)
        led.off()
        time.sleep_ms(200)

while True:
    cmd = input("command(on/off/blink/blink5/quit): ").strip().lower()

    if cmd == "on":
        led.on()
        print("LED on")
    elif cmd == "off":
        led.off()
        print("LED off")
    elif cmd == "blink":
        blink(3)
    elif cmd == "blink5":
        blink(5)
    elif cmd == "quit":
        led.off()
        print("bye")
        break
    else:
        print("unknown command")
```

## Case 10：開機自我測試程式

### 1. 要做的主題

設計一段可存成 `main.py` 的開機自我測試：LED 先閃爍，等待按鈕確認後才進入待機。

### 2. 分階段逐步教學

**階段 A：開機提示**

LED 快閃表示程式已啟動。

**階段 B：等待按鈕確認**

學生按下按鈕表示硬體輸入正常。

**階段 C：進入待機狀態**

LED 慢閃代表準備好。

**階段 D：銜接小車專題**

未來可在按鈕確認後啟動馬達或避障程式。

### 3. 完整程式碼

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

def flash(times, delay_ms):
    for i in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

print("boot self-test")
flash(5, 100)

print("press button to enter ready mode")
while btn.value() != BUTTON_ACTIVE:
    led.on()
    time.sleep_ms(50)
    led.off()
    time.sleep_ms(450)

while btn.value() == BUTTON_ACTIVE:
    time.sleep_ms(20)

print("ready")

while True:
    led.toggle()
    time.sleep_ms(700)
```

### 4. 最終成果展現

開機後 LED 快閃 5 次，接著等待按鈕；按下後進入慢閃待機。這能確認 LED、按鈕與主程式都正常。

### 5. 應用題與解答

**題目：** 如果 10 秒內沒有按下按鈕，讓 LED 快閃表示錯誤。

**解答：**

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

def flash(times, delay_ms):
    for i in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

start = time.ticks_ms()
confirmed = False

while time.ticks_diff(time.ticks_ms(), start) < 10000:
    if btn.value() == BUTTON_ACTIVE:
        confirmed = True
        break
    led.toggle()
    time.sleep_ms(500)

if confirmed:
    flash(2, 100)
    while True:
        led.toggle()
        time.sleep_ms(700)
else:
    while True:
        flash(3, 80)
        time.sleep_ms(1000)
```

### 4. 最終成果展現

待機時 LED 慢慢閃爍；按一下後 LED 長亮代表啟動；再按一下回到待機慢閃。這就是後續專題中「小車啟停控制」的核心架構。

### 5. 應用題與解答

**題目：** 加入 `mode` 變數，讓每次按鈕切換三種狀態：`0=待機慢閃`、`1=啟動長亮`、`2=警示快閃`。

**解答：**

```python
from machine import Pin
import time

BUTTON_ACTIVE = 1

led = Pin(25, Pin.OUT)
btn = Pin(3, Pin.IN)

mode = 0
blink_on = False
last_blink = time.ticks_ms()

def wait_button_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

while True:
    if btn.value() == BUTTON_ACTIVE:
        mode = (mode + 1) % 3
        print("mode =", mode)
        time.sleep_ms(250)
        wait_button_release()

    now = time.ticks_ms()

    if mode == 0:
        if time.ticks_diff(now, last_blink) >= 700:
            blink_on = not blink_on
            led.value(1 if blink_on else 0)
            last_blink = now
    elif mode == 1:
        led.on()
    else:
        if time.ticks_diff(now, last_blink) >= 150:
            blink_on = not blink_on
            led.value(1 if blink_on else 0)
            last_blink = now

    time.sleep_ms(20)
```
