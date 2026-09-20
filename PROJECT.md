# microcar 網頁設計專案

> 工作規則見本目錄 `AGENTS.md`，並遵循使用者的全域指示；本檔記錄網站 repository 的來源、發布邊界、
> 維護方式與目前狀態。

- 最後盤點日期：2026-09-20（首頁、導覽、字型、平板排版與韌體救援入口）
- 歷史名稱：`roboweb`，先前記錄為使用者於 2026-08-28 指定的資料夾名稱。
- 本機位置：`C:\Users\User\Documents\NTUB_microcar_web`
- GitHub repository：`https://github.com/KennethWYLee/microcar`
- GitHub Pages：`https://kennethwylee.github.io/microcar/`
- Repository：獨立 Git repository，不再巢狀放在 `robodev/`。

## 目前負責範圍

- 2026-09-08：使用者指定此專案負責 `KennethWYLee/microcar` 的網頁設計。
- 在此工作區維護網站的視覺設計、頁面配置、導覽、手機與桌面顯示、互動及網站資產。
- 延續既有教材內容與來源規則；具體設計調整依使用者後續需求實作。
- 2026-09-08：本機 `main` 與遠端 `main` 均為
  `19df7ff2f84c173a01ca4cfb817d5b7144f9f9c5`；設定負責範圍前工作目錄乾淨。
- 2026-09-18：已確認目前教材來源為 `../NTUB_UGV/`，亦即
  `C:\Users\User\Documents\NTUB_UGV`。產生器與目前維護文件使用此位置；
  歷史紀錄中的 `robodev`、`roboweb` 保留原名稱供追溯。

## 網站資訊與決策依據

- 網站資訊、內容編排、功能調整與發布歷程主要依據：
  `codex://threads/019d66f5-f174-7ff2-ab98-fa30052e7e0d`。
- 使用者目前的明確指示優先於該 task 的較早紀錄。
- `../NTUB_UGV/microcar/` 與 `../NTUB_UGV/trackedcar/` 仍保存程式、教材與硬體
  資料來源；從這些來源選擇哪些內容放上網站時，以上述 Codex task 的網站
  決策為主要依據。
- 若該 task、目前網站檔案與 `NTUB_UGV` 來源互相衝突，先保留各自版本並回報
  差異，不自行混合不相容的腳位、版本、教材內容或發布範圍。

## 來源與發布邊界

- microcar 權威來源：`../NTUB_UGV/microcar/`
- trackedcar 權威來源：`../NTUB_UGV/trackedcar/`
- 本網站 repository 只保存公開網頁、網站資產、經篩選下載檔與網站建置工具。
- 車種程式、firmware、完整教材、測試紀錄、原始素材及歷史版本仍由
  `NTUB_UGV/` 管理，不因網站引用而移入本 repository。
- 網站不得保存真實憑證、個資、未核准答案、未確認授權素材或本機 UF2。

## 維護方式

```powershell
python -B tools/build_case_topic_pages.py --check
python -B tools/build_case_topic_pages.py
python -B tools/build_case_topic_pages.py --check
python -B tools/verify_site.py
```

- 產生器只重建 01-08 主題頁並同步核准下載副本。
- `index.html`、`downloads.html`、`firmware.html`、`setup.html` 與
  `topic-09-tracked-car-info-flow.html` 為人工維護頁面。
- 發布前另行檢查 credentials、個資、授權、檔案大小與 staged files。
- 靜態與渲染檢查不代表 Pico / Mango 小車或履帶車已通過實機測試。

## 2026-09-18 規則入口與來源路徑檢查

- 新增本專案 `AGENTS.md` 與相同內容的 `CLAUDE.md`，明確記錄來源、產生頁面、
  人工維護頁、驗證與發布邊界。
- 產生器的教材來源已由不存在的 `../robodev/` 改為 `../NTUB_UGV/`。
- `python -B tools/build_case_topic_pages.py --check` 通過：01–08 主題頁與核准
  下載副本均與來源一致。教材相容性驗證報告的下載副本只更新本機函式庫路徑，
  內容由維護中的原始報告複製，沒有改變硬體規格或驗證結論。
