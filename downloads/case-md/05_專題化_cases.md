# 05 專題化延伸 Cases：任務設計、策略比較與成果評量

本篇延伸整份教材，將 LED、按鈕、蜂鳴器、RGB、超音波、馬達、循跡與伺服整合成專題任務。每個 case 都適合作為課堂挑戰或分組活動。

參考資料：

- MicroPython `machine.Pin`：https://docs.micropython.org/en/latest/library/machine.Pin.html
- MicroPython `machine.PWM`：https://docs.micropython.org/en/latest/library/machine.PWM.html
- MicroPython `machine.ADC`：https://docs.micropython.org/en/v1.14/library/machine.ADC.html
- MicroPython `time.ticks_ms()` / `ticks_diff()`：https://docs.micropython.org/en/latest/pyboard/library/utime.html
- MicroPython `machine.I2C`：https://docs.micropython.org/en/latest/library/machine.I2C.html
- Raspberry Pi Pico Python SDK：https://datasheets.raspberrypi.com/pico/sdk/pico_python_sdk.pdf
- Raspberry Pi Pico MicroPython examples：https://github.com/raspberrypi/pico-micropython-examples

## Case 1：按鈕啟停避障車

### 1. 要做的主題

把按鈕加入避障車，做到「按一下啟動，再按一下停止」。

### 2. 分階段逐步教學

**階段 A：建立 `running` 狀態**

`False` 代表待機，`True` 代表自走。

**階段 B：按鈕切換狀態**

沿用入門篇的按鈕切換寫法。

**階段 C：待機時停車並亮藍燈**

讓學生看得出小車目前沒有執行任務。

**階段 D：啟動後執行避障**

將避障流程放在 `if running` 裡。

### 3. 完整程式碼

```python
from machine import Pin
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1

btn = Pin(3, Pin.IN)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

running = False

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

while True:
    if btn.value() == BUTTON_ACTIVE:
        running = not running
        print("running =", running)
        time.sleep_ms(250)
        wait_release()

    if running:
        dist = sensor.ping()
        print("distance =", dist)

        if dist < 20:
            sensor.rgb_all((255, 0, 0))
            drive(5, 30)
        else:
            sensor.rgb_all((0, 255, 0))
            drive(18, 18)
    else:
        stop()
        sensor.rgb_all((0, 0, 255))

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車待機時藍燈且不動；按下按鈕後開始避障自走；再按一次後停止。

### 5. 應用題與解答

**題目：** 加入長按緊急停止，長按超過 1 秒就立刻停止並亮紅燈。

**解答：**

```python
from machine import Pin
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
running = False

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

while True:
    if btn.value() == BUTTON_ACTIVE:
        start = time.ticks_ms()
        while btn.value() == BUTTON_ACTIVE:
            time.sleep_ms(20)
        duration = time.ticks_diff(time.ticks_ms(), start)

        if duration > 1000:
            running = False
            stop()
            sensor.rgb_all((255, 0, 0))
            time.sleep(1)
        else:
            running = not running

    if running:
        if sensor.ping() < 20:
            sensor.rgb_all((255, 0, 0))
            drive(5, 30)
        else:
            sensor.rgb_all((0, 255, 0))
            drive(18, 18)
    else:
        stop()
        sensor.rgb_all((0, 0, 255))

    time.sleep_ms(100)
```

## Case 2：避障策略比較實驗

### 1. 要做的主題

讓學生用同一台小車比較不同避障策略：固定左轉、固定右轉、左右交替。

### 2. 分階段逐步教學

**階段 A：建立策略變數**

`strategy = 0/1/2` 代表不同策略。

**階段 B：把避障動作封裝成函式**

不同策略只改轉向方式。

**階段 C：加入遇障計數**

讓學生觀察策略執行次數。

**階段 D：記錄測試結果**

比較哪個策略比較不會卡住。

### 3. 完整程式碼

```python
from mango import Motor, RUS04
import time

strategy = 2  # 0=left, 1=right, 2=alternate
turn_left_next = True
avoid_count = 0

sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def avoid():
    global turn_left_next, avoid_count
    avoid_count += 1
    print("avoid count =", avoid_count)

    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(400)

    if strategy == 0:
        drive(-20, 20)
    elif strategy == 1:
        drive(20, -20)
    else:
        if turn_left_next:
            drive(-20, 20)
        else:
            drive(20, -20)
        turn_left_next = not turn_left_next

    time.sleep_ms(650)
    stop()

