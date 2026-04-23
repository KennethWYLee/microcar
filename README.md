# Raspberry Pi Pico 小車主題教材

網站入口：
- [GitHub Pages 網站](https://kennethwylee.github.io/microcar/)
- [GitHub Repository](https://github.com/KennethWYLee/microcar)

這個網站將機器人課程教材整理成 5 個主題，讓學習者可以依序從基礎輸出入、感測器、馬達控制，一路走到無人車應用與專題任務。

## 目前 5 個主題

1. `入門：LED、按鈕與狀態控制`
說明：建立輸出、輸入、判斷與狀態概念。

2. `感測與輸出：蜂鳴器、RGB 與超音波`
說明：把感測資料轉成聲音、燈號與距離回饋。

3. `小車移動：馬達、速度與控制模組`
說明：從單顆馬達測試走到雙輪小車與速度控制。

4. `無人車：差速、避障、循跡與伺服掃描`
說明：把感測器與馬達整合成無人車策略。

5. `專題化：任務設計、策略比較與成果評量`
說明：整合前面技巧，並加入規則式、P、PD、PID 循跡演算法延伸 cases。

## 網站結構

- `index.html`
  網站首頁與 5 主題地圖。
- `topic-01-intro.html`
  主題 1：LED、按鈕與狀態控制。
- `topic-02-sensor-output.html`
  主題 2：蜂鳴器、RGB 與超音波。
- `topic-03-car-motion.html`
  主題 3：馬達、速度與控制模組。
- `topic-04-autonomous-car.html`
  主題 4：差速、避障、循跡與伺服掃描。
- `topic-05-project-cases.html`
  主題 5：任務設計、策略比較與成果評量。
- `downloads.html`
  依主題整理的 Markdown 教材下載區。
- `bootcamp.html`
  1 小時體驗課支援頁，保留作為快速入門活動，不列入正式 5 主題。
- `code-viewer.html`
  程式檢視與複製支援頁。

## 教材來源

網頁主題內容由下列 Markdown 教材轉成 HTML：

- `01_入門_cases.md`
- `02_感測輸出_cases.md`
- `03_小車移動_cases.md`
- `04_無人車_cases.md`
- `05_專題化_cases.md`

網站中的 Markdown 下載檔放在：

- `downloads/case-md/`

## 教學使用方式

建議依照主題順序上課：

1. 先完成 LED、按鈕與狀態控制。
2. 再加入蜂鳴器、RGB 與超音波感測器。
3. 接著練習馬達方向、速度與小車移動。
4. 再把小車推進到避障、循跡與伺服掃描。
5. 最後進入專題任務與循跡演算法比較。

每個 case 都保留固定結構：主題、分階段教學、完整程式碼、最終成果、應用題與解答。

## 備註

- 舊的 `循跡入門 / 循跡進階 / 循跡演算法` 獨立主題已從公開主線移除。
- 循跡演算法中較有價值的規則式、P、PD、PID 內容已整合到 `05_專題化_cases.md`。
- 網站設計進度請見 [WEB_DESIGN_PROGRESS.md](./WEB_DESIGN_PROGRESS.md)。
