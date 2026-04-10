# Raspberry Pi Pico 小車入門教學站

網站連結：

- [GitHub Pages 網站](https://kennethwylee.github.io/microcar/)
- [GitHub Repository](https://github.com/KennethWYLee/microcar)

這個專案是一個以機器人課程教材為基礎重新整理的教學網站，主題聚焦在 `Raspberry Pi Pico` 小車入門教學。

網站不是把原始教材直接堆上來，而是重新篩選成適合老師授課、也適合學生自學的版本。  
目前教學主線先聚焦在第一堂課最需要的內容：

- 電腦與小車連線(Connection)
- `Thonny` 操作與執行
- 鍵盤控制(Keyboard Control)
- 小車基本移動(Car Motion)

藍牙遙控(Bluetooth Control)、感測器與循跡等內容目前視為後續進階案例，不放在第一階段主線首頁。

## 這個網站適合誰

- 國中生
- 國小高年級學生
- 想帶 1 小時入門課的老師

## 目前首頁只有四區

- `1 小時 Boot Camp`
- `教師區(Teacher Zone)`
- `學生區(Student Zone)`
- `下載區(Downloads)`

這樣的設計是為了讓首頁保持清楚，不把內部設計訊息或與主線無關的素材塞進首頁。

## 目前網站結構

網站現在不是只有首頁，而是：

- `index.html`
  首頁入口，提供四個主題的概覽。
- `bootcamp.html`
  1 小時 Boot Camp 的完整教學頁。
- `teacher-zone.html`
  教師區完整頁。
- `student-zone.html`
  學生區完整頁。
- `student-handout.html`
  學生版單頁講義，可直接投影或列印。
- `downloads.html`
  下載區完整頁，並依使用順序整理檔案。

## 內容特色

### 1. 1 小時 Boot Camp

給老師快速掌握一堂 60 分鐘小車入門課可以怎麼帶，包括：

- 課程定位
- 建議節奏
- 材料準備
- 學生的第一個成功目標

### 2. 教師區(Teacher Zone)

這一區偏備課與授課使用，內容較完整，包含：

- 學習目標(Learning Outcomes)
- 建議授課順序(Teaching Route)
- 第一堂課不建議先放進來的內容
- 簡單評量方式(Assessment)

### 3. 學生區(Student Zone)

這一區偏國中與國小高年級的閱讀習慣，做法是：

- 先看圖
- 再看短程式
- 最後自己改一點點

目前學生區的重點有：

- 鍵盤控制與動作對照
- `Thonny` 操作圖解
- 小車移動函式
- 常見問題排除

### 4. 下載區(Downloads)

下載區現在先把第一堂必用資源排在最前面，例如：

- 學生講義頁
- 1 小時授課建議
- 小車鍵盤控制範例
- 馬達基本函式範例
- 距離感測範例
- PDF 補充教材

另外也新增了 `延伸教材(Extension Materials)`，把目前不屬於主線的內容另外分區：

- `AmebaAI / AmebaNN`
  另外一台車的教材
- `Board & Library`
  和電路板、套件環境比較相關的資源

## 專案檔案結構

```text
microcar/
├─ archive/
│  ├─ legacy-extra-packages/
│  └─ legacy-smart-fan/
├─ bootcamp.html
├─ downloads.html
├─ index.html
├─ styles.css
├─ script.js
├─ student-handout.html
├─ student-zone.html
├─ teacher-zone.html
├─ README.md
├─ WEB_DESIGN_PROGRESS.md
├─ .nojekyll
├─ assets/
│  ├─ control-board.png
│  ├─ mechanism-rig.png
│  ├─ motion-sensor.png
│  └─ ir-sensor.png
└─ downloads/
   ├─ one-hour-bootcamp-teaching-plan.txt
   ├─ keyboard-car-control.py
   ├─ basic-motor-functions.py
   ├─ distance-sensor-rgb.py
   ├─ robot-programming-practice-python.pdf
   ├─ robot-code-jumpstart.pdf
   └─ extensions/
      ├─ board-library/
      │  └─ mango-library.zip
      └─ other-car/
         ├─ ameba-ai.zip
         └─ ameba-nn.zip
```

## 使用方式

### 給老師

建議從 `教師區(Teacher Zone)` 開始：

1. 先看 `1 小時 Boot Camp`
2. 再看 `student-handout.html`，確認學生會看到的版本
3. 再看 `教師區(Teacher Zone)` 的授課重點
4. 最後到 `下載區(Downloads)` 取用需要的程式或教材

### 給學生

建議從 `學生區(Student Zone)` 開始：

1. 先看 `student-handout.html`
2. 再看動作和按鍵圖解
3. 再讀短程式
4. 最後下載範例程式自己試改

## 進度紀錄

如果要看網站目前的設計決策與後續規劃，請看：

- [WEB_DESIGN_PROGRESS.md](./WEB_DESIGN_PROGRESS.md)
