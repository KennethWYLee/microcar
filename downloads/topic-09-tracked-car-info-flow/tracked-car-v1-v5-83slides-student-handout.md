# 履帶小車 V1-V5 微拆解資訊流講義

這份講義用一張總圖建立全貌，再把 App、Wi-Fi、AMB82、UART、X3/RP2040、RTSP、WebSocketViewer、server、gateway 之間的資料傳遞拆成小段。

## 001. V1-V5 的完整資訊流

流程：操作端 -> Wi-Fi -> AMB82 -> UART -> X3/RP2040 -> Motor

個案分析：
- 現象：先看整張地圖，再把每一小段拆開。
- 判讀：本頁只切開「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這一段，不把後面所有問題混在一起。
- 處理：遠端鏈：V5 先把影像觀看方式換成 WebSocket，再思考 server 與 gateway。

名詞解釋：
- 資訊流: 定義：資料從哪裡產生、經過哪裡、最後造成什麼效果。 本案：在本頁對應到「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這段資訊流。
- 鏈路: 定義：一段完整的傳遞路徑。 本案：在本頁對應到「操作端 → Wi-Fi → AMB82 → UART → X3/RP2040 → Motor」這段資訊流。


## 002. V1-V5 的主題與遇到的問題

流程：V1 移動 -> V2 影像 -> V3 穩定 -> V4 延遲 -> V5 Future

個案分析：
- 現象：每一版不是重新開始，而是解決上一版暴露出的問題。
- 判讀：本頁只切開「V1 移動 → V2 影像 → V3 穩定 → V4 延遲 → V5 Future」這一段，不把後面所有問題混在一起。
- 處理：V3 到 V5 分別處理控制/影像分流、低延遲、以及 WebSocket 影像路線。

名詞解釋：
- 版本: 定義：每版代表一個工程目標。 本案：V1 到 V5 對應控制、影像、穩定、延遲與 WebSocket future work。
- 問題導向: 定義：先看現象，再看資料流。 本案：先看現象，再沿資料流找出問題卡在哪一段。


## 003. 兩條主線：控制與影像

流程：控制線 -> 車子動作 -> 影像線

個案分析：
- 現象：小車不是只有一條網路，它同時有命令與影像。
- 判讀：本頁只切開「控制線 → 車子動作 → 影像線」這一段，不把後面所有問題混在一起。
- 處理：v3 之後的核心想法是：控制先穩，影像按需要再啟動。

名詞解釋：
- 控制線: 定義：讓車子前進、停止、左右轉。 本案：在本頁對應到「控制線 → 車子動作 → 影像線」這段資訊流。
- 影像線: 定義：讓操作者看到畫面。 本案：在本頁對應到「控制線 → 車子動作 → 影像線」這段資訊流。


## 004. 一個按鈕如何變成車輪動作

流程：手指按下 -> 網路命令 -> 腳位輸出

個案分析：
- 現象：先把整件事想成資料一路換形式。
- 判讀：本頁只切開「手指按下 → 網路命令 → 腳位輸出」這一段，不把後面所有問題混在一起。
- 處理：理解這條路後，後面的 log 才看得懂。

名詞解釋：
- 資訊流: 定義：資料從產生到造成效果的路徑。 本案：在本頁對應到「手指按下 → 網路命令 → 腳位輸出」這段資訊流。
- GPIO: 定義：微控制器控制外部電路的腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。


## 005. IP 像地址：先知道送到哪裡

流程：寄件人 -> 地址 -> 收件人

個案分析：
- 現象：沒有正確 IP，資料會送到錯的地方。
- 判讀：本頁只切開「寄件人 → 地址 → 收件人」這一段，不把後面所有問題混在一起。
- 處理：所以 monitor 印出的 AMB82 IP 是重要線索。

名詞解釋：
- IP: 定義：網路上的地址。 本案：在本案是 AMB82 目前連上 Wi-Fi 後取得的位置，換熱點常會改變。
- SSID: 定義：Wi-Fi 熱點名稱。 本案：在本頁對應到「寄件人 → 地址 → 收件人」這段資訊流。


## 006. port 像門口：同一地址有不同入口

流程：AMB82 IP -> port 8765 -> port 554

個案分析：
- 現象：同一台 AMB82 上，控制與影像入口不同。
- 判讀：本頁只切開「AMB82 IP → port 8765 → port 554」這一段，不把後面所有問題混在一起。
- 處理：測錯 port，就像敲錯門。

名詞解釋：
- port: 定義：同一台設備上不同服務的入口。 本案：在本案 8765 是控制入口，554 是 RTSP 入口。
- RTSP: 定義：建立影像播放會話的協定。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。


## 007. payload 像信件內容

流程：封包外層 -> payload -> 接收端判斷

個案分析：
- 現象：地址對了，內容也要對。
- 判讀：本頁只切開「封包外層 → payload → 接收端判斷」這一段，不把後面所有問題混在一起。
- 處理：同一個入口可以收到 FORWARD、LEFT、STOP 等不同內容。

名詞解釋：
- payload: 定義：封包真正承載的資料。 本案：在本案通常就是 cmd=FORWARD 這類真正要送的命令內容。
- cmd: 定義：命令欄位，代表要做的動作。 本案：在本案是封包中的命令欄位，後面元件會照它決定動作。


## 008. AMB82 像轉運站

流程：Wi-Fi UDP -> AMB82 -> UART Text

個案分析：
- 現象：它收到網路命令，再轉成 X3/RP2040 能懂的形式。
- 判讀：本頁只切開「Wi-Fi UDP → AMB82 → UART Text」這一段，不把後面所有問題混在一起。
- 處理：monitor 印出 X3: LEFT，表示 AMB82 已經完成轉送。

名詞解釋：
- AMB82: 定義：本案中負責 Wi-Fi、camera、RTSP 與轉接命令的板子。 本案：在本頁對應到「Wi-Fi UDP → AMB82 → UART Text」這段資訊流。
- UART: 定義：板子與板子之間的序列通訊。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。


## 009. UART 像兩塊板子的簡訊

流程：AMB82 TX -> UART 線 -> X3/RP2040 RX

個案分析：
- 現象：AMB82 到 X3/RP2040 不再走 Wi-Fi，而是走序列文字。
- 判讀：本頁只切開「AMB82 TX → UART 線 → X3/RP2040 RX」這一段，不把後面所有問題混在一起。
- 處理：若接線 TX/RX 錯，X3/RP2040 就收不到命令。

名詞解釋：
- UART: 定義：序列通訊，一次一段資料依序傳。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。
- baud: 定義：序列通訊的速度設定。 本案：在本頁對應到「AMB82 TX → UART 線 → X3/RP2040 RX」這段資訊流。


## 010. X3/RP2040 像最後的執行員

