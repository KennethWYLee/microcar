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

const codePages = {
  "keyboard-car-control": {
    path: "downloads/keyboard-car-control.py",
    title: "Boot Camp 鍵盤控制主程式",
    summary: "這份程式是主題 1 的唯一主程式。學生把它貼到 Thonny 後，就可以用 W / A / S / D / X 控制小車。",
    stage: "主題 1：1 hr Boot Camp",
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
        range: "第 1-9 行",
        lines: [1, 9],
        tone: "teacher"
      },
      {
        title: "馬達方向函式",
        summary: "_set_motor() 會決定馬達現在要前進、後退還是停止。",
        range: "第 12-20 行",
        lines: [12, 20],
        tone: "student"
      },
      {
        title: "五個基本動作",
        summary: "前進、後退、左轉、右轉、停止都是由前面的函式組合而成。",
        range: "第 23-42 行",
        lines: [23, 42],
        tone: "teacher"
      },
      {
        title: "讀取指令",
        summary: "主程式會一直等待輸入，再決定小車要做哪個動作。",
        range: "第 45-64 行",
        lines: [45, 64],
        tone: "student"
      }
    ],
    fallbackText: `from machine import Pin
import time

# Raspberry Pi Pico 小車 1 hr Boot Camp
# 在 Thonny Shell 輸入 w / a / s / d / x 後按 Enter

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)
LED = Pin(25, Pin.OUT)


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


def stop():
    _set_motor(M1_A, M1_B, 0)
    _set_motor(M2_A, M2_B, 0)


def forward():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, 1)


def backward():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, -1)


def turn_left():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, 1)


def turn_right():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, -1)


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
    summary: "這份程式把小車的五個基本動作拆成獨立函式，適合在 Boot Camp 後補充閱讀。",
    stage: "主題 1：Boot Camp 補充",
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
        range: "第 1-7 行",
        lines: [1, 7],
        tone: "teacher"
      },
      {
        title: "共用控制函式",
        summary: "_set_motor() 負責決定一個馬達的方向。",
        range: "第 10-18 行",
        lines: [10, 18],
        tone: "student"
      },
      {
        title: "五個動作函式",
        summary: "後面的函式就是 Boot Camp 五個基本動作的來源。",
        range: "第 21-41 行",
        lines: [21, 41],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin

# Raspberry Pi Pico 小車基本動作函式

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)


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


def stop():
    _set_motor(M1_A, M1_B, 0)
    _set_motor(M2_A, M2_B, 0)


def forward():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, 1)


def backward():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, -1)


def turn_left():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, 1)


def turn_right():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, -1)


stop()
`
  },
  "sensor-rgb-warmup": {
    path: "downloads/sensor-rgb-warmup.py",
    title: "感測器主題暖身程式",
    summary: "這份暖身程式先讓學生看見 RGB LED 的變化，再進入距離感測與條件判斷。",
    stage: "主題 2：感測器操控暖身",
    backHref: "sensor-control.html",
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
    backHref: "sensor-control.html",
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
    stage: "主題 3：循跡入門暖身",
    backHref: "line-following-intro.html",
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
    title: "循跡入門主程式",
    summary: "這份主程式把左右循跡感測值直接轉成基本轉向規則，是進入進階循跡前的入門版本。",
    stage: "主題 3：循跡入門",
    backHref: "line-following-intro.html",
    steps: [
      "先讀取左右循跡感測器的值。",
      "再用四種規則決定前進、左修正、右修正或停止。",
      "先完成基本循跡，之後再往進階控制延伸。"
    ],
    highlights: [
      {
        title: "馬達與感測器設定",
        summary: "先準備兩側馬達腳位，再定義左右循跡感測器腳位。",
        range: "第 1-15 行",
        lines: [1, 15],
        tone: "teacher"
      },
      {
        title: "基本動作函式",
        summary: "這裡保留前進、左轉、右轉、停止四種最基本動作。",
        range: "第 18-42 行",
        lines: [18, 42],
        tone: "student"
      },
      {
        title: "四種循跡規則",
        summary: "左右感測值不同時，小車就依照規則做修正。",
        range: "第 50-64 行",
        lines: [50, 64],
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

M1_A = Pin(12, Pin.OUT)
M1_B = Pin(13, Pin.OUT)
M2_A = Pin(10, Pin.OUT)
M2_B = Pin(11, Pin.OUT)

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


def stop():
    _set_motor(M1_A, M1_B, 0)
    _set_motor(M2_A, M2_B, 0)


def forward():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, 1)


def turn_left():
    _set_motor(M1_A, M1_B, -1)
    _set_motor(M2_A, M2_B, 1)


def turn_right():
    _set_motor(M1_A, M1_B, 1)
    _set_motor(M2_A, M2_B, -1)


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
    stage: "主題 4：循跡進階暖身",
    backHref: "line-following-advanced.html",
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
    title: "循跡進階主程式",
    summary: "這份主程式把固定規則升級成速度差控制，並引入 last_error 與 derivative，讓循跡反應更平滑。",
    stage: "主題 4：循跡進階",
    backHref: "line-following-advanced.html",
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
    summaryNode.textContent = "請從 Boot Camp、感測器主題或下載區重新打開程式頁。";
    codeContent.textContent = "Unknown file key.";
    fileLabelNode.textContent = "UNKNOWN";
    stageNode.textContent = "未指定主題";
    downloadNode.href = "downloads.html";
    backNode.href = "downloads.html";
  } else {
    document.title = `${meta.title} | Raspberry Pi Pico 小車入門教學站`;
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
