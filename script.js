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
    summary: "本程式為 1 小時 Boot Camp 的主程式，執行後可於 Thonny Shell 輸入 w / a / s / d / x 控制小車。",
    stage: "Boot Camp 主程式",
    backHref: "bootcamp.html",
    steps: [
      "先在 Thonny 開啟本程式。",
      "按下 Run 後，到下方 Shell 輸入 w / a / s / d / x。",
      "建議先練習 w 與 x，再加入其他動作。"
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
    ]
  },
  "basic-motor-functions": {
    path: "downloads/basic-motor-functions.py",
    title: "馬達基本函式",
    summary: "本程式適合用來補充說明 forward()、backward()、turn_left()、turn_right()、stop() 等基本函式。",
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
    summaryNode.textContent = "請回到下載區重新選擇要查看的程式檔。";
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
