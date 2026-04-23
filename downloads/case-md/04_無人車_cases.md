# 04 無人車延伸 Cases：差速、避障、循跡與伺服掃描

本篇延伸原教材第 59-65 頁，將馬達、超音波、RGB、尋跡感測器與伺服馬達整合成無人車應用。每個 case 都從明確策略開始，再逐步轉成程式。

參考資料：

- MicroPython `machine.PWM`：https://docs.micropython.org/en/latest/library/machine.PWM.html
- MicroPython `machine.ADC`：https://docs.micropython.org/en/v1.14/library/machine.ADC.html
- MicroPython `machine.I2C`：https://docs.micropython.org/en/latest/library/machine.I2C.html
- MicroPython RP2 quick reference：https://docs.micropython.org/en/latest/rp2/quickref.html
- Raspberry Pi Pico Python SDK：https://datasheets.raspberrypi.com/pico/sdk/pico_python_sdk.pdf
- Pololu QTR reflectance sensor guide：https://www.pololu.com/docs/0J19/all

## Case 1：差速控制展示

### 1. 要做的主題

用左右輪不同速度展示直行、弧線轉向與原地旋轉。

### 2. 分階段逐步教學

**階段 A：建立左右馬達**

使用 `mango.Motor` 建立右輪與左輪。

**階段 B：定義 `drive(left, right)`**

左輪與右輪速度分開控制。

**階段 C：依序測試動作**

同速直行、左右不同速弧線轉向、左右反向原地旋轉。

**階段 D：對照車體運動表**

讓學生把數值和小車軌跡連起來。

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

motions = [
    ("straight", 20, 20, 2),
    ("arc left", 10, 35, 2),
    ("arc right", 35, 10, 2),
    ("spin left", -20, 20, 1),
    ("spin right", 20, -20, 1),
]

for name, left, right, seconds in motions:
    print(name, left, right)
    drive(left, right)
    time.sleep(seconds)

stop()
```

### 4. 最終成果展現

小車會依序展示直行、左右弧線與左右原地旋轉。學生可以觀察差速對路徑的影響。

### 5. 應用題與解答

**題目：** 設計一個「小車迴避動作」：先後退 0.5 秒，再原地右旋 0.8 秒，最後停止。

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

drive(-20, -20)
time.sleep(0.5)
drive(20, -20)
time.sleep(0.8)
stop()
```

## Case 2：固定左轉避障車

### 1. 要做的主題

使用超音波偵測障礙物，距離小於 20 cm 時固定左轉。

### 2. 分階段逐步教學

**階段 A：先讓小車直行**

安全距離時左右輪同速前進。

**階段 B：讀取超音波距離**

使用 `RUS04.ping()`。

**階段 C：加入距離判斷**

小於 20 cm 代表障礙物太近。

**階段 D：加入 RGB 狀態燈**

綠燈直行，紅燈避障。

### 3. 完整程式碼

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

while True:
    dist = sensor.ping()
    print("distance =", dist, "cm")

    if dist < 20:
        sensor.rgb_all((255, 0, 0))
        drive(5, 30)   # left slow, right fast -> turn left
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```

## Case 3：倒車後轉向避障

### 1. 要做的主題

遇到障礙物時先停下、後退，再轉向。這比直接轉向更不容易卡在障礙物前。

### 2. 分階段逐步教學

**階段 A：建立緊急避障流程**

停止、後退、轉向、恢復前進。

**階段 B：把流程寫成 `avoid()` 函式**

讓主迴圈保持簡潔。

**階段 C：使用時間控制動作**

後退與轉向都用固定時間。

**階段 D：調整速度與時間**

讓學生依場地調整參數。

### 3. 完整程式碼

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def avoid():
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)

    drive(-18, -18)
    time.sleep_ms(500)

    drive(20, -20)
    time.sleep_ms(700)

    stop()

while True:
    dist = sensor.ping()
    print("distance =", dist, "cm")

    if dist < 20:
        avoid()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車遇到障礙時會先後退，再原地右旋，最後繼續前進。

### 5. 應用題與解答

**題目：** 改成「後退後原地左旋」。

**解答：**

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def avoid_left():
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(500)
    drive(-20, 20)
    time.sleep_ms(700)
    stop()

while True:
    if sensor.ping() < 20:
        avoid_left()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)
    time.sleep_ms(100)
```

## Case 4：左右交替避障策略

### 1. 要做的主題

