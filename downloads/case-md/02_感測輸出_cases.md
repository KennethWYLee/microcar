# 02 感測與輸出延伸 Cases：蜂鳴器、RGB 與超音波

本篇延伸原教材第 31-44 頁，從 PWM 蜂鳴器、WS2812B RGB 燈，到 RUS04 超音波測距。教學順序是：先控制輸出，再讀取感測器，最後把感測值轉成聲光回饋。

參考資料：

- MicroPython `machine.PWM`：https://docs.micropython.org/en/latest/library/machine.PWM.html
- MicroPython `machine.ADC`：https://docs.micropython.org/en/v1.12/library/machine.ADC.html
- MicroPython `neopixel`：https://micropython.org/resources/docs/en/latest/library/neopixel.html
- MicroPython `machine.time_pulse_us`：https://docs.micropython.org/en/latest/library/machine.html
- Raspberry Pi Pico MicroPython examples：https://github.com/raspberrypi/pico-micropython-examples

## Case 1：蜂鳴器單音控制

### 1. 要做的主題

使用 PWM 控制板載蜂鳴器，讓它發出指定頻率的聲音。

### 2. 分階段逐步教學

**階段 A：理解 PWM 與蜂鳴器**

蜂鳴器需要頻率才能發出聲音，`freq` 影響音高，`duty_u16` 影響輸出強度。

**階段 B：建立 PWM 物件**

用 `PWM(Pin(6))` 控制板載蜂鳴器。

**階段 C：寫成 `beep()` 函式**

讓每次發聲都有頻率、時間與音量參數。

**階段 D：停止聲音**

發聲後要把 duty 設為 0。

### 3. 完整程式碼

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6, Pin.OUT))

def beep(freq=800, duration_ms=300, duty=5000):
    buzzer.freq(freq)
    buzzer.duty_u16(duty)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

beep(500, 300)
time.sleep(0.5)
beep(900, 300)
time.sleep(0.5)
beep(1200, 300)

buzzer.deinit()
```

### 4. 最終成果展現

蜂鳴器依序發出三個不同音高的短音。學生可明顯聽到頻率改變造成音高不同。

### 5. 應用題與解答

**題目：** 做出「倒數提示音」：低音、低音、高音。

**解答：**

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6, Pin.OUT))

def beep(freq, duration_ms=200):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)
    time.sleep_ms(150)

beep(500)
beep(500)
beep(1200, 500)

buzzer.deinit()
```

## Case 2：蜂鳴器旋律播放器

### 1. 要做的主題

用陣列儲存旋律，讓蜂鳴器依序播放音符。

### 2. 分階段逐步教學

**階段 A：把音符抽象成資料**

每個音符用 `(頻率, 時間)` 表示。

**階段 B：用迴圈播放**

`for note in melody` 逐一播放音符。

**階段 C：加入休止符**

頻率為 `0` 時代表安靜。

**階段 D：調整節奏**

讓學生改變 duration 觀察節奏差異。

### 3. 完整程式碼

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6, Pin.OUT))

melody = [
    (523, 200),  # C5
    (587, 200),  # D5
    (659, 200),  # E5
    (0,   150),  # pause
    (659, 200),
    (587, 200),
    (523, 400),
]

def play_tone(freq, duration_ms, duty=5000):
    if freq == 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)

    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)
    time.sleep_ms(60)

for freq, duration in melody:
    play_tone(freq, duration)

buzzer.deinit()
```

### 4. 最終成果展現

蜂鳴器會播放一小段簡單旋律。學生可以把旋律資料改掉，練習資料驅動控制。

### 5. 應用題與解答

**題目：** 加入一個警示旋律：高音、低音交替 5 次。

**解答：**

```python
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6, Pin.OUT))

def play(freq, duration_ms=150):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)
    time.sleep_ms(80)

for i in range(5):
    play(1200)
    play(500)

