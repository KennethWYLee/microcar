# Raspberry Pi Pico 小車主題教材

網站入口：
- [GitHub Pages 網站](https://kennethwylee.github.io/microcar/)
- [GitHub Repository](https://github.com/KennethWYLee/microcar)

這個網站將機器人課程教材整理成可依序學習的主題式教學網站。課程從 Raspberry Pi Pico 小車的基本輸出入開始，逐步進入感測器、馬達控制、無人車任務、專題化整合、藍芽遙控，以及電路板作品應用。

`開始前設定` 是所有自學者的第一站，先完成 Thonny 連線、MicroPython 解譯器、`mango` 函式庫上傳、import 測試與馬達方向校正。完成後再進入 `BootCamp` 或 01-05 小車核心主線。

`BootCamp` 保留為一小時快速體驗課入口，適合第一次上課時讓學生先用 Thonny 連接小車、貼上程式並完成前進、後退、左右轉與停止。它不是正式 01-08 主題的一部分。

## 目前 8 個主題

1. `01 入門：LED、按鈕與狀態控制`
2. `02 感測與輸出：蜂鳴器、RGB 與超音波`
3. `03 小車移動：馬達、速度與控制模組`
4. `04 無人車：差速、避障、循跡與伺服掃描`
5. `05 專題化：任務設計、策略比較與成果評量`
6. `06 藍芽遙控小車：Flutter App 與 Pico BLE`
7. `07 電路板教材：Python 控制與腳位導讀`
8. `08 電路板應用：擺頭電扇`

## 網站頁面

- `index.html`：首頁與 8 主題總覽。
- `setup.html`：開始前設定，包含 `mango` 函式庫上傳、import 測試與馬達校正。
- `bootcamp.html`：BootCamp 快速體驗課。
- `topic-01-intro.html` 到 `topic-05-project-cases.html`：五個小車核心主題。
- `topic-06-bluetooth-car.html`：Flutter App 與 Pico BLE 藍芽遙控小車。
- `topic-07-board-python.html`：依 `機器人程式設計實務-Python.pdf` 整理的電路板與腳位導讀。
- `topic-08-fan-application.html`：依 `擺頭電扇-課程簡報.pptx` 整理的電路板應用作品。
- `downloads.html`：依主題整理的教材、程式、PDF 與簡報下載區。
- `code-viewer.html`：可顯示網站中保留的獨立 Python 範例。

## 教材來源與下載

01-05 主題由 Markdown cases 產生，原始檔放在 `downloads/case-md/`。06 主題提供 Flutter `main.dart` 與 Pico BLE 小車端程式，07 主題提供 Python PDF，08 主題提供擺頭電扇課程簡報。

開始前必備檔案放在下載區：

- `downloads/extensions/board-library/mango-library.zip`：上傳到 Pico 的 `mango` 函式庫。
- `downloads/mango-import-test.py`：確認 `mango` 函式庫可正常 import。
- `downloads/motor-calibration.py`：確認右輪、左輪、前進、後退與左右轉方向。

## 檔案位置觀念

本教材特別把「電腦本機端」與「Pico 板子端」分開說明。網站、PDF、PPT、Markdown 與下載素材會先留在電腦；只有 Pico 需要 import 的函式庫，或要直接執行的 MicroPython 程式，才需要用 Thonny 上傳到 Pico。

```text
電腦本機 microcar/
├─ index.html / setup.html / topic-xx.html
├─ downloads/
│  ├─ case-md/
│  ├─ mango-import-test.py
│  ├─ motor-calibration.py
│  └─ extensions/board-library/mango-library.zip
└─ assets/
```

```text
Raspberry Pi Pico /
├─ mango/        ← 使用 from mango import ... 前必須先上傳
├─ practice.py   ← 平常練習檔，名稱可自訂
└─ main.py       ← 只有要開機自動執行時才使用
```

學生上課時建議流程：

1. 從網站複製當天的程式。
2. 在 Thonny 按 `File > New` 建立新檔。
3. 貼上程式後先按 `Run` 測試。
4. 如果程式需要 `mango`，確認 Pico 根目錄已經有 `mango/`。
5. 練習檔可以存成自訂名稱；最後穩定版本才存成 Pico 上的 `main.py`。

## 建議使用方式

自學或正式授課建議先從 `開始前設定` 開始，確認環境、函式庫與馬達方向都正確。第一次上課可接著使用 `BootCamp`，讓學生建立「電腦連到小車、程式貼上去、小車會動」的成功經驗。後續課程再依序進入 01-05 主題建立小車能力。

06 是進階藍芽遙控主題，建議學生已完成 03 小車移動後再做。07 是電路板與腳位查表導讀，適合備課與除錯。08 是延伸作品，把小車課程中的控制概念移植到擺頭電扇，不屬於小車核心必修。

更多網站設計進度請見 [WEB_DESIGN_PROGRESS.md](./WEB_DESIGN_PROGRESS.md)。

