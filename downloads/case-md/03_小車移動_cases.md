# 03 小車移動延伸 Cases：馬達、速度與控制模組

本篇延伸原教材第 45-58 頁，重點是讓學生從一顆馬達的正反轉，逐步走到雙輪小車、PWM 速度控制、校正與模組化。

參考資料：

- MicroPython `machine.Pin`：https://docs.micropython.org/en/latest/library/machine.Pin.html
- MicroPython `machine.PWM`：https://docs.micropython.org/en/latest/library/machine.PWM.html
- MicroPython RP2 quick reference：https://docs.micropython.org/en/latest/rp2/quickref.html
- Raspberry Pi Pico hardware documentation：https://www.raspberrypi.com/documentation/pico-sdk/hardware.html
- Raspberry Pi Pico MicroPython examples：https://github.com/raspberrypi/pico-micropython-examples

## Case 1：單顆馬達方向測試

### 1. 要做的主題

用兩個 GPIO 腳位控制一顆直流馬達，觀察停止、正轉、反轉、煞車。

### 2. 分階段逐步教學

**階段 A：理解馬達需要兩個控制點**

一顆馬達的方向由 a、b 兩個腳位的高低電位決定。

**階段 B：依序測試四種組合**

`00`、`01`、`10`、`11` 都要實測。

**階段 C：記錄實際方向**

不同接線可能讓正反轉相反。

**階段 D：建立校正觀念**

不要背方向，要依車子實際結果修正程式。

### 3. 完整程式碼

```python
from machine import Pin
import time

a = Pin(12, Pin.OUT)
b = Pin(13, Pin.OUT)

def set_motor(av, bv, label, seconds=2):
    print(label, "a =", av, "b =", bv)
    a.value(av)
    b.value(bv)
    time.sleep(seconds)

set_motor(0, 0, "stop")
set_motor(0, 1, "direction 1")
set_motor(0, 0, "stop", 1)
set_motor(1, 0, "direction 2")
set_motor(1, 1, "brake", 1)
set_motor(0, 0, "stop")
```

### 4. 最終成果展現

學生可以觀察一顆馬達在四種輸出組合下的實際行為，並填寫自己的馬達方向表。

### 5. 應用題與解答

**題目：** 寫一個 `motor_forward()` 和 `motor_stop()` 函式，讓馬達前進 3 秒後停止。

**解答：**

```python
from machine import Pin
import time

a = Pin(12, Pin.OUT)
b = Pin(13, Pin.OUT)

def motor_forward():
    a.value(1)
    b.value(0)

def motor_stop():
    a.value(0)
    b.value(0)

motor_forward()
time.sleep(3)
motor_stop()
```

## Case 2：雙馬達基本移動

### 1. 要做的主題

控制 M1、M2 兩顆馬達，做出小車前進、後退、左轉、右轉與停止。

### 2. 分階段逐步教學

**階段 A：宣告四個馬達腳位**

M1 使用 `12, 13`，M2 使用 `11, 10`。

**階段 B：先測試前進**

若小車不是前進，要校正左右馬達方向。

**階段 C：封裝基本動作**

把每個動作寫成函式。

**階段 D：建立測試流程**

讓小車依序前進、後退、右轉、左轉、停止。

### 3. 完整程式碼

```python
from machine import Pin
import time

m1a = Pin(12, Pin.OUT)
m1b = Pin(13, Pin.OUT)
m2a = Pin(11, Pin.OUT)
m2b = Pin(10, Pin.OUT)

def forward():
    m1a.value(1)
    m1b.value(0)
    m2a.value(1)
    m2b.value(0)

def backward():
    m1a.value(0)
    m1b.value(1)
    m2a.value(0)
    m2b.value(1)

def turn_left():
    m1a.value(1)
    m1b.value(0)
    m2a.value(0)
    m2b.value(0)

def turn_right():
    m1a.value(0)
    m1b.value(0)
    m2a.value(1)
    m2b.value(0)

def stop():
    m1a.value(0)
    m1b.value(0)
    m2a.value(0)
    m2b.value(0)

forward()
time.sleep(2)
backward()
time.sleep(2)
turn_left()
time.sleep(1)
turn_right()
time.sleep(1)
stop()
```