buzzer.deinit()
```

## Case 3：RGB 狀態燈

### 1. 要做的主題

使用芒果平台的 `WS2812B` 控制 RGB 彩燈，建立紅、綠、藍三種狀態。

### 2. 分階段逐步教學

**階段 A：建立 RGB 物件**

使用 `WS2812B(pin=2, leds=6)`。

**階段 B：定義狀態顏色**

綠色代表正常，藍色代表待機，紅色代表警示。

**階段 C：封裝 `show_status()`**

用函式管理狀態，不讓主程式到處寫顏色。

**階段 D：依序展示狀態**

讓學生看見狀態燈的用途。

### 3. 完整程式碼

```python
from mango import WS2812B
import time

rgb = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)

STATUS_COLORS = {
    "ready": (0, 0, 255),
    "run": (0, 255, 0),
    "warn": (255, 150, 0),
    "danger": (255, 0, 0),
    "off": (0, 0, 0),
}

def show_status(name):
    color = STATUS_COLORS[name]
    rgb.show_all(color)

show_status("ready")
time.sleep(1)
show_status("run")
time.sleep(1)
show_status("warn")
time.sleep(1)
show_status("danger")
time.sleep(1)
show_status("off")
```

### 4. 最終成果展現

RGB 會依序顯示藍、綠、橘、紅、關燈，形成可辨識的小車狀態燈。

### 5. 應用題與解答

**題目：** 增加 `charging` 狀態，顏色為紫色，並讓它顯示 2 秒。

**解答：**

```python
from mango import WS2812B
import time

rgb = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)

STATUS_COLORS = {
    "ready": (0, 0, 255),
    "run": (0, 255, 0),
    "warn": (255, 150, 0),
    "danger": (255, 0, 0),
    "charging": (180, 0, 255),
    "off": (0, 0, 0),
}

def show_status(name):
    rgb.show_all(STATUS_COLORS[name])

show_status("charging")
time.sleep(2)
show_status("off")
```

## Case 4：RGB 跑馬燈

### 1. 要做的主題

讓 6 顆 RGB 燈依序亮起，製作小車啟動動畫。

### 2. 分階段逐步教學

**階段 A：理解 LED 索引**

6 顆 LED 的索引是 `0-5`。

**階段 B：一次只亮一顆**

先關閉全部，再點亮指定索引。

**階段 C：用迴圈移動亮點**

每次 `i` 增加，亮點就往下一顆移動。

**階段 D：做成函式**

未來啟動小車時可直接呼叫。

### 3. 完整程式碼

```python
from mango import WS2812B
import time

rgb = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)

def clear():
    rgb.show_all((0, 0, 0))

def chase(color=(0, 255, 0), rounds=3, delay_ms=120):
    for r in range(rounds):
        for i in range(6):
            clear()
            rgb.set_pixels(i, color)
            rgb.show()
            time.sleep_ms(delay_ms)

chase((0, 255, 0), rounds=3)
clear()
```

### 4. 最終成果展現

RGB 會形成綠色跑馬燈，適合當成小車啟動或任務開始動畫。

### 5. 應用題與解答

**題目：** 讓跑馬燈從紅色開始，每跑一圈換成綠色、藍色。

**解答：**

```python
from mango import WS2812B
import time

rgb = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

for color in colors:
    for i in range(6):
        rgb.show_all((0, 0, 0))
        rgb.set_pixels(i, color)
        rgb.show()
        time.sleep_ms(120)

rgb.close()
```

## Case 5：超音波距離監測

### 1. 要做的主題

使用 `RUS04` 超音波模組讀取距離，並在 Shell 中印出公分值。

### 2. 分階段逐步教學

**階段 A：建立 RUS04 物件**

芒果車使用 `sensor_pin=15`、`rgb_pin=14`。

**階段 B：呼叫 `ping()`**

取得距離值。

**階段 C：週期性讀取**

每 0.2 秒讀一次，避免讀太快。

**階段 D：觀察穩定度**

讓學生把手靠近、遠離感測器。

### 3. 完整程式碼

```python
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)

while True:
    dist = sensor.ping()
    print("distance =", dist, "cm")
    time.sleep_ms(200)
```

### 4. 最終成果展現

Thonny Shell 會持續印出距離。物體靠近時數字變小，遠離時數字變大。

### 5. 應用題與解答

**題目：** 只在距離小於 20 cm 時印出 `Too close!`。

**解答：**

```python
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)