讓小車每次遇到障礙時左右交替轉向，避免永遠往同一邊卡住。

### 2. 分階段逐步教學

**階段 A：建立方向狀態**

用 `turn_left_next` 記錄下一次要左轉還是右轉。

**階段 B：每次避障後切換方向**

`turn_left_next = not turn_left_next`。

**階段 C：保留後退動作**

先後退再轉向，降低撞擊。

**階段 D：觀察策略差異**

和固定左轉相比，看哪個比較不容易卡住。

### 3. 完整程式碼

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

turn_left_next = True

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def avoid():
    global turn_left_next

    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)

    drive(-18, -18)
    time.sleep_ms(450)

    if turn_left_next:
        drive(-20, 20)
        print("avoid: left")
    else:
        drive(20, -20)
        print("avoid: right")

    time.sleep_ms(650)
    stop()

    turn_left_next = not turn_left_next

while True:
    dist = sensor.ping()

    if dist < 20:
        avoid()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車第一次遇障往左避，第二次往右避，之後左右交替。

### 5. 應用題與解答

**題目：** 讓小車每遇到 3 次障礙後，原地旋轉更久一點，嘗試脫困。

**解答：**

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

count = 0
turn_left_next = True

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def avoid():
    global count, turn_left_next

    count += 1
    drive(-18, -18)
    time.sleep_ms(400)

    turn_time = 1200 if count % 3 == 0 else 650

    if turn_left_next:
        drive(-20, 20)
    else:
        drive(20, -20)

    time.sleep_ms(turn_time)
    stop()
    turn_left_next = not turn_left_next

while True:
    if sensor.ping() < 20:
        sensor.rgb_all((255, 0, 0))
        avoid()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)
    time.sleep_ms(100)
```

## Case 5：尋跡感測器讀值與基礎循跡

### 1. 要做的主題

讀取 I2C 灰度尋跡感測器的數位狀態，並用簡單判斷控制小車循線。

### 2. 分階段逐步教學

**階段 A：建立 I2C 與 GraySensor8**

使用 Mango 內建 `bus.i2c` 與 `GraySensor8`。

**階段 B：先只印出狀態**

觀察黑線在不同位置時字串如何變化。

**階段 C：挑中間四路判斷**

使用 `digital_channels='4'`，取得類似 `L2 L1 R1 R2` 的狀態。

**階段 D：根據狀態修正方向**

中間在線上直行，偏左/偏右就修正。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

while True:
    state = line.digital_state
    print("line =", state)

    if state == "0110":
        drive(18, 18)
    elif state in ("1100", "1000", "0100"):
        drive(8, 22)
    elif state in ("0011", "0001", "0010"):
        drive(22, 8)
    elif state == "0000":
        stop()
    else:
        drive(12, 12)

    time.sleep_ms(30)
```

### 4. 最終成果展現

小車可以用最基本的左右修正方式沿著黑線前進。若感測器黑白邏輯相反，需依實際 `print()` 結果調整狀態字串。

### 5. 應用題與解答

**題目：** 當完全離線 `0000` 時，不要立刻停止，改成慢速原地左轉搜尋線。

**解答：**

```python
from mango import GraySensor8
from mango import bus
from mango import Motor
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

while True:
    state = line.digital_state
    print("line =", state)

    if state == "0110":
        drive(18, 18)
    elif state in ("1100", "1000", "0100"):
        drive(8, 22)
    elif state in ("0011", "0001", "0010"):
        drive(22, 8)
    elif state == "0000":
        drive(-10, 10)
    else:
        drive(12, 12)

    time.sleep_ms(30)
```

## Case 6：伺服掃描式避障

### 1. 要做的主題

把超音波裝在伺服馬達上，遇到障礙時左右掃描，選擇距離較遠的一側轉向。

### 2. 分階段逐步教學

**階段 A：控制伺服角度**

使用 `Servo.position(angle)`。

**階段 B：在不同角度讀取距離**

左、中、右各讀一次。

**階段 C：比較左右距離**

哪邊距離大，就往哪邊轉。

**階段 D：回到中間繼續前進**

掃描後伺服回正，車子繼續走。

### 3. 完整程式碼