流程：X3/RP2040 收命令 -> 程式函式 -> 馬達腳位

個案分析：
- 現象：X3/RP2040 不管 RTSP，只管馬達腳位。
- 判讀：本頁只切開「X3/RP2040 收命令 → 程式函式 → 馬達腳位」這一段，不把後面所有問題混在一起。
- 處理：車不動時，X3/RP2040 是否收到命令是很重要的分界點。

名詞解釋：
- function: 定義：程式中負責特定動作的一段邏輯。 本案：在本頁對應到「X3/RP2040 收命令 → 程式函式 → 馬達腳位」這段資訊流。
- GPIO: 定義：X3/RP2040 控制馬達驅動板的輸出腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。


## 011. 影像不是一個命令，而是一串 frame

流程：Camera -> Encoder -> Player

個案分析：
- 現象：影像資料量比 FORWARD 大非常多。
- 判讀：本頁只切開「Camera → Encoder → Player」這一段，不把後面所有問題混在一起。
- 處理：所以控制順不代表影像一定順。

名詞解釋：
- frame: 定義：影像中的一張畫面。 本案：在本案是 camera 產生的一張畫面；沒有 frame，播放器只會黑畫面。
- H264: 定義：常見影片壓縮格式。 本案：在本案是 AMB82 把 camera 畫面壓縮後送給播放器的格式。


## 012. 延遲是很多小等待加起來

流程：Camera -> Wi-Fi -> Player buffer

個案分析：
- 現象：畫面晚幾秒通常不是單一原因。
- 判讀：本頁只切開「Camera → Wi-Fi → Player buffer」這一段，不把後面所有問題混在一起。
- 處理：V4B 的低延遲就是在這些段落一起減壓。

名詞解釋：
- latency: 定義：從現場事件到使用者看到結果的時間差。 本案：在本案指車子已經動了，但畫面幾秒後才反映出來。
- buffer: 定義：播放器先暫存資料再播放。 本案：在本案讓影像較穩，但也會讓畫面晚幾秒。


## 013. log 像路邊監視器

流程：App log -> AMB82 monitor -> X3/RP2040 shell

個案分析：
- 現象：每個 log 只看得到自己那一段。
- 判讀：本頁只切開「App log → AMB82 monitor → X3/RP2040 shell」這一段，不把後面所有問題混在一起。
- 處理：X3/RP2040 shell 有 Received，才代表 X3/RP2040 真的收到。

名詞解釋：
- log: 定義：系統執行時留下的紀錄。 本案：在本案用來確認資訊流走到哪一段。
- 分段除錯: 定義：一次只確認一小段是否正常。 本案：在本頁對應到「App log → AMB82 monitor → X3/RP2040 shell」這段資訊流。


## 014. App 有 Sent，但 AMB82 沒反應

流程：App log -> Wi-Fi / IP -> AMB82 monitor

個案分析：
- 現象：這通常先看 IP、Wi-Fi、port。
- 判讀：本頁只切開「App log → Wi-Fi / IP → AMB82 monitor」這一段，不把後面所有問題混在一起。
- 處理：再確認電腦和小車是否在同一個 Wi-Fi/subnet。

名詞解釋：
- IP: 定義：網路上的地址。 本案：在本案是 AMB82 目前連上 Wi-Fi 後取得的位置，換熱點常會改變。
- subnet: 定義：同一段區域網路範圍。 本案：在本頁對應到「App log → Wi-Fi / IP → AMB82 monitor」這段資訊流。


## 015. AMB82 有 X3:，但 X3/RP2040 沒 Received

流程：AMB82 monitor -> UART 線路 -> X3/RP2040 shell

個案分析：
- 現象：這通常先看 UART 與 X3/RP2040 程式。
- 判讀：本頁只切開「AMB82 monitor → UART 線路 → X3/RP2040 shell」這一段，不把後面所有問題混在一起。
- 處理：也要確認 X3/RP2040 main.py 正在執行。

名詞解釋：
- UART: 定義：AMB82 與 X3/RP2040 之間的文字通道。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。
- GND: 定義：兩塊板子需要共地才能可靠通訊。 本案：在本頁對應到「AMB82 monitor → UART 線路 → X3/RP2040 shell」這段資訊流。


## 016. X3/RP2040 有 Received，但車不動

流程：X3/RP2040 shell -> GPIO -> Motor Driver

個案分析：
- 現象：這時問題已經更靠近馬達端。
- 判讀：本頁只切開「X3/RP2040 shell → GPIO → Motor Driver」這一段，不把後面所有問題混在一起。
- 處理：這就是分段除錯的好處：不要一直回頭改 App。

名詞解釋：
- GPIO: 定義：X3/RP2040 控制馬達驅動板的腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。
- Motor Driver: 定義：把 X3/RP2040 小電流控制轉成馬達需要的電流。 本案：在本頁對應到「X3/RP2040 shell → GPIO → Motor Driver」這段資訊流。


## 017. VLC 連上 RTSP，但畫面黑

流程：VLC -> RTSP Session -> Frame

個案分析：
- 現象：連線成功只代表入口存在。
- 判讀：本頁只切開「VLC → RTSP Session → Frame」這一段，不把後面所有問題混在一起。
- 處理：不要只把問題歸因到 VLC 或 App 播放器。

名詞解釋：
- RTSP: 定義：控制播放會話的協定。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。
- frame: 定義：播放器真正需要顯示的畫面資料。 本案：在本案是 camera 產生的一張畫面；沒有 frame，播放器只會黑畫面。


## 018. REQUEST_PLAY 後看到 sf:0

流程：REQUEST_PLAY -> RTP started -> sf:0

個案分析：
- 現象：VLC 已進入 PLAY，但 monitor 顯示 sf:0，代表會話存在、影像 frame 沒送出。
- 判讀：本頁只切開「REQUEST_PLAY → RTP started → sf:0」這一段，不把後面所有問題混在一起。
- 處理：下一步不是改播放器，而是檢查 camera frame、encoder 與 getImage 結果。

名詞解釋：
- PLAY: 定義：RTSP 中要求開始傳媒體。 本案：在本案是播放器正式要求 AMB82 開始送影像。
- sf:0: 定義：送出的影像 frame 數為 0 的線索。 本案：在本頁對應到「REQUEST_PLAY → RTP started → sf:0」這段資訊流。


## 019. getImage 卡住或 Image len 非零

流程：Camera.getImage() -> Image len

個案分析：
- 現象：這一步用來判斷 camera 是否真的能取圖。
- 判讀：本頁只切開「Camera.getImage() → Image len」這一段，不把後面所有問題混在一起。
- 處理：這也是判斷某些車可能是硬體問題的依據。