while True:
    dist = sensor.ping()

    if dist < 20:
        print("Too close!", dist, "cm")

    time.sleep_ms(200)
```

## Case 6：距離警示器

### 1. 要做的主題

整合超音波、RGB 與蜂鳴器：距離越近，燈色越危險，蜂鳴器提示越急促。

### 2. 分階段逐步教學

**階段 A：先分距離區間**

近距離、中距離、安全距離。

**階段 B：距離對應 RGB**

紅色危險、橘色警告、綠色安全。

**階段 C：加入蜂鳴器**

危險時短促警示，中距離低頻提醒，安全時安靜。

**階段 D：把它視為避障車前置案例**

後續只要把蜂鳴器換成馬達控制，就變成避障邏輯。

### 3. 完整程式碼

```python
from machine import Pin, PWM
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
buzzer = PWM(Pin(6, Pin.OUT))

def beep(freq=900, duration_ms=80):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

while True:
    dist = sensor.ping()
    print("distance =", dist, "cm")

    if dist < 15:
        sensor.rgb_all((255, 0, 0))
        beep(1200, 80)
        time.sleep_ms(80)
    elif dist < 35:
        sensor.rgb_all((255, 150, 0))
        beep(600, 120)
        time.sleep_ms(250)
    else:
        sensor.rgb_all((0, 255, 0))
        buzzer.duty_u16(0)
        time.sleep_ms(200)
```

## Case 7：ADC 旋鈕控制 LED 亮度

### 1. 要做的主題

使用 ADC 讀取可變電阻或旋鈕的類比電壓，並把讀到的 0-65535 數值轉成 LED 的 PWM 亮度。

### 2. 分階段逐步教學

**階段 A：理解 ADC**

ADC 會把類比電壓轉成數字。MicroPython 的 `read_u16()` 會回傳 0 到 65535，數字越大代表輸入電壓越高。

**階段 B：接上可變電阻**

可變電阻兩端接 3.3V 與 GND，中間腳接 Pico 可用的 ADC 腳位，例如 GP26。

**階段 C：把 ADC 數值送給 PWM**

LED 的 `duty_u16()` 也使用 0 到 65535，因此可以直接把 ADC 數值當亮度。

**階段 D：用序列輸出觀察數值**

在 Thonny Shell 印出原始值，讓學生看到「旋鈕位置」與「數字大小」的關係。

### 3. 完整程式碼

```python
from machine import Pin, PWM, ADC
import time

pot = ADC(Pin(26))
led = PWM(Pin(7, Pin.OUT))
led.freq(1000)

while True:
    raw = pot.read_u16()
    led.duty_u16(raw)
    print("adc =", raw, "duty =", raw)
    time.sleep_ms(100)
```

### 4. 最終成果展現

旋轉可變電阻時，LED 會平滑變亮或變暗。學生可以同時在 Shell 看到 ADC 數值同步改變。

### 5. 應用題與解答

**題目：** 改成「旋鈕越大，LED 越暗」的反向控制。

**解答：**

```python
from machine import Pin, PWM, ADC
import time

pot = ADC(Pin(26))
led = PWM(Pin(7, Pin.OUT))
led.freq(1000)

while True:
    raw = pot.read_u16()
    duty = 65535 - raw
    led.duty_u16(duty)
    print("adc =", raw, "reverse duty =", duty)
    time.sleep_ms(100)
```

## Case 8：ADC 旋鈕控制蜂鳴器音高

### 1. 要做的主題

把 ADC 讀到的旋鈕數值轉換成蜂鳴器頻率，做出可以手動調音高的小樂器。

### 2. 分階段逐步教學

**階段 A：複習 PWM 蜂鳴器**

蜂鳴器的 `freq()` 控制音高，`duty_u16()` 控制輸出強度。

**階段 B：設定頻率範圍**

為了避免太低或太尖銳，先把頻率限制在 200 Hz 到 2000 Hz。

**階段 C：撰寫比例轉換函式**

把 0-65535 轉成 200-2000，讓旋鈕位置可以對應到可聽見的音高。

**階段 D：加入短暫延遲**

每 50 ms 更新一次，聲音變化會足夠即時，也不會讓 Shell 輸出過快。

### 3. 完整程式碼

```python
from machine import Pin, PWM, ADC
import time