while True:
    dist = sensor.ping()

    if dist < 20:
        sensor.rgb_all((255, 0, 0))
        avoid()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```

### 4. 最終成果展現

同一份程式可切換三種避障策略，學生能用實測比較哪一種在場地中表現較好。

### 5. 應用題與解答

**題目：** 加入第四種策略 `strategy = 3`，遇障時原地旋轉 1.2 秒。

**解答：**

```python
def avoid():
    global turn_left_next, avoid_count
    avoid_count += 1

    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(400)

    if strategy == 0:
        drive(-20, 20)
        time.sleep_ms(650)
    elif strategy == 1:
        drive(20, -20)
        time.sleep_ms(650)
    elif strategy == 2:
        if turn_left_next:
            drive(-20, 20)
        else:
            drive(20, -20)
        turn_left_next = not turn_left_next
        time.sleep_ms(650)
    else:
        drive(25, -25)
        time.sleep_ms(1200)

    stop()
```

## Case 3：測試紀錄與參數調整

### 1. 要做的主題

把避障測試資料寫入開發板檔案，讓學生用數據調整速度與距離門檻。

### 2. 分階段逐步教學

**階段 A：建立測試參數**

例如速度、距離門檻。

**階段 B：每次遇障記錄一次**

記錄時間、距離、速度、門檻。

**階段 C：寫入 CSV 檔案**

方便之後打開觀察。

**階段 D：根據數據調整**

如果太常遇障，可降低速度或提高門檻。

### 3. 完整程式碼

```python
from mango import Motor, RUS04
import time

SPEED = 18
THRESHOLD = 25
LOG_FILE = "avoid_log.csv"

sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def log_event(dist):
    with open(LOG_FILE, "a") as f:
        line = "{},{},{}\n".format(time.ticks_ms(), dist, SPEED)
        f.write(line)

def avoid(dist):
    log_event(dist)
    sensor.rgb_all((255, 0, 0))
    drive(-18, -18)
    time.sleep_ms(400)
    drive(20, -20)
    time.sleep_ms(600)
    stop()

with open(LOG_FILE, "w") as f:
    f.write("ticks_ms,distance,speed\n")

while True:
    dist = sensor.ping()

    if dist < THRESHOLD:
        avoid(dist)
    else:
        sensor.rgb_all((0, 255, 0))
        drive(SPEED, SPEED)

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車執行避障時，會把每次遇到障礙物的時間、距離與速度記錄到 `avoid_log.csv`。

### 5. 應用題與解答

**題目：** 在記錄中加入 `threshold` 欄位。

**解答：**

```python
def log_event(dist):
    with open(LOG_FILE, "a") as f:
        line = "{},{},{},{}\n".format(
            time.ticks_ms(),
            dist,
            SPEED,
            THRESHOLD
        )
        f.write(line)

with open(LOG_FILE, "w") as f:
    f.write("ticks_ms,distance,speed,threshold\n")
```

## Case 4：循跡挑戰賽

### 1. 要做的主題

設計一個循跡挑戰：小車沿黑線前進，離線時自動搜尋路線。

### 2. 分階段逐步教學

**階段 A：印出感測器狀態**

先觀察 `digital_state`。

**階段 B：建立基本循跡規則**

中間在線上直行，偏左/偏右修正。

**階段 C：加入離線搜尋**

失去線時依上一次偏移方向搜尋。

**階段 D：進行競速與穩定度比較**

調整速度與修正幅度。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

last_dir = "left"

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

while True:
    state = line.digital_state
    print(state)

    if state == "0110":
        drive(20, 20)
    elif state in ("1100", "1000", "0100"):
        drive(8, 25)
        last_dir = "left"
    elif state in ("0011", "0001", "0010"):
        drive(25, 8)
        last_dir = "right"
    elif state == "0000":
        if last_dir == "left":
            drive(-10, 12)
        else:
            drive(12, -10)
    else:
        drive(12, 12)

    time.sleep_ms(20)
```

### 4. 最終成果展現

小車可以沿黑線前進，短暫離線時會依最後偏移方向搜尋路線。

### 5. 應用題與解答

**題目：** 將直行速度提高到 25，但轉向修正維持低速，觀察穩定度。

**解答：**

```python
if state == "0110":
    drive(25, 25)
elif state in ("1100", "1000", "0100"):
    drive(8, 25)
    last_dir = "left"