### 4. 最終成果展現

小車依序前進、後退、左轉、右轉，最後停止。若方向不符合預期，學生要回到馬達方向表修正。

### 5. 應用題與解答

**題目：** 讓小車走出一個正方形，每次前進 2 秒、右轉 0.8 秒，共重複 4 次。

**解答：**

```python
from machine import Pin
import time

m1a = Pin(12, Pin.OUT)
m1b = Pin(13, Pin.OUT)
m2a = Pin(11, Pin.OUT)
m2b = Pin(10, Pin.OUT)

def forward():
    m1a.value(1)
    m1b.value(0)
    m2a.value(1)
    m2b.value(0)

def turn_right():
    m1a.value(0)
    m1b.value(0)
    m2a.value(1)
    m2b.value(0)

def stop():
    m1a.value(0)
    m1b.value(0)
    m2a.value(0)
    m2b.value(0)

for i in range(4):
    forward()
    time.sleep(2)
    turn_right()
    time.sleep(0.8)

stop()
```

## Case 3：PWM 馬達速度控制

### 1. 要做的主題

把馬達從「全速/停止」提升到「可調速度」，用百分比控制 PWM duty。

### 2. 分階段逐步教學

**階段 A：理解 duty 範圍**

MicroPython 的 `duty_u16` 使用 `0-65535`。

**階段 B：建立速度轉換函式**

把 `0-100` 轉成 `0-65535`。

**階段 C：測試不同速度**

讓馬達依序用 20%、50%、80% 轉動。

**階段 D：觀察低速限制**

馬達太低速可能不動，這是實體摩擦與電壓問題。

### 3. 完整程式碼

```python
from machine import Pin, PWM
import time

FULL_DUTY = 65535

m1a = PWM(Pin(12, Pin.OUT), freq=1000)
m1b = PWM(Pin(13, Pin.OUT), freq=1000)

def speed_to_duty(speed):
    if speed < 0:
        speed = 0
    if speed > 100:
        speed = 100
    return int(FULL_DUTY * speed / 100)

def motor_speed(speed):
    duty = speed_to_duty(speed)
    m1a.duty_u16(duty)
    m1b.duty_u16(0)

def motor_stop():
    m1a.duty_u16(0)
    m1b.duty_u16(0)

for speed in [20, 50, 80]:
    print("speed =", speed)
    motor_speed(speed)
    time.sleep(2)

motor_stop()
```

### 4. 最終成果展現

同一顆馬達會用不同速度轉動。學生能看到 duty 越大，馬達速度越快。

### 5. 應用題與解答

**題目：** 讓馬達從 10% 慢慢加速到 100%，每次增加 10%。

**解答：**

```python
from machine import Pin, PWM
import time

m1a = PWM(Pin(12, Pin.OUT), freq=1000)
m1b = PWM(Pin(13, Pin.OUT), freq=1000)

def speed_to_duty(speed):
    return int(65535 * speed / 100)

for speed in range(10, 101, 10):
    print("speed =", speed)
    m1a.duty_u16(speed_to_duty(speed))
    m1b.duty_u16(0)
    time.sleep(0.5)

m1a.duty_u16(0)
m1b.duty_u16(0)
```

## Case 4：雙輪速度差轉向

### 1. 要做的主題

用左右輪不同速度控制小車弧線轉向，理解差速控制。

### 2. 分階段逐步教學

**階段 A：左右輪都用 PWM**

每顆馬達都能用百分比速度控制。

**階段 B：建立 `run(left, right)`**

左右輪速度分開輸入。

**階段 C：測試直行與弧線轉向**

左右同速直行，左慢右快會向左轉。