pot = ADC(Pin(26))
buzzer = PWM(Pin(6, Pin.OUT))

def map_range(value, in_min, in_max, out_min, out_max):
    return out_min + (value - in_min) * (out_max - out_min) // (in_max - in_min)

while True:
    raw = pot.read_u16()
    freq = map_range(raw, 0, 65535, 200, 2000)
    buzzer.freq(freq)
    buzzer.duty_u16(4000)
    print("adc =", raw, "freq =", freq)
    time.sleep_ms(50)
```

### 4. 最終成果展現

轉動旋鈕時，蜂鳴器音高會連續變化，學生能把 ADC、數值比例轉換與 PWM 頻率連成同一個控制流程。

### 5. 應用題與解答

**題目：** 加入靜音區：當 ADC 小於 5000 時，蜂鳴器不發聲。

**解答：**

```python
from machine import Pin, PWM, ADC
import time

pot = ADC(Pin(26))
buzzer = PWM(Pin(6, Pin.OUT))

def map_range(value, in_min, in_max, out_min, out_max):
    return out_min + (value - in_min) * (out_max - out_min) // (in_max - in_min)

while True:
    raw = pot.read_u16()

    if raw < 5000:
        buzzer.duty_u16(0)
        print("adc =", raw, "mute")
    else:
        freq = map_range(raw, 5000, 65535, 200, 2000)
        buzzer.freq(freq)
        buzzer.duty_u16(4000)
        print("adc =", raw, "freq =", freq)

    time.sleep_ms(50)
```

## Case 9：超音波距離 RGB 條形圖

### 1. 要做的主題

使用超音波測距，把距離轉成 RGB 燈條顯示：越接近，亮起的燈越多，並用顏色表示危險程度。

### 2. 分階段逐步教學

**階段 A：讀取距離**

使用 `RUS04.ping()` 取得目前距離。

**階段 B：決定顏色**

距離小於 15 cm 顯示紅色，15-35 cm 顯示橘色，35 cm 以上顯示綠色。

**階段 C：把距離轉成燈數**

越靠近越危險，因此距離越小，亮起的 LED 數量越多。

**階段 D：重複更新**

每 100 ms 更新一次燈條，形成即時距離儀表。

### 3. 完整程式碼

```python
from mango import RUS04, WS2812B
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
bar = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def distance_to_count(dist):
    dist = clamp(dist, 5, 60)
    return 1 + (60 - dist) * 5 // 55

def distance_to_color(dist):
    if dist < 15:
        return (255, 0, 0)
    if dist < 35:
        return (255, 120, 0)
    return (0, 255, 0)

def show_bar(count, color):
    for i in range(6):
        if i < count:
            bar.set_pixels(i, color)
        else:
            bar.set_pixels(i, (0, 0, 0))
    bar.show()

while True:
    dist = sensor.ping()
    count = distance_to_count(dist)
    color = distance_to_color(dist)
    show_bar(count, color)
    print("distance =", dist, "leds =", count)
    time.sleep_ms(100)
```

### 4. 最終成果展現

學生把手靠近超音波感測器時，RGB 燈條會亮更多顆，並從綠色逐步變成橘色、紅色，像一個倒車雷達儀表。

### 5. 應用題與解答

**題目：** 改成「距離越遠，亮起的燈越多」的展示模式。

**解答：**

```python
from mango import RUS04, WS2812B
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
bar = WS2812B(pin=2, leds=6, sm_id=4, brightness=0.2)

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def distance_to_count(dist):
    dist = clamp(dist, 5, 60)
    return 1 + (dist - 5) * 5 // 55

def show_bar(count):
    for i in range(6):
        if i < count:
            bar.set_pixels(i, (0, 80, 255))
        else:
            bar.set_pixels(i, (0, 0, 0))
    bar.show()

while True:
    dist = sensor.ping()
    count = distance_to_count(dist)
    show_bar(count)
    print("distance =", dist, "leds =", count)
    time.sleep_ms(100)