elif state in ("0011", "0001", "0010"):
    drive(25, 8)
    last_dir = "right"
```

## Case 5：伺服閘門運送任務

### 1. 要做的主題

使用伺服馬達做簡單閘門，讓小車到達目的地後打開/關閉機構。

### 2. 分階段逐步教學

**階段 A：控制伺服角度**

用 `Servo.position()` 開關閘門。

**階段 B：用距離判斷目的地**

當前方距離小於 12 cm 時視為到達。

**階段 C：停車並開門**

小車停止，伺服打開。

**階段 D：完成後後退離開**

關門，後退一小段。

### 3. 完整程式碼

```python
from mango import Motor, RUS04, Servo
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
gate = Servo(pin=6)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def gate_open():
    gate.position(110)

def gate_close():
    gate.position(10)

gate_close()

while True:
    dist = sensor.ping()
    print("distance =", dist)

    if dist < 12:
        stop()
        sensor.rgb_all((0, 0, 255))
        gate_open()
        time.sleep(2)
        gate_close()
        time.sleep_ms(500)
        drive(-15, -15)
        time.sleep(1)
        stop()
        break
    else:
        sensor.rgb_all((0, 255, 0))
        drive(15, 15)

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車前進到目標前方，停車、開啟伺服閘門、關閉後後退離開。

### 5. 應用題與解答

**題目：** 加入蜂鳴器，開門前嗶兩聲。

**解答：**

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6, Pin.OUT))

def beep():
    buzzer.freq(1000)
    buzzer.duty_u16(5000)
    time.sleep_ms(100)
    buzzer.duty_u16(0)
    time.sleep_ms(100)

for i in range(2):
    beep()

buzzer.deinit()
```

注意：如果伺服和蜂鳴器使用同一腳位，需改用不同腳位或只選一個裝置。

## Case 6：總整合任務：可啟停的避障任務車

### 1. 要做的主題

整合按鈕、RGB、蜂鳴器、超音波與馬達，完成一台可啟停、有狀態回饋的避障任務車。

### 2. 分階段逐步教學

**階段 A：待機狀態**

藍燈慢閃，小車停止。

**階段 B：啟動提示**

按下按鈕後蜂鳴器短嗶，綠燈亮。

**階段 C：避障行為**

距離安全就前進，太近就紅燈並避障。

**階段 D：再次按鈕停止**

停止馬達並回待機。

### 3. 完整程式碼

```python
from machine import Pin, PWM
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1

btn = Pin(3, Pin.IN)
buzzer = PWM(Pin(6, Pin.OUT))
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

running = False
blink_on = False
last_blink = time.ticks_ms()

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def beep(freq=1000, duration_ms=100):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def avoid():
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(400)
    drive(20, -20)
    time.sleep_ms(650)
    stop()

while True:
    if btn.value() == BUTTON_ACTIVE:
        running = not running
        beep(1200, 100)
        wait_release()

    if running:
        dist = sensor.ping()
        print("distance =", dist)

        if dist < 20:
            avoid()
        else:
            sensor.rgb_all((0, 255, 0))
            drive(18, 18)
    else:
        stop()
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) > 700:
            blink_on = not blink_on
            if blink_on:
                sensor.rgb_all((0, 0, 255))
            else:
                sensor.rgb_all((0, 0, 0))
            last_blink = now

    time.sleep_ms(80)
```

### 4. 最終成果展現

小車待機時藍燈慢閃；按下按鈕後嗶一聲開始自走；遇障會紅燈、後退、轉向；再按一次停止並回待機。

### 5. 應用題與解答

**題目：** 將 `avoid()` 改成左右交替避障。

**解答：**

```python
turn_left_next = True

def avoid():
    global turn_left_next

    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(400)

    if turn_left_next:
        drive(-20, 20)
    else:
        drive(20, -20)

    time.sleep_ms(650)
    stop()
    turn_left_next = not turn_left_next
```

## Case 7：任務計時賽

### 1. 要做的主題

設計一個按鈕啟動的計時賽：按下按鈕後小車出發，接近終點牆時停止，並在 Shell 顯示完成時間。

### 2. 分階段逐步教學

**階段 A：定義比賽流程**

流程分成待機、起跑、行駛、抵達終點四個狀態。

**階段 B：用 `ticks_ms()` 計時**

用 `time.ticks_ms()` 記錄起跑時間，再用 `time.ticks_diff()` 算出經過時間，避免計時器回繞造成錯誤。

**階段 C：用超音波判斷終點**

終點可以放一面牆或紙板，當距離小於 12 cm 時視為抵達。

**階段 D：用聲光提示結果**

待機藍燈、行駛綠燈、完成黃燈加提示音。

### 3. 完整程式碼

```python
from machine import Pin, PWM
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
buzzer = PWM(Pin(6, Pin.OUT))
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