名詞解釋：
- JPEG: 定義：單張壓縮圖片格式。 本案：在本案用 snapshot 測試 camera 是否能產生單張圖片。
- Image len: 定義：抓到圖片資料的長度。 本案：在本案若為非零，代表 getImage 抓到有效影像資料。


## 020. 接行動電源後變順

流程：USB 供電 -> AMB82/Wi-Fi -> Power Bank

個案分析：
- 現象：這代表供電也會影響資訊流。
- 判讀：本頁只切開「USB 供電 → AMB82/Wi-Fi → Power Bank」這一段，不把後面所有問題混在一起。
- 處理：這提醒學生：不是所有問題都是程式問題。

名詞解釋：
- 電壓降: 定義：負載變大時電壓短暫下降。 本案：在本頁對應到「USB 供電 → AMB82/Wi-Fi → Power Bank」這段資訊流。
- 供電隔離: 定義：讓不同負載不要互相干擾。 本案：在本頁對應到「USB 供電 → AMB82/Wi-Fi → Power Bank」這段資訊流。


## 021. 同一個 Wi-Fi 不等於一定可連

流程：電腦 -> AMB82 -> port test

個案分析：
- 現象：還要看 IP 範圍與路由。
- 判讀：本頁只切開「電腦 → AMB82 → port test」這一段，不把後面所有問題混在一起。
- 處理：校園網路、手機熱點、電腦熱點的路由規則可能不同。

名詞解釋：
- ping: 定義：測 IP 是否可達的工具。 本案：在本案先確認電腦是否看得到 AMB82。
- port test: 定義：測某個服務入口是否能連。 本案：在本案用來確認 554 或 8765 服務是否可連。


## 022. 跨校園時要多一個中繼角色

流程：Lab -> Server -> Gateway

個案分析：
- 現象：車不在同一個 LAN，直接連線通常會失敗。
- 判讀：本頁只切開「Lab → Server → Gateway」這一段，不把後面所有問題混在一起。
- 處理：server 再把 lab 的命令與車上的影像做中繼。

名詞解釋：
- server: 定義：兩端都能連到的固定入口。 本案：在本頁對應到「Lab → Server → Gateway」這段資訊流。
- gateway: 定義：車上對外與對內轉接的設備。 本案：在 V5 是車上的手機/電腦，負責外部網路和車內 AMB82 的橋接。


## 023. V1 總圖：只處理移動

流程：Flutter App -> AMB82 -> X3/RP2040 -> Motor

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「Flutter App → AMB82 → X3/RP2040 → Motor」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UDP: 定義：用來送簡短控制命令。 本案：在本案用來送 FORWARD/STOP，資料小、反應快，但要靠 heartbeat/failsafe 補安全。
- GPIO: 定義：X3/RP2040 控制馬達驅動板的輸出腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。


## 024. 按下按鈕後，App 先改狀態

流程：Button Down -> App State

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「Button Down → App State」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UI state: 定義：App 畫面內部記住的狀態。 本案：在本頁對應到「Button Down → App State」這段資訊流。
- 本機事件: 定義：還沒有經過 Wi-Fi 的動作。 本案：在本頁對應到「Button Down → App State」這段資訊流。


## 025. App 把狀態包成 UDP 封包

流程：App State -> UDP Payload

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「App State → UDP Payload」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- payload: 定義：封包裡真正要送的資料。 本案：在本案通常就是 cmd=FORWARD 這類真正要送的命令內容。
- cmd: 定義：command 的縮寫，代表命令欄位。 本案：在本案是封包中的命令欄位，後面元件會照它決定動作。


## 026. UDP 封包需要 IP 與 port

流程：UDP Payload -> AMB82 Address

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「UDP Payload → AMB82 Address」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- IP: 定義：網路上的地址。 本案：在本案是 AMB82 目前連上 Wi-Fi 後取得的位置，換熱點常會改變。
- port: 定義：同一台設備上不同服務的入口號碼。 本案：在本案 8765 是控制入口，554 是 RTSP 入口。


## 027. AMB82 收到 UDP 後，只做轉接

流程：AMB82 UDP -> UART Text

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「AMB82 UDP → UART Text」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- UART: 定義：兩塊板子之間的序列通訊。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。
- newline: 定義：命令結尾，用來分辨一行命令結束。 本案：在本頁對應到「AMB82 UDP → UART Text」這段資訊流。


## 028. X3/RP2040 解析 UART 文字

流程：UART Text -> X3/RP2040 Function

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「UART Text → X3/RP2040 Function」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- parse: 定義：把文字拆解成程式能理解的命令。 本案：在本頁對應到「UART Text → X3/RP2040 Function」這段資訊流。
- function: 定義：程式裡負責做某件事的一段邏輯。 本案：在本頁對應到「UART Text → X3/RP2040 Function」這段資訊流。


## 029. X3/RP2040 用 GPIO 控制馬達驅動板

流程：X3/RP2040 forward() -> Motor Driver

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「X3/RP2040 forward() → Motor Driver」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- GPIO: 定義：微控制器可控制的輸出入腳位。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。
- H-bridge: 定義：常見馬達正反轉控制電路。 本案：在本頁對應到「X3/RP2040 forward() → Motor Driver」這段資訊流。


## 030. STOP 是另一個命令，不是按鈕放開的魔法

流程：STOP Payload -> X3/RP2040 stop()

個案分析：
- 現象：車子會維持上一個方向，因此停止也必須是一個完整送達的命令。
- 判讀：本頁只切開「STOP Payload → X3/RP2040 stop()」這一段，不把後面所有問題混在一起。
- 處理：確認 App log、AMB82 monitor、X3/RP2040 shell 都有 STOP，再談馬達是否真的停。

名詞解釋：
- failsafe: 定義：命令中斷時自動停車的保護機制。 本案：在本案是 X3/RP2040 收不到新命令時自動停車，避免斷線後繼續跑。
- heartbeat: 定義：持續送出的控制心跳。 本案：在本案是 App 反覆送目前方向，讓 Wi-Fi 抖動時控制不中斷。


## 031. 三個 log 對應三段路

流程：App Log -> AMB82 Monitor -> X3/RP2040 Shell

個案分析：
- 現象：第一階段只驗證移動控制，目標是讓 FORWARD/STOP 穩定到達 X3/RP2040。
- 判讀：本頁只切開「App Log → AMB82 Monitor → X3/RP2040 Shell」這一段，不把後面所有問題混在一起。
- 處理：用 App log、AMB82 monitor、X3/RP2040 shell 對照，找出斷在哪一段。

名詞解釋：
- log: 定義：系統留下的執行紀錄。 本案：在本案用來確認資訊流走到哪一段。
- 分段除錯: 定義：一次只確認一小段是否正常。 本案：在本頁對應到「App Log → AMB82 Monitor → X3/RP2040 Shell」這段資訊流。


## 032. V2 總圖：加入 RTSP 影像

