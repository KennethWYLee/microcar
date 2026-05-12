# 履帶小車 V1-V5 微拆解資訊流講義

這份講義用一張總圖建立全貌，再把 App、Wi-Fi、AMB82、UART、X3/RP2040、RTSP、server、gateway 之間的資料傳遞拆成小段。

## 001. V1-V5 的完整資訊流

流程：操作端 -> Wi-Fi -> AMB82 -> UART -> X3/RP2040 -> Motor

個案分析：
- 現象：先看整張地圖，再把每一小段拆開。
- 判讀：本頁只切開「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這一段，不把後面所有問題混在一起。
- 處理：遠端鏈：V5 多了 server 與 gateway，但車內控制鏈仍沿用已驗證的 AMB82 到 X3/RP2040。

名詞解釋：
- 資訊流: 定義：資料從哪裡產生、經過哪裡、最後造成什麼效果。 本案：在本頁對應到「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這段資訊流。
- 鏈路: 定義：一段完整的傳遞路徑。 本案：在本頁對應到「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這段資訊流。


## 002. V1-V5 的主題與遇到的問題

流程：V1 移動 -> V2 影像 -> V3 穩定 -> V4 延遲 -> V5 遠端

個案分析：
- 現象：每一版不是重新開始，而是解決上一版暴露出的問題。
- 判讀：本頁只切開「V1 移動 → V2 影像 → V3 穩定 → V4 延遲 → V5 遠端」這一段，不把後面所有問題混在一起。
- 處理：V3 到 V5 分別處理控制/影像分流、低延遲、跨校園中繼。

名詞解釋：
- 版本: 定義：每一版代表一個工程目標，不是只改名字。 本案：在本頁對應到「V1 移動 → V2 影像 → V3 穩定 → V4 延遲 → V5 遠端」這段資訊流。
- 問題導向: 定義：先描述現象，再用 log 與資訊流找出是哪一段出問題。 本案：在本頁對應到「V1 移動 → V2 影像 → V3 穩定 → V4 延遲 → V5 遠端」這段資訊流。


## 003. 兩條主線：控制與影像

流程：控制線 -> 車子動作 -> 影像線

個案分析：
- 現象：小車不是只有一條網路，它同時有命令與影像。
- 判讀：本頁只切開「控制線 → 車子動作 → 影像線」這一段，不把後面所有問題混在一起。
- 處理：v3 之後的核心想法是：控制先穩，影像按需要再啟動。

名詞解釋：
- 控制線: 定義：讓車子前進、停止、左右轉。 本案：在本頁對應到「控制線 → 車子動作 → 影像線」這段資訊流。
- 影像線: 定義：讓操作者看到畫面。 本案：在本頁對應到「控制線 → 車子動作 → 影像線」這段資訊流。


## 004. V1 總圖：只處理移動

流程：Flutter App -> AMB82 -> X3/RP2040 -> Motor

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「Flutter App → AMB82 → X3/RP2040 → Motor」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UDP: 定義：用來送簡短控制命令。 本案：在本案用來送 FORWARD/STOP，資料小、反應快，但要靠 heartbeat/failsafe 補安全。
- GPIO: 定義：X3/RP2040 控制馬達驅動板的輸出腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。


## 005. 按下按鈕後，App 先改狀態

流程：Button Down -> App State

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「Button Down → App State」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UI state: 定義：App 畫面內部記住的狀態。 本案：在本頁對應到「Button Down → App State」這段資訊流。
- 本機事件: 定義：還沒有經過 Wi-Fi 的動作。 本案：在本頁對應到「Button Down → App State」這段資訊流。


## 006. App 把狀態包成 UDP 封包

流程：App State -> UDP Payload

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「App State → UDP Payload」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- payload: 定義：封包裡真正要送的資料。 本案：在本案通常就是 cmd=FORWARD 這類真正要送的命令內容。
- cmd: 定義：command 的縮寫，代表命令欄位。 本案：在本案是封包中的命令欄位，後面元件會照它決定動作。


## 007. UDP 封包需要 IP 與 port