running = False
start_ticks = 0

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def beep(freq=1200, duration_ms=120):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def start_race():
    global running, start_ticks
    running = True
    start_ticks = time.ticks_ms()
    sensor.rgb_all((0, 255, 0))
    beep(1000, 100)
    print("race start")

def finish_race():
    global running
    running = False
    stop()
    elapsed_ms = time.ticks_diff(time.ticks_ms(), start_ticks)
    sensor.rgb_all((255, 180, 0))
    print("finish time =", elapsed_ms / 1000, "s")
    for i in range(3):
        beep(1500, 80)
        time.sleep_ms(80)

while True:
    if not running:
        sensor.rgb_all((0, 0, 255))
        stop()

        if btn.value() == BUTTON_ACTIVE:
            wait_release()
            start_race()
    else:
        dist = sensor.ping()
        print("distance =", dist)

        if dist < 12:
            finish_race()
        else:
            drive(20, 20)

    time.sleep_ms(60)
```

### 4. 最終成果展現

學生按下按鈕後小車出發，靠近終點牆時停止，Shell 會印出秒數。這可以直接變成分組競賽或參數調校活動。

### 5. 應用題與解答

**題目：** 記錄目前最佳秒數，若本次成績刷新紀錄就發出較高音。

**解答：**

```python
best_ms = None

def finish_race():
    global running, best_ms
    running = False
    stop()
    elapsed_ms = time.ticks_diff(time.ticks_ms(), start_ticks)
    sensor.rgb_all((255, 180, 0))
    print("finish time =", elapsed_ms / 1000, "s")

    if best_ms is None or elapsed_ms < best_ms:
        best_ms = elapsed_ms
        print("new best =", best_ms / 1000, "s")
        beep(1800, 250)
    else:
        beep(1000, 250)
```

## Case 8：多模式任務車

### 1. 要做的主題

用同一台車支援多種任務模式：待機、展示路徑、避障、循跡，並用按鈕切換模式。

### 2. 分階段逐步教學

**階段 A：建立模式清單**

用 `MODES = ["standby", "demo", "avoid", "line"]` 讓程式有明確任務名稱。

**階段 B：按鈕切換模式**

每按一次按鈕，模式往下一個切換，最後回到待機。

**階段 C：把每種模式寫成函式**

展示路徑、避障、循跡都各自獨立，主迴圈只負責選擇要執行哪個函式。

**階段 D：用 RGB 顯示模式**

藍色待機、紫色展示、紅色避障、綠色循跡，方便學生除錯。

### 3. 完整程式碼

```python
from machine import Pin
from mango import GraySensor8
from mango import bus
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

MODES = ["standby", "demo", "avoid", "line"]
mode_index = 0

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def switch_mode():
    global mode_index
    mode_index = (mode_index + 1) % len(MODES)
    print("mode =", MODES[mode_index])

def run_standby():
    sensor.rgb_all((0, 0, 255))
    stop()

def run_demo():
    sensor.rgb_all((120, 0, 255))
    drive(20, 20)
    time.sleep_ms(600)
    drive(20, -20)
    time.sleep_ms(400)
    stop()
    time.sleep_ms(400)

def run_avoid():
    dist = sensor.ping()
    print("avoid distance =", dist)

    if dist < 20:
        sensor.rgb_all((255, 0, 0))
        drive(-18, -18)
        time.sleep_ms(350)
        drive(20, -20)
        time.sleep_ms(500)
    else:
        sensor.rgb_all((255, 80, 0))
        drive(18, 18)

def run_line():
    state = line.digital_state
    sensor.rgb_all((0, 255, 0))
    print("line =", state)

    if state == "0110":
        drive(18, 18)
    elif state in ("1100", "1000"):
        drive(5, 22)
    elif state in ("0011", "0001"):
        drive(22, 5)
    else:
        drive(12, 12)