```python
from mango import Motor, RUS04, Servo
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
servo = Servo(pin=6)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def scan(angle):
    servo.position(angle)
    time.sleep_ms(500)
    return sensor.ping()

def choose_direction():
    stop()
    center = scan(90)
    left = scan(150)
    right = scan(30)
    servo.position(90)

    print("scan center/left/right =", center, left, right)

    if left > right:
        drive(-20, 20)
    else:
        drive(20, -20)

    time.sleep_ms(700)
    stop()

servo.position(90)

while True:
    dist = sensor.ping()
    print("front =", dist)

    if dist < 25:
        sensor.rgb_all((255, 0, 0))
        choose_direction()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```

### 4. 最終成果展現

小車遇到障礙物時會停下，伺服帶著超音波左右掃描，選擇較空曠的一邊轉向。

### 5. 應用題與解答

**題目：** 若左右距離都小於 20 cm，讓小車後退 1 秒再重新掃描。

**解答：**

```python
from mango import Motor, RUS04, Servo
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
servo = Servo(pin=6)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def scan(angle):
    servo.position(angle)
    time.sleep_ms(500)
    return sensor.ping()

def scan_and_turn():
    left = scan(150)
    right = scan(30)
    servo.position(90)

    if left < 20 and right < 20:
        drive(-18, -18)
        time.sleep(1)
        stop()
        return

    if left > right:
        drive(-20, 20)
    else:
        drive(20, -20)

    time.sleep_ms(700)
    stop()

servo.position(90)

while True:
    if sensor.ping() < 25:
        sensor.rgb_all((255, 0, 0))
        stop()
        scan_and_turn()
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(100)
```
## Case 7：I2C 掃描與尋跡感測器診斷

### 1. 要做的主題

在開始循跡前，先用 I2C 掃描與灰階感測器讀值診斷，確認硬體連線、位址與黑白讀值都正常。

### 2. 分階段逐步教學

**階段 A：掃描 I2C 裝置**

使用 `bus.i2c.scan()` 列出目前掛在 I2C 匯流排上的裝置位址。

**階段 B：確認 ADS1115 位址**

依原教材第 64 頁，本車課程預設使用 I2C 四路尋跡狀態；Mango 函式庫以 `GraySensor8(..., digital_channels='4')` 讀取中間四路，常見 I2C 位址為 `0x48` 與 `0x49`。

**階段 C：讀取類比值與數位狀態**

`read_analog()` 可看原始數值，`digital_state` 可看黑白判斷結果。

**階段 D：用手或黑線逐一遮住感測器**

學生要觀察每一個位置的數字是否會改變，建立「感測器排序」概念。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
import time

addresses = bus.i2c.scan()
print("I2C addresses =", [hex(addr) for addr in addresses])

if 0x48 not in addresses:
    print("warning: cannot find left ADS1115 at 0x48")

if 0x49 not in addresses:
    print("warning: cannot find right ADS1115 at 0x49")

line = GraySensor8(i2c=bus.i2c, digital_channels='4')

while True:
    analog = line.read_analog()
    digital = line.digital_state
    print("digital =", digital, "analog =", analog)
    time.sleep_ms(300)
```

### 4. 最終成果展現

Shell 會顯示 I2C 裝置位址、四路黑白狀態與底層類比讀值。學生可以在循跡前先排除「沒有接到」「左右接反」「某一路沒有反應」等問題。

### 5. 應用題與解答

**題目：** 顯示目前偵測到黑線的感測器數量。

**解答：**

```python
from mango import GraySensor8
from mango import bus
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')

while True:
    state = line.digital_state
    black_count = state.count("1")
    print("state =", state, "black sensors =", black_count)
    time.sleep_ms(300)
```

## Case 8：加權循跡比例控制

### 1. 要做的主題

把四路尋跡感測器的黑線位置轉成誤差值，再用比例控制調整左右輪速度，讓循跡比單純 if/elif 更平滑。

### 2. 分階段逐步教學

**階段 A：定義感測器權重**

由左到右設定為 `-2, -1, 1, 2`。黑線越偏左，誤差越負；越偏右，誤差越正。

**階段 B：計算加權平均**

只把讀到黑線的感測器納入平均，得到目前黑線相對於車身中心的位置。

**階段 C：用 Kp 算修正量**

`correction = error * KP`，偏左時左輪慢、右輪快；偏右時右輪慢、左輪快。

**階段 D：限制速度範圍**

避免修正後超出馬達可用速度，讓控制更穩定。

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
KP = 5
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

def stop():
    left_motor.stop()
    right_motor.stop()

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
    correction = int(error * KP)
    left = clamp(BASE_SPEED + correction, -35, 35)
    right = clamp(BASE_SPEED - correction, -35, 35)

    print("error =", error, "left =", left, "right =", right)
    drive(left, right)
    time.sleep_ms(40)
```