```

## Case 10：距離移動平均濾波警示器

### 1. 要做的主題

使用移動平均降低超音波測距跳動，讓 RGB 與蜂鳴器警示更穩定。

### 2. 分階段逐步教學

**階段 A：觀察原始距離跳動**

超音波遇到斜面、邊角或太近的物體時，數值可能忽大忽小。

**階段 B：保留最近幾筆資料**

用 list 保存最近 5 次距離讀值。

**階段 C：計算平均距離**

用平均值判斷危險程度，避免單次異常讀值造成誤報。

**階段 D：比較原始值與平均值**

同時印出 raw 與 avg，讓學生看到濾波前後的差別。

### 3. 完整程式碼

```python
from machine import Pin, PWM
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
buzzer = PWM(Pin(6, Pin.OUT))
samples = []

def add_sample(value):
    samples.append(value)
    if len(samples) > 5:
        samples.pop(0)
    return sum(samples) / len(samples)

def beep(freq, duration_ms):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

while True:
    raw = sensor.ping()
    avg = add_sample(raw)
    print("raw =", raw, "avg =", avg)

    if avg < 15:
        sensor.rgb_all((255, 0, 0))
        beep(1400, 60)
        time.sleep_ms(80)
    elif avg < 35:
        sensor.rgb_all((255, 120, 0))
        beep(700, 80)
        time.sleep_ms(220)
    else:
        sensor.rgb_all((0, 255, 0))
        buzzer.duty_u16(0)
        time.sleep_ms(120)
```

### 4. 最終成果展現

距離警示不再因為單次讀值跳動而忽然變色或亂叫。學生能理解「感測器資料需要整理後再拿來決策」。

### 5. 應用題與解答

**題目：** 忽略不合理讀值：距離等於 0 或大於 300 cm 時，不加入平均。

**解答：**

```python
from machine import Pin, PWM
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
buzzer = PWM(Pin(6, Pin.OUT))
samples = []

def add_sample(value):
    if value == 0 or value > 300:
        return None
    samples.append(value)
    if len(samples) > 5:
        samples.pop(0)
    return sum(samples) / len(samples)

def beep(freq, duration_ms):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

while True:
    raw = sensor.ping()
    avg = add_sample(raw)

    if avg is None:
        print("ignore raw =", raw)
        time.sleep_ms(100)
        continue

    print("raw =", raw, "avg =", avg)

    if avg < 15:
        sensor.rgb_all((255, 0, 0))
        beep(1400, 60)
        time.sleep_ms(80)
    elif avg < 35:
        sensor.rgb_all((255, 120, 0))
        beep(700, 80)
        time.sleep_ms(220)
    else:
        sensor.rgb_all((0, 255, 0))
        buzzer.duty_u16(0)
        time.sleep_ms(120)
```

### 4. 最終成果展現

距離安全時亮綠燈；接近物體時亮橘燈並發出慢速提示；非常接近時亮紅燈並快速警示。

### 5. 應用題與解答

**題目：** 加入「超近距離停止警報」：距離小於 8 cm 時，紅燈長亮並連續嗶 3 次。

**解答：**

```python
from machine import Pin, PWM
from mango import RUS04
import time

sensor = RUS04(sensor_pin=15, rgb_pin=14)
buzzer = PWM(Pin(6, Pin.OUT))

def beep(freq=1300, duration_ms=80):
    buzzer.freq(freq)
    buzzer.duty_u16(5000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)
    time.sleep_ms(80)

while True:
    dist = sensor.ping()
    print("distance =", dist, "cm")

    if dist < 8:
        sensor.rgb_all((255, 0, 0))
        for i in range(3):
            beep()
        time.sleep_ms(300)
    elif dist < 15:
        sensor.rgb_all((255, 0, 0))
        beep(1200, 80)
    elif dist < 35:
        sensor.rgb_all((255, 150, 0))
        beep(600, 120)
        time.sleep_ms(250)
    else:
        sensor.rgb_all((0, 255, 0))
        buzzer.duty_u16(0)
        time.sleep_ms(200)
```