while True:
    if btn.value() == BUTTON_ACTIVE:
        wait_release()
        switch_mode()

    mode = MODES[mode_index]

    if mode == "standby":
        run_standby()
    elif mode == "demo":
        run_demo()
    elif mode == "avoid":
        run_avoid()
    elif mode == "line":
        run_line()

    time.sleep_ms(80)
```

### 4. 最終成果展現

同一份程式可以切換四種任務，學生能看到「專題」不一定是一長串 if，而是由模式與函式組合出來。

### 5. 應用題與解答

**題目：** 新增 `stop` 模式，切到此模式時紅燈慢閃且馬達停止。

**解答：**

```python
from machine import Pin
from mango import GraySensor8
from mango import bus
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

MODES = ["standby", "demo", "avoid", "line", "stop"]
mode_index = 0
blink_on = False
last_blink = 0

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def switch_mode():
    global mode_index
    mode_index = (mode_index + 1) % len(MODES)
    print("mode =", MODES[mode_index])

def run_standby():
    sensor.rgb_all((0, 0, 255))
    stop()

def run_demo():
    sensor.rgb_all((120, 0, 255))
    drive(20, 20)
    time.sleep_ms(600)
    drive(20, -20)
    time.sleep_ms(400)
    stop()
    time.sleep_ms(400)

def run_avoid():
    dist = sensor.ping()
    if dist < 20:
        sensor.rgb_all((255, 0, 0))
        drive(-18, -18)
        time.sleep_ms(350)
        drive(20, -20)
        time.sleep_ms(500)
    else:
        sensor.rgb_all((255, 80, 0))
        drive(18, 18)

def run_line():
    state = line.digital_state
    sensor.rgb_all((0, 255, 0))

    if state == "0110":
        drive(18, 18)
    elif state in ("1100", "1000"):
        drive(5, 22)
    elif state in ("0011", "0001"):
        drive(22, 5)
    else:
        drive(12, 12)

def run_stop_mode():
    global blink_on, last_blink
    stop()
    now = time.ticks_ms()

    if time.ticks_diff(now, last_blink) > 500:
        blink_on = not blink_on
        last_blink = now

        if blink_on:
            sensor.rgb_all((255, 0, 0))
        else:
            sensor.rgb_all((0, 0, 0))

while True:
    if btn.value() == BUTTON_ACTIVE:
        wait_release()
        switch_mode()

    mode = MODES[mode_index]

    if mode == "standby":
        run_standby()
    elif mode == "demo":
        run_demo()
    elif mode == "avoid":
        run_avoid()
    elif mode == "line":
        run_line()
    elif mode == "stop":
        run_stop_mode()

    time.sleep_ms(80)
```

## Case 9：循跡參數實驗與資料記錄

### 1. 要做的主題

讓學生用同一條跑道測試多組循跡參數，並把時間、誤差與馬達輸出印成 CSV 形式，方便比較。

### 2. 分階段逐步教學

**階段 A：定義實驗參數**

把 `BASE_SPEED` 與 `KP` 寫成清單，每一組代表一次實驗。

**階段 B：按鈕開始每次實驗**

每組參數都由學生手動按下按鈕開始，方便重新擺正小車。

**階段 C：固定測試時間**

每次跑 8 秒，避免不同組別測試長度不一致。

**階段 D：輸出 CSV 資料**

Shell 印出 `trial,time_ms,state,error,left,right`，學生可以複製到試算表分析。

### 3. 完整程式碼

```python
from machine import Pin
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
CONFIGS = [
    (16, 4),
    (18, 5),
    (20, 6),
]

last_error = 0

def wait_press():
    while btn.value() != BUTTON_ACTIVE:
        time.sleep_ms(20)
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def get_error(state):
    global last_error
    total = 0
    count = 0

    for i in range(4):
        if state[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error

    last_error = total / count
    return last_error

def run_trial(trial_id, base_speed, kp, duration_ms=8000):
    global last_error
    last_error = 0
    start = time.ticks_ms()
    print("trial,time_ms,state,error,left,right")

    while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, start)
        state = line.digital_state
        error = get_error(state)
        correction = int(error * kp)
        left = clamp(base_speed + correction, -35, 35)
        right = clamp(base_speed - correction, -35, 35)
        drive(left, right)
        print(trial_id, elapsed, state, error, left, right, sep=",")
        time.sleep_ms(80)

    stop()

for trial_id, config in enumerate(CONFIGS, start=1):
    base_speed, kp = config
    print("ready trial", trial_id, "base =", base_speed, "kp =", kp)
    print("press button to start")
    wait_press()
    run_trial(trial_id, base_speed, kp)
    time.sleep(1)