### 4. 最終成果展現

小車會依黑線偏移量連續調整左右輪速度，而不是突然切換方向。學生會看到循跡從「規則判斷」進一步變成「比例控制」。

### 5. 應用題與解答

**題目：** 當完全找不到黑線時，依照最後一次誤差方向原地搜尋。

**解答：**

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
KP = 5
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

def get_error_and_seen():
    global last_error

    state = line.digital_state
    total = 0
    count = 0

    for i in range(4):
        if state[i] == "1":
            total += WEIGHTS[i]
            count += 1

    if count == 0:
        return last_error, False

    last_error = total / count
    return last_error, True

while True:
    error, seen = get_error_and_seen()

    if not seen:
        if last_error < 0:
            drive(-18, 18)
        else:
            drive(18, -18)
        print("search line, last_error =", last_error)
        time.sleep_ms(80)
        continue

    correction = int(error * KP)
    left = clamp(BASE_SPEED + correction, -35, 35)
    right = clamp(BASE_SPEED - correction, -35, 35)
    drive(left, right)
    print("follow line, error =", error)
    time.sleep_ms(40)
```

## Case 9：循跡結合超音波避障

### 1. 要做的主題

把循跡車與超音波避障整合：平常沿著黑線走，前方太近時先避開障礙，再回到循跡。

### 2. 分階段逐步教學

**階段 A：設定任務優先順序**

安全優先於循跡。只要前方距離小於門檻，先執行避障。

**階段 B：保留循跡函式**

循跡控制獨立寫成 `follow_line_step()`，方便被主迴圈呼叫。

**階段 C：設計避障動作**

避障先停、後退、旋轉，再交回循跡控制。

**階段 D：加入 RGB 狀態提示**

綠色代表循跡，紅色代表避障，方便觀察狀態切換。

### 3. 完整程式碼

```python
from mango import GraySensor8
from mango import bus
from mango import Motor, RUS04
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
BASE_SPEED = 18
KP = 5
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

def stop():
    left_motor.stop()
    right_motor.stop()

def get_line_error():
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

def follow_line_step():
    error = get_line_error()
    correction = int(error * KP)
    left = clamp(BASE_SPEED + correction, -35, 35)
    right = clamp(BASE_SPEED - correction, -35, 35)
    sensor.rgb_all((0, 255, 0))
    drive(left, right)
    print("line error =", error)

def avoid_obstacle():
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(500)
    drive(20, -20)
    time.sleep_ms(700)
    stop()

while True:
    dist = sensor.ping()
    print("distance =", dist)

    if dist < 18:
        avoid_obstacle()
    else:
        follow_line_step()

    time.sleep_ms(50)
```

### 4. 最終成果展現

小車能沿黑線行駛，遇到前方障礙時會先紅燈避開，再回到循跡邏輯。這個 case 適合作為「多感測器整合」的第一個完整任務。

### 5. 應用題與解答

**題目：** 加入中距離警示：距離 18-30 cm 時亮橘燈並降低循跡速度。

**解答：**

```python
from mango import GraySensor8
from mango import bus
from mango import Motor, RUS04
import time

line = GraySensor8(i2c=bus.i2c, digital_channels='4')
sensor = RUS04(sensor_pin=15, rgb_pin=14)
right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)

WEIGHTS = [-2, -1, 1, 2]
KP = 5
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

def stop():
    left_motor.stop()
    right_motor.stop()

def get_line_error():
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

def follow_line_step(base_speed):
    error = get_line_error()
    correction = int(error * KP)
    left = clamp(base_speed + correction, -35, 35)
    right = clamp(base_speed - correction, -35, 35)
    drive(left, right)

def avoid_obstacle():
    sensor.rgb_all((255, 0, 0))
    stop()
    time.sleep_ms(150)
    drive(-18, -18)
    time.sleep_ms(500)
    drive(20, -20)
    time.sleep_ms(700)
    stop()

while True:
    dist = sensor.ping()

    if dist < 18:
        avoid_obstacle()
    elif dist < 30:
        sensor.rgb_all((255, 120, 0))
        follow_line_step(12)
    else:
        sensor.rgb_all((0, 255, 0))
        follow_line_step(18)

    time.sleep_ms(50)