**階段 D：觀察車體軌跡**

讓學生把速度差與轉彎半徑連結起來。

### 3. 完整程式碼

```python
from machine import Pin, PWM
import time

m1a = PWM(Pin(12, Pin.OUT), freq=1000)  # right motor
m1b = PWM(Pin(13, Pin.OUT), freq=1000)
m2a = PWM(Pin(11, Pin.OUT), freq=1000)  # left motor
m2b = PWM(Pin(10, Pin.OUT), freq=1000)

def duty(speed):
    if speed < 0:
        speed = 0
    if speed > 100:
        speed = 100
    return int(65535 * speed / 100)

def run(left_speed, right_speed):
    m1a.duty_u16(duty(right_speed))
    m1b.duty_u16(0)
    m2a.duty_u16(duty(left_speed))
    m2b.duty_u16(0)

def stop():
    m1a.duty_u16(0)
    m1b.duty_u16(0)
    m2a.duty_u16(0)
    m2b.duty_u16(0)

run(30, 30)   # straight
time.sleep(2)
run(10, 35)   # arc left
time.sleep(2)
run(35, 10)   # arc right
time.sleep(2)
stop()
```

### 4. 最終成果展現

小車先直行，再向左畫弧線，接著向右畫弧線。學生會理解「方向不是只有左轉/右轉，而是左右輪速度差」。

### 5. 應用題與解答

**題目：** 讓小車以 S 型前進：左弧 2 秒、右弧 2 秒，重複 3 次。

**解答：**

```python
from machine import Pin, PWM
import time

m1a = PWM(Pin(12, Pin.OUT), freq=1000)
m1b = PWM(Pin(13, Pin.OUT), freq=1000)
m2a = PWM(Pin(11, Pin.OUT), freq=1000)
m2b = PWM(Pin(10, Pin.OUT), freq=1000)

def duty(speed):
    return int(65535 * speed / 100)

def run(left_speed, right_speed):
    m1a.duty_u16(duty(right_speed))
    m1b.duty_u16(0)
    m2a.duty_u16(duty(left_speed))
    m2b.duty_u16(0)

def stop():
    m1a.duty_u16(0)
    m1b.duty_u16(0)
    m2a.duty_u16(0)
    m2b.duty_u16(0)

for i in range(3):
    run(10, 35)
    time.sleep(2)
    run(35, 10)
    time.sleep(2)

stop()
```

## Case 5：使用 `mango.motor.Motor` 控制馬達

### 1. 要做的主題

使用本機 Mango 函式庫中的 `Motor` 類別，簡化 PWM 馬達控制。

### 2. 分階段逐步教學

**階段 A：認識 `Motor.speed()`**

`speed(正值)` 正轉，`speed(負值)` 反轉，`speed(0)` 停止。

**階段 B：建立左右馬達物件**

右輪 M1：`12, 13`；左輪 M2：`11, 10`。

**階段 C：封裝小車動作**

用 `forward()`、`backward()`、`stop()` 控制。

**階段 D：觀察類別的好處**

主程式不再直接處理 duty。

### 3. 完整程式碼

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def forward(speed=20):
    right_motor.speed(speed)
    left_motor.speed(speed)

def backward(speed=20):
    right_motor.speed(-speed)
    left_motor.speed(-speed)

def stop():
    right_motor.stop()
    left_motor.stop()

forward(20)
time.sleep(2)
backward(20)
time.sleep(2)
stop()
```

### 4. 最終成果展現

小車用 Mango 的 `Motor` 類別完成前進、後退與停止，程式比直接 PWM 控制更容易閱讀。

### 5. 應用題與解答

**題目：** 加入 `spin_left(speed)`，讓左右輪反向旋轉，形成原地左旋。

**解答：**

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def spin_left(speed=20):
    right_motor.speed(speed)
    left_motor.speed(-speed)

def stop():
    right_motor.stop()
    left_motor.stop()

spin_left(20)
time.sleep(2)
stop()
```