流程：Camera -> AMB82 Encoder -> RTSP/RTP -> Player

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Camera → AMB82 Encoder → RTSP/RTP → Player」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- RTSP: 定義：建立播放會話的控制協定。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。
- RTP: 定義：實際承載影音資料的協定。 本案：在本案負責把 H264 frame 切成封包送到播放器。


## 033. 播放器先連到 RTSP port 554

流程：VLC / App -> AMB82 RTSP

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「VLC / App → AMB82 RTSP」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- TCP: 定義：可靠連線，RTSP 控制通常走 TCP。 本案：在本案常出現在 RTSP 控制連線；可靠但卡住時可能累積延遲。
- 554: 定義：RTSP 常用 port。 本案：在本頁對應到「VLC / App → AMB82 RTSP」這段資訊流。


## 034. OPTIONS 詢問支援哪些方法

流程：Player -> RTSP Server

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → RTSP Server」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- OPTIONS: 定義：詢問 RTSP server 支援的方法。 本案：在本案是 RTSP 連線初期播放器詢問 AMB82 支援哪些方法。
- handshake: 定義：正式傳輸前的協商。 本案：在本頁對應到「Player → RTSP Server」這段資訊流。


## 035. DESCRIBE 取得 SDP

流程：Player -> SDP

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → SDP」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- SDP: 定義：Session Description Protocol，描述媒體串流。 本案：在本案是 RTSP DESCRIBE 回傳給播放器的串流說明書。
- codec: 定義：影像壓縮格式，例如 H264。 本案：在本案通常是 H264，表示影像如何被壓縮。


## 036. SETUP 決定 RTP 怎麼送

流程：SETUP -> RTP Channel

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「SETUP → RTP Channel」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- UDP: 定義：低延遲但不保證送達。 本案：在本案用來送 FORWARD/STOP，資料小、反應快，但要靠 heartbeat/failsafe 補安全。
- TCP interleaved: 定義：RTP 包在 RTSP TCP 連線裡傳。 本案：在本頁對應到「SETUP → RTP Channel」這段資訊流。


## 037. PLAY 才開始要求影像資料

流程：Player -> AMB82

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Player → AMB82」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- PLAY: 定義：要求 RTSP server 開始送媒體。 本案：在本案是播放器正式要求 AMB82 開始送影像。
- sf: 定義：送出的 frame 數或相關統計。 本案：在本頁對應到「Player → AMB82」這段資訊流。


## 038. Camera frame 要先進 encoder

流程：Camera Frame -> Encoder

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「Camera Frame → Encoder」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- frame: 定義：影像中的一張畫面。 本案：在本案是 camera 產生的一張畫面；沒有 frame，播放器只會黑畫面。
- H264: 定義：常見低頻寬影片壓縮格式。 本案：在本案是 AMB82 把 camera 畫面壓縮後送給播放器的格式。


## 039. sf:0 代表沒有有效影像送出

流程：REQUEST_PLAY -> sf:0

個案分析：
- 現象：VLC 已進入 PLAY，但 monitor 顯示 sf:0，代表會話存在、影像 frame 沒送出。
- 判讀：本頁只切開「REQUEST_PLAY → sf:0」這一段，不把後面所有問題混在一起。
- 處理：下一步不是改播放器，而是檢查 camera frame、encoder 與 getImage 結果。

名詞解釋：
- sf:0: 定義：送出的影像 frame 統計為 0。 本案：在本頁對應到「REQUEST_PLAY → sf:0」這段資訊流。
- 黑畫面: 定義：播放器有連線，但沒有可顯示影像。 本案：在本頁對應到「REQUEST_PLAY → sf:0」這段資訊流。


## 040. keepalive timeout 是會話維持問題

流程：RTSP Session -> Keepalive

個案分析：
- 現象：加入影像後，連線成功不等於有畫面，必須拆 RTSP 控制與 RTP 影像資料。
- 判讀：本頁只切開「RTSP Session → Keepalive」這一段，不把後面所有問題混在一起。
- 處理：依序檢查 OPTIONS、DESCRIBE、SETUP、PLAY，再看 frame 是否真的送出。

名詞解釋：
- keepalive: 定義：維持連線活著的訊號。 本案：在本案是維持 RTSP session 不被 server 判定失聯。
- timeout: 定義：等待太久沒有回應。 本案：在本案可能代表 RTSP 會話逾時，或 X3/RP2040 太久沒收到命令而停車。


## 041. HTTP JPEG 用來隔離 camera 問題

流程：Browser -> Camera.getImage()

個案分析：
- 現象：RTSP 黑畫面後，用 snapshot/getImage 直接測 camera，確認問題是否在影像來源。
- 判讀：本頁只切開「Browser → Camera.getImage()」這一段，不把後面所有問題混在一起。
- 處理：觀察是否印出非零 Image len；若卡住，就把懷疑範圍縮到 camera/硬體。

名詞解釋：
- JPEG: 定義：單張壓縮圖片格式。 本案：在本案用 snapshot 測試 camera 是否能產生單張圖片。
- Image len: 定義：抓到的圖片資料長度，非零通常代表有影像。 本案：在本案若為非零，代表 getImage 抓到有效影像資料。


## 042. V3 總圖：控制優先，影像按需啟動

流程：UDP Control -> AMB82 -> X3/RP2040 -> RTSP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「UDP Control → AMB82 → X3/RP2040 → RTSP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- on demand: 定義：需要時才啟動。 本案：在本頁對應到「UDP Control → AMB82 → X3/RP2040 → RTSP」這段資訊流。
- decouple: 定義：把兩條鏈路的故障影響切開。 本案：在本頁對應到「UDP Control → AMB82 → X3/RP2040 → RTSP」這段資訊流。


## 043. UDP ready 只代表控制入口建立

流程：Connect UDP -> AMB82 UDP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「Connect UDP → AMB82 UDP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- UDP ready: 定義：App 已準備往指定 IP:port 送命令。 本案：在本頁對應到「Connect UDP → AMB82 UDP」這段資訊流。
- boot safety: 定義：開機先停車。 本案：在本頁對應到「Connect UDP → AMB82 UDP」這段資訊流。


## 044. Start Embedded 送的是 START_RTSP

流程：Start Embedded -> START_RTSP

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「Start Embedded → START_RTSP」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- START_RTSP: 定義：要求 AMB82 啟動 RTSP pipeline。 本案：在本頁對應到「Start Embedded → START_RTSP」這段資訊流。
- embedded: 定義：App 內嵌播放器。 本案：在本頁對應到「Start Embedded → START_RTSP」這段資訊流。


## 045. RTSP start-once 避免重複啟動

