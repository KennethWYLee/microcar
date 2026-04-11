# Raspberry Pi Pico 小車入門教學站

網站入口：
- [GitHub Pages 網站](https://kennethwylee.github.io/microcar/)
- [GitHub Repository](https://github.com/KennethWYLee/microcar)

這個網站以 `Raspberry Pi Pico` 小車為主軸，將原本分散的教材整理成「依主題學習」的教學網站。網站不再以教師或學生身分區分，而是讓每一個主題都帶著使用者完成一個明確功能，先做出結果，再理解程式。

## 目前主題

1. `1 hr Boot Camp`
說明：在 1 小時內完成電腦與小車連線，使用 Thonny 貼上完整程式，並透過 `W / A / S / D / X` 控制小車。

2. `感測器的操控`
說明：讀取距離感測器數值，使用 `if / elif / else` 搭配 RGB LED 表現距離變化。

3. `循跡入門`
說明：從左右循跡感測值出發，先用最基本的四種規則讓小車沿著黑線前進。

4. `循跡進階`
說明：把固定規則升級成速度差控制，並加入 PD / PID 與閉迴路控制的入門觀念。

5. `循跡演算法`
說明：把規則式、P、PD、PID 放在一起比較，並提供可直接複製到 Thonny 的程式版本。

額外模組：
- `電路板入門`

## 網站結構

- `index.html`
  網站首頁與主題地圖。
- `bootcamp.html`
  主題 1：1 小時 Boot Camp。
- `sensor-control.html`
  主題 2：感測器的操控。
- `line-following-intro.html`
  主題 3：循跡入門。
- `line-following-advanced.html`
  主題 4：循跡進階。
- `line-following-algorithms.html`
  主題 5：循跡演算法。
- `student-handout.html`
  Boot Camp 學習單，可投影或列印。
- `downloads.html`
  依主題整理的下載區。
- `code-viewer.html`
  在網站中直接查看與複製程式。
- `styles.css`
  網站樣式。
- `script.js`
  動畫、程式載入與複製按鈕邏輯。

## 下載區分類

### 主題 1：Boot Camp
- `student-handout.html`
- `one-hour-bootcamp-teaching-plan.txt`
- `keyboard-car-control.py`
- `basic-motor-functions.py`

### 主題 2：感測器的操控
- `sensor-rgb-warmup.py`
- `distance-sensor-rgb.py`

### 主題 3：循跡入門
- `line-sensor-read.py`
- `line-following-intro.py`

### 主題 4：循跡進階
- `line-error-to-speed.py`
- `line-following-advanced.py`

### 主題 5：循跡演算法
- `line-following-p.py`
- `line-following-pid.py`

### 延伸教材
- `AmebaAI / AmebaNN`
- `Mango Library`
- 其他 PDF 與板子相關資源

## 教學使用方式

第一堂課建議直接從 `bootcamp.html` 開始，讓學生：

1. 接上 Raspberry Pi Pico 小車。
2. 打開 Thonny。
3. 在 Boot Camp 頁面照著 12 個步驟完成操作。
4. 把完整程式貼到 Thonny，按下 Run。
5. 在 Shell 輸入 `W / A / S / D / X` 控制小車。

第二堂課再進入 `sensor-control.html`，讓學生先觀察 RGB LED 的變化，再理解距離感測器與條件判斷。

第三堂課可以接著打開 `line-following-intro.html`，讓學生把感測器值和小車轉向規則連在一起，開始做最基本的循跡。

第四堂課可以打開 `line-following-advanced.html`，讓學生從固定規則跨到速度差控制，開始理解 error、correction、PD / PID 這些進階觀念。

第五堂課可以打開 `line-following-algorithms.html`，讓學生比較規則式、P、PD、PID 的差異，並直接從網站複製不同演算法的程式去測試。

## 備註

- 目前公開導覽已全面改成主題式結構。
- 舊版身分分流頁面僅保留作為歷史參考，不再作為網站主線。
- 網站設計進度請見 [WEB_DESIGN_PROGRESS.md](./WEB_DESIGN_PROGRESS.md)。