## Case 6：小車控制模組化

### 1. 要做的主題

把小車動作整理成 `bot.py` 模組，讓主程式只負責任務流程。

### 2. 分階段逐步教學

**階段 A：建立 `bot.py`**

把馬達物件與動作函式放進模組。

**階段 B：建立 `main.py`**

主程式只呼叫 `bot.forward()`、`bot.stop()`。

**階段 C：測試模組**

確認 `import bot` 可用。

**階段 D：理解模組化**

未來避障車、循跡車都可以重用同一份 `bot.py`。

### 3. 完整程式碼

`bot.py`

```python
from mango import Motor

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def forward(speed=20):
    right_motor.speed(speed)
    left_motor.speed(speed)

def backward(speed=20):
    right_motor.speed(-speed)
    left_motor.speed(-speed)

def turn(left_speed, right_speed):
    left_motor.speed(left_speed)
    right_motor.speed(right_speed)

def spin_left(speed=20):
    left_motor.speed(-speed)
    right_motor.speed(speed)

def spin_right(speed=20):
    left_motor.speed(speed)
    right_motor.speed(-speed)

def stop():
    left_motor.stop()
    right_motor.stop()
```

`main.py`

```python
import time
import bot

bot.forward(20)
time.sleep(2)

bot.turn(10, 35)
time.sleep(2)

bot.turn(35, 10)
time.sleep(2)

bot.spin_left(20)
time.sleep(1)

bot.stop()
```

### 4. 最終成果展現

小車會依照主程式流程完成直行、左右弧線、原地旋轉與停止。學生會看到「底層控制」和「任務流程」被分開。

### 5. 應用題與解答

**題目：** 在 `bot.py` 新增 `square(speed)` 函式，讓小車走出近似正方形。

**解答：**

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def forward(speed=20):
    right_motor.speed(speed)
    left_motor.speed(speed)

def spin_right(speed=20):
    left_motor.speed(speed)
    right_motor.speed(-speed)

def stop():
    left_motor.stop()
    right_motor.stop()

def square(speed=20):
    for i in range(4):
        forward(speed)
        time.sleep(2)
        spin_right(speed)
        time.sleep(0.7)
    stop()

square(20)
```

## Case 7：雙馬達方向校正工具

### 1. 要做的主題

建立一支校正程式，快速測試左右馬達正負速度是否符合「正值前進、負值後退」的約定。

### 2. 分階段逐步教學

**階段 A：定義校正係數**

用 `LEFT_SIGN` 與 `RIGHT_SIGN` 表示左右馬達方向。若某邊馬達接線方向相反，就把係數改成 `-1`。

**階段 B：只測一邊馬達**

先單獨讓左輪、右輪轉動，確認哪一邊的正轉方向不對。

**階段 C：測雙輪直行**

當左右輪正值都能讓小車往前，後續所有 case 才有穩定基礎。

**階段 D：把校正結果保留下來**

學生可以把校正後的 `drive()` 函式複製到之後的小車任務中。

### 3. 完整程式碼

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

LEFT_SIGN = 1
RIGHT_SIGN = 1

def drive(left, right):
    left_motor.speed(left * LEFT_SIGN)
    right_motor.speed(right * RIGHT_SIGN)

def stop():
    left_motor.stop()
    right_motor.stop()

tests = [
    ("left wheel forward", 20, 0, 1.5),
    ("right wheel forward", 0, 20, 1.5),
    ("both wheels forward", 20, 20, 2),
    ("both wheels backward", -20, -20, 2),
]

for name, left, right, seconds in tests:
    print(name, "left =", left, "right =", right)
    drive(left, right)
    time.sleep(seconds)
    stop()
    time.sleep(1)
```

### 4. 最終成果展現

學生能知道左右馬達是否接反，並得到一個符合自己車體的 `drive(left, right)` 函式。

### 5. 應用題與解答

