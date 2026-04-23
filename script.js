document.documentElement.classList.add("js");

const revealNodes = document.querySelectorAll(".reveal");

if (revealNodes.length) {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  revealNodes.forEach(node => observer.observe(node));
}

const activeNavLink = document.querySelector(".site-nav a[aria-current='page']");

if (activeNavLink) {
  requestAnimationFrame(() => {
    activeNavLink.scrollIntoView({
      behavior: "auto",
      block: "nearest",
      inline: "center"
    });
  });
}

const codePages = {
  "keyboard-car-control": {
    path: "downloads/keyboard-car-control.py",
    title: "BootCamp 鍵盤控制主程式",
    summary: "這份程式是 BootCamp 的唯一主程式。學生把它貼到 Thonny 後，就可以用 W / A / S / D / X 控制小車。",
    stage: "BootCamp",
    backHref: "bootcamp.html",
    steps: [
      "在 Thonny 建立新的 .py 檔案。",
      "把這份程式完整複製並貼進去。",
      "存成 keyboard_car.py，按下 Run。",
      "到 Shell 輸入 w / a / s / d / x，再按 Enter。"
    ],
    highlights: [
      {
        title: "腳位設定",
        summary: "一開始先準備四個馬達腳位與板上的 LED。",
        range: "第 1-15 行",
        lines: [1, 15],
        tone: "teacher"
      },
      {
        title: "馬達方向函式",
        summary: "_set_motor() 會決定馬達現在要前進、後退還是停止。",
        range: "第 18-27 行",
        lines: [18, 27],
        tone: "student"
      },
      {
        title: "五個基本動作",
        summary: "前進、後退、左轉、右轉、停止都是由前面的函式組合而成。",
        range: "第 30-52 行",
        lines: [30, 52],
        tone: "teacher"
      },
      {
        title: "讀取指令",
        summary: "主程式會一直等待輸入，再決定小車要做哪個動作。",
        range: "第 55-82 行",
        lines: [55, 82],
        tone: "student"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Raspberry Pi Pico 小車 1 hr Boot Camp
# 在 Thonny Shell 輸入 w / a / s / d / x 後按 Enter

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)
LED = Pin(25, Pin.OUT)

# If the car moves backward during the forward command, change one sign to -1.
RIGHT_SIGN = 1
LEFT_SIGN = 1


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


def forward():
    drive(1, 1)


def backward():
    drive(-1, -1)


def turn_left():
    drive(-1, 1)


def turn_right():
    drive(1, -1)


print("Raspberry Pi Pico 小車 Boot Camp")
print("請在 Thonny Shell 輸入 w / a / s / d / x 後按 Enter")
print("w=前進 s=後退 a=左轉 d=右轉 x=停止")

stop()
LED.off()

while True:
    command = input("Command (w/a/s/d/x): ").strip().lower()

    if command == "w":
        print("前進")
        forward()
    elif command == "s":
        print("後退")
        backward()
    elif command == "a":
        print("左轉")
        turn_left()
    elif command == "d":
        print("右轉")
        turn_right()
    else:
        print("停止")
        stop()

    LED.toggle()
    time.sleep(0.05)
`
  },
  "basic-motor-functions": {
    path: "downloads/basic-motor-functions.py",
    title: "基本動作函式",
    summary: "這份程式把小車的五個基本動作拆成獨立函式，適合在 BootCamp 後補充閱讀。",
    stage: "BootCamp 補充",
    backHref: "bootcamp.html",
    steps: [
      "先看腳位設定。",
      "再看 _set_motor() 如何控制方向。",
      "最後看 forward()、backward()、turn_left()、turn_right()、stop()。"
    ],
    highlights: [
      {
        title: "腳位設定",
        summary: "先定義左右馬達的四個輸出腳位。",
        range: "第 1-11 行",
        lines: [1, 11],
        tone: "teacher"
      },
      {
        title: "共用控制函式",
        summary: "_set_motor() 負責決定一個馬達的方向。",
        range: "第 14-23 行",
        lines: [14, 23],
        tone: "student"
      },
      {
        title: "五個動作函式",
        summary: "後面的函式就是 BootCamp 五個基本動作的來源。",
        range: "第 26-48 行",
        lines: [26, 48],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin

# Raspberry Pi Pico 小車基本動作函式

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

RIGHT_SIGN = 1
LEFT_SIGN = 1


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


def forward():
    drive(1, 1)


def backward():
    drive(-1, -1)


def turn_left():
    drive(-1, 1)


def turn_right():
    drive(1, -1)


stop()
`
  },
  "mango-import-test": {
    path: "downloads/mango-import-test.py",
    title: "mango 函式庫 import 測試",
    summary: "這份程式用來確認 Pico 上已經成功上傳 mango 函式庫。看到 mango import OK 後，再進入需要 mango 的主題。",
    stage: "開始前設定",
    backHref: "setup.html",
    steps: [
      "先下載 mango-library.zip 並解壓縮。",
      "把整個 mango 資料夾上傳到 Pico 根目錄。",
      "執行這份測試程式。",
      "看到 mango import OK 後再進入 02-05。"
    ],
    highlights: [
      {
        title: "載入常用類別",
        summary: "Motor、RUS04、WS2812B 是後續小車主題最常用的 mango 類別。",
        range: "第 1 行",
        lines: [1, 1],
        tone: "teacher"
      },
      {
        title: "成功訊息",
        summary: "如果 Shell 印出 OK，就代表函式庫路徑正確。",
        range: "第 3-4 行",
        lines: [3, 4],
        tone: "student"
      }
    ],
    fallbackText: `from mango import Motor, RUS04, WS2812B

print("mango import OK")
print("Motor, RUS04, and WS2812B are ready.")
`
  },
  "motor-calibration": {
    path: "downloads/motor-calibration.py",
    title: "馬達方向校正程式",
    summary: "這份程式會依序測右輪、左輪、前進、後退與左右轉。若方向相反，先修改 RIGHT_SIGN 或 LEFT_SIGN。",
    stage: "開始前設定",
    backHref: "setup.html",
    steps: [
      "把小車放在平坦桌面或地面。",
      "貼上或打開這份程式，按 Run。",
      "觀察每個中文/英文提示對應的輪子方向。",
      "如果方向相反，停止程式後修改 RIGHT_SIGN 或 LEFT_SIGN。"
    ],
    highlights: [
      {
        title: "統一腳位",
        summary: "右馬達使用 GP12/GP13，左馬達使用 GP11/GP10。",
        range: "第 1-12 行",
        lines: [1, 12],
        tone: "teacher"
      },
      {
        title: "方向校正",
        summary: "RIGHT_SIGN 與 LEFT_SIGN 是修正馬達方向最重要的地方。",
        range: "第 14-16 行",
        lines: [14, 16],
        tone: "student"
      },
      {
        title: "測試動作表",
        summary: "程式會依序測每個輪子與整台車的方向。",
        range: "第 39-46 行",
        lines: [39, 46],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Raspberry Pi Pico microcar motor calibration
# Course pin map:
#   right motor M1 = GP12 / GP13
#   left motor M2  = GP11 / GP10

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

# If one side moves backward during the forward test, change 1 to -1.
RIGHT_SIGN = 1
LEFT_SIGN = 1


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


tests = [
    ("right wheel forward", 0, 1),
    ("left wheel forward", 1, 0),
    ("car forward", 1, 1),
    ("car backward", -1, -1),
    ("turn left in place", -1, 1),
    ("turn right in place", 1, -1),
]

print("Motor calibration start")
print("If a direction is wrong, press Ctrl+C and edit RIGHT_SIGN or LEFT_SIGN.")

for label, left, right in tests:
    print(label)
    drive(left, right)
    time.sleep(1.2)
    stop()
    time.sleep(0.8)

print("Motor calibration done")
stop()
`
  },
  "sensor-rgb-warmup": {
    path: "downloads/sensor-rgb-warmup.py",
    title: "感測器主題暖身程式",
    summary: "這份暖身程式先讓學生看見 RGB LED 的變化，再進入距離感測與條件判斷。",
    stage: "主題 2：感測器操控暖身",
    backHref: "topic-02-sensor-output.html",
    steps: [
      "先在 Thonny 開新檔。",
      "把程式貼上後按 Run。",
      "觀察 RGB LED 是否依序切換三種顏色。"
    ],
    highlights: [
      {
        title: "建立感測器物件",
        summary: "先建立 RUS04 物件，包含感測器腳位與 RGB LED 腳位。",
        range: "第 1-6 行",
        lines: [1, 6],
        tone: "teacher"
      },
      {
        title: "顏色切換",
        summary: "這一段會依序切換紅、綠、藍三種顏色。",
        range: "第 8-15 行",
        lines: [8, 15],
        tone: "student"
      },
      {
        title: "關閉 RGB",
        summary: "程式最後會把 RGB LED 關掉，避免顏色一直亮著。",
        range: "第 17-18 行",
        lines: [17, 18],
        tone: "teacher"
      }
    ],
    fallbackText: `import time
from mango import RUS04

# 主題 2：感測器操控暖身程式

sensor = RUS04(sensor_pin=15, rgb_pin=14)

sensor.rgb_all((255, 0, 0))
time.sleep(1)

sensor.rgb_all((0, 255, 0))
time.sleep(1)

sensor.rgb_all((0, 0, 255))
time.sleep(1)

sensor.rgb_close()
`
  },
  "distance-sensor-rgb": {
    path: "downloads/distance-sensor-rgb.py",
    title: "距離感測主程式",
    summary: "這份主程式會讀取距離數值，並透過 if / elif / else 切換 RGB LED 顏色。",
    stage: "主題 2：感測器操控",
    backHref: "topic-02-sensor-output.html",
    steps: [
      "先看如何建立感測器物件。",
      "再看 sensor.ping() 如何讀取距離。",
      "最後看 if / elif / else 如何切換顏色。"
    ],
    highlights: [
      {
        title: "建立感測器",
        summary: "一開始先建立 RUS04 感測器與 RGB LED 物件。",
        range: "第 1-6 行",
        lines: [1, 6],
        tone: "teacher"
      },
      {
        title: "讀取距離",
        summary: "在迴圈中持續用 sensor.ping() 讀取目前距離。",
        range: "第 9-11 行",
        lines: [9, 11],
        tone: "student"
      },
      {
        title: "條件判斷",
        summary: "依據近、中、遠三種距離範圍，切換不同 RGB LED 顏色。",
        range: "第 13-20 行",
        lines: [13, 20],
        tone: "teacher"
      }
    ],
    fallbackText: `import time
from mango import RUS04
from mango import utils

# 主題 2：距離感測主程式
sensor = RUS04(sensor_pin=15, rgb_pin=14)
sensor.rgb_all((255, 0, 0))

for _ in range(500):
    dist = sensor.ping()
    print(f"distance = {dist} cm")

    if dist < 10:
        sensor.rgb_all(utils.COLOR_RED)
    elif 10 <= dist < 20:
        sensor.rgb_all(utils.COLOR_BLUE)
    else:
        sensor.rgb_all(utils.COLOR_GREEN)

    time.sleep(0.1)

sensor.rgb_close()
`
  },
  "line-sensor-read": {
    path: "downloads/line-sensor-read.py",
    title: "循跡感測器讀值程式",
    summary: "這份暖身程式先把左右循跡感測器的值印到 Shell，幫助學生看懂黑線與白底的差異。",
    stage: "主題 4：無人車循跡暖身",
    backHref: "topic-04-autonomous-car.html",
    steps: [
      "先在 Thonny 開新檔。",
      "把程式貼上後按 Run。",
      "把感測器移到黑線和白底上，觀察左右兩邊輸出的 0 / 1。"
    ],
    highlights: [
      {
        title: "設定左右感測器",
        summary: "先建立左、右兩個循跡感測器輸入腳位。",
        range: "第 1-10 行",
        lines: [1, 10],
        tone: "teacher"
      },
      {
        title: "持續讀值",
        summary: "在迴圈裡反覆讀取左右感測值，並印到 Shell。",
        range: "第 12-18 行",
        lines: [12, 18],
        tone: "student"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Topic 3 warm-up: read two line sensor values
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

print("Line sensor warm-up")
print("black = 1, white = 0")

while True:
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    print("left =", left_value, "right =", right_value)
    time.sleep(0.1)
`
  },
  "line-following-intro": {
    path: "downloads/line-following-intro.py",
    title: "無人車循跡基礎程式",
    summary: "這份主程式把左右循跡感測值直接轉成基本轉向規則，是進入進階循跡前的入門版本。",
    stage: "主題 4：無人車",
    backHref: "topic-04-autonomous-car.html",
    steps: [
      "先讀取左右循跡感測器的值。",
      "再用四種規則決定前進、左修正、右修正或停止。",
      "先完成基本循跡，之後再往進階控制延伸。"
    ],
    highlights: [
      {
        title: "馬達與感測器設定",
        summary: "先準備兩側馬達腳位，再定義左右循跡感測器腳位。",
        range: "第 1-19 行",
        lines: [1, 19],
        tone: "teacher"
      },
      {
        title: "基本動作函式",
        summary: "這裡保留前進、左轉、右轉、停止四種最基本動作。",
        range: "第 22-52 行",
        lines: [22, 52],
        tone: "student"
      },
      {
        title: "四種循跡規則",
        summary: "左右感測值不同時，小車就依照規則做修正。",
        range: "第 61-78 行",
        lines: [61, 78],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Topic 3: line following intro
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

RIGHT_SIGN = 1
LEFT_SIGN = 1

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


def forward():
    drive(1, 1)


def turn_left():
    drive(-1, 1)


def turn_right():
    drive(1, -1)


print("Line following intro")
print("left black + right black  -> forward")
print("left black + right white  -> turn left")
print("left white + right black  -> turn right")
print("left white + right white  -> stop")

while True:
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        forward()
        print("forward", left_value, right_value)
    elif left_value == 1 and right_value == 0:
        turn_left()
        print("left", left_value, right_value)
    elif left_value == 0 and right_value == 1:
        turn_right()
        print("right", left_value, right_value)
    else:
        stop()
        print("stop", left_value, right_value)

    time.sleep(0.05)
`
  },
  "line-error-to-speed": {
    path: "downloads/line-error-to-speed.py",
    title: "速度差暖身程式",
    summary: "這份暖身程式先把左右循跡感測值轉成 error、correction 與左右速度，幫助學生建立速度差控制的直覺。",
    stage: "主題 5：專題化循跡調參",
    backHref: "topic-05-project-cases.html",
    steps: [
      "先讀取左右循跡感測值。",
      "再把感測值轉成 error。",
      "觀察 correction 對左右速度的影響。"
    ],
    highlights: [
      {
        title: "感測器與參數",
        summary: "先設定左右感測器、基礎速度、最大速度與比例增益 KP。",
        range: "第 1-15 行",
        lines: [1, 15],
        tone: "teacher"
      },
      {
        title: "把感測值轉成 error",
        summary: "左右黑線位置不同時，就用不同 error 表示偏左或偏右。",
        range: "第 22-36 行",
        lines: [22, 36],
        tone: "student"
      },
      {
        title: "速度差計算",
        summary: "用 correction 讓左右輪速度出現差距，為真正的循跡控制做準備。",
        range: "第 42-55 行",
        lines: [42, 55],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Topic 4 bridge: turn line sensor values into speed difference
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 10000

last_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        error = previous_error

    return left_value, right_value, error


print("Topic 4 bridge")
print("Observe sensor values, error, and left/right speed")

while True:
    left_value, right_value, error = read_error(last_error)
    correction = KP * error
    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    print(
        "left =", left_value,
        "right =", right_value,
        "error =", error,
        "left_speed =", left_speed,
        "right_speed =", right_speed,
    )

    last_error = error
    time.sleep(0.1)
`
  },
  "line-following-advanced": {
    path: "downloads/line-following-advanced.py",
    title: "專題化 PD 循跡程式",
    summary: "這份主程式把固定規則升級成速度差控制，並引入 last_error 與 derivative，讓循跡反應更平滑。",
    stage: "主題 5：專題化",
    backHref: "topic-05-project-cases.html",
    steps: [
      "先確認左右感測器的黑白讀值。",
      "把感測值轉成 error 與 derivative。",
      "再用 correction 調整左右輪速度差。"
    ],
    highlights: [
      {
        title: "PWM 馬達與控制參數",
        summary: "先準備四個 PWM 馬達腳位，再設定 BASE_SPEED、KP、KD 等參數。",
        range: "第 1-19 行",
        lines: [1, 19],
        tone: "teacher"
      },
      {
        title: "error 與 last_error",
        summary: "用 read_error() 把感測器狀態轉成控制所需的 error。",
        range: "第 46-64 行",
        lines: [46, 64],
        tone: "student"
      },
      {
        title: "PD 速度差控制",
        summary: "用 correction 同步調整左右速度，讓小車不只是轉彎，而是更平滑地修正方向。",
        range: "第 70-89 行",
        lines: [70, 89],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin, PWM
import time

# Topic 4: line following advanced
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0
# Motor PWM pins follow the Pico car course materials

FREQUENCY = 1000
BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 11000
KD = 5000

RIGHT_FORWARD = PWM(Pin(13))
RIGHT_BACKWARD = PWM(Pin(12))
LEFT_FORWARD = PWM(Pin(10))
LEFT_BACKWARD = PWM(Pin(11))

for motor in (RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD):
    motor.freq(FREQUENCY)

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

last_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def stop():
    RIGHT_FORWARD.duty_u16(0)
    RIGHT_BACKWARD.duty_u16(0)
    LEFT_FORWARD.duty_u16(0)
    LEFT_BACKWARD.duty_u16(0)


def drive_forward(left_speed, right_speed):
    LEFT_FORWARD.duty_u16(left_speed)
    LEFT_BACKWARD.duty_u16(0)
    RIGHT_FORWARD.duty_u16(right_speed)
    RIGHT_BACKWARD.duty_u16(0)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        if previous_error > 0:
            error = 1.5
        elif previous_error < 0:
            error = -1.5
        else:
            error = 0.0

    return left_value, right_value, error


print("Topic 4: line following advanced")
print("This version uses speed difference instead of fixed turns")

while True:
    left_value, right_value, error = read_error(last_error)
    derivative = error - last_error
    correction = KP * error + KD * derivative

    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    if left_value == 0 and right_value == 0 and last_error == 0:
        stop()
        print("stop", left_value, right_value, "error =", error)
    else:
        drive_forward(left_speed, right_speed)
        print(
            "left =", left_value,
            "right =", right_value,
            "error =", error,
            "left_speed =", left_speed,
            "right_speed =", right_speed,
        )

    last_error = error
    time.sleep(0.03)
`
  }
};

codePages["line-algorithm-rule"] = {
  ...codePages["line-following-intro"],
  title: "規則式循跡演算法",
  summary: "這是最直觀的循跡寫法。看到黑線就照固定規則前進、左修正、右修正或停止。",
  stage: "主題 5：專題化",
  backHref: "topic-05-project-cases.html",
  steps: [
    "先看左右循跡感測值。",
    "再用固定規則決定車子現在該做什麼。",
    "這個版本最好懂，也最適合拿來當第一個比較基準。"
  ]
};

codePages["line-algorithm-p"] = {
  path: "downloads/line-following-p.py",
  title: "P 循跡演算法",
  summary: "這份程式把 error 直接轉成 correction，讓左右輪用速度差修正方向。",
  stage: "主題 5：專題化",
  backHref: "topic-05-project-cases.html",
  steps: [
    "先把左右感測值換成 error。",
    "再用 correction = KP * error 算出修正量。",
    "觀察比例控制如何讓小車比規則式更平順。"
  ],
  highlights: [
    {
      title: "PWM 與比例參數",
      summary: "先準備 PWM 馬達腳位，再設定 BASE_SPEED 與 KP。",
      range: "第 1-19 行",
      lines: [1, 19],
      tone: "teacher"
    },
    {
      title: "error 轉換",
      summary: "把左右感測器的黑白狀態轉成偏左、偏右或置中的 error。",
      range: "第 46-64 行",
      lines: [46, 64],
      tone: "student"
    },
    {
      title: "P 控制主迴圈",
      summary: "每次都用 KP * error 更新左右速度差，這就是最基礎的比例控制。",
      range: "第 70-88 行",
      lines: [70, 88],
      tone: "teacher"
    }
  ],
  fallbackText: `from machine import Pin, PWM
import time

# Topic 5: proportional line following
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0

FREQUENCY = 1000
BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 10000

RIGHT_FORWARD = PWM(Pin(13))
RIGHT_BACKWARD = PWM(Pin(12))
LEFT_FORWARD = PWM(Pin(10))
LEFT_BACKWARD = PWM(Pin(11))

for motor in (RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD):
    motor.freq(FREQUENCY)

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

last_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def stop():
    RIGHT_FORWARD.duty_u16(0)
    RIGHT_BACKWARD.duty_u16(0)
    LEFT_FORWARD.duty_u16(0)
    LEFT_BACKWARD.duty_u16(0)


def drive_forward(left_speed, right_speed):
    LEFT_FORWARD.duty_u16(left_speed)
    LEFT_BACKWARD.duty_u16(0)
    RIGHT_FORWARD.duty_u16(right_speed)
    RIGHT_BACKWARD.duty_u16(0)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        if previous_error > 0:
            error = 1.5
        elif previous_error < 0:
            error = -1.5
        else:
            error = 0.0

    return left_value, right_value, error


print("P line following")
print("correction = KP * error")

while True:
    left_value, right_value, error = read_error(last_error)
    correction = KP * error

    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    if left_value == 0 and right_value == 0 and last_error == 0:
        stop()
        print("stop", left_value, right_value, "error =", error)
    else:
        drive_forward(left_speed, right_speed)
        print(
            "left =", left_value,
            "right =", right_value,
            "error =", error,
            "left_speed =", left_speed,
            "right_speed =", right_speed,
        )

    last_error = error
    time.sleep(0.03)
`
};

codePages["line-algorithm-pd"] = {
  ...codePages["line-following-advanced"],
  title: "PD 循跡演算法",
  summary: "這份版本在比例控制之外再加入微分項，讓循跡反應更平順、也更不容易左右擺動。",
  stage: "主題 5：專題化",
  backHref: "topic-05-project-cases.html",
  steps: [
    "先把感測值轉成 error。",
    "再算出 derivative，看誤差現在變化得多快。",
    "最後用 PD 控制一起調整左右輪速度差。"
  ]
};

codePages["line-algorithm-pid"] = {
  path: "downloads/line-following-pid.py",
  title: "PID 循跡演算法",
  summary: "這份版本加入積分項與微分項，是目前網站裡最完整的循跡控制教學程式。",
  stage: "主題 5：專題化",
  backHref: "topic-05-project-cases.html",
  steps: [
    "先看 error 與 derivative。",
    "再把過去偏差累積成 sum_error。",
    "最後用 PID 同步決定修正量與左右輪速度差。"
  ],
  highlights: [
    {
      title: "PID 參數與積分上限",
      summary: "先準備 KP、KI、KD，並用 INTEGRAL_LIMIT 避免積分項無限制累積。",
      range: "第 1-23 行",
      lines: [1, 23],
      tone: "teacher"
    },
    {
      title: "誤差與積分",
      summary: "每次都更新 error、derivative 與 sum_error，這是 PID 的核心狀態。",
      range: "第 58-87 行",
      lines: [58, 87],
      tone: "student"
    },
    {
      title: "PID 修正量",
      summary: "用 KP、KI、KD 三個項目一起決定 correction，讓小車依照誤差狀態持續修正。",
      range: "第 89-109 行",
      lines: [89, 109],
      tone: "teacher"
    }
  ],
  fallbackText: `from machine import Pin, PWM
import time

# Topic 5: simplified PID line following
# Assumption:
#   left sensor  -> GP15
#   right sensor -> GP14
# Black line = 1, white floor = 0
# This is a teaching version for two digital sensors.

FREQUENCY = 1000
BASE_SPEED = 24000
MAX_SPEED = 42000
KP = 9500
KI = 900
KD = 4200
INTEGRAL_LIMIT = 4.0

RIGHT_FORWARD = PWM(Pin(13))
RIGHT_BACKWARD = PWM(Pin(12))
LEFT_FORWARD = PWM(Pin(10))
LEFT_BACKWARD = PWM(Pin(11))

for motor in (RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD):
    motor.freq(FREQUENCY)

LEFT_SENSOR = Pin(15, Pin.IN)
RIGHT_SENSOR = Pin(14, Pin.IN)

last_error = 0.0
sum_error = 0.0


def clamp_speed(value):
    if value < 0:
        return 0
    if value > MAX_SPEED:
        return MAX_SPEED
    return int(value)


def clamp_integral(value):
    if value > INTEGRAL_LIMIT:
        return INTEGRAL_LIMIT
    if value < -INTEGRAL_LIMIT:
        return -INTEGRAL_LIMIT
    return value


def stop():
    RIGHT_FORWARD.duty_u16(0)
    RIGHT_BACKWARD.duty_u16(0)
    LEFT_FORWARD.duty_u16(0)
    LEFT_BACKWARD.duty_u16(0)


def drive_forward(left_speed, right_speed):
    LEFT_FORWARD.duty_u16(left_speed)
    LEFT_BACKWARD.duty_u16(0)
    RIGHT_FORWARD.duty_u16(right_speed)
    RIGHT_BACKWARD.duty_u16(0)


def read_error(previous_error):
    left_value = LEFT_SENSOR.value()
    right_value = RIGHT_SENSOR.value()

    if left_value == 1 and right_value == 1:
        error = 0.0
    elif left_value == 1 and right_value == 0:
        error = 1.0
    elif left_value == 0 and right_value == 1:
        error = -1.0
    else:
        if previous_error > 0:
            error = 1.5
        elif previous_error < 0:
            error = -1.5
        else:
            error = 0.0

    return left_value, right_value, error


print("PID line following")
print("correction = KP * error + KI * sum_error + KD * derivative")

while True:
    left_value, right_value, error = read_error(last_error)
    derivative = error - last_error
    sum_error = clamp_integral(sum_error + error)

    correction = KP * error + KI * sum_error + KD * derivative

    left_speed = clamp_speed(BASE_SPEED - correction)
    right_speed = clamp_speed(BASE_SPEED + correction)

    if left_value == 0 and right_value == 0 and last_error == 0:
        stop()
        print("stop", left_value, right_value, "error =", error)
    else:
        drive_forward(left_speed, right_speed)
        print(
            "left =", left_value,
            "right =", right_value,
            "error =", error,
            "sum_error =", round(sum_error, 2),
            "left_speed =", left_speed,
            "right_speed =", right_speed,
        )

    last_error = error
    time.sleep(0.03)
`
};

const escapeHtml = value =>
  value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");

const renderCode = (node, text, highlights = []) => {
  if (!node) {
    return;
  }

  const ranges = highlights.map(item => ({
    start: item.lines[0],
    end: item.lines[1],
    tone: item.tone
  }));
  const lines = text.split("\n");

  node.innerHTML = lines
    .map((line, index) => {
      const lineNo = index + 1;
      const activeRange = ranges.find(range => lineNo >= range.start && lineNo <= range.end);
      const toneClass = activeRange ? ` highlight-${activeRange.tone}` : "";
      const highlightClass = activeRange ? " is-highlight" : "";
      return `<span class="code-line${highlightClass}${toneClass}"><span class="code-line-no">${lineNo}</span><span class="code-line-text">${escapeHtml(line) || "&nbsp;"}</span></span>`;
    })
    .join("");
};

const renderHighlights = (node, highlights) => {
  if (!node || !highlights?.length) {
    return;
  }

  node.innerHTML = highlights
    .map(
      item => `
        <article class="code-highlight-card ${item.tone === "student" ? "student-card" : "teacher-card"}">
          <span class="download-type">${item.range}</span>
          <h3>${item.title}</h3>
          <p>${item.summary}</p>
        </article>
      `
    )
    .join("");
};

const setCopyButtonState = (button, label) => {
  button.textContent = label;
  window.setTimeout(() => {
    button.textContent = button.dataset.defaultLabel;
  }, 1500);
};

const attachCopyHandler = (button, getText) => {
  if (!button) {
    return;
  }

  button.dataset.defaultLabel = button.textContent;
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(getText());
      setCopyButtonState(button, "已複製");
    } catch (error) {
      setCopyButtonState(button, "複製失敗");
    }
  });
};

const loadCodeText = async meta => {
  try {
    const response = await fetch(meta.path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.text();
  } catch (error) {
    if (meta.fallbackText) {
      return meta.fallbackText;
    }
    throw error;
  }
};

const codeContent = document.getElementById("code-content");

if (codeContent) {
  const params = new URLSearchParams(window.location.search);
  const fileKey = params.get("file");
  const meta = codePages[fileKey];
  const titleNode = document.getElementById("code-title");
  const summaryNode = document.getElementById("code-summary");
  const fileLabelNode = document.getElementById("code-file-label");
  const stageNode = document.getElementById("code-stage");
  const downloadNode = document.getElementById("code-download");
  const backNode = document.getElementById("code-back");
  const stepsNode = document.getElementById("code-steps");
  const copyNode = document.getElementById("copy-code");
  const highlightGrid = document.getElementById("code-highlight-grid");

  if (!meta) {
    titleNode.textContent = "找不到對應的程式";
    summaryNode.textContent = "請從 BootCamp、感測器主題或下載區重新打開程式頁。";
    codeContent.textContent = "Unknown file key.";
    fileLabelNode.textContent = "UNKNOWN";
    stageNode.textContent = "未指定主題";
    downloadNode.href = "downloads.html";
    backNode.href = "downloads.html";
  } else {
    document.title = `${meta.title} | Raspberry Pi Pico 小車主題教材`;
    titleNode.textContent = meta.title;
    summaryNode.textContent = meta.summary;
    fileLabelNode.textContent = meta.path;
    stageNode.textContent = meta.stage;
    downloadNode.href = meta.path;
    downloadNode.textContent = "下載原始檔";
    backNode.href = meta.backHref;
    stepsNode.innerHTML = meta.steps.map(step => `<li>${step}</li>`).join("");
    renderHighlights(highlightGrid, meta.highlights);

    loadCodeText(meta)
      .then(text => {
        renderCode(codeContent, text, meta.highlights);
        attachCopyHandler(copyNode, () => text);
      })
      .catch(error => {
        codeContent.textContent = `程式載入失敗：${error.message}`;
      });
  }
}

const attachInlineCodeBlock = (nodeId, buttonId, pageKey, useHighlights = false) => {
  const codeNode = document.getElementById(nodeId);
  const copyButton = document.getElementById(buttonId);

  if (!codeNode) {
    return;
  }

  const meta = codePages[pageKey];
  if (!meta) {
    codeNode.textContent = "找不到對應程式。";
    return;
  }

  loadCodeText(meta)
    .then(text => {
      renderCode(codeNode, text, useHighlights ? meta.highlights : []);
      attachCopyHandler(copyButton, () => text);
    })
    .catch(error => {
      codeNode.textContent = `程式載入失敗：${error.message}`;
    });
};

attachInlineCodeBlock("bootcamp-full-code", "bootcamp-copy-code", "keyboard-car-control", false);
attachInlineCodeBlock("sensor-full-code", "sensor-copy-code", "distance-sensor-rgb", true);
attachInlineCodeBlock("line-following-full-code", "line-following-copy-code", "line-following-intro", true);
attachInlineCodeBlock("line-advanced-full-code", "line-advanced-copy-code", "line-following-advanced", true);

document.querySelectorAll(".case-code-card").forEach(card => {
  const button = card.querySelector(".copy-md-code");
  const code = card.querySelector("code");
  attachCopyHandler(button, () => code?.textContent ?? "");
});