流程：UDP Payload -> AMB82 Address

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「UDP Payload → AMB82 Address」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- IP: 定義：網路上的地址。 本案：在本案是 AMB82 目前連上 Wi-Fi 後取得的位置，換熱點常會改變。
- port: 定義：同一台設備上不同服務的入口號碼。 本案：在本案 8765 是控制入口，554 是 RTSP 入口。


## 008. AMB82 收到 UDP 後，只做轉接

流程：AMB82 UDP -> UART Text

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「AMB82 UDP → UART Text」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UART: 定義：兩塊板子之間的序列通訊。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。
- newline: 定義：命令結尾，用來分辨一行命令結束。 本案：在本頁對應到「AMB82 UDP → UART Text」這段資訊流。


## 009. X3/RP2040 解析 UART 文字

流程：UART Text -> X3/RP2040 Function

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「UART Text → X3/RP2040 Function」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- parse: 定義：把文字拆解成程式能理解的命令。 本案：在本頁對應到「UART Text → X3/RP2040 Function」這段資訊流。
- function: 定義：程式裡負責做某件事的一段邏輯。 本案：在本頁對應到「UART Text → X3/RP2040 Function」這段資訊流。


## 010. X3/RP2040 用 GPIO 控制馬達驅動板

流程：X3/RP2040 forward() -> Motor Driver

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「X3/RP2040 forward() → Motor Driver」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- GPIO: 定義：微控制器可控制的輸出入腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。
- H-bridge: 定義：常見馬達正反轉控制電路。 本案：在本頁對應到「X3/RP2040 forward() → Motor Driver」這段資訊流。


## 011. STOP 是另一個命令，不是按鈕放開的魔法

流程：STOP Payload -> X3/RP2040 stop()

個案分析：
- 現象：車子會維持上一個方向，因此停止也必須是一個完整送達的命令。
- 判讀：本頁只切開「STOP Payload → X3/RP2040 stop()」這一段，不把後面所有問題混在一起。
- 處理：確認 App log、AMB82 monitor、X3/RP2040 shell 都有 STOP，再談馬達是否真的停。

名詞解釋：
- failsafe: 定義：命令中斷時自動停車的保護機制。 本案：在本案是 X3/RP2040 收不到新命令時自動停車，避免斷線後繼續跑。
- heartbeat: 定義：持續送出的控制心跳。 本案：在本案是 App 反覆送目前方向，讓 Wi-Fi 抖動時控制不中斷。


## 012. 三個 log 對應三段路

流程：App Log -> AMB82 Monitor -> X3/RP2040 Shell

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「App Log → AMB82 Monitor → X3/RP2040 Shell」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- log: 定義：系統留下的執行紀錄。 本案：在本頁對應到「App Log → AMB82 Monitor → X3/RP2040 Shell」這段資訊流。
- 分段除錯: 定義：一次只確認一小段是否正常。 本案：在本頁對應到「App Log → AMB82 Monitor → X3/RP2040 Shell」這段資訊流。


## 013. V2 總圖：加入 RTSP 影像

流程：Camera -> AMB82 Encoder -> RTSP/RTP -> Player

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Camera → AMB82 Encoder → RTSP/RTP → Player」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- RTSP: 定義：建立播放會話的控制協定。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。
- RTP: 定義：實際承載影音資料的協定。 本案：在本案負責把 H264 frame 切成封包送到播放器。


## 014. 播放器先連到 RTSP port 554

流程：VLC / App -> AMB82 RTSP

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「VLC / App → AMB82 RTSP」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- TCP: 定義：可靠連線，RTSP 控制通常走 TCP。 本案：在本案常出現在 RTSP 控制連線；可靠但卡住時可能累積延遲。
- 554: 定義：RTSP 常用 port。 本案：在本頁對應到「VLC / App → AMB82 RTSP」這段資訊流。


## 015. OPTIONS 詢問支援哪些方法

流程：Player -> RTSP Server

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → RTSP Server」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- OPTIONS: 定義：詢問 RTSP server 支援的方法。 本案：在本案是 RTSP 連線初期播放器詢問 AMB82 支援哪些方法。
- handshake: 定義：正式傳輸前的協商。 本案：在本頁對應到「Player → RTSP Server」這段資訊流。


