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

  if (!meta) {
    titleNode.textContent = "找不到這份程式";
    summaryNode.textContent = "請回下載區重新選擇要查看的程式。";
    codeContent.textContent = "Unknown file key.";
    fileLabelNode.textContent = "UNKNOWN";
    stageNode.textContent = "請重新選擇";
    downloadNode.href = "downloads.html";
    backNode.href = "downloads.html";
  } else {
    document.title = `${meta.title} | Raspberry Pi Pico 循跡小車教學站`;
    titleNode.textContent = meta.title;
    summaryNode.textContent = meta.summary;
    fileLabelNode.textContent = meta.path;
    stageNode.textContent = meta.stage;
    downloadNode.href = meta.path;
    backNode.href = meta.backHref;
    stepsNode.innerHTML = meta.steps.map(step => `<li>${step}</li>`).join("");

    fetch(meta.path)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.text();
      })
      .then(text => {
        codeContent.textContent = text;

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