**題目：** 如果右輪在正速度時往後轉，請修改程式讓 `drive(20, 20)` 可以前進。

**解答：**

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

LEFT_SIGN = 1
RIGHT_SIGN = -1

def drive(left, right):
    left_motor.speed(left * LEFT_SIGN)
    right_motor.speed(right * RIGHT_SIGN)

def stop():
    left_motor.stop()
    right_motor.stop()

drive(20, 20)
time.sleep(2)
stop()
```

## Case 8：軟啟動與軟停止

### 1. 要做的主題

讓小車速度逐步增加與逐步降低，避免一啟動就暴衝，也讓學生理解速度曲線的概念。

### 2. 分階段逐步教學

**階段 A：建立目前速度**

用 `current_left` 與 `current_right` 記錄目前馬達速度。

**階段 B：每次只改一小步**

目標速度不是一次到位，而是每隔一小段時間增加或減少 `step`。

**階段 C：封裝成 `ramp_to()`**

未來不論要直行、後退或停止，都可以共用同一個函式。

**階段 D：比較立即啟動與軟啟動**

讓學生觀察車身晃動、輪胎打滑與行進距離是否變穩定。

### 3. 完整程式碼

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

current_left = 0
current_right = 0

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def approach(current, target, step):
    if current < target:
        return min(current + step, target)
    if current > target:
        return max(current - step, target)
    return current

def ramp_to(target_left, target_right, step=2, delay_ms=80):
    global current_left, current_right

    while current_left != target_left or current_right != target_right:
        current_left = approach(current_left, target_left, step)
        current_right = approach(current_right, target_right, step)
        drive(current_left, current_right)
        print("speed =", current_left, current_right)
        time.sleep_ms(delay_ms)

def stop():
    ramp_to(0, 0)
    left_motor.stop()
    right_motor.stop()

ramp_to(30, 30)
time.sleep(2)
ramp_to(10, 35)
time.sleep(2)
stop()
```

### 4. 最終成果展現

小車會慢慢加速到直行速度，再平滑變成弧線轉彎，最後逐步減速停止。

### 5. 應用題與解答

**題目：** 加入按鈕急停：軟啟動過程中只要按下按鈕，就立刻停止。

**解答：**

```python
from machine import Pin
from mango import Motor
import time

BUTTON_ACTIVE = 1
btn = Pin(3, Pin.IN)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

current_left = 0
current_right = 0

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def hard_stop():
    left_motor.stop()
    right_motor.stop()

def approach(current, target, step):
    if current < target:
        return min(current + step, target)
    if current > target:
        return max(current - step, target)
    return current

def ramp_to(target_left, target_right, step=2, delay_ms=80):
    global current_left, current_right

    while current_left != target_left or current_right != target_right:
        if btn.value() == BUTTON_ACTIVE:
            current_left = 0
            current_right = 0
            hard_stop()
            print("emergency stop")
            return False

        current_left = approach(current_left, target_left, step)
        current_right = approach(current_right, target_right, step)
        drive(current_left, current_right)
        time.sleep_ms(delay_ms)

    return True

if ramp_to(35, 35):
    time.sleep(3)

ramp_to(0, 0)
hard_stop()
```

## Case 9：動作腳本播放器

### 1. 要做的主題

把小車動作寫成一份腳本清單，讓程式依序播放前進、轉彎、停止等動作。

### 2. 分階段逐步教學

**階段 A：定義動作格式**

每個動作用 `(名稱, 左輪速度, 右輪速度, 秒數)` 表示。

**階段 B：建立 `play_script()`**

函式逐筆讀取清單，執行馬達速度與等待時間。

**階段 C：把路徑變成資料**

學生只要修改清單，就能改變小車路線，不必一直改函式。

**階段 D：加入動作名稱輸出**

讓 Shell 成為除錯工具，知道小車目前正在執行哪一步。