- `python -B tools/verify_site.py` 通過：19 個 HTML 頁面、677 個本機引用與錨點、
  26 個 Python 檔，以及 6 個 ZIP/PPTX、4 個 PDF、2 個 7z 通過既有檢查；
  JavaScript 語法與網站檢查亦通過。
- 本次修改限於規則、維護文件、來源路徑與上述報告副本；未改頁面設計，
  未做瀏覽器互動或實機測試，未 commit、push 或發布網站。

## 2026-09-20 網站顯示與首頁整理

- 使用者要求修正檢查發現的手機空白、學習順序說明、韌體救援入口及首頁重複內容。
- 教材區塊直接顯示，移除捲動後才顯示內容的 JavaScript 與 CSS；長區塊不再受
  螢幕高度限制。移除載入時捲回導覽列的動作，調整段落跳轉的頂端距離。
- 首頁保留一份九主題總覽及設定、BootCamp、下載區、Firmware 入口；01–05
  依序學習，06–09 依原有先備能力與需求選讀。保留既有主題名稱與教材內容。
- 手機教材段落限制在畫面寬度內，長網址可換行；程式碼仍保留原始排版並在
  程式區塊內橫向捲動。首頁標籤改為橫向排列並視寬度換行。
- 韌體救援依 Raspberry Pi 官方文件及 `pico-sdk-prebuilts` 說明，改用
  `nuke_universal.uf2` 的官方說明與發行頁入口，說明清除資料及回到 BOOTSEL
  的行為；不保存 UF2。依據與完整檢查紀錄見 `WEB_DESIGN_PROGRESS.md`。
- 本機網站檢查通過：19 個 HTML、649 個本機引用與錨點、26 個 Python，
  JavaScript 語法及既有下載檔檢查通過。01–08 產生頁與核准下載副本仍與來源一致。
- 瀏覽器驗證：390×667、390×844 首頁無隱藏區塊或橫向溢出；1280×900 桌面
  首頁及主題跳轉正常。Firmware 救援段落在桌面與手機可讀；主題 05 手機段落
  與程式碼捲動正常，主題 05 及 BootCamp 複製按鈕回報成功。
- 上述檢查完成時尚未 commit、push 或發布；未測試實體硬體，也未下載或驗證官方 UF2 二進位內容。
- 2026-09-20：使用者隨後明確要求 commit 與 push，本次提交包含網站修正及
  已驗證的專案規則、來源路徑與維護紀錄；公開網站部署結果需於推送後另行確認。

## 整理決策

- 2026-08-28：完整網站 repository 從 `robodev/webdev/` 移至工作區根層的
  `roboweb/`；保留 `.git`、commit 歷史、branch 與 remote。
- 2026-08-28：網站產生器改從同層的 `../robodev/` 讀取 microcar 與
  trackedcar 權威來源。
- 2026-08-28：公開課堂照片只使用人物、螢幕、QR code、存取資訊與教室識別
  內容已不可辨認的版本；原始人物照片與課堂影片不放在公開 repository。
- 2026-08-28：公開 ZIP 不得包含真實 Wi-Fi 名稱或密碼、IDE 工作檔；公開
  PDF/PPTX 先清除個人中繼資料，簡報中的電子郵件不公開。
- 2026-08-28：未被網站引用的舊版簡報 archive 不再公開。授權範圍依
  `README.md` 與 `NOTICE.md`，不把整個 repository 視為單一授權作品。

## Git 狀態

- Branch：`main`
- Remote：`https://github.com/KennethWYLee/microcar.git`
- 2026-08-28：取得使用者明確核准後重寫 `main` 歷史；清理前的 ZIP、PDF、
  PPTX、人物媒體與舊簡報路徑已從先前 commits 移除，已清理版本只在最新
  commit 重新加入。
- 發布後需確認遠端 ref、GitHub Pages、移除檔案 URL 與下載檔 hash。歷史
  重寫不能使曾公開的憑證失效，也不能控制既有 fork 或快取，因此密碼仍需
  另行更換。