stop()
print("all trials done")
```

### 4. 最終成果展現

學生能以同一條跑道比較不同速度與 Kp 的效果，並取得可分析的文字資料。這會把「調參」從感覺變成有證據的工程實驗。

### 5. 應用題與解答

**題目：** 在資料中加入 `black_count` 欄位，記錄每次有幾顆感測器偵測到黑線。

**解答：**

```python
def run_trial(trial_id, base_speed, kp, duration_ms=8000):
    global last_error
    last_error = 0
    start = time.ticks_ms()
    print("trial,time_ms,state,black_count,error,left,right")

    while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, start)
        state = line.digital_state
        black_count = state.count("1")
        error = get_error(state)
        correction = int(error * kp)
        left = clamp(base_speed + correction, -35, 35)
        right = clamp(base_speed - correction, -35, 35)
        drive(left, right)
        print(trial_id, elapsed, state, black_count, error, left, right, sep=",")
        time.sleep_ms(80)

    stop()
```

## Case 10：期末專題骨架：狀態機任務車

### 1. 要做的主題

建立一個可擴充的期末專題程式骨架，使用狀態機整合待機、循跡、避障與完成任務。

### 2. 分階段逐步教學

**階段 A：定義狀態**

使用 `WAIT`、`RUN`、`AVOID`、`FINISH` 表示任務流程，不讓所有邏輯擠在同一層。

**階段 B：把行為拆成函式**

`run_wait()`、`run_mission()`、`run_avoid()`、`run_finish()` 各自處理一種狀態。

**階段 C：主迴圈只做狀態切換**

主迴圈讀按鈕與感測器，根據條件決定下一個狀態。

**階段 D：留下專題擴充點**

學生可以把任務完成條件改成經過終點、看到特定線型、完成指定圈數或抵達停車格。

### 3. 完整程式碼

```python
from machine import Pin, PWM
from mango import GraySensor8
from mango import bus
from mango import Motor, RUS04
import time

BUTTON_ACTIVE = 1
WAIT = "WAIT"
RUN = "RUN"
AVOID = "AVOID"
FINISH = "FINISH"

btn = Pin(3, Pin.IN)
buzzer = PWM(Pin(6, Pin.OUT))
line = GraySensor8(i2c=bus.i2c, digital_channels='4')
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

state = WAIT
mission_start = 0
last_error = 0
avoid_left_next = True

WEIGHTS = [-2, -1, 1, 2]
BASE_SPEED = 18
KP = 5
MISSION_LIMIT_MS = 30000

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def beep(freq=1200, duration_ms=100):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