### 3. 完整程式碼

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def play_script(script):
    for name, left, right, seconds in script:
        print("action =", name, "left =", left, "right =", right)
        drive(left, right)
        time.sleep(seconds)
        stop()
        time.sleep_ms(300)

path = [
    ("forward 1", 22, 22, 1.5),
    ("turn right", 24, -24, 0.55),
    ("forward 2", 22, 22, 1.5),
    ("turn left", -24, 24, 0.55),
    ("finish", 0, 0, 0.5),
]

play_script(path)
```

### 4. 最終成果展現

小車會依照清單完成一段固定路徑。學生可以像修改劇本一樣修改路線，也能把測試結果回寫成更準確的秒數。

### 5. 應用題與解答

**題目：** 讓同一段路徑重複播放 3 次。

**解答：**

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def play_script(script, repeat=1):
    for round_id in range(repeat):
        print("round =", round_id + 1)
        for name, left, right, seconds in script:
            print("action =", name)
            drive(left, right)
            time.sleep(seconds)
            stop()
            time.sleep_ms(300)

path = [
    ("forward", 22, 22, 1.2),
    ("spin right", 24, -24, 0.5),
]

play_script(path, repeat=3)
stop()
```

## Case 10：Shell 文字指令遙控車

### 1. 要做的主題

使用 Thonny Shell 輸入文字指令控制小車，建立簡易的人機介面。

### 2. 分階段逐步教學

**階段 A：定義指令表**

用 `f`、`b`、`l`、`r`、`s` 代表前進、後退、左轉、右轉、停止。

**階段 B：用 `input()` 讀取命令**

小車每次等待一個指令，收到後才動作。

**階段 C：加入預設速度與時間**

每個動作只執行短時間，避免輸入錯誤時一直跑。

**階段 D：加入錯誤提示**

學生輸入未知指令時，程式不應該失控，而是顯示可用指令。

### 3. 完整程式碼

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

SPEED = 22
MOVE_TIME = 0.6

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def run_command(cmd):
    if cmd == "f":
        drive(SPEED, SPEED)
    elif cmd == "b":
        drive(-SPEED, -SPEED)
    elif cmd == "l":
        drive(-SPEED, SPEED)
    elif cmd == "r":
        drive(SPEED, -SPEED)
    elif cmd == "s":
        stop()
        return
    else:
        print("commands: f b l r s q")
        return

    time.sleep(MOVE_TIME)
    stop()

while True:
    command = input("car> ").strip().lower()

    if command == "q":
        stop()
        print("bye")
        break

    run_command(command)
```

### 4. 最終成果展現

學生可以在 Thonny Shell 輸入 `f`、`b`、`l`、`r`、`s` 控制小車，並理解「控制介面」與「馬達動作」可以分開設計。

### 5. 應用題與解答

**題目：** 支援 `f 30` 這種指令，讓第二個數字代表速度。

**解答：**

```python
from mango import Motor
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

DEFAULT_SPEED = 22
MOVE_TIME = 0.6

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def parse_command(text):
    parts = text.strip().lower().split()
    if len(parts) == 0:
        return "", DEFAULT_SPEED

    cmd = parts[0]
    speed = DEFAULT_SPEED

    if len(parts) >= 2:
        speed = int(parts[1])
        if speed < 0:
            speed = 0
        if speed > 60:
            speed = 60

    return cmd, speed

def run_command(cmd, speed):
    if cmd == "f":
        drive(speed, speed)
    elif cmd == "b":
        drive(-speed, -speed)
    elif cmd == "l":
        drive(-speed, speed)
    elif cmd == "r":
        drive(speed, -speed)
    elif cmd == "s":
        stop()
        return
    else:
        print("commands: f 30, b 20, l 25, r 25, s, q")
        return

    time.sleep(MOVE_TIME)
    stop()

while True:
    text = input("car> ")
    cmd, speed = parse_command(text)

    if cmd == "q":
        stop()
        print("bye")
        break

    run_command(cmd, speed)
```
