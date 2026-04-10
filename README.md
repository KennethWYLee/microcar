# 機器人程式設計教學站

這個專案是一個以 `機器人` 課程教材為基礎整理而成的教學網站，主題聚焦在小車程式、感測器互動、馬達控制與機構整合。  
網站不是單純把原始教材上傳，而是重新整理成更適合教學與自學的形式。

目前網站已分成兩條主要閱讀路線：
- `教師區(Teacher Zone)`：提供較專業的授課導引、節奏安排、學習目標與評量建議。
- `學生區(Student Zone)`：提供更適合國小與國中學生閱讀的圖解、任務卡與自學路線。

網站首頁：
- [index.html](./index.html)

## 專案定位

這個網站適合以下使用情境：
- 老師上課前快速掌握這一節要教什麼、怎麼帶、學生可以做到哪裡。
- 學生課堂中跟著圖解理解小車動作與程式之間的關係。
- 學生課後回家重新看一次網站內容，照著範例練習。

這份教材的核心不是只有「做出作品」，而是讓學生逐步理解：
- 輸入(Input)
- 判斷(Condition)
- 輸出(Output)
- 動作(Motion)
- 感測回饋(Sensor Feedback)
- 機構整合(Mechanism Integration)

## 教材來源

本網站內容主要整理自 `機器人` 課程中的以下教材與資源：
- 課程簡報(PPT)
- PDF 教材
- Python / MicroPython 範例程式
- 控制板、感測器與機構相關圖片

網站整合的主題包含：
- 小車程式(Car Program)
- 數位輸入輸出(Digital I/O)
- 脈衝寬度調變(PWM)
- 感測器(Sensor)
- 馬達控制(Motor Control)
- 藍牙遙控(Bluetooth Control)
- 連桿與齒輪機構(Linkage & Gear Mechanism)

## 網站特色

### 1. 教師區(Teacher Zone)

教師區的設計偏向授課與備課用途，內容較完整，適合老師快速規劃課堂：
- 學習目標(Learning Outcomes)
- 授課節奏(Pacing)
- 差異化教學(Differentiation)
- 評量建議(Assessment)

### 2. 學生區(Student Zone)

學生區的設計偏向國小與國中學生閱讀習慣，內容更簡單、更直觀：
- 用簡單任務卡代替太多抽象說明
- 先看圖，再看程式，再做小修改
- 降低第一次接觸程式時的壓力

### 3. 圖解學習(Illustrated Learning)

網站加入了大量教學圖解，不是裝飾圖，而是幫助學生理解程式邏輯的圖：
- 指令與動作對照圖
- 小車程式骨架流程圖
- 感測器判斷圖
- 藍牙控制資料流圖
- 常用函式對照圖

### 4. 程式練習(Code Practice)

網站整理了較適合入門的範例程式，讓學生可以從小段程式開始：
- LED 基礎練習
- 按鈕控制 LED
- 感測器條件判斷
- 小車動作函式

### 5. 下載區(Downloads)

網站保留了課堂常用教材的下載入口，方便老師備課與學生課後複習。

## 網站內容結構

目前首頁主要包含以下區塊：
- 教師區(Teacher Zone)
- 學生區(Student Zone)
- 導覽區(Navigation)
- 課程定位(Overview)
- 授課建議(Teaching Plan)
- 單元地圖(Lesson Map)
- 圖解學習(Illustrated Learning)
- 材料與機構(Build Kit)
- 程式練習(Code Practice)
- 下載區(Downloads)

## 專案檔案結構

```text
microcar/
├─ index.html
├─ styles.css
├─ script.js
├─ README.md
├─ .nojekyll
├─ assets/
│  ├─ control-board.png
│  ├─ mechanism-rig.png
│  ├─ motion-sensor.png
│  └─ ir-sensor.png
└─ downloads/
   ├─ smart-fan-smart-control-programming.pptx
   ├─ smart-fan-mechanism-structure.pptx
   ├─ smart-fan-course-slides.pptx
   ├─ robot-programming-practice-python.pdf
   ├─ robot-code-jumpstart.pdf
   ├─ mango-library.zip
   ├─ ameba-ai.zip
   └─ ameba-nn.zip
```

## 主要檔案說明

- `index.html`
  網站首頁與主要內容。
- `styles.css`
  網站整體視覺樣式與版面設計。
- `script.js`
  頁面互動與滾動顯示效果。
- `assets/`
  網站中使用的圖片素材。
- `downloads/`
  提供老師與學生下載的教材檔案。

## 適合的使用方式

### 給老師

建議從 `教師區(Teacher Zone)` 開始使用：
- 先看學習目標與授課節奏
- 再對照圖解與程式範例安排示範順序
- 最後引導學生做小修改與口頭說明

### 給學生

建議從 `學生區(Student Zone)` 開始使用：
- 先看圖，知道每個動作代表什麼
- 再照著打一段範例程式
- 最後自己改一點點，觀察小車的反應

## 學生怎樣使用這個網站

如果你是第一次看這個網站，可以照這個順序：

1. 先進入 `學生區(Student Zone)`。
2. 看懂小車的基本動作和圖解。
3. 到 `程式練習(Code Practice)` 跟著打一段程式。
4. 自己改一個速度、方向或距離。
5. 如果還想繼續學，再到 `下載區(Downloads)` 下載簡報和教材。

只要你能做到「看得懂動作、打得出程式、改得動一點點」，就已經是在學真正的程式設計了。