## 016. DESCRIBE 取得 SDP

流程：Player -> SDP

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → SDP」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- SDP: 定義：Session Description Protocol，描述媒體串流。 本案：在本案是 RTSP DESCRIBE 回傳給播放器的串流說明書。
- codec: 定義：影像壓縮格式，例如 H264。 本案：在本案通常是 H264，表示影像如何被壓縮。


## 017. SETUP 決定 RTP 怎麼送

流程：SETUP -> RTP Channel

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「SETUP → RTP Channel」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- UDP: 定義：低延遲但不保證送達。 本案：在本案用來送 FORWARD/STOP，資料小、反應快，但要靠 heartbeat/failsafe 補安全。
- TCP interleaved: 定義：RTP 包在 RTSP TCP 連線裡傳。 本案：在本頁對應到「SETUP → RTP Channel」這段資訊流。


## 018. PLAY 才開始要求影像資料

流程：Player -> AMB82

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → AMB82」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- PLAY: 定義：要求 RTSP server 開始送媒體。 本案：在本案是播放器正式要求 AMB82 開始送影像。
- sf: 定義：送出的 frame 數或相關統計。 本案：在本頁對應到「Player → AMB82」這段資訊流。


## 019. Camera frame 要先進 encoder

流程：Camera Frame -> Encoder

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Camera Frame → Encoder」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- frame: 定義：影像中的一張畫面。 本案：在本案是 camera 產生的一張畫面；沒有 frame，播放器只會黑畫面。
- H264: 定義：常見低頻寬影片壓縮格式。 本案：在本案是 AMB82 把 camera 畫面壓縮後送給播放器的格式。


## 020. sf:0 代表沒有有效影像送出

流程：REQUEST_PLAY -> sf:0

個案分析：
- 現象：VLC 已進入 PLAY，但 monitor 顯示 sf:0，代表會話存在、影像 frame 沒送出。
- 判讀：本頁只切開「REQUEST_PLAY → sf:0」這一段，不把後面所有問題混在一起。
- 處理：下一步不是改播放器，而是檢查 camera frame、encoder 與 getImage 結果。

名詞解釋：
- sf:0: 定義：送出的影像 frame 統計為 0。 本案：在本頁對應到「REQUEST_PLAY → sf:0」這段資訊流。
- 黑畫面: 定義：播放器有連線，但沒有可顯示影像。 本案：在本頁對應到「REQUEST_PLAY → sf:0」這段資訊流。


## 021. keepalive timeout 是會話維持問題

流程：RTSP Session -> Keepalive

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「RTSP Session → Keepalive」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- keepalive: 定義：維持連線活著的訊號。 本案：在本案是維持 RTSP session 不被 server 判定失聯。
- timeout: 定義：等待太久沒有回應。 本案：在本案可能代表 RTSP 會話逾時，或 X3/RP2040 太久沒收到命令而停車。


## 022. HTTP JPEG 用來隔離 camera 問題

流程：Browser -> Camera.getImage()

個案分析：
- 現象：RTSP 黑畫面後，用 snapshot/getImage 直接測 camera，確認問題是否在影像來源。
- 判讀：本頁只切開「Browser → Camera.getImage()」這一段，不把後面所有問題混在一起。
- 處理：觀察是否印出非零 Image len；若卡住，就把懷疑範圍縮到 camera/硬體。

名詞解釋：
- JPEG: 定義：單張壓縮圖片格式。 本案：在本案用 snapshot 測試 camera 是否能產生單張圖片。
- Image len: 定義：抓到的圖片資料長度，非零通常代表有影像。 本案：在本案若為非零，代表 getImage 抓到有效影像資料。


## 023. V3 總圖：控制優先，影像按需啟動

流程：UDP Control -> AMB82 -> X3/RP2040 -> RTSP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「UDP Control → AMB82 → X3/RP2040 → RTSP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- on demand: 定義：需要時才啟動。 本案：在本頁對應到「UDP Control → AMB82 → X3/RP2040 → RTSP」這段資訊流。
- decouple: 定義：把兩條鏈路的故障影響切開。 本案：在本頁對應到「UDP Control → AMB82 → X3/RP2040 → RTSP」這段資訊流。