流程：AMB82 -> RTSP ON

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「AMB82 → RTSP ON」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- pipeline: 定義：影像從 camera 到 encoder 到網路的處理流程。 本案：在本頁對應到「AMB82 → RTSP ON」這段資訊流。
- idempotent: 定義：重複執行不改變狀態。 本案：在本頁對應到「AMB82 → RTSP ON」這段資訊流。


## 046. App 用 heartbeat 持續送目前方向

流程：App Direction -> Heartbeat

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「App Direction → Heartbeat」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- heartbeat: 定義：固定間隔送出的控制訊號。 本案：在本案是 App 反覆送目前方向，讓 Wi-Fi 抖動時控制不中斷。
- lag tolerant: 定義：容忍短暫網路延遲。 本案：在本頁對應到「App Direction → Heartbeat」這段資訊流。


## 047. X3/RP2040 failsafe 負責最後一道安全

流程：X3/RP2040 -> Auto Stop

個案分析：
- 現象：控制和影像綁在一起會互相干擾，所以 V3 改成先保控制，再按需開影像。
- 判讀：本頁只切開「X3/RP2040 → Auto Stop」這一段，不把後面所有問題混在一起。
- 處理：把 UDP movement、START_RTSP、X3/RP2040 failsafe 分開測，避免混在一起判斷。

名詞解釋：
- timeout: 定義：超過指定時間沒有收到新命令。 本案：在本案可能代表 RTSP 會話逾時，或 X3/RP2040 太久沒收到命令而停車。
- 安全邊界: 定義：順暢與防失控之間的取捨。 本案：在本頁對應到「X3/RP2040 → Auto Stop」這段資訊流。


## 048. Thonny 會改變 X3/RP2040 的執行狀態

流程：Thonny -> X3/RP2040 main.py

個案分析：
- 現象：接 Thonny 時車能動，拔線後不穩或不動，表示 X3/RP2040 開機自動執行需要另外確認。
- 判讀：本頁只切開「Thonny → X3/RP2040 main.py」這一段，不把後面所有問題混在一起。
- 處理：用 os.listdir() 確認 boot.py/main.py 在 X3/RP2040 內，再測獨立供電開機。

名詞解釋：
- REPL: 定義：MicroPython 互動命令列。 本案：在本案是 Thonny 與 X3/RP2040 互動測試的命令列。
- boot.py: 定義：X3/RP2040 開機時先執行的檔案。 本案：在本案確保 X3/RP2040 拔線後能自動執行 main.py。


## 049. V4A 總圖：穩定優先，但影像有延遲

流程：Power Bank -> UDP Control -> RTSP -> Delay

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Power Bank → UDP Control → RTSP → Delay」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- latency: 定義：從事件發生到畫面看到的時間差。 本案：在本案指車子已經動了，但畫面幾秒後才反映出來。
- bitrate: 定義：每秒傳輸的影像資料量。 本案：在本案代表 RTSP 每秒資料量，太高會增加 Wi-Fi 與播放器壓力。


## 050. 供電不穩會被誤認為網路問題

流程：Motor / AMB82 -> Wi-Fi / RTSP

個案分析：
- 現象：接電腦 USB 時車子不穩，改用行動電源後控制變順，顯示供電會影響通訊。
- 判讀：本頁只切開「Motor / AMB82 → Wi-Fi / RTSP」這一段，不把後面所有問題混在一起。
- 處理：測試時把 AMB82 供電與馬達負載分開觀察，不要把電源問題誤判為網路問題。

名詞解釋：
- 電壓降: 定義：負載增加時電壓短暫下降。 本案：在本頁對應到「Motor / AMB82 → Wi-Fi / RTSP」這段資訊流。
- 供電隔離: 定義：讓 AMB82 與馬達電力互相干擾較少。 本案：在本頁對應到「Motor / AMB82 → Wi-Fi / RTSP」這段資訊流。


## 051. RTSP buffer 讓畫面變穩但變慢

流程：RTP Packets -> Player Buffer

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「RTP Packets → Player Buffer」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- buffer: 定義：播放器暫存資料的空間。 本案：在本案讓影像較穩，但也會讓畫面晚幾秒。
- jitter: 定義：封包抵達時間忽快忽慢。 本案：在本案是封包有時快、有時慢，會讓播放器需要更多 buffer。


## 052. FPS 與 bitrate 會影響延遲

流程：15 fps / 1 Mbps -> Wi-Fi Load

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「15 fps / 1 Mbps → Wi-Fi Load」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- FPS: 定義：每秒幾張影像。 本案：在本案用來取捨畫面流暢與低延遲，例如 V4B 降到 10fps。
- Mbps: 定義：每秒多少百萬位元資料。 本案：在本頁對應到「15 fps / 1 Mbps → Wi-Fi Load」這段資訊流。


## 053. 手機熱點會讓延遲變動

流程：Phone Hotspot -> Ping / Delay

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Phone Hotspot → Ping / Delay」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- ping: 定義：測量來回延遲的工具。 本案：在本案先確認電腦是否看得到 AMB82。
- packet loss: 定義：封包遺失。 本案：在本案是 Wi-Fi 或熱點不穩時封包消失，影像比控制更容易受影響。


## 054. V4B 總圖：低延遲優先

流程：RTSP -> Bitrate -> Player -> Driver

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「RTSP → Bitrate → Player → Driver」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- low latency: 定義：降低操作到畫面回應的時間。 本案：在本頁對應到「RTSP → Bitrate → Player → Driver」這段資訊流。
- tradeoff: 定義：用某些犧牲換取另一個目標。 本案：在本頁對應到「RTSP → Bitrate → Player → Driver」這段資訊流。


## 055. Scan AMB82 也是一段資訊流

流程：App Scan -> UDP Probe -> AMB82

個案分析：
- 現象：按 Scan AMB82 後 Flutter 視窗無回應，問題點轉向 App 搜尋流程本身。
- 判讀：本頁只切開「App Scan → UDP Probe → AMB82」這一段，不把後面所有問題混在一起。
- 處理：先用手動 IP 或優先檢查目前 IP，避免全網段掃描把 UI thread 卡住。

名詞解釋：
- /24: 定義：一個常見子網範圍，約 254 個可用地址。 本案：在本頁對應到「App Scan → UDP Probe → AMB82」這段資訊流。
- probe: 定義：試探某個 IP 是否有服務回應。 本案：在本頁對應到「App Scan → UDP Probe → AMB82」這段資訊流。


## 056. UI thread 卡住，畫面就沒有回應

流程：many futures -> UI thread

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「many futures → UI thread」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- future: 定義：未來會完成的非同步工作。 本案：在本頁對應到「many futures → UI thread」這段資訊流。
- UI thread: 定義：負責畫面反應的執行緒。 本案：在本頁對應到「many futures → UI thread」這段資訊流。


## 057. 低延遲不是只改 FPS

