# roboweb - Project Context

> 工作區規則見 `../AGENTS.md`；本檔記錄網站 repository 的來源、發布邊界、
> 維護方式與目前狀態。

- 最後盤點日期：2026-08-28
- 核准名稱：`roboweb`，使用者於 2026-08-28 指定為網站專案資料夾名稱。
- 本機位置：`C:\Users\User\Documents\Lecture materials\roboweb`
- GitHub repository：`https://github.com/KennethWYLee/microcar`
- GitHub Pages：`https://kennethwylee.github.io/microcar/`
- Repository：獨立 Git repository，不再巢狀放在 `robodev/`。

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

## Git 狀態

- Branch：`main`
- Remote：`https://github.com/KennethWYLee/microcar.git`
- 搬移前本機比 `origin/main` 超前 3 個 commits；尚未 push。