## 024. UDP ready 只代表控制入口建立

流程：Connect UDP -> AMB82 UDP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「Connect UDP → AMB82 UDP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- UDP ready: 定義：App 已準備往指定 IP:port 送命令。 本案：在本頁對應到「Connect UDP → AMB82 UDP」這段資訊流。
- boot safety: 定義：開機先停車。 本案：在本頁對應到「Connect UDP → AMB82 UDP」這段資訊流。


## 025. Start Embedded 送的是 START_RTSP

流程：Start Embedded -> START_RTSP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「Start Embedded → START_RTSP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- START_RTSP: 定義：要求 AMB82 啟動 RTSP pipeline。 本案：在本頁對應到「Start Embedded → START_RTSP」這段資訊流。
- embedded: 定義：App 內嵌播放器。 本案：在本頁對應到「Start Embedded → START_RTSP」這段資訊流。


## 026. RTSP start-once 避免重複啟動

流程：AMB82 -> RTSP ON

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「AMB82 → RTSP ON」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- pipeline: 定義：影像從 camera 到 encoder 到網路的處理流程。 本案：在本頁對應到「AMB82 → RTSP ON」這段資訊流。
- idempotent: 定義：重複執行不改變狀態。 本案：在本頁對應到「AMB82 → RTSP ON」這段資訊流。


## 027. App 用 heartbeat 持續送目前方向

流程：App Direction -> Heartbeat

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「App Direction → Heartbeat」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- heartbeat: 定義：固定間隔送出的控制訊號。 本案：在本案是 App 反覆送目前方向，讓 Wi-Fi 抖動時控制不中斷。
- lag tolerant: 定義：容忍短暫網路延遲。 本案：在本頁對應到「App Direction → Heartbeat」這段資訊流。


## 028. X3/RP2040 failsafe 負責最後一道安全

流程：X3/RP2040 -> Auto Stop

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「X3/RP2040 → Auto Stop」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- timeout: 定義：超過指定時間沒有收到新命令。 本案：在本案可能代表 RTSP 會話逾時，或 X3/RP2040 太久沒收到命令而停車。
- 安全邊界: 定義：順暢與防失控之間的取捨。 本案：在本頁對應到「X3/RP2040 → Auto Stop」這段資訊流。


## 029. Thonny 會改變 X3/RP2040 的執行狀態

流程：Thonny -> X3/RP2040 main.py

個案分析：
- 現象：接 Thonny 時車能動，拔線後不穩或不動，表示 X3/RP2040 開機自動執行需要另外確認。
- 判讀：本頁只切開「Thonny → X3/RP2040 main.py」這一段，不把後面所有問題混在一起。
- 處理：用 os.listdir() 確認 boot.py/main.py 在 X3/RP2040 內，再測獨立供電開機。

名詞解釋：
- REPL: 定義：MicroPython 互動命令列。 本案：在本案是 Thonny 與 X3/RP2040 互動測試的命令列。
- boot.py: 定義：X3/RP2040 開機時先執行的檔案。 本案：在本案確保 X3/RP2040 拔線後能自動執行 main.py。


## 030. V4A 總圖：穩定優先，但影像有延遲

流程：Power Bank -> UDP Control -> RTSP -> Delay

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Power Bank → UDP Control → RTSP → Delay」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- latency: 定義：從事件發生到畫面看到的時間差。 本案：在本案指車子已經動了，但畫面幾秒後才反映出來。
- bitrate: 定義：每秒傳輸的影像資料量。 本案：在本案代表 RTSP 每秒資料量，太高會增加 Wi-Fi 與播放器壓力。


## 031. 供電不穩會被誤認為網路問題

流程：Motor / AMB82 -> Wi-Fi / RTSP

個案分析：
- 現象：接電腦 USB 時車子不穩，改用行動電源後控制變順，顯示供電會影響通訊。
- 判讀：本頁只切開「Motor / AMB82 → Wi-Fi / RTSP」這一段，不把後面所有問題混在一起。
- 處理：測試時把 AMB82 供電與馬達負載分開觀察，不要把電源問題誤判為網路問題。

