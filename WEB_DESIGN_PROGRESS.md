# 網頁設計進度紀錄
最後更新：2026-04-11

## 目前定位

網站已從「依身分區分」改成「依主題區分」。

目前公開主線為：
1. `1 hr Boot Camp`
2. `感測器的操控`
3. `循跡入門`
4. `循跡進階`
5. `循跡演算法`

後續主題規劃：
額外模組：`電路板入門`

## 這一輪完成內容

### 1. 網站主結構改成純主題導覽
- 首頁導覽改為：
  - `Boot Camp`
  - `感測器操控`
  - `循跡入門`
  - `下載區`
- 首頁移除教師支援與學生練習的公開主線定位。
- README 與下載區同步改為依主題分類。

### 2. 主題 1：1 hr Boot Camp
- `bootcamp.html` 保留為目前最重要的第一主題頁。
- 主線內容為：
  - `12 個步驟`
  - `完整程式`
  - `Code Walkthrough`
- 學生不必先下載 `.py`，可直接從網站複製程式到 Thonny。
- 12 個步驟已整理成由上到下的單一路徑，搭配對應 GIF。

### 3. 主題 2：感測器的操控
- `sensor-control.html` 已作為第二主題頁上線。
- 主題內容包含：
  - 感測器主題路線
  - RGB 暖身程式
  - 距離感測主程式
  - 主程式重點解讀

### 4. 主題 3：循跡入門
- 新增 `line-following-intro.html` 作為第三主題頁。
- 主題內容包含：
  - 感測器讀值暖身
  - 循跡入門主程式
  - 真實循跡影片
  - 循跡規則重點說明
- 新增：
  - `downloads/line-sensor-read.py`
  - `downloads/line-following-intro.py`
- `script.js` 已接上第三主題的程式頁與頁內複製功能。

### 5. 程式頁與下載區整理
- `code-viewer.html` 改為中性程式頁，不再使用身分導向文案。
- `downloads.html` 目前分成：
  - `主題 1：Boot Camp`
  - `主題 2：感測器操控`
  - `主題 3：循跡入門`
  - `主題 4：循跡進階`
  - `延伸教材`
- 目前網站可直接展示與複製的程式包含：
  - `keyboard-car-control.py`
  - `basic-motor-functions.py`
  - `sensor-rgb-warmup.py`
  - `distance-sensor-rgb.py`
  - `line-sensor-read.py`
  - `line-following-intro.py`
  - `line-error-to-speed.py`
  - `line-following-advanced.py`

### 6. 文件同步
- `README.md` 已改為主題式專案介紹。
- 本進度檔同步更新為主題式網站架構。

### 7. 主題 4：循跡進階
- 新增 `line-following-advanced.html` 作為第四主題頁。
- 主題內容包含：
  - 速度差控制概念
  - 橋接程式
  - 循跡進階主程式
  - PD / PID 與閉迴路控制的專業補充
  - 真實循跡影片
- 新增：
  - `downloads/line-error-to-speed.py`
  - `downloads/line-following-advanced.py`
- `script.js` 已接上第四主題的程式頁與頁內複製功能。

### 8. 主題 5：循跡演算法
- 新增 `line-following-algorithms.html` 作為第五主題頁。
- 主題內容包含：
  - 規則式、P、PD、PID 的比較
  - 各演算法適用情境
  - 可直接打開並複製的程式頁
  - 官方控制理論補充連結
- 新增：
  - `downloads/line-following-p.py`
  - `downloads/line-following-pid.py`
- `script.js` 已接上主題 5 的演算法程式頁。

## 目前保留但降級的內容

- 舊版身分分流頁面目前保留為歷史參考，不再作為公開主線導覽。

## 下一步建議

1. 開始製作 `電路板入門` 主題頁。
2. 補更多真實影片與調參示意圖，讓主題 4、主題 5 更直觀。
3. 規劃一頁專門比較不同車體與感測器配置對演算法的影響。