流程：Camera Encode -> Network -> Player Cache

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「Camera Encode → Network → Player Cache」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- cache: 定義：播放器暫存資料。 本案：在本頁對應到「Camera Encode → Network → Player Cache」這段資訊流。
- end-to-end: 定義：從 camera 到人眼看到的完整路徑。 本案：在本頁對應到「Camera Encode → Network → Player Cache」這段資訊流。


## 058. V4A 與 V4B 的選擇

流程：V4A -> V4B

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「V4A → V4B」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- 穩定性: 定義：系統長時間不出錯的能力。 本案：在本頁對應到「V4A → V4B」這段資訊流。
- 延遲: 定義：看到畫面落後現場多少時間。 本案：在本頁對應到「V4A → V4B」這段資訊流。


## 059. V5 Future Work：影像改走 WebSocket

流程：V4B -> V5 -> Future

個案分析：
- 現象：V5 不是重寫控制鏈，而是把影像從 RTSP player 轉向 WebSocketViewer，作為後續遠端影像的起點。
- 判讀：本頁只切開「V4B → V5 → Future」這一段，不把後面所有問題混在一起。
- 處理：先把 V5 定義成 future work：保留 UDP 控制，單獨驗證 WebSocketViewer 影像路線。

名詞解釋：
- Future Work: 定義：下一階段要探索的方向。 本案：在本案代表下一階段要驗證的方向，不代表已經完成跨校園部署。
- WS Viewer: 定義：AMB82 官方提供的瀏覽器影像頁。 本案：在 V5 指 AMB82 官方 WebSocketViewer，用瀏覽器觀看影像。


## 060. RTSP 像監視器串流

流程：VLC / Player -> AMB82 RTSP -> Buffer

個案分析：
- 現象：RTSP 適合監視器式串流，但播放器 buffer 可能讓畫面穩定卻延遲變長。
- 判讀：本頁只切開「VLC / Player → AMB82 RTSP → Buffer」這一段，不把後面所有問題混在一起。
- 處理：用這頁說明 RTSP 的 session、RTP frame 與 buffer，讓學生理解為何會 lag。

名詞解釋：
- RTSP: 定義：建立與控制影音播放會話。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。
- buffer: 定義：播放器先累積一段資料再播放。 本案：在本案讓影像較穩，但也會讓畫面晚幾秒。


## 061. WebSocket 像一條持續開著的資料管

流程：Browser -> WebSocket -> AMB82

個案分析：
- 現象：WebSocket 讓瀏覽器和 AMB82 保持長連線，較容易做自訂的最新畫面策略。
- 判讀：本頁只切開「Browser → WebSocket → AMB82」這一段，不把後面所有問題混在一起。
- 處理：用 browser 與 AMB82 的長連線解釋 WebSocketViewer，不把它講成 WebRTC。

名詞解釋：
- WebSocket: 定義：瀏覽器與設備之間的雙向長連線。 本案：在 V5 用來讓瀏覽器與 AMB82 或未來 gateway/server 維持長連線。
- HTTP upgrade: 定義：從一般網頁連線升級成 WebSocket。 本案：在 V5 是瀏覽器先用 HTTP 進入，再升級成 WebSocket 長連線。


## 062. 為什麼 WebSocket 較容易處理 lag

流程：Frame #100 -> Frame #110 -> Browser

個案分析：
- 現象：開車時寧可少看幾張，也不要看 8 秒前的畫面；這就是 latest frame wins 的需求。
- 判讀：本頁只切開「Frame #100 → Frame #110 → Browser」這一段，不把後面所有問題混在一起。
- 處理：示範丟舊 frame、看最新 frame 的概念，說明低延遲不等於每張都播放。

名詞解釋：
- latest frame wins: 定義：延遲時丟掉舊畫面，優先顯示最新畫面。 本案：在 V5 future work 中代表延遲時丟舊 frame，優先看最新畫面。
- lag: 定義：畫面落後真實車況的時間。 本案：在本頁對應到「Frame #100 → Frame #110 → Browser」這段資訊流。


## 063. 但 WebSocket 也不是萬能

流程：Wi-Fi jitter -> TCP stream -> Viewer

個案分析：
- 現象：WebSocket 仍跑在 TCP 上，網路很差時可能因前面資料卡住而等待。
- 判讀：本頁只切開「Wi-Fi jitter → TCP stream → Viewer」這一段，不把後面所有問題混在一起。
- 處理：補上限制：WebSocket 可降低播放器複雜度，但網路品質差仍會卡。

名詞解釋：
- TCP: 定義：可靠、有順序的傳輸。 本案：在本案常出現在 RTSP 控制連線；可靠但卡住時可能累積延遲。
- HOL blocking: 定義：前面資料卡住，後面也要排隊。 本案：Head-of-line blocking 的縮寫；在 V5 用來提醒 WebSocket 仍跑在 TCP 上，前面卡住後面也可能等。


## 064. 目前 V5：AMB82 開 WebSocketViewer

流程：Camera -> StreamIO -> WebSocketViewer

個案分析：
- 現象：目前 V5 的實作是 AMB82 用 Camera -> StreamIO -> WebSocketViewer，Flutter 只負責啟動與控車。
- 判讀：本頁只切開「Camera → StreamIO → WebSocketViewer」這一段，不把後面所有問題混在一起。
- 處理：對照 V5 firmware marker 與 START_VIEWER，確認影像是被按需啟動。

名詞解釋：
- StreamIO: 定義：AMB82 內部的影像資料管線。 本案：在 V5 是 AMB82 把 camera stream 接到 WebSocketViewer 的內部管線。
- START cmd: 定義：啟動 WebSocketViewer 的 UDP 命令。 本案：在 V5 是 Flutter 送出的 START_VIEWER 命令，用來啟動 AMB82 WebSocketViewer。


## 065. V5 App 不再內嵌播放器

流程：Flutter App -> Browser -> AMB82

個案分析：
- 現象：V5 把影像交給瀏覽器，降低 Flutter 內嵌播放器與 RTSP cache 的干擾。
- 判讀：本頁只切開「Flutter App → Browser → AMB82」這一段，不把後面所有問題混在一起。
- 處理：讓學生記住：App 控車、Browser 看影像，兩條線分開測。

名詞解釋：
- browser viewer: 定義：用瀏覽器開 AMB82 提供的影像頁。 本案：在 V5 是把影像播放交給瀏覽器，不再由 Flutter 內嵌 RTSP 播放器處理。
- media_kit: 定義：先前 Flutter 內嵌播放器用到的套件。 本案：在 V4 是 Flutter 內嵌播放器相關套件；V5 已把它移出主要影像路徑。


## 066. V5 的控制鏈仍然沿用 V4B

流程：Flutter -> AMB82 -> X3/RP2040