名詞解釋：
- 電壓降: 定義：負載增加時電壓短暫下降。 本案：在本頁對應到「Motor / AMB82 → Wi-Fi / RTSP」這段資訊流。
- 供電隔離: 定義：讓 AMB82 與馬達電力互相干擾較少。 本案：在本頁對應到「Motor / AMB82 → Wi-Fi / RTSP」這段資訊流。


## 032. RTSP buffer 讓畫面變穩但變慢

流程：RTP Packets -> Player Buffer

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「RTP Packets → Player Buffer」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- buffer: 定義：播放器暫存資料的空間。 本案：在本案讓影像較穩，但也會讓畫面晚幾秒。
- jitter: 定義：封包抵達時間忽快忽慢。 本案：在本案是封包有時快、有時慢，會讓播放器需要更多 buffer。


## 033. FPS 與 bitrate 會影響延遲

流程：15 fps / 1 Mbps -> Wi-Fi Load

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「15 fps / 1 Mbps → Wi-Fi Load」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- FPS: 定義：每秒幾張影像。 本案：在本案用來取捨畫面流暢與低延遲，例如 V4B 降到 10fps。
- Mbps: 定義：每秒多少百萬位元資料。 本案：在本頁對應到「15 fps / 1 Mbps → Wi-Fi Load」這段資訊流。


## 034. 手機熱點會讓延遲變動

流程：Phone Hotspot -> Ping / Delay

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Phone Hotspot → Ping / Delay」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- ping: 定義：測量來回延遲的工具。 本案：在本頁對應到「Phone Hotspot → Ping / Delay」這段資訊流。
- packet loss: 定義：封包遺失。 本案：在本案是 Wi-Fi 或熱點不穩時封包消失，影像比控制更容易受影響。


## 035. V4B 總圖：低延遲優先

流程：RTSP -> Bitrate -> Player -> Driver

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「RTSP → Bitrate → Player → Driver」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- low latency: 定義：降低操作到畫面回應的時間。 本案：在本頁對應到「RTSP → Bitrate → Player → Driver」這段資訊流。
- tradeoff: 定義：用某些犧牲換取另一個目標。 本案：在本頁對應到「RTSP → Bitrate → Player → Driver」這段資訊流。


## 036. Scan AMB82 也是一段資訊流

流程：App Scan -> UDP Probe -> AMB82

個案分析：
- 現象：按 Scan AMB82 後 Flutter 視窗無回應，問題點轉向 App 搜尋流程本身。
- 判讀：本頁只切開「App Scan → UDP Probe → AMB82」這一段，不把後面所有問題混在一起。
- 處理：先用手動 IP 或優先檢查目前 IP，避免全網段掃描把 UI thread 卡住。

名詞解釋：
- /24: 定義：一個常見子網範圍，約 254 個可用地址。 本案：在本頁對應到「App Scan → UDP Probe → AMB82」這段資訊流。
- probe: 定義：試探某個 IP 是否有服務回應。 本案：在本頁對應到「App Scan → UDP Probe → AMB82」這段資訊流。


## 037. UI thread 卡住，畫面就沒有回應

流程：many futures -> UI thread

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「many futures → UI thread」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- future: 定義：未來會完成的非同步工作。 本案：在本頁對應到「many futures → UI thread」這段資訊流。
- UI thread: 定義：負責畫面反應的執行緒。 本案：在本頁對應到「many futures → UI thread」這段資訊流。


## 038. 低延遲不是只改 FPS

流程：Camera Encode -> Network -> Player Cache

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Camera Encode → Network → Player Cache」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- cache: 定義：播放器暫存資料。 本案：在本頁對應到「Camera Encode → Network → Player Cache」這段資訊流。
- end-to-end: 定義：從 camera 到人眼看到的完整路徑。 本案：在本頁對應到「Camera Encode → Network → Player Cache」這段資訊流。


## 039. V4A 與 V4B 的選擇