def wait_release():
    while btn.value() == BUTTON_ACTIVE:
        time.sleep_ms(20)

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def get_line_error():
    global last_error

    state_text = line.digital_state
    total = 0
    count = 0

    for i in range(4):
        if state_text[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error

    last_error = total / count
    return last_error

def follow_line_step():
    error = get_line_error()
    correction = int(error * KP)
    left = clamp(BASE_SPEED + correction, -35, 35)
    right = clamp(BASE_SPEED - correction, -35, 35)
    drive(left, right)

def run_wait():
    global state, mission_start
    stop()
    sensor.rgb_all((0, 0, 255))

    if btn.value() == BUTTON_ACTIVE:
        wait_release()
        mission_start = time.ticks_ms()
        beep(1000, 120)
        state = RUN

def run_mission():
    global state
    sensor.rgb_all((0, 255, 0))

    elapsed = time.ticks_diff(time.ticks_ms(), mission_start)
    dist = sensor.ping()

    if elapsed > MISSION_LIMIT_MS:
        state = FINISH
        return

    if dist < 18:
        state = AVOID
        return

    follow_line_step()

def run_avoid():
    global state, avoid_left_next
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(120)
    drive(-18, -18)
    time.sleep_ms(400)

    if avoid_left_next:
        drive(-22, 22)
    else:
        drive(22, -22)

    time.sleep_ms(650)
    stop()
    avoid_left_next = not avoid_left_next
    state = RUN

def run_finish():
    global state
    stop()
    sensor.rgb_all((255, 180, 0))
    beep(1500, 150)
    time.sleep_ms(120)
    beep(1800, 150)
    print("mission finish")
    state = WAIT

while True:
    if state == WAIT:
        run_wait()
    elif state == RUN:
        run_mission()
    elif state == AVOID:
        run_avoid()
    elif state == FINISH:
        run_finish()

    time.sleep_ms(60)
```

### 4. 最終成果展現

學生得到一份完整可執行、可擴充的專題骨架。它不是單一技巧展示，而是把課程中的按鈕、聲光、馬達、超音波、循跡與任務流程整理成一個可以繼續發展的作品架構。

### 5. 應用題與解答

**題目：** 將任務完成條件改成「看到寬黑線」：當四路感測器中至少 3 路偵測到黑線，就進入完成狀態。

**解答：**

```python
def is_finish_line():
    state_text = line.digital_state
    return state_text.count("1") >= 3

def run_mission():
    global state
    sensor.rgb_all((0, 255, 0))
    dist = sensor.ping()

    if is_finish_line():
        state = FINISH
        return

    if dist < 18:
        state = AVOID
        return

    follow_line_step()
```

## Case 11：規則式循跡演算法比較

### 1. 要做的主題

把四路循跡感測器的狀態轉成固定規則，讓小車可以依照「偏左、偏右、在線上、失去線」做出不同動作。這是最容易理解的循跡演算法，也是後續 P、PD、PID 控制的基礎。

### 2. 分階段逐步教學

**階段 A：讀取四路循跡狀態**

使用 `GraySensor8(..., digital_channels='4')` 讀取四路循跡感測器，並用 `line.digital_state` 取得目前狀態。

**階段 B：把狀態轉成規則**

若中間接近黑線就前進，若黑線偏左就左修正，若黑線偏右就右修正。

**階段 C：處理失去黑線**

當感測器都沒有看到黑線時，先停止或依照最後方向慢慢找回黑線。

**階段 D：比較規則式的優缺點**

規則式很適合初學，但轉向較突然，速度提高後容易左右搖晃。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

BASE_SPEED = 20
TURN_SPEED = 16
last_turn = "stop"

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def rule_follow_step():
    global last_turn

    state = line.digital_state
    print("line =", state)

    if state in ("0110", "1111", "0010", "0100"):
        drive(BASE_SPEED, BASE_SPEED)
        last_turn = "forward"
    elif state in ("1000", "1100", "0100"):
        drive(-TURN_SPEED, TURN_SPEED)
        last_turn = "left"
    elif state in ("0001", "0011", "0010"):
        drive(TURN_SPEED, -TURN_SPEED)
        last_turn = "right"
    else:
        if last_turn == "left":
            drive(-12, 12)
        elif last_turn == "right":
            drive(12, -12)
        else:
            stop()

while True:
    rule_follow_step()
    time.sleep_ms(60)
```

### 4. 最終成果展現

學生可以看到小車依照黑線位置做出固定反應，理解「感測器狀態」如何被轉換成「馬達動作」。這個 case 適合作為循跡演算法比較的第一站。

### 5. 應用題與解答

**題目：** 如果小車在彎道轉得太急，請把左右修正速度從 `TURN_SPEED = 16` 改成更溫和的速度。

**解答：**

```python
TURN_SPEED = 12
```

## Case 12：P 比例循跡控制

### 1. 要做的主題

把循跡感測器狀態轉成 `error`，再用 `correction = KP * error` 產生左右輪速度差。這讓小車不再只做固定轉向，而是依照偏離程度調整修正力道。

### 2. 分階段逐步教學

**階段 A：建立權重**

四路循跡可以用 `[-2, -1, 1, 2]` 代表黑線偏左、偏右的程度。

**階段 B：計算 error**

把看到黑線的位置加權平均，得到目前偏差。

**階段 C：把 error 轉成速度差**

`KP` 越大，修正越明顯；`KP` 太大，小車可能左右擺動。

**階段 D：實測調整 KP**

先用低速測試，再逐步調整 `BASE_SPEED` 與 `KP`。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
BASE_SPEED = 20
KP = 6
last_error = 0

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def get_error():
    global last_error

    state = line.digital_state
    total = 0
    count = 0

    for i in range(4):
        if state[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error

    last_error = total / count
    return last_error

while True:
    error = get_error()
    correction = KP * error

    left_speed = clamp(BASE_SPEED + correction, -35, 35)
    right_speed = clamp(BASE_SPEED - correction, -35, 35)

    drive(left_speed, right_speed)
    print("error =", error, "left =", left_speed, "right =", right_speed)
    time.sleep_ms(50)
```

### 4. 最終成果展現

學生可以觀察到小車的轉向不再只有固定幾種，而是會依照偏差大小產生不同速度差。這是從規則式循跡進入控制演算法的關鍵轉換。

### 5. 應用題與解答

**題目：** 如果小車修正太慢，請提高比例參數。

**解答：**

```python
KP = 8
```

## Case 13：PD 循跡控制與擺動修正

### 1. 要做的主題

在 P 控制上加入 D 項，讓程式不只看「現在偏多少」，也看「偏差變化有多快」。PD 控制常用來減少循跡小車左右來回擺動。

### 2. 分階段逐步教學

**階段 A：保留 P 控制**

P 項負責依照目前偏差修正方向。

**階段 B：加入 derivative**

`derivative = error - last_error` 可以看出偏差是否快速變大。

**階段 C：加入 KD**

D 項會抑制太突然的變化，讓小車轉向更平滑。

**階段 D：比較 P 與 PD**

同一條跑道上，讓學生比較 P 與 PD 哪一個比較不晃。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
BASE_SPEED = 20
KP = 6
KD = 4
last_error = 0

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def get_error():
    global last_error

    state = line.digital_state
    total = 0
    count = 0

    for i in range(4):
        if state[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error

    return total / count

while True:
    error = get_error()
    derivative = error - last_error
    correction = KP * error + KD * derivative

    left_speed = clamp(BASE_SPEED + correction, -35, 35)
    right_speed = clamp(BASE_SPEED - correction, -35, 35)

    drive(left_speed, right_speed)
    print("error =", error, "d =", derivative)

    last_error = error
    time.sleep_ms(50)
```

### 4. 最終成果展現

學生可以看到 PD 控制通常比單純 P 控制更穩，尤其在彎道或感測器剛偵測到黑線變化時，車身比較不容易大幅搖擺。

### 5. 應用題與解答

**題目：** 如果小車仍然左右晃動，請先稍微提高 `KD`。

**解答：**

```python
KD = 6
```

## Case 14：PID 循跡調參挑戰

### 1. 要做的主題

在 PD 控制之外加入 I 項，讓程式可以累積長時間偏差。這個 case 適合放在進階討論，重點不是背公式，而是理解 `KP`、`KI`、`KD` 對小車行為的影響。

### 2. 分階段逐步教學

**階段 A：複習 P、D 的角色**

P 看目前偏差，D 看偏差變化速度。

**階段 B：加入積分項**

I 項會累積偏差，適合處理小車長時間偏向某一邊的情況。

**階段 C：限制積分大小**

為避免積分越累積越大，使用 `INTEGRAL_LIMIT` 限制範圍。

**階段 D：做調參紀錄**

每組學生記錄 `KP`、`KI`、`KD` 與實際表現，學會用實驗方式調整參數。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
BASE_SPEED = 20
KP = 6
KI = 1
KD = 4
INTEGRAL_LIMIT = 8

last_error = 0
sum_error = 0

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def get_error():
    global last_error

    state = line.digital_state
    total = 0
    count = 0

    for i in range(4):
        if state[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error

    return total / count

while True:
    error = get_error()
    derivative = error - last_error
    sum_error = clamp(sum_error + error, -INTEGRAL_LIMIT, INTEGRAL_LIMIT)

    correction = KP * error + KI * sum_error + KD * derivative

    left_speed = clamp(BASE_SPEED + correction, -35, 35)
    right_speed = clamp(BASE_SPEED - correction, -35, 35)

    drive(left_speed, right_speed)
    print("P =", error, "I =", sum_error, "D =", derivative)

    last_error = error
    time.sleep_ms(50)
```

### 4. 最終成果展現

學生可以把同一台小車放在同一條跑道上，測試不同 `KP`、`KI`、`KD` 組合造成的差異。這個 case 適合作為專題化課程中的演算法比較與資料紀錄活動。

### 5. 應用題與解答

**題目：** 請建立一張調參紀錄表，至少記錄三組參數與小車表現。

**解答：**

| 組別 | KP | KI | KD | 觀察結果 |
|---|---:|---:|---:|---|
| A | 6 | 0 | 4 | 穩定但轉彎稍慢 |
| B | 8 | 0 | 5 | 轉彎較快但有些晃動 |
| C | 6 | 1 | 4 | 可補償長時間偏差，但需避免 KI 太大 |
