# microcar

機器人程式設計教學網站，主題為「智慧型可擺動調速電風扇」專題。

本專案是根據既有的課程教材重新設計而成的靜態網站，目標不是只展示作品，而是整理成一個更適合老師授課、也方便學生課後自學的教學頁面。網站內容以中文為主，並在重要概念後補上英文關鍵字，格式為 `中文(English)`，方便教學、查詢與跨語言理解。

## 專案目標

這個網站主要解決三件事：

1. 把原本分散在簡報、PDF、程式檔中的內容整理成更清楚的教學結構。
2. 讓老師可以直接依照網站頁面進行授課，不需要每次重新整理講課順序。
3. 讓學生在課後可以依照相同順序回看網站，自行複習並完成自學。

## 教材來源

本網站主要依據以下教材內容整理：

- `擺頭電扇-智慧控制程式設計.pptx`
- `擺頭電扇-機構結構.pptx`
- `擺頭電扇-課程簡報.pptx`
- `機器人程式設計實務-Python.pdf`
- `Robot_Code_Jumpstart.pdf`
- 課程資料夾中的 Python / MicroPython 程式範例

網站中的教學結構，特別聚焦於以下主題：

- 樹莓派 Pico(Raspberry Pi Pico)
- 數位輸入輸出(Digital Input / Output)
- 脈衝寬度調變(PWM)
- 感測器(Sensor)
- 馬達控制(Motor Control)
- 齒輪傳動(Gear Transmission)
- 連桿機構(Linkage Mechanism)
- 藍牙遙控(Bluetooth Control)
- 整合專題(Project Integration)

## 網站特色

這一版網站是「老師授課版(Teacher Edition)」，因此在設計上有幾個明確方向：

- 中文為主，適合本地課堂直接使用
- 關鍵字附英文，方便學生建立雙語概念
- 內容安排以教學順序為中心，而不是單純作品展示
- 提供下載區，讓學生能直接取得簡報、PDF 與套件資源
- 資訊切成較短、較容易閱讀的段落，降低學生閱讀負擔

## 網站內容架構

目前首頁大致分成以下區塊：

### 1. 導覽區(Navigation)

幫老師快速掌握網站的使用方式，也讓學生知道從哪裡開始看。

### 2. 課程定位(Overview)

說明這門課的核心不只是做一台電風扇，而是學會如何整合：

- 電路(Circuit)
- 程式(Programming)
- 感測(Sensing)
- 機構(Mechanism)

### 3. 授課建議(Teaching Plan)

專門給老師使用，整理課前、課中與課後比較合適的教學節奏。

### 4. 單元地圖(Lesson Map)

依照原始 PPT 內容重新整理出較清楚的授課順序，例如：

- 控制板與韌體(Control Board & Firmware)
- 數位輸入輸出(Digital I/O)
- 類比控制與感測(Analog Control & Sensing)
- 馬達與智慧控制(Motor & Smart Control)
- 機構設計與組裝(Mechanism & Assembly)

### 5. 材料設備(Build Kit)

整理出老師上課前需要準備、學生課後需要認識的元件與材料。

### 6. 機構概念(Mechanism)

把原本較分散的機構說明濃縮成幾個較容易教學的重點，例如：

- 機構(Mechanism)
- 齒輪傳動(Gear Transmission)
- 四連桿(Four-bar Linkage)

### 7. 程式練習(Code Practice)

選出最有代表性的練習內容，幫助學生從簡單範例逐步走向整合作品。

### 8. 自學路徑(Self-study Path)

提供學生課後可直接照著走的複習順序。

### 9. 下載區(Downloads)

集中放置老師與學生常用的教材檔案，減少在資料夾中翻找檔案的時間。

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
  網站首頁與教學內容主體。

- `styles.css`
  網站版面、色彩、字體、卡片與響應式設計。

- `script.js`
  頁面捲動時的淡入顯示效果。

- `assets/`
  由課程簡報擷取、整理後放入網站的圖片素材。

- `downloads/`
  供老師與學生直接下載的教材與套件資源。

## 適合的使用情境

### 老師使用

本網站適合以下教學情境：

- 上課前作為課程大綱與教材入口頁
- 課堂中當成投影授課頁面
- 示範程式時快速切換到相關單元
- 課後提供學生統一網址進行複習

### 學生使用

本網站適合以下學習情境：

- 課前先預習這堂課會學什麼
- 課中跟著老師同步查看概念與範例
- 課後依照自學路徑重做程式與複習簡報
- 從下載區補抓教材與 PDF

## 本機預覽方式

如果要在本機開啟網站，可直接進入專案資料夾後啟動簡易伺服器：

```powershell
cd "C:\Users\User\Documents\Lecture materials\microcar"
python -m http.server 8008
```

之後在瀏覽器開啟：

```text
http://127.0.0.1:8008/
```

## GitHub Pages 部署

本專案是純靜態網站，適合直接使用 GitHub Pages。

部署步驟：

1. 將本專案 push 到 GitHub repository。
2. 到 GitHub repository 的 **Settings**。
3. 找到 **Pages**。
4. 在 **Build and deployment** 中選擇 **Deploy from a branch**。
5. Branch 選擇 `main`，資料夾選擇 `/ (root)`。
6. 儲存後，等待 GitHub Pages 完成部署。

如果部署成功，GitHub Pages 會提供一個公開網址，學生之後只要開這個網址即可使用網站與下載教材。

## 後續可延伸方向

這個網站之後還可以繼續擴充，例如：

- 拆成「老師版」與「學生版」兩個入口
- 加上每一節課的授課時間建議
- 加上更多逐步實作範例與接線圖
- 加上每一份簡報的摘要頁
- 加上作業區與成果展示區

## 學生如何使用這個網站

如果你是學生，建議你依照下面的順序使用這個網站：

1. 先看「導覽區(Navigation)」，知道網站有哪些區塊。
2. 再看「課程定位(Overview)」，理解這門課最後要做出什麼作品。
3. 接著看「單元地圖(Lesson Map)」，知道每一節課的學習順序。
4. 進入「程式練習(Code Practice)」，從簡單的 LED、按鈕與感測器開始練習。
5. 看完後再讀「機構概念(Mechanism)」，理解作品為什麼能擺動。
6. 最後到「下載區(Downloads)」，把簡報、PDF 和套件下載回去複習。

建議不要一開始就直接做完整專題，而是先把：

- LED 控制
- 按鈕輸入
- PWM 調光
- 感測器回饋
- 馬達控制

這些基礎練習完成後，再回頭整合成完整作品。這樣你會更容易理解整個系統，也比較不容易在中途卡住。
