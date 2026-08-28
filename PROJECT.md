# roboweb - Project Context

> 工作區規則見 `../AGENTS.md`；本檔記錄網站 repository 的來源、發布邊界、
> 維護方式與目前狀態。

- 最後盤點日期：2026-08-28
- 核准名稱：`roboweb`，使用者於 2026-08-28 指定為網站專案資料夾名稱。
- 本機位置：`C:\Users\User\Documents\Lecture materials\roboweb`
- GitHub repository：`https://github.com/KennethWYLee/microcar`
- GitHub Pages：`https://kennethwylee.github.io/microcar/`
- Repository：獨立 Git repository，不再巢狀放在 `robodev/`。

## 網站資訊與決策依據

- 網站資訊、內容編排、功能調整與發布歷程主要依據：
  `codex://threads/019d66f5-f174-7ff2-ab98-fa30052e7e0d`。
- 使用者目前的明確指示優先於該 task 的較早紀錄。
- `../robodev/microcar/` 與 `../robodev/trackedcar/` 仍保存程式、教材與硬體
  資料來源；從這些來源選擇哪些內容放上網站時，以上述 Codex task 的網站
  決策為主要依據。
- 若該 task、目前網站檔案與 `robodev` 來源互相衝突，先保留各自版本並回報
  差異，不自行混合不相容的腳位、版本、教材內容或發布範圍。

## 來源與發布邊界

- microcar 權威來源：`../robodev/microcar/`
- trackedcar 權威來源：`../robodev/trackedcar/`
- `roboweb/` 只保存公開網頁、網站資產、經篩選下載檔與網站建置工具。
- 車種程式、firmware、完整教材、測試紀錄、原始素材及歷史版本仍由
  `robodev/` 管理，不因網站引用而移入本 repository。
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
- 2026-08-28：公開工作樹清理 commit `be9a7cb` 已推送至 `origin/main`；GitHub
  Pages 已提供匿名化圖片與清理後 ZIP，原始人物照片與課堂影片 URL 回傳 404。
- 舊 commit 仍保存清理前的 ZIP、文件與人物媒體；若要從 GitHub 歷史移除，
  需在取得明確核准後重寫歷史並 force-push。