流程：V4A -> V4B

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「V4A → V4B」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- 穩定性: 定義：系統長時間不出錯的能力。 本案：在本頁對應到「V4A → V4B」這段資訊流。
- 延遲: 定義：看到畫面落後現場多少時間。 本案：在本頁對應到「V4A → V4B」這段資訊流。


## 040. V5 總圖：跨校園需要中繼

流程：Lab Computer -> Server -> Car Gateway -> AMB82/X3/RP2040

個案分析：
- 現象：小車離開同一個 LAN 後，lab 電腦無法假設可以直接打到車上的 IP。
- 判讀：本頁只切開「Lab Computer → Server → Car Gateway → AMB82/X3/RP2040」這一段，不把後面所有問題混在一起。
- 處理：讓車上 gateway 主動連 server，再由 server 轉發控制與影像資料。

名詞解釋：
- relay: 定義：中繼轉送。 本案：在 V5 是 server 把 lab 的命令或車上的影像轉送給另一端。
- gateway: 定義：車上負責對外連線與對內轉接的設備。 本案：在 V5 是車上的手機/電腦，負責外部網路和車內 AMB82 的橋接。


## 041. 同一個 LAN 才容易直接連

流程：Computer -> AMB82

個案分析：
- 現象：V1-V4 大多建立在同一個 Wi-Fi 網段。
- 判讀：本頁只切開「Computer → AMB82」這一段，不把後面所有問題混在一起。
- 處理：跨校園時，這個條件通常不成立。

名詞解釋：
- LAN: 定義：同一區域網路。 本案：在本頁對應到「Computer → AMB82」這段資訊流。
- subnet: 定義：同一段 IP 網路範圍。 本案：在本頁對應到「Computer → AMB82」這段資訊流。


## 042. NAT 會擋住外部主動連入

流程：Public Internet -> Phone NAT -> Car

個案分析：
- 現象：小車離開同一個 LAN 後，lab 電腦無法假設可以直接打到車上的 IP。
- 判讀：本頁只切開「Public Internet → Phone NAT → Car」這一段，不把後面所有問題混在一起。
- 處理：讓車上 gateway 主動連 server，再由 server 轉發控制與影像資料。

名詞解釋：
- NAT: 定義：內外網地址轉換。 本案：在 V5 會讓外部電腦難以直接連進車上的設備，因此需要中繼架構。
- public IP: 定義：外部網路可以直接看到的地址。 本案：在本頁對應到「Public Internet → Phone NAT → Car」這段資訊流。


## 043. 控制命令先到 server

流程：Lab App -> Server

個案分析：
- 現象：Lab 不直接找車，而是把命令交給固定入口。
- 判讀：本頁只切開「Lab App → Server」這一段，不把後面所有問題混在一起。
- 處理：命令格式仍可保持簡短，例如 direction=FORWARD。

名詞解釋：
- token: 定義：操作端與車端的通行證。 本案：在 V5 用來限制誰可以控制車，避免任何人都能送命令。
- domain: 定義：例如 car.ntub.edu.tw 這類固定名稱。 本案：在本頁對應到「Lab App → Server」這段資訊流。


## 044. 車上 gateway 保持長連線

流程：Gateway -> Server

個案分析：
- 現象：車端主動連 server，避開 NAT 的限制。
- 判讀：本頁只切開「Gateway → Server」這一段，不把後面所有問題混在一起。
- 處理：這比讓外部直接連進車上的 AMB82 更可行。

名詞解釋：
- WebSocket: 定義：適合雙向長連線。 本案：在 V5 可讓車上 gateway 與 server 長時間保持雙向連線。
- MQTT: 定義：用 topic 發布與訂閱訊息。 本案：在 V5 可用 topic 發送控制命令與回報 telemetry。


## 045. gateway 再轉回 AMB82 UDP

流程：Gateway -> AMB82 -> X3/RP2040

個案分析：
- 現象：車外路徑改了，車內路徑不一定要改。
- 判讀：本頁只切開「Gateway → AMB82 → X3/RP2040」這一段，不把後面所有問題混在一起。
- 處理：gateway 負責把遠端命令翻成 AMB82 已經會收的 UDP。

