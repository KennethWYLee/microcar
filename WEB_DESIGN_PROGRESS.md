# 網頁設計進度紀錄

最後更新：2026-08-28

## 目前位置

- 本機網站專案：`C:\Users\User\Documents\Lecture materials\roboweb`
- GitHub Repository：`https://github.com/KennethWYLee/microcar`
- GitHub Pages：`https://kennethwylee.github.io/microcar/`
- 發布分支：`main`

## 專案維護準則

- 後續整份 `roboweb` 專案維護需先遵循 `C:\Users\User\Documents\Lecture materials\CLAUDE.md`。
- 工作方式以先釐清假設、保持簡單、只做必要修改、修改後驗證為原則。
- `CLAUDE.md` 中針對其他 codebase 的專用路徑規則不硬套到本靜態網站；但「不要亂改無關內容、不要覆蓋正式資料、驗證後再交付」仍作為本專案共同準則。

## 本機開發來源

- `C:\Users\User\Documents\Lecture materials\robodev\microcar\website_cases`：microcar 的 MicroPython 案例來源。
- `C:\Users\User\Documents\Lecture materials\robodev\trackedcar\website_cases\09_Ameba82_智慧無人車`：trackedcar 主題可供網站整理的案例來源。
- `C:\Users\User\Documents\Lecture materials\robodev\microcar\無人車網頁開發`：microcar 的 Flutter 介面、預覽輸出與藍牙控制整合素材。
- 上述來源都放在 `roboweb` 網站 repo 外；完成內容、授權與發布範圍檢查後，才把需要公開的副本放入網站正式路徑。

## 2026-08-28 移動網站 repository

- 使用者核准網站資料夾名稱 `roboweb`。
- 完整網站 repository 已從
  `C:\Users\User\Documents\Lecture materials\robodev\webdev` 移至
  `C:\Users\User\Documents\Lecture materials\roboweb`。
- `.git`、commit 歷史與 `https://github.com/KennethWYLee/microcar.git` remote
  均保留；GitHub repository 名稱與 GitHub Pages 網址不因本機資料夾移動而改變。
- microcar 與 trackedcar 的權威來源仍在 `robodev/`，網站產生器透過
  `../robodev/microcar/` 與 `../robodev/trackedcar/` 讀取來源。

## 目前網站架構

網站目前定位為 Raspberry Pi Pico 小車與履帶車主題教材。首頁保留「網站建置中，所有 code 跟流程都還在驗證」提醒，避免學生或老師把尚未實機確認的內容視為最終版。

目前線上主頁面包含：

1. `BootCamp`：一小時快速體驗課。
2. `開始前設定`：Thonny、MicroPython、mango、import 測試與馬達校正。
3. `01 入門`：LED、按鈕與狀態控制。
4. `02 感測與輸出`：蜂鳴器、RGB 與超音波。
5. `03 小車移動`：馬達、速度與控制模組。
6. `04 無人車`：差速、避障、循跡與伺服掃描。
7. `05 專題化`：任務設計、策略比較與成果評量。
8. `06 藍芽遙控小車`：Flutter App 與 Pico BLE。
9. `07 電路板教材`：Python 控制與腳位導讀。
10. `08 電路板應用`：擺頭電扇。
11. `09 履帶車網路資訊流`：V1-V5 遠端控制、影像串流與系統除錯。
12. `Firmware`：Pico / Pico W / Pico 2 / Pico 2 W 的官方 MicroPython 韌體下載入口與板型對應表。
13. `下載區`：彙整程式、Markdown、PDF、PPT、官方 firmware 入口與延伸素材。

## 2026-05-12 修正

- 確認 `WEB_DESIGN_PROGRESS.md` 原始檔本身是 UTF-8 正常中文；先前看到亂碼是 PowerShell 顯示編碼造成。
- 重新整理本紀錄檔，避免日後從終端輸出時誤判為內容損壞。
- 移除所有 HTML 內的 Google Fonts 外部載入，避免網站本體依賴 `fonts.googleapis.com` 或 `fonts.gstatic.com`。
- 將 Creative Commons 標章圖片改為本機檔案：`assets/cc-by-nc-sa.svg`。
- 保留 Creative Commons 授權條款、MicroPython、Raspberry Pi、Pololu、Thonny 等外部文件連結，這些是參考連結，不是網站載入資源。

## 2026-05-12 新增主題 09

