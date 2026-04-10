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

document.querySelectorAll(".reveal").forEach(node => observer.observe(node));

const codePages = {
  "keyboard-car-control": {
    path: "downloads/keyboard-car-control.py",
    title: "Thonny 鍵盤控制範例",
    summary: "這是 1 小時 Boot Camp 的主力程式。執行後可以直接在 Thonny Shell 輸入 w / a / s / d / x 控制小車。",
    stage: "Boot Camp 主程式",
    backHref: "bootcamp.html",
    steps: [
      "先在 Thonny 開啟這份程式。",
      "按 Run 執行後，到下方 Shell 輸入 w / a / s / d / x。",
      "先試 w 和 x，再慢慢加入其他動作。"
    ],
    highlights: [
      {
        title: "接腳與 LED",
        summary: "這一段先告訴 Pico 小車，哪些腳位要拿來控制左右馬達和板上的 LED。",
        range: "第 1-12 行",
        lines: [1, 12],
        tone: "teacher"
      },
      {
        title: "動作函式",
        summary: "這裡把前進、後退、左轉、右轉、停止包成函式，之後只要呼叫函式就能控制小車。",
        range: "第 15-49 行",
        lines: [15, 49],
        tone: "student"
      },
      {
        title: "啟動與讀取按鍵",
        summary: "這一段會先印出提示，再一直等待你從 Thonny Shell 輸入字母。",
        range: "第 52-88 行",
        lines: [52, 88],
        tone: "teacher"
      }
    ]
  },
  "basic-motor-functions": {
    path: "downloads/basic-motor-functions.py",
    title: "馬達基本函式",
    summary: "這份程式適合補充說明 forward()、backward()、turn_left()、turn_right()、stop() 這些基本函式。",
    stage: "補充程式",
    backHref: "bootcamp.html",
    steps: [
      "先看 stop() 和 forward()。",
      "再看 backward()、turn_left()、turn_right()。",
      "把每一個函式和實際動作連起來。"
    ],
    highlights: [
      {
        title: "接腳設定",
        summary: "先把控制左右馬達的 4 個腳位設定好，這樣後面的函式才知道要控制哪裡。",
        range: "第 1-11 行",
        lines: [1, 11],
        tone: "teacher"
      },
      {
        title: "核心控制函式",
        summary: "_set_motor() 是最底層的控制器，其他動作函式都會用到它。",
        range: "第 13-22 行",
        lines: [13, 22],
        tone: "student"
      },
      {
        title: "五個基本動作",
        summary: "這一段把停止、前進、後退、左轉、右轉拆成清楚的函式。",
        range: "第 25-50 行",
        lines: [25, 50],
        tone: "teacher"
      }
    ]
  },
  "distance-sensor-rgb": {
    path: "downloads/distance-sensor-rgb.py",
    title: "距離感測範例",
    summary: "這份是下一堂延伸課才會用到的程式，用來加入感測器和條件判斷。",
    stage: "延伸程式",
    backHref: "downloads.html",
    steps: [
      "這份不一定要在第一堂課打開。",
      "先看感測器讀值，再看 if 判斷。",
      "等學生熟悉鍵盤控制後再加入這份。"
    ],
    highlights: [
      {
        title: "匯入與初始化",
        summary: "先載入距離感測器與顏色工具，再建立超音波感測器和 RGB LED。",
        range: "第 1-8 行",
        lines: [1, 8],
        tone: "teacher"
      },
      {
        title: "重複量測",
        summary: "for 迴圈會一直量距離，所以這份程式會持續更新感測結果。",
        range: "第 9-21 行",
        lines: [9, 21],
        tone: "student"
      },
      {
        title: "距離判斷",
        summary: "if / elif / else 會依照距離不同，改變 RGB 燈號顏色。",
        range: "第 14-19 行",
        lines: [14, 19],
        tone: "teacher"
      }
    ]
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

  const escapeHtml = value =>
    value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");

  const renderCode = (text, highlights = []) => {
    const ranges = highlights.map(item => ({
      start: item.lines[0],
      end: item.lines[1],
      tone: item.tone
    }));
    const lines = text.split("\n");
    codeContent.innerHTML = lines
      .map((line, index) => {
        const lineNo = index + 1;
        const activeRange = ranges.find(range => lineNo >= range.start && lineNo <= range.end);
        const toneClass = activeRange ? ` highlight-${activeRange.tone}` : "";
        const highlightClass = activeRange ? " is-highlight" : "";
        return `<span class="code-line${highlightClass}${toneClass}"><span class="code-line-no">${lineNo}</span><span class="code-line-text">${escapeHtml(line) || "&nbsp;"}</span></span>`;
      })
      .join("");
  };

  const renderHighlights = highlights => {
    if (!highlightGrid || !highlights?.length) {
      return;
    }
    highlightGrid.innerHTML = highlights
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

  if (!meta) {
    titleNode.textContent = "找不到這份程式";
    summaryNode.textContent = "請回下載區重新選擇要查看的程式。";
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
    backNode.href = meta.backHref;
    stepsNode.innerHTML = meta.steps.map(step => `<li>${step}</li>`).join("");
    renderHighlights(meta.highlights);

    fetch(meta.path)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.text();
      })
      .then(text => {
        renderCode(text, meta.highlights);

        copyNode.addEventListener("click", async () => {
          try {
            await navigator.clipboard.writeText(text);
            copyNode.textContent = "已複製";
            window.setTimeout(() => {
              copyNode.textContent = "複製程式";
            }, 1500);
          } catch (error) {
            copyNode.textContent = "複製失敗";
            window.setTimeout(() => {
              copyNode.textContent = "複製程式";
            }, 1500);
          }
        });
      })
      .catch(error => {
        codeContent.textContent = `載入失敗: ${error.message}`;
      });
  }
}