名詞解釋：
- 重用: 定義：保留已驗證的模組。 本案：在本頁對應到「Gateway → AMB82 → X3/RP2040」這段資訊流。
- 車內路徑: 定義：Gateway/AMB82/X3/RP2040 之間的短距離控制鏈。 本案：在本頁對應到「Gateway → AMB82 → X3/RP2040」這段資訊流。


## 046. ACK 與 telemetry 讓遠端知道車還活著

流程：Gateway -> Lab App

個案分析：
- 現象：遠端操控不能只送命令，也要知道車端狀態。
- 判讀：本頁只切開「Gateway → Lab App」這一段，不把後面所有問題混在一起。
- 處理：沒有回報時，操作者不知道是車沒收到還是畫面只是延遲。

名詞解釋：
- ACK: 定義：收到命令的確認訊息。 本案：在本案用來確認某段命令已收到，但不一定代表馬達已動。
- telemetry: 定義：設備狀態回報。 本案：在本案可回報電量、延遲、Wi-Fi 品質，協助遠端判斷狀態。


## 047. 影像中繼比控制中繼更重

流程：AMB82 RTSP -> Gateway -> Server

個案分析：
- 現象：控制命令很小，影像資料很大。
- 判讀：本頁只切開「AMB82 RTSP → Gateway → Server」這一段，不把後面所有問題混在一起。
- 處理：server 端可以再轉成適合遠端播放的格式。

名詞解釋：
- 轉碼: 定義：把影像轉成另一種格式或參數。 本案：在本頁對應到「AMB82 RTSP → Gateway → Server」這段資訊流。
- uplink: 定義：車端往 server 上傳的網路方向。 本案：在本頁對應到「AMB82 RTSP → Gateway → Server」這段資訊流。


## 048. WebRTC 通常放在 gateway 或 server

流程：AMB82 -> Gateway / Server -> Browser/App

個案分析：
- 現象：不是寫在 X3/RP2040，也通常不是直接寫在 AMB82。
- 判讀：本頁只切開「AMB82 → Gateway / Server → Browser/App」這一段，不把後面所有問題混在一起。
- 處理：X3/RP2040 只負責馬達控制，不適合處理影像協定。

名詞解釋：
- WebRTC: 定義：低延遲影音通訊技術。 本案：在本頁對應到「AMB82 → Gateway / Server → Browser/App」這段資訊流。
- bridge: 定義：把一種協定轉接到另一種協定。 本案：在本頁對應到「AMB82 → Gateway / Server → Browser/App」這段資訊流。


## 049. server 申請需求

流程：Server -> Firewall

個案分析：
- 現象：要跨校園，server 需要被 lab 與車端都連得到。
- 判讀：本頁只切開「Server → Firewall」這一段，不把後面所有問題混在一起。
- 處理：若要轉發影像，還要評估頻寬、CPU、儲存與資安。

名詞解釋：
- DNS: 定義：把名稱轉成 IP。 本案：在 V5 讓 lab 與 gateway 用固定名稱找到 server，不必記 IP。
- firewall: 定義：限制哪些連線可以進出的規則。 本案：在本頁對應到「Server → Firewall」這段資訊流。


## 050. 同一個 FORWARD 在各版本的路徑

流程：V1-V4 -> V5

個案分析：
- 現象：比較版本時，先看哪一段多了節點。
- 判讀：本頁只切開「V1-V4 → V5」這一段，不把後面所有問題混在一起。
- 處理：新增 server/gateway 後，要多測 ACK 與延遲。

名詞解釋：
- 車外路徑: 定義：Lab 到 server 到車上 gateway。 本案：在本頁對應到「V1-V4 → V5」這段資訊流。
- 車內路徑: 定義：Gateway 到 AMB82 到 X3/RP2040 到馬達。 本案：在本頁對應到「V1-V4 → V5」這段資訊流。


## 051. Ping 只證明 IP 可達，不證明服務可用

流程：ping IP -> Port 554