- 新增 `09 履帶車網路資訊流：V1-V5 遠端控制與影像串流`。
- 來源資料夾：`C:\Users\User\Documents\Lecture materials\robodev\trackedcar\course_materials\course_tracked_car_v1_v5_complete`。
- 主題命名理由：教材核心不是單純履帶車操作，而是 V1-V5 開發歷程中的 UDP 控制、UART 轉接、AMB82、X3/RP2040、RTSP 影像、延遲、log 判讀與跨網段中繼。
- 上傳策略：放 56 張基準版與 83 張課堂強化版 PDF/PPTX、學生講義與總覽圖；不公開 75 張延伸版、早期 171 張完整名詞版、教師筆記、逐頁 PNG、產生腳本與 `__pycache__`。
- 新增公開檔案：
  - `topic-09-tracked-car-info-flow.html`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-56slides.pdf`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-56slides.pptx`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-student-handout.md`
  - `assets/tracked-car-info-flow-contact-sheet.png`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-83slides-classroom.pdf`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-83slides-classroom.pptx`
  - `downloads/topic-09-tracked-car-info-flow/tracked-car-v1-v5-83slides-student-handout.md`
  - `assets/tracked-car-info-flow-contact-sheet-83slides.png`

## 2026-05-18 新增韌體檔

- 原先加入的履帶車 ZIP 韌體已確認為錯誤檔案，後續需移除。

## 2026-05-19 修正韌體下載策略

- 移除錯誤的履帶車 ZIP 韌體檔。
- 依照「韌體官方網頁已有提供」的策略，移除網站 repo 內的 UF2 韌體檔。
- 更新 `firmware.html`、`downloads.html`、`topic-09-tracked-car-info-flow.html` 與首頁下載入口，改為依板子名稱連到 MicroPython 官方下載頁。

## 2026-05-21 新增 Port 消失救援流程

- 在 `firmware.html` 新增 `Port 消失救援` solution。
- 說明當 Thonny 沒有出現 Pico Port 時，可先進入 BOOTSEL，使用 Raspberry Pi 官方 `flash_nuke.uf2` 清空外部 flash，再重新刷入正確的 MicroPython 韌體。
- 仍維持不把 UF2 檔案放進網站 repo 的策略，只保留官方文件與官方 UF2 入口。

## 網路資料來源政策

網站本體資料應來自 `microcar` repo，也就是線上 URL 應落在：

- `https://kennethwylee.github.io/microcar/`
- `https://github.com/KennethWYLee/microcar`

本體資料包含：

- HTML 頁面。
- CSS 與 JavaScript。
- 圖片、GIF、影片、SVG。
- 下載檔案。
- 韌體 UF2 檔不放入網站 repo，只保留官方下載頁連結。
- 課程用 Markdown、Python、Dart、PDF、PPTX、ZIP/7Z。

外部文件連結可保留，但只能作為參考閱讀，不應作為網站畫面載入所需的資料。這類連結目前包含 Creative Commons 授權條款、MicroPython 文件、Raspberry Pi 文件、Thonny 官網與相關技術參考。

## 驗證狀態

- 主要線上頁面已確認可回應 `200`。
- 本機主要 HTML、CSS、JS、圖片與下載檔案均存在。
- 2026-05-12 修正後，網站本體載入資源已改為相對路徑或 `microcar` 站內路徑。
- 2026-08-27：`tools/build_case_topic_pages.py --check` 通過。產生器只重建
  01-08 主題頁，不覆寫首頁、下載總覽、Firmware、開始設定與 09 主題，且
  不會建立 `downloads/firmware/` 或複製 UF2。
- 2026-08-27：五份 case Markdown、相容性報告、06 藍牙程式與 09 履帶車
  56/83 頁授課檔均已與 `../robodev/microcar/`、
  `../robodev/trackedcar/` 現行來源同步。
- 2026-08-27：`tools/verify_site.py` 檢查 19 個 HTML、677 個本機連結與
  錨點、12 個程式載入路徑、25 個網站 Python 檔、JavaScript、6 個
  ZIP/PPTX、4 個 PDF 與 2 個 7z，未發現阻擋問題。
- 2026-08-27：Edge 已渲染檢查桌面首頁、桌面 07 主題與 390px 手機首頁；
  未發現圖片、標題或按鈕重疊。手機導覽保留橫向捲動。
- 實體 Pico / Mango 小車與 AMB82 + X3/RP2040 履帶車仍未測試；Flutter、
  Dart 與 7-Zip 工具在目前環境不可用，因此 App 編譯與 7z 解壓內容未驗證。
- 若要確認線上版已套用最新修正，需要 commit 並 push 到 `main` 後，等待 GitHub Pages 部署完成，再重新掃描線上頁面。

## 後續建議

1. 先依 `../robodev/microcar/docs/hardware_test_plan.md` 完成 Pico / Mango 小車實機
   測試。完成條件是板型、供電、停止、馬達方向、感測器、I2C 與 BootCamp
   都有可追溯結果。
2. 小車完成後，再依 `../robodev/trackedcar/docs/hardware_test_plan.md` 測試 AMB82 +
   X3/RP2040 履帶車，不沿用小車的腳位與供電假設。
3. 逐步把 01-09 每個 case 或教材檔對應到明確的板子端檔案位置與電腦端檔案位置。
4. 將 `robodev/microcar/website_cases` 視為日後網站程式碼的穩定來源，減少從舊資料夾取檔造成版本混亂。
5. 若未來要把 AmebaAI / AmebaNN 車納入網站，另開延伸主題，不混入目前 Pico 小車與履帶車主線。