個案分析：
- 現象：V5 改影像路徑，但 FORWARD/STOP 仍走 Flutter -> UDP -> AMB82 -> UART -> X3/RP2040。
- 判讀：本頁只切開「Flutter → AMB82 → X3/RP2040」這一段，不把後面所有問題混在一起。
- 處理：不要重寫已穩定的車內控制鏈，只替換影像觀看路線。

名詞解釋：
- watchdog: 定義：長時間沒收到控制 heartbeat 時自動停車。 本案：在本頁對應到「Flutter → AMB82 → X3/RP2040」這段資訊流。
- failsafe: 定義：斷線或程式卡住時避免車繼續跑的保護。 本案：在本案是 X3/RP2040 收不到新命令時自動停車，避免斷線後繼續跑。


## 067. Future Work：把 WebSocketViewer 接到 server

流程：AMB82 -> Gateway -> Server

個案分析：
- 現象：未來若要跨校園，WebSocketViewer 需要 gateway/server 中繼，不能只靠 lab 直接連車上 IP。
- 判讀：本頁只切開「AMB82 → Gateway → Server」這一段，不把後面所有問題混在一起。
- 處理：下一步才規劃 gateway 主動連 server，再把影像與控制狀態 relay 出去。

名詞解釋：
- gateway: 定義：車上負責對外連線與對內轉接的設備。 本案：在 V5 是車上的手機/電腦，負責外部網路和車內 AMB82 的橋接。
- relay: 定義：把一端資料轉送到另一端。 本案：在 V5 是 server 把 lab 的命令或車上的影像轉送給另一端。


## 068. Future Work：server 需要的能力

流程：Server -> Firewall -> Dashboard

個案分析：
- 現象：未來若要跨校園，WebSocketViewer 需要 gateway/server 中繼，不能只靠 lab 直接連車上 IP。
- 判讀：本頁只切開「Server → Firewall → Dashboard」這一段，不把後面所有問題混在一起。
- 處理：下一步才規劃 gateway 主動連 server，再把影像與控制狀態 relay 出去。

名詞解釋：
- DNS: 定義：把名稱轉成 IP。 本案：在 V5 讓 lab 與 gateway 用固定名稱找到 server，不必記 IP。
- token: 定義：限制誰可以控制車的通行證。 本案：在 V5 用來限制誰可以控制車，避免任何人都能送命令。


## 069. 同一個 FORWARD：目前 V5 與未來遠端版

流程：目前 V5 -> Future Remote

個案分析：
- 現象：目前 V5 沒有 server/gateway；控制仍走 App -> AMB82 -> X3/RP2040，server/gateway 是 future work。
- 判讀：本頁只切開「目前 V5 → Future Remote」這一段，不把後面所有問題混在一起。
- 處理：把目前 V5 與 Future Remote 分開：先驗證車內控制，再把 server/gateway 當下一階段測試。

名詞解釋：
- 車外路徑: 定義：Lab 到 server 到車上 gateway。 本案：在本頁對應到「目前 V5 → Future Remote」這段資訊流。
- 車內路徑: 定義：App 到 AMB82 到 X3/RP2040。 本案：在本頁對應到「目前 V5 → Future Remote」這段資訊流。


## 070. Ping 只證明 IP 可達，不證明服務可用

流程：ping IP -> Port 554

個案分析：
- 現象：ping 成功與 RTSP 成功是兩件事。
- 判讀：本頁只切開「ping IP → Port 554」這一段，不把後面所有問題混在一起。
- 處理：UDP 8765 不能用 TCP Test-NetConnection 判斷是否開著。

名詞解釋：
- ICMP: 定義：ping 使用的網路診斷協定。 本案：在本頁對應到「ping IP → Port 554」這段資訊流。
- port test: 定義：測某個服務入口是否能連。 本案：在本案用來確認 554 或 8765 服務是否可連。


## 071. COM port 是電腦到板子的本地通道

流程：USB Cable -> COM Port

個案分析：
- 現象：COM port 問題和 Wi-Fi 不是同一件事。
- 判讀：本頁只切開「USB Cable → COM Port」這一段，不把後面所有問題混在一起。
- 處理：PermissionError 通常代表 port 被別的程式佔住。

名詞解釋：
- COM port: 定義：Windows 給序列裝置的編號。 本案：在本案是 Windows 連 X3/RP2040 或 AMB82 monitor 的本地序列入口。
- PermissionError: 定義：程式沒有權限或裝置被占用。 本案：在本頁對應到「USB Cable → COM Port」這段資訊流。


## 072. X3/RP2040 的 boot.py 決定拔線後會不會自動跑

流程：boot.py -> main.py

個案分析：
- 現象：接 Thonny 時車能動，拔線後不穩或不動，表示 X3/RP2040 開機自動執行需要另外確認。
- 判讀：本頁只切開「boot.py → main.py」這一段，不把後面所有問題混在一起。
- 處理：用 os.listdir() 確認 boot.py/main.py 在 X3/RP2040 內，再測獨立供電開機。

名詞解釋：
- main.py: 定義：MicroPython 預設主程式檔名。 本案：在本案是 X3/RP2040 車控程式的主要檔案。
- soft reboot: 定義：MicroPython 重新啟動。 本案：在本頁對應到「boot.py → main.py」這段資訊流。


## 073. Camera.getImage 能區分軟體與硬體問題

流程：Camera.getImage() -> Image len

個案分析：
- 現象：RTSP 黑畫面後，用 snapshot/getImage 直接測 camera，確認問題是否在影像來源。
- 判讀：本頁只切開「Camera.getImage() → Image len」這一段，不把後面所有問題混在一起。
- 處理：觀察是否印出非零 Image len；若卡住，就把懷疑範圍縮到 camera/硬體。

名詞解釋：
- 隔離測試: 定義：拿掉其他因素，只測一段。 本案：在本頁對應到「Camera.getImage() → Image len」這段資訊流。
- hardware suspect: 定義：懷疑硬體或接線。 本案：在本頁對應到「Camera.getImage() → Image len」這段資訊流。


## 074. 四台車的結果其實是可靠度資料

流程：1-2 號車 -> 3-4 號車

個案分析：
- 現象：不是每台板子都能假設狀態一樣。
- 判讀：本頁只切開「1-2 號車 → 3-4 號車」這一段，不把後面所有問題混在一起。
- 處理：課堂上可以把這當成工程排查的真實案例。

名詞解釋：
- 可靠度: 定義：多台設備是否能穩定重現結果。 本案：在本頁對應到「1-2 號車 → 3-4 號車」這段資訊流。
- 最小化測試: 定義：移除不必要功能後再測。 本案：在本頁對應到「1-2 號車 → 3-4 號車」這段資訊流。


## 075. V1-V5 的主線

流程：V1 -> V2 -> V3 -> V4 -> V5