個案分析：
- 現象：ping 成功與 RTSP 成功是兩件事。
- 判讀：本頁只切開「ping IP → Port 554」這一段，不把後面所有問題混在一起。
- 處理：UDP 8765 不能用 TCP Test-NetConnection 判斷是否開著。

名詞解釋：
- ICMP: 定義：ping 使用的網路診斷協定。 本案：在本頁對應到「ping IP → Port 554」這段資訊流。
- port test: 定義：測某個服務入口是否能連。 本案：在本頁對應到「ping IP → Port 554」這段資訊流。


## 052. COM port 是電腦到板子的本地通道

流程：USB Cable -> COM Port

個案分析：
- 現象：COM port 問題和 Wi-Fi 不是同一件事。
- 判讀：本頁只切開「USB Cable → COM Port」這一段，不把後面所有問題混在一起。
- 處理：PermissionError 通常代表 port 被別的程式佔住。

名詞解釋：
- COM port: 定義：Windows 給序列裝置的編號。 本案：在本案是 Windows 連 X3/RP2040 或 AMB82 monitor 的本地序列入口。
- PermissionError: 定義：程式沒有權限或裝置被占用。 本案：在本頁對應到「USB Cable → COM Port」這段資訊流。


## 053. X3/RP2040 的 boot.py 決定拔線後會不會自動跑

流程：boot.py -> main.py

個案分析：
- 現象：接 Thonny 時車能動，拔線後不穩或不動，表示 X3/RP2040 開機自動執行需要另外確認。
- 判讀：本頁只切開「boot.py → main.py」這一段，不把後面所有問題混在一起。
- 處理：用 os.listdir() 確認 boot.py/main.py 在 X3/RP2040 內，再測獨立供電開機。

名詞解釋：
- main.py: 定義：MicroPython 預設主程式檔名。 本案：在本案是 X3/RP2040 車控程式的主要檔案。
- soft reboot: 定義：MicroPython 重新啟動。 本案：在本頁對應到「boot.py → main.py」這段資訊流。


## 054. Camera.getImage 能區分軟體與硬體問題

流程：Camera.getImage() -> Image len

個案分析：
- 現象：RTSP 黑畫面後，用 snapshot/getImage 直接測 camera，確認問題是否在影像來源。
- 判讀：本頁只切開「Camera.getImage() → Image len」這一段，不把後面所有問題混在一起。
- 處理：觀察是否印出非零 Image len；若卡住，就把懷疑範圍縮到 camera/硬體。

名詞解釋：
- 隔離測試: 定義：拿掉其他因素，只測一段。 本案：在本頁對應到「Camera.getImage() → Image len」這段資訊流。
- hardware suspect: 定義：懷疑硬體或接線。 本案：在本頁對應到「Camera.getImage() → Image len」這段資訊流。


## 055. 四台車的結果其實是可靠度資料

流程：1-2 號車 -> 3-4 號車

個案分析：
- 現象：不是每台板子都能假設狀態一樣。
- 判讀：本頁只切開「1-2 號車 → 3-4 號車」這一段，不把後面所有問題混在一起。
- 處理：課堂上可以把這當成工程排查的真實案例。

名詞解釋：
- 可靠度: 定義：多台設備是否能穩定重現結果。 本案：在本頁對應到「1-2 號車 → 3-4 號車」這段資訊流。
- 最小化測試: 定義：移除不必要功能後再測。 本案：在本頁對應到「1-2 號車 → 3-4 號車」這段資訊流。


## 056. V1-V5 的主線

流程：V1 -> V2 -> V3 -> V4 -> V5

個案分析：
- 現象：每一版都在回答一個新的資訊流問題。
- 判讀：本頁只切開「V1 → V2 → V3 → V4 → V5」這一段，不把後面所有問題混在一起。
- 處理：V5 把同一台小車推向跨網段與遠端控制。

名詞解釋：
- 版本演進: 定義：每一版解決上一版暴露的新問題。 本案：在本頁對應到「V1 → V2 → V3 → V4 → V5」這段資訊流。
- 資訊流思維: 定義：用資料路徑切開問題。 本案：在本頁對應到「V1 → V2 → V3 → V4 → V5」這段資訊流。

