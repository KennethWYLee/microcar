# 網頁設計進度紀錄

最後更新：2026-04-23

## 目前定位

網站已調整為「5 個正式教材主題」：

1. `入門：LED、按鈕與狀態控制`
2. `感測與輸出：蜂鳴器、RGB 與超音波`
3. `小車移動：馬達、速度與控制模組`
4. `無人車：差速、避障、循跡與伺服掃描`
5. `專題化：任務設計、策略比較與成果評量`

`1 hr Boot Camp` 仍保留為快速體驗課支援頁，但不再列為正式主題。

2026-04-23 補充：Boot Camp 已重新放回全站導覽與首頁快速入口，確保使用者能直接找到一小時課程。

## 這一輪完成內容

- 移除公開主線中的舊三個循跡主題：
  - `循跡入門`
  - `循跡進階`
  - `循跡演算法`
- 新增 5 個由 Markdown 產生的正式主題頁：
  - `topic-01-intro.html`
  - `topic-02-sensor-output.html`
  - `topic-03-car-motion.html`
  - `topic-04-autonomous-car.html`
  - `topic-05-project-cases.html`
- 將 `05_專題化_cases.md` 擴充為 14 cases。
- 新增的 4 個 case 來自原循跡演算法內容整理：
  - Case 11：規則式循跡演算法比較
  - Case 12：P 比例循跡控制
  - Case 13：PD 循跡控制與擺動修正
  - Case 14：PID 循跡調參挑戰
- 首頁與下載區改成 5 主題架構。
- Markdown 原始教材同步複製到 `downloads/case-md/`。
- 新增 `tools/build_case_topic_pages.py`，之後可由 Markdown 重建主題頁。

## 視覺與互動設計

- 5 個主題頁沿用現有網站風格：hero、卡片、case map、accordion case list、程式碼區塊。
- 每個 case 都可展開閱讀。
- Markdown 程式碼區塊加入「複製程式」按鈕。
- 下載區同時提供主題頁入口與 Markdown 下載。

## 驗證重點

- 5 份 Markdown case 順序已驗證。
- `05_專題化_cases.md` 目前為 14 cases，code fence 成對。
- 舊的三個循跡 HTML 已移除。
- 首頁、下載區與 5 個新主題頁已改成新架構。
- 首頁新增 Boot Camp 快速體驗課區塊，說明它保留但不併入 5 個正式主題。

## 下一步建議

1. 針對 5 個主題頁補更精準的真實照片或示意圖。
2. 將每個 case 的程式碼抽成可單獨下載的 `.py` 檔。
3. 針對第 5 主題加入調參紀錄表與課堂評量表。