個案分析：
- 現象：每一版都在回答一個新的資訊流問題。
- 判讀：本頁只切開「V1 → V2 → V3 → V4 → V5」這一段，不把後面所有問題混在一起。
- 處理：V5 把同一台小車推向跨網段與遠端控制。

名詞解釋：
- 版本演進: 定義：每一版解決上一版暴露的新問題。 本案：在本頁對應到「V1 → V2 → V3 → V4 → V5」這段資訊流。
- 資訊流思維: 定義：用資料路徑切開問題。 本案：在本頁對應到「V1 → V2 → V3 → V4 → V5」這段資訊流。


## 076. 從 App log 看到第一段

流程：Flutter App -> UDP 8765 -> 下一步

個案分析：
- 現象：Sent 代表 App 已經把指令丟出去，不代表車一定會動。
- 判讀：本頁只切開「Flutter App → UDP 8765 → 下一步」這一段，不把後面所有問題混在一起。
- 處理：這時先查 IP、Wi-Fi、UDP port，不要先拆馬達。

名詞解釋：
- log: 定義：程式執行時留下的文字紀錄。 本案：在本案用來確認資訊流走到哪一段。
- UDP: 定義：適合小型控制指令，但不保證每包都到。 本案：在本案用來送 FORWARD/STOP，資料小、反應快，但要靠 heartbeat/failsafe 補安全。


## 077. 從 AMB82 monitor 看到第二段

流程：AMB82 monitor -> UART -> X3/RP2040 shell

個案分析：
- 現象：X3: FORWARD 代表 AMB82 已經收到 UDP，並準備轉給 X3/RP2040。
- 判讀：本頁只切開「AMB82 monitor → UART → X3/RP2040 shell」這一段，不把後面所有問題混在一起。
- 處理：這一頁把網路問題與板子之間的文字傳輸問題分開。

名詞解釋：
- UART: 定義：兩塊板子之間用 TX/RX 傳文字。 本案：在本案是 AMB82 到 X3/RP2040 的車內文字命令線，例如 FORWARD\n。
- REPL: 定義：Thonny 看到 X3/RP2040 回應的互動介面。 本案：在本案是 Thonny 與 X3/RP2040 互動測試的命令列。


## 078. X3/RP2040 有收到，但車不動

流程：X3/RP2040 shell -> GPIO -> Motor Driver

個案分析：
- 現象：這時資訊流已經到 X3/RP2040，下一段要查馬達與供電。
- 判讀：本頁只切開「X3/RP2040 shell → GPIO → Motor Driver」這一段，不把後面所有問題混在一起。
- 處理：這能避免把所有問題都誤判成 Wi-Fi 或 App 問題。

名詞解釋：
- GPIO: 定義：X3/RP2040 控制馬達板的腳位輸出。 本案：在本案是 X3/RP2040 最後控制馬達驅動板的腳位輸出。
- 供電: 定義：馬達負載需要穩定電源，不能只看 USB 有沒有亮。 本案：在本案影響 Wi-Fi、AMB82 與馬達穩定度。


## 079. RTSP 黑畫面要看哪一段

流程：VLC / player -> RTSP server -> frame counter

個案分析：
- 現象：REQUEST_PLAY 代表播放器要求開始播，但不代表已經有 frame。
- 判讀：本頁只切開「VLC / player → RTSP server → frame counter」這一段，不把後面所有問題混在一起。
- 處理：這時要查 camera pipeline，而不是只查 VLC。

名詞解釋：
- RTSP: 定義：播放器控制影像串流的協定。 本案：在本案是播放器向 AMB82 要求開始看影像的控制流程。
- frame: 定義：影像裡的一張畫面。 本案：在本案是 camera 產生的一張畫面；沒有 frame，播放器只會黑畫面。


## 080. Camera.getImage 是影像源頭測試

流程：Camera.getImage -> JPEG buffer -> 判斷

個案分析：
- 現象：RTSP 黑畫面後，用 snapshot/getImage 直接測 camera，確認問題是否在影像來源。
- 判讀：本頁只切開「Camera.getImage → JPEG buffer → 判斷」這一段，不把後面所有問題混在一起。
- 處理：觀察是否印出非零 Image len；若卡住，就把懷疑範圍縮到 camera/硬體。

名詞解釋：
- JPEG: 定義：單張壓縮圖片格式。 本案：在本案用 snapshot 測試 camera 是否能產生單張圖片。
- Image len: 定義：圖片資料長度，非零通常代表有成功取圖。 本案：在本案若為非零，代表 getImage 抓到有效影像資料。


## 081. V4A 與 V4B 為什麼同時存在

流程：V4A -> 取捨 -> V4B

個案分析：
- 現象：車子已能動，接著要處理影像延遲、Wi-Fi 抖動與播放器 buffer。
- 判讀：本頁只切開「V4A → 取捨 → V4B」這一段，不把後面所有問題混在一起。
- 處理：用 FPS、bitrate、player cache、ping/jitter 逐項調整，而不是只改一個參數。

名詞解釋：
- latency: 定義：按下按鈕到看到結果之間的等待時間。 本案：在本案指車子已經動了，但畫面幾秒後才反映出來。
- bitrate: 定義：影像每秒傳輸的資料量。 本案：在本案代表 RTSP 每秒資料量，太高會增加 Wi-Fi 與播放器壓力。


## 082. 用 log 判斷問題在哪一段

流程：App Sent -> AMB82 X3/RP2040 -> X3/RP2040 Received -> RTSP PLAY

個案分析：
- 現象：不要一次猜整台車壞掉，先找資訊流斷在哪裡。
- 判讀：本頁只切開「App Sent → AMB82 X3/RP2040 → X3/RP2040 Received → RTSP PLAY」這一段，不把後面所有問題混在一起。
- 處理：X3/RP2040 有 Received 但車不動：查 GPIO、馬達板、電源與接線。

名詞解釋：
- 斷點: 定義：資訊流停止的位置。 本案：在本案代表資訊流停止的位置。
- 故障排除: 定義：用證據逐段縮小問題範圍。 本案：在本案是用 log 逐段縮小問題範圍。


## 083. 上課現場可以照這個順序測

流程：1. ping -> 2. UDP -> 3. UART -> 4. RTSP

個案分析：
- 現象：每一步只確認一件事，才不會越修越亂。
- 判讀：本頁只切開「1. ping → 2. UDP → 3. UART → 4. RTSP」這一段，不把後面所有問題混在一起。
- 處理：最後再開 RTSP 影像，避免控制問題與影像問題混在一起。

名詞解釋：
- ping: 定義：測試某個 IP 是否可到達。 本案：在本案先確認電腦是否看得到 AMB82。
- port test: 定義：測試某個服務入口是否可連。 本案：在本案用來確認 554 或 8765 服務是否可連。

