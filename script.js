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
    title: "Thonny 鍵盤控制範例",
    summary:
      "這份程式可直接從網頁整份複製到 Thonny 新檔。執行後可於 Thonny Shell 輸入 w / a / s / d / x 控制小車。",
    stage: "Boot Camp 主程式",
    backHref: "bootcamp.html",
    steps: [
      "先在 Thonny 建立一個新的 `.py` 檔。",
      "回到本頁按「複製這份程式」，再貼到 Thonny。",
      "按下 Run 後，到下方 Shell 輸入 w / a / s / d / x。"
    ],
    highlights: [
      {
        title: "接腳與 LED",
        summary: "本段設定左右馬達與板上 LED 所需的控制腳位。",
        range: "第 1-12 行",
        lines: [1, 12],
        tone: "teacher"
      },
      {
        title: "動作函式",
        summary: "本段將前進、後退、左轉、右轉與停止封裝成函式，便於後續直接呼叫。",
        range: "第 15-49 行",
        lines: [15, 49],
        tone: "student"
      },
      {
        title: "啟動與讀取按鍵",
        summary: "本段先顯示提示訊息，再持續等待 Thonny Shell 輸入按鍵指令。",
        range: "第 52-88 行",
        lines: [52, 88],
        tone: "teacher"
      }
    ],
    fallbackText: `from machine import Pin
import sys
import time

# Raspberry Pi Pico 小車 1 小時 Boot Camp
# 在 Thonny 執行後，到 Shell 輸入 w / a / s / d / x 再按 Enter

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
print("w=前進, s=後退, a=左轉, d=右轉, x=停止")

stop()
LED.off()

while True:
    cmd = sys.stdin.read(1)
    if not cmd:
        continue

    cmd = cmd.strip().lower()
    if not cmd:
        continue

    if cmd == "w":
        print("前進")
        forward()
    elif cmd == "s":
        print("後退")
        backward()
    elif cmd == "a":
        print("左轉")
        turn_left()
    elif cmd == "d":
        print("右轉")
        turn_right()
    elif cmd == "x":
        print("停止")
        stop()
    else:
        print("未知指令:", cmd)
        stop()

    LED.toggle()
    time.sleep(0.05)
`
  },
  "basic-motor-functions": {
    path: "downloads/basic-motor-functions.py",
    title: "馬達基本函式",
    summary:
      "本程式適合用來補充說明 forward()、backward()、turn_left()、turn_right()、stop() 等基本函式。",
    stage: "補充程式",
    backHref: "bootcamp.html",
    steps: [
      "建議先閱讀 stop() 與 forward()。",
      "再閱讀 backward()、turn_left() 與 turn_right()。",
      "將各函式與實際動作對應起來。"
    ],
    highlights: [
      {
        title: "接腳設定",
        summary: "本段設定控制左右馬達的 4 個腳位，作為後續函式的基礎。",
        range: "第 1-11 行",
        lines: [1, 11],
        tone: "teacher"
      },
      {
        title: "核心控制函式",
        summary: "_set_motor() 為底層控制函式，其他動作函式皆會呼叫此函式。",
        range: "第 13-22 行",
        lines: [13, 22],
        tone: "student"
      },
      {
        title: "五個基本動作",
        summary: "本段將停止、前進、後退、左轉與右轉整理成獨立函式。",
        range: "第 25-50 行",
        lines: [25, 50],
        tone: "teacher"
      }
    ]
  },
  "distance-sensor-rgb": {
    path: "downloads/distance-sensor-rgb.py",
    title: "距離感測範例",
    summary: "本程式為延伸課使用內容，示範如何加入感測器與條件判斷。",
    stage: "延伸程式",
    backHref: "downloads.html",
    steps: [
      "本程式不列入第一堂課必要內容。",
      "建議先閱讀感測器讀值，再閱讀 if 判斷。",
      "待學生熟悉鍵盤控制後，再納入延伸學習。"
    ],
    highlights: [
      {
        title: "匯入與初始化",
        summary: "本段載入距離感測器與顏色工具，並建立超音波感測器與 RGB LED。",
        range: "第 1-8 行",
        lines: [1, 8],
        tone: "teacher"
      },
      {
        title: "重複量測",
        summary: "本段以 for 迴圈持續量測距離，並更新感測結果。",
        range: "第 9-21 行",
        lines: [9, 21],
        tone: "student"
      },
      {
        title: "距離判斷",
        summary: "本段透過 if / elif / else 依照距離變化調整 RGB 燈號顏色。",
        range: "第 14-19 行",
        lines: [14, 19],
        tone: "teacher"
      }
    ]
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
    titleNode.textContent = "找不到這份程式";
    summaryNode.textContent = "請回到 Boot Camp 或下載區重新選擇要查看的程式。";
    codeContent.textContent = "Unknown file key.";
    fileLabelNode.textContent = "UNKNOWN";
    stageNode.textContent = "請重新選擇";
    downloadNode.href = "downloads.html";
    backNode.href = "downloads.html";
  } else {
    document.title = `${meta.title} | Raspberry Pi Pico 小車入門教學站`;
    titleNode.textContent = meta.title;
    summaryNode.textContent = meta.summary;
    fileLabelNode.textContent = meta.path;
    stageNode.textContent = meta.stage;
    downloadNode.href = meta.path;
    downloadNode.textContent = "原始檔備用";
    backNode.href = meta.backHref;
    stepsNode.innerHTML = meta.steps.map(step => `<li>${step}</li>`).join("");
    renderHighlights(highlightGrid, meta.highlights);

    loadCodeText(meta)
      .then(text => {
        renderCode(codeContent, text, meta.highlights);
        attachCopyHandler(copyNode, () => text);
      })
      .catch(error => {
        codeContent.textContent = `載入失敗: ${error.message}`;
      });
  }
}

const bootcampCodeNode = document.getElementById("bootcamp-full-code");
const bootcampCopyButton = document.getElementById("bootcamp-copy-code");

if (bootcampCodeNode) {
  const meta = codePages["keyboard-car-control"];
  loadCodeText(meta)
    .then(text => {
      renderCode(bootcampCodeNode, text, []);
      attachCopyHandler(bootcampCopyButton, () => text);
    })
    .catch(error => {
      bootcampCodeNode.textContent = `載入失敗: ${error.message}`;
    });
}
