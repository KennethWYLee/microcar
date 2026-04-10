# 循跡小車入門教學站

網站連結：

- [GitHub Pages 網站](https://kennethwylee.github.io/microcar/)
- [GitHub Repository](https://github.com/KennethWYLee/microcar)

這個專案是一個以機器人課程教材為基礎重新整理的教學網站，主題聚焦在「循跡小車的初階教學」。

網站不是把原始教材直接堆上來，而是重新篩選成適合老師授課、也適合學生自學的版本。  
目前教學主線先聚焦在：

- 小車基本移動(Car Motion)
- 感測器(Sensor)
- 條件判斷(Condition)
- 入門程式邏輯(Beginner Logic)

藍牙遙控(Bluetooth Control) 等內容目前視為後續進階案例，不放在第一階段首頁主線。

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
- 感測器讀值與判斷
- 小車移動函式

### 4. 下載區(Downloads)

下載區現在只放和初階小車教學直接相關的資源，例如：

- 1 小時授課建議
- 小車鍵盤控制範例
- 馬達基本函式範例
- 距離感測範例
- PDF 補充教材
- Mango 套件

## 專案檔案結構

```text
microcar/
├─ archive/
│  ├─ legacy-extra-packages/
│  └─ legacy-smart-fan/
├─ index.html
├─ styles.css
├─ script.js
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
   └─ mango-library.zip
```

## 使用方式

### 給老師

建議從 `教師區(Teacher Zone)` 開始：

1. 先看 `1 小時 Boot Camp`
2. 再看 `教師區(Teacher Zone)` 的授課重點
3. 最後到 `下載區(Downloads)` 取用需要的程式或教材

### 給學生

建議從 `學生區(Student Zone)` 開始：

1. 先看動作和感測器圖解
2. 再讀短程式
3. 最後下載範例程式自己試改

## 進度紀錄

如果要看網站目前的設計決策與後續規劃，請看：

- [WEB_DESIGN_PROGRESS.md](./WEB_DESIGN_PROGRESS.md)