```

## Case 10：伺服多角度環境掃描

### 1. 要做的主題

讓伺服馬達帶著超音波感測器掃描多個角度，找出最空曠的方向，再決定小車轉向。

### 2. 分階段逐步教學

**階段 A：設定掃描角度**

使用 `[30, 60, 90, 120, 150]` 代表右側、右前、正前、左前、左側。

**階段 B：每個角度讀一次距離**

伺服轉到角度後等待穩定，再讀取超音波距離。

**階段 C：尋找最大距離**

最大距離代表最可能安全通過的方向。

**階段 D：把角度轉成動作**

如果最佳角度小於 90 度，向右轉；大於 90 度，向左轉；等於 90 度則直行。

### 3. 完整程式碼

```python
from mango import Motor, RUS04, Servo
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
servo = Servo(pin=6)

ANGLES = [30, 60, 90, 120, 150]

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def read_at(angle):
    servo.position(angle)
    time.sleep_ms(450)
    return sensor.ping()

def scan_world():
    results = []
    for angle in ANGLES:
        dist = read_at(angle)
        results.append((angle, dist))
        print("angle =", angle, "distance =", dist)
    servo.position(90)
    return results

def choose_best(results):
    best_angle = results[0][0]
    best_dist = results[0][1]

    for angle, dist in results:
        if dist > best_dist:
            best_angle = angle
            best_dist = dist

    return best_angle, best_dist

def turn_to(angle):
    if angle < 80:
        drive(22, -22)
        time.sleep_ms(650)
    elif angle > 100:
        drive(-22, 22)
        time.sleep_ms(650)
    else:
        drive(18, 18)
        time.sleep_ms(500)
    stop()

servo.position(90)

while True:
    if sensor.ping() < 25:
        sensor.rgb_all((255, 0, 0))
        stop()
        results = scan_world()
        best_angle, best_dist = choose_best(results)
        print("best =", best_angle, best_dist)
        turn_to(best_angle)
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(80)
```

### 4. 最終成果展現

小車前方受阻時，會停下來左右掃描多個角度，選擇距離最大的方向轉過去。學生能把「感測資料表」轉成「決策」。

### 5. 應用題與解答

**題目：** 如果所有角度都小於 20 cm，讓小車先後退 1 秒，再重新掃描。

**解答：**

```python
from mango import Motor, RUS04, Servo
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)
servo = Servo(pin=6)

ANGLES = [30, 60, 90, 120, 150]

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

def stop():
    left_motor.stop()
    right_motor.stop()

def read_at(angle):
    servo.position(angle)
    time.sleep_ms(450)
    return sensor.ping()

def scan_world():
    results = []
    for angle in ANGLES:
        results.append((angle, read_at(angle)))
    servo.position(90)
    return results

def choose_best(results):
    best_angle = results[0][0]
    best_dist = results[0][1]

    for angle, dist in results:
        if dist > best_dist:
            best_angle = angle
            best_dist = dist

    return best_angle, best_dist

def back_up():
    drive(-18, -18)
    time.sleep(1)
    stop()

def turn_to(angle):
    if angle < 80:
        drive(22, -22)
    elif angle > 100:
        drive(-22, 22)
    else:
        drive(18, 18)

    time.sleep_ms(650)
    stop()

servo.position(90)

while True:
    if sensor.ping() < 25:
        sensor.rgb_all((255, 0, 0))
        stop()
        results = scan_world()
        best_angle, best_dist = choose_best(results)
        print("best =", best_angle, best_dist)

        if best_dist < 20:
            back_up()
        else:
            turn_to(best_angle)
    else:
        sensor.rgb_all((0, 255, 0))
        drive(18, 18)

    time.sleep_ms(80)
```

### 4. 最終成果展現

小車平常直行；前方遇到障礙物時亮紅燈並左轉，距離安全後回到綠燈直行。

### 5. 應用題與解答

**題目：** 把避障門檻改成 30 cm，並讓轉向時速度更慢。

**解答：**

```python
from mango import Motor, RUS04
import time

right_motor = Motor(a_pin=12, b_pin=13)
left_motor = Motor(a_pin=11, b_pin=10)
sensor = RUS04(sensor_pin=15, rgb_pin=14)

def drive(left, right):
    left_motor.speed(left)
    right_motor.speed(right)

while True:
    dist = sensor.ping()

    if dist < 30:
        sensor.rgb_all((255, 0, 0))
        drive(5, 18)
    else:
        sensor.rgb_all((0, 255, 0))
        drive(15, 15)

    time.sleep_ms(100)
```

