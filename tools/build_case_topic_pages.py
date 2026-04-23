from __future__ import annotations

import html
import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIR = (
    REPO.parent
    / "機器人"
    / "主題整理"
    / "01_課程講義與教材"
    / "講義"
    / "教材分類_md_延伸版"
)
DOWNLOAD_MD_DIR = REPO / "downloads" / "case-md"
ROBOT_DIR = SOURCE_DIR.parents[3]
ROBOT_HANDOUT_DIR = ROBOT_DIR / "講義"
ROBOT_WEB_DIR = ROBOT_DIR / "無人車網頁開發"
DOWNLOAD_TOPIC_06_DIR = REPO / "downloads" / "topic-06-bluetooth-car"
DOWNLOAD_TOPIC_08_DIR = REPO / "downloads" / "topic-08-fan-application"
ASSET_VERSION = "20260423-license"


@dataclass(frozen=True)
class Topic:
    source: str
    output: str
    label: str
    title: str
    subtitle: str
    summary: str
    chips: tuple[str, ...]
    accent: str
    image: str


@dataclass(frozen=True)
class StaticTopic:
    output: str
    label: str
    title: str
    subtitle: str
    summary: str
    chips: tuple[str, ...]
    accent: str
    image: str
    download_href: str
    download_label: str


TOPICS: tuple[Topic, ...] = (
    Topic(
        source="01_入門_cases.md",
        output="topic-01-intro.html",
        label="主題 01",
        title="01 入門：LED、按鈕與狀態控制",
        subtitle="從最小硬體控制開始建立程式直覺",
        summary="本主題讓學習者先理解輸出、輸入、判斷與狀態，適合作為 Raspberry Pi Pico 小車課程的起點。",
        chips=("LED", "Button", "State"),
        accent="product-primary",
        image="assets/control-board.png",
    ),
    Topic(
        source="02_感測輸出_cases.md",
        output="topic-02-sensor-output.html",
        label="主題 02",
        title="02 感測與輸出：蜂鳴器、RGB 與超音波",
        subtitle="把感測資料轉成聲光回饋",
        summary="本主題從蜂鳴器與 RGB 輸出延伸到超音波距離感測，讓學生看見程式如何回應環境變化。",
        chips=("Buzzer", "RGB", "Ultrasonic"),
        accent="product-teacher",
        image="assets/ir-sensor.png",
    ),
    Topic(
        source="03_小車移動_cases.md",
        output="topic-03-car-motion.html",
        label="主題 03",
        title="03 小車移動：馬達、速度與控制模組",
        subtitle="讓小車從單顆馬達走到雙輪控制",
        summary="本主題聚焦馬達方向、PWM 速度、左右輪差速與模組化，建立小車可以穩定移動的基礎。",
        chips=("Motor", "PWM", "Drive"),
        accent="product-student",
        image="assets/real-bootcamp-car.jpg",
    ),
    Topic(
        source="04_無人車_cases.md",
        output="topic-04-autonomous-car.html",
        label="主題 04",
        title="04 無人車：差速、避障、循跡與伺服掃描",
        subtitle="把感測器與馬達整合成自走策略",
        summary="本主題把差速控制、避障、循跡與伺服掃描整合成無人車應用，適合銜接較完整的小車任務。",
        chips=("Obstacle", "Line", "Servo"),
        accent="product-advanced",
        image="assets/video-line-following-demo-poster.jpg",
    ),
    Topic(
        source="05_專題化_cases.md",
        output="topic-05-project-cases.html",
        label="主題 05",
        title="05 專題化：任務設計、策略比較與成果評量",
        subtitle="把多個技巧整合成可以展示的作品",
        summary="本主題把前面學到的輸入、輸出、馬達、感測與循跡控制整合成任務挑戰，並加入規則式、P、PD、PID 循跡演算法 cases。",
        chips=("Project", "Strategy", "PID"),
        accent="product-algorithm",
        image="assets/photo-student-work.jpg",
    ),
)


SUPPLEMENT_TOPICS: tuple[StaticTopic, ...] = (
    StaticTopic(
        output="topic-06-bluetooth-car.html",
        label="主題 06",
        title="06 藍芽遙控小車：Flutter App 與 Pico BLE",
        subtitle="把手機 App、藍芽通訊與小車端程式串成一個完整遙控專案",
        summary="本主題是進階遙控單元，建議先完成 03 小車移動，再使用既有 Flutter 介面與 Pico BLE 小車程式完成手機控制。",
        chips=("Flutter", "BLE", "Remote"),
        accent="product-advanced",
        image="assets/topic-06-flutter-app.png",
        download_href="downloads/topic-06-bluetooth-car/main.dart",
        download_label="下載 Flutter main.dart",
    ),
    StaticTopic(
        output="topic-07-board-python.html",
        label="主題 07",
        title="07 電路板教材：Python 控制與腳位導讀",
        subtitle="不拆成基礎單元，而是用原 PDF 建立完整板子導讀與腳位對照",
        summary="本主題依照機器人程式設計實務-Python.pdf 與相容性驗證報告，整理 Raspberry Pi Pico 主板、腳位、輸入輸出與馬達控制的授課導讀。",
        chips=("Pico", "Pinout", "Python"),
        accent="product-primary",
        image="assets/topic-07-python-pdf-page.png",
        download_href="downloads/robot-programming-practice-python.pdf",
        download_label="下載 Python PDF",
    ),
    StaticTopic(
        output="topic-08-fan-application.html",
        label="主題 08",
        title="08 電路板應用：擺頭電扇",
        subtitle="把電路板控制放進真實作品，從機構、電路到智慧控制完整整合",
        summary="本主題是延伸作品單元，使用擺頭電扇-課程簡報整理風扇機構、Pico X2 腳位與 PWM 控制應用，不屬於小車核心必修。",
        chips=("Fan", "Mechanism", "PWM"),
        accent="product-teacher",
        image="assets/fan-assembled.png",
        download_href="downloads/topic-08-fan-application/fan-course-slides.pptx",
        download_label="下載擺頭電扇簡報",
    ),
)


def all_topics() -> tuple[Topic | StaticTopic, ...]:
    return (*TOPICS, *SUPPLEMENT_TOPICS)


MAINLINE_STEPS: tuple[tuple[str, str, str, str], ...] = (
    (
        "00",
        "開始前設定",
        "先讓 Thonny、MicroPython、mango 函式庫與馬達方向全部確認正確。",
        "setup.html",
    ),
    (
        "BootCamp",
        "一小時快速體驗",
        "用完整程式先讓小車前進、後退、左轉、右轉與停止，建立成功經驗。",
        "bootcamp.html",
    ),
    (
        "01",
        "輸出入與狀態",
        "用 LED、按鈕、狀態變數和 Shell 指令建立硬體控制直覺。",
        "topic-01-intro.html",
    ),
    (
        "02",
        "感測與回饋",
        "把蜂鳴器、RGB、超音波與 ADC 讀值轉成可以觀察的聲光反應。",
        "topic-02-sensor-output.html",
    ),
    (
        "03",
        "馬達與校正",
        "確認左右輪、方向、速度差與基本動作，讓小車可以穩定受控。",
        "topic-03-car-motion.html",
    ),
    (
        "04",
        "自走任務",
        "把馬達和感測器整合成避障、循跡、伺服掃描等無人車行為。",
        "topic-04-autonomous-car.html",
    ),
    (
        "05",
        "專題整合",
        "用狀態機、策略比較與循跡演算法完成可以展示與調參的作品。",
        "topic-05-project-cases.html",
    ),
)


TOPIC_CHECKLISTS: dict[str, tuple[str, ...]] = {
    "setup.html": (
        "Thonny 已連上 Raspberry Pi Pico，並可以執行最小測試程式。",
        "mango 資料夾已上傳到 Pico，import 測試不會報錯。",
        "右輪與左輪方向已校正，前進時小車真的往前走。",
        "我知道如果後面程式報錯，要先回來檢查函式庫、腳位與馬達方向。",
    ),
    "topic-01-intro.html": (
        "我能讓 LED 閃爍，並說出 Pin.OUT 的意思。",
        "我能讀取按鈕值，知道按下時是 0 還是 1。",
        "我能用狀態變數切換 LED，而不是只靠 sleep()。",
        "我能在 Thonny Shell 輸入指令並觸發不同動作。",
    ),
    "topic-02-sensor-output.html": (
        "我能讓蜂鳴器、RGB 或 LED 根據程式改變輸出。",
        "我能在 Shell 看到超音波或 ADC 感測數值。",
        "我能把感測數值分成安全、警告、危險等區間。",
        "我能先測單一感測器，再把它接到小車任務。",
    ),
    "topic-03-car-motion.html": (
        "我能分別測試右馬達與左馬達方向。",
        "我能修正左右輪方向，讓前進真的往前走。",
        "我能用速度差做左轉、右轉與原地旋轉。",
        "我能把小車動作整理成 forward()、stop() 等函式。",
    ),
    "topic-04-autonomous-car.html": (
        "我能讓小車用距離感測器判斷是否避障。",
        "我能讀取循跡感測器，判斷黑線在左、中或右。",
        "我能把感測結果轉成馬達動作，而不是只印數字。",
        "我能先降低速度測試，再逐步提高任務難度。",
    ),
    "topic-05-project-cases.html": (
        "我能選一個任務目標，說明需要哪些輸入、輸出與馬達動作。",
        "我能用狀態或模式整理大型程式。",
        "我能比較不同策略或參數造成的小車行為差異。",
        "我能完成一個可以展示、測試與改良的小車作品。",
    ),
    "topic-06-bluetooth-car.html": (
        "我已完成 03 小車移動，知道小車端前後左右如何控制。",
        "我知道 Pico 端需要上傳 blue.py、bot.py、rcbot.py 等檔案。",
        "我知道 App 掃描名稱、服務 UUID、特徵值要和小車端一致。",
        "我能先用 Thonny Shell 確認小車端收到指令，再測手機 App。",
    ),
    "topic-07-board-python.html": (
        "我能用腳位表查出 LED、按鈕、蜂鳴器、馬達與感測器的接腳。",
        "我能判斷一個元件需要 Pin、PWM、ADC、I2C 還是 UART。",
        "我能用 PDF 對照網頁 case，找出程式中的腳位來源。",
        "我能用腳位表作為除錯第一步，而不是只改程式。",
    ),
    "topic-08-fan-application.html": (
        "我知道這是延伸作品，不是小車核心操控必修單元。",
        "我能說明馬達、齒輪、連桿和擺頭動作的關係。",
        "我能把 PWM 調速概念從小車延伸到風扇馬達。",
        "我能從作品需求反推需要哪些輸入、輸出和控制流程。",
    ),
}


FILE_LOCATION_GUIDES: dict[str, dict[str, tuple[str, ...] | str]] = {
    "setup.html": {
        "title": "先分清楚：電腦本機端 vs Pico 板子端",
        "intro": "學生只要記住一件事：下載檔會先在電腦裡，真正要被 Pico import 或開機執行的檔案，才需要用 Thonny 上傳到 Pico。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ setup.html                 ← 先看這一頁",
            "├─ downloads/",
            "│  ├─ mango-import-test.py    ← 複製到 Thonny 測試",
            "│  ├─ motor-calibration.py    ← 複製到 Thonny 校正馬達",
            "│  └─ mango-library.zip       ← 解壓縮後準備上傳",
            "└─ topic-01 到 topic-08        ← 閱讀教材，不會自動跑到 Pico",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/                     ← 必須上傳，給 from mango import ... 使用",
            "│  ├─ __init__.py",
            "│  └─ ...",
            "├─ main.py                    ← 只有要開機自動執行才存這個名字",
            "└─ practice.py                ← 平常練習可用任意檔名",
        ),
        "flow": (
            "先在電腦打開網站與下載區，確認今天要用的程式或 zip。",
            "在 Thonny 左側檔案視窗分清楚 This computer 與 Raspberry Pi Pico。",
            "把 mango 資料夾上傳到 Pico 根目錄；PDF、PPT、Markdown 不需要上傳到 Pico。",
            "練習程式先貼到 Thonny 按 Run，確定成功後再決定是否存到 Pico。",
            "只有希望 Pico 重新插電後自動跑，才把最後版本存成 Pico 上的 main.py。",
        ),
    },
    "downloads.html": {
        "title": "下載檔不是全部都要上傳到 Pico",
        "intro": "下載區的檔案有兩種：教材檔留在電腦閱讀，MicroPython 函式庫或要執行的程式才放到 Pico。",
        "computer_title": "留在電腦本機閱讀或備課",
        "computer_tree": (
            "downloads/",
            "├─ case-md/                   ← Markdown 教材，給老師備課",
            "├─ robot-programming-practice-python.pdf",
            "├─ topic-08-fan-application/fan-course-slides.pptx",
            "└─ topic-06-bluetooth-car/    ← Flutter App 與藍芽專案素材",
        ),
        "pico_title": "需要時才上傳到 Pico",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/                     ← 02-05 常用函式庫",
            "├─ main.py                    ← 最終要自動執行的主程式",
            "├─ motor-calibration.py       ← 可暫存，用完可刪",
            "└─ blue.py / bot.py / moto.py ← 06 藍芽小車需要的 Pico 端檔案",
        ),
        "flow": (
            "先看下載卡片的說明，判斷它是教材、函式庫、還是 Pico 程式。",
            "教材檔留在電腦；函式庫資料夾與 Pico 程式才用 Thonny 上傳。",
            "如果只是從網頁複製程式碼，可以不用先下載 .py 檔，直接貼到 Thonny 測試。",
            "每次遇到 ModuleNotFoundError，先回來確認對應資料夾是否真的在 Pico 上。",
        ),
    },
    "topic-01-intro.html": {
        "title": "01 入門的檔案放置方式",
        "intro": "本章多數 case 是 LED、按鈕與狀態控制，重點是學會在 Thonny 建立新檔、貼上程式、按 Run。基礎 case 通常不需要 mango。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ topic-01-intro.html        ← 主要閱讀頁",
            "└─ downloads/case-md/01_入門_cases.md",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ led_blink.py               ← 練習檔名可自訂",
            "├─ button_test.py             ← 練習檔名可自訂",
            "└─ main.py                    ← 只有要開機自動跑才使用",
        ),
        "flow": (
            "打開本頁 case，複製第一段完整程式。",
            "在 Thonny 按 File > New，貼上程式後先按 Run。",
            "若要存檔，練習時可存到電腦；要放進 Pico 才選 Raspberry Pi Pico。",
            "不要一開始就全部存成 main.py，先確認程式真的會動。",
        ),
    },
    "topic-02-sensor-output.html": {
        "title": "02 感測與輸出的檔案放置方式",
        "intro": "本章會進入蜂鳴器、RGB、超音波與感測讀值；只要程式有寫 from mango import ...，mango 資料夾就必須已經在 Pico 上。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ topic-02-sensor-output.html",
            "├─ downloads/sensor-rgb-warmup.py",
            "├─ downloads/distance-sensor-rgb.py",
            "└─ downloads/case-md/02_感測輸出_cases.md",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/                     ← RGB、超音波常用",
            "├─ sensor_test.py             ← 當天練習程式",
            "└─ main.py                    ← 完成後才改存自動執行",
        ),
        "flow": (
            "先確認 setup.html 的 mango import 測試已通過。",
            "複製本章 case 程式到 Thonny，新檔先直接 Run。",
            "如果程式需要 mango，確認 Pico 根目錄看得到 mango 資料夾。",
            "感測器讀值不穩時，先檢查接線與腳位，再檢查程式。",
        ),
    },
    "topic-03-car-motion.html": {
        "title": "03 小車移動的檔案放置方式",
        "intro": "本章開始真正驅動馬達。馬達校正程式可以留在電腦複製貼上，也可以暫時存到 Pico；但最終控制程式才需要保留為 main.py。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ topic-03-car-motion.html",
            "├─ downloads/motor-calibration.py",
            "├─ downloads/basic-motor-functions.py",
            "└─ downloads/case-md/03_小車移動_cases.md",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/                     ← 若使用 Motor 模組就需要",
            "├─ motor_test.py              ← 馬達測試或校正用",
            "├─ keyboard_car.py            ← 手動控制練習",
            "└─ main.py                    ← 確定方向正確後才存",
        ),
        "flow": (
            "先跑 motor-calibration.py，確認左右輪與前後方向。",
            "方向錯誤時，先修改 RIGHT_SIGN 或 LEFT_SIGN，不要急著改後面所有程式。",
            "複製本章 case 程式到 Thonny，按 Run 觀察小車。",
            "完成穩定前進、後退、轉向後，再進入 04 無人車。",
        ),
    },
    "topic-04-autonomous-car.html": {
        "title": "04 無人車任務的檔案放置方式",
        "intro": "本章把感測器與馬達整合成避障、循跡與伺服掃描。Pico 上需要有 mango，也需要保留當天要執行的主程式。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ topic-04-autonomous-car.html",
            "├─ downloads/line-sensor-read.py",
            "├─ downloads/line-following-intro.py",
            "└─ downloads/case-md/04_無人車_cases.md",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/                     ← 感測器與馬達模組",
            "├─ line_sensor_test.py        ← 先讀循跡感測器",
            "├─ obstacle_car.py            ← 避障練習",
            "└─ main.py                    ← 最終任務版本",
        ),
        "flow": (
            "先單獨測感測器讀值，再接上馬達控制。",
            "避障或循跡不穩時，先回到感測器測試檔，不要直接改整份大程式。",
            "每完成一個任務版本，先另存檔名備份，再決定是否覆蓋 main.py。",
            "完成本章代表小車已經能根據環境做出反應。",
        ),
    },
    "topic-05-project-cases.html": {
        "title": "05 專題化的檔案放置方式",
        "intro": "本章適合把專題版本分成多個檔名保存，例如 base、p、pid、final，避免學生把能跑的版本覆蓋掉。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "microcar/",
            "├─ topic-05-project-cases.html",
            "├─ downloads/line-error-to-speed.py",
            "├─ downloads/line-following-p.py",
            "├─ downloads/line-following-pid.py",
            "└─ downloads/case-md/05_專題化_cases.md",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ mango/",
            "├─ project_base.py            ← 可以跑的基礎版",
            "├─ project_pid.py             ← 調參實驗版",
            "└─ main.py                    ← 最後展示版",
        ),
        "flow": (
            "先複製基礎版，確認能跑再做策略改良。",
            "每次調整演算法前，先保留上一個成功版本。",
            "把參數寫在程式上方，方便比較不同策略。",
            "展示前再把最穩定版本存成 Pico 上的 main.py。",
        ),
    },
    "topic-06-bluetooth-car.html": {
        "title": "06 藍芽遙控小車的檔案放置方式",
        "intro": "這個主題有兩邊：Flutter App 留在電腦或手機端開發，Pico 端只放 BLE 與小車控制需要的 Python 檔案。",
        "computer_title": "電腦本機端 / App 端",
        "computer_tree": (
            "downloads/topic-06-bluetooth-car/",
            "├─ main.dart                  ← Flutter App 主畫面",
            "├─ controler_ble.7z           ← App 專案壓縮檔",
            "└─ flutter-app-preview.png    ← 網頁預覽圖",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ blue.py                    ← BLE 通訊",
            "├─ bot.py                     ← 小車動作",
            "├─ moto.py                    ← 馬達控制",
            "├─ rcbot.py                   ← 主程式",
            "└─ main.py                    ← 若要開機自動啟動，可由 rcbot.py 改名",
        ),
        "flow": (
            "先完成 03 小車移動，確認不靠 App 也能前進、後退與轉向。",
            "再把 Pico 端 BLE Python 檔案上傳到 Pico。",
            "Flutter 專案留在電腦端，不要整包上傳到 Pico。",
            "App 連線失敗時，先用 Thonny Shell 確認 Pico 端程式有啟動。",
        ),
    },
    "topic-07-board-python.html": {
        "title": "07 電路板教材的檔案放置方式",
        "intro": "PDF 是給學生與老師查表用，留在電腦閱讀即可；Pico 上只需要放正在練習的 MicroPython 程式。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "downloads/",
            "└─ robot-programming-practice-python.pdf ← 腳位與電路板導讀",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ pin_test.py                ← 腳位測試",
            "├─ pwm_test.py                ← PWM 測試",
            "└─ main.py                    ← 只有最終作品才需要",
        ),
        "flow": (
            "先在 PDF 找到元件與腳位，再回到網頁看操作範例。",
            "練習程式從 Thonny 新檔開始，先 Run 再存檔。",
            "PDF、圖片與講義不需要上傳到 Pico。",
            "遇到元件不動時，先比對接線、腳位與程式中的 Pin 編號。",
        ),
    },
    "topic-08-fan-application.html": {
        "title": "08 電路板應用的檔案放置方式",
        "intro": "擺頭電扇簡報留在電腦端教學；Pico 上只放控制馬達、伺服或 PWM 的程式。",
        "computer_title": "電腦本機端",
        "computer_tree": (
            "downloads/topic-08-fan-application/",
            "└─ fan-course-slides.pptx     ← 教師授課與作品說明",
        ),
        "pico_title": "Raspberry Pi Pico 端",
        "pico_tree": (
            "Raspberry Pi Pico /",
            "├─ fan_pwm_test.py            ← 先測風扇或馬達速度",
            "├─ servo_scan.py              ← 再測擺頭角度",
            "└─ main.py                    ← 最終擺頭電扇作品",
        ),
        "flow": (
            "先用簡報理解作品結構，不要把 PPT 上傳到 Pico。",
            "先分開測 PWM、馬達與伺服，再整合成完整作品。",
            "每次接線改動後，先跑最小測試檔確認硬體正常。",
            "最後展示版本再存成 main.py。",
        ),
    },
}


CASE_RE = re.compile(r"(?m)^## Case\s+(\d+)：(.+)$")
SUBHEAD_RE = re.compile(r"(?m)^###\s+(.+)$")


def inline_markdown(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"(https?://[^\s<]+)",
        r'<a class="text-link" href="\1" target="_blank" rel="noreferrer">\1</a>',
        escaped,
    )
    return escaped


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [inline_markdown(cell) for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""

    head = rows[0]
    body = rows[1:]
    thead = "".join(f"<th>{cell}</th>" for cell in head)
    tbody = "\n".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in body
    )
    return (
        '<div class="table-wrap"><table class="topic-table">'
        f"<thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>"
    )


def render_fragment(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    table_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False
    code_index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append("<p>" + inline_markdown(" ".join(paragraph)) + "</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("<ul class=\"detail-list\">" + "".join(list_items) + "</ul>")
            list_items = []

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            output.append(render_table(table_lines))
            table_lines = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                code_index += 1
                code_text = "\n".join(code_lines)
                output.append(
                    '<div class="case-code-card">'
                    '<div class="code-toolbar">'
                    f'<span>程式碼 {code_index}</span>'
                    '<button class="button ghost copy-md-code" type="button">複製程式</button>'
                    "</div>"
                    f'<pre class="code-block markdown-code"><code>{html.escape(code_text)}</code></pre>'
                    "</div>"
                )
                in_code = False
                code_lines = []
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue

        if line.startswith("- "):
            flush_paragraph()
            flush_table()
            list_items.append(f"<li>{inline_markdown(line[2:])}</li>")
            continue

        if line.startswith("**") and line.endswith("**"):
            flush_paragraph()
            flush_list()
            flush_table()
            output.append(f"<h4>{inline_markdown(line)}</h4>")
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    flush_table()
    return "\n".join(output)


def split_cases(markdown: str) -> tuple[str, list[dict[str, object]]]:
    matches = list(CASE_RE.finditer(markdown))
    if not matches:
        return markdown, []

    intro = markdown[: matches[0].start()].strip()
    cases: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[match.end() : end].strip()
        sections = []
        subheads = list(SUBHEAD_RE.finditer(body))
        for sub_index, subhead in enumerate(subheads):
            sub_end = subheads[sub_index + 1].start() if sub_index + 1 < len(subheads) else len(body)
            sections.append(
                {
                    "title": subhead.group(1).strip(),
                    "body": body[subhead.end() : sub_end].strip(),
                }
            )
        cases.append(
            {
                "number": int(match.group(1)),
                "title": match.group(2).strip(),
                "sections": sections,
            }
        )
    return intro, cases


def nav_html(active_output: str | None = None) -> str:
    links = [("bootcamp.html", "BootCamp"), ("setup.html", "開始設定")] + [
        (topic.output, topic.title.split("：", 1)[0]) for topic in all_topics()
    ]
    link_html = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if href == active_output else ""}>{label}</a>'
        for href, label in links
    )
    return f"""      <nav class="site-nav" aria-label="主題導覽">
{link_html}
        <a href="downloads.html">下載區</a>
      </nav>"""


def site_notice_html() -> str:
    return """    <aside class="site-notice" aria-label="網站狀態提醒">
      <span class="notice-label">網站建置中</span>
      <span>本網站教材、所有程式碼與操作流程仍在持續驗證。實際上課前，請以教師現場測試與最新版本為準。</span>
    </aside>
"""


def header_html(active_output: str | None = None) -> str:
    return f"""{site_notice_html()}    <header class="site-header">
      <a class="brand" href="index.html">
        <span class="brand-mark">MC</span>
        <span class="brand-copy">
          <strong>Raspberry Pi Pico 小車主題教材</strong>
          <small>Topic-based Microcar Course</small>
        </span>
      </a>
{nav_html(active_output)}
    </header>"""


def footer_html() -> str:
    return """    <footer class="site-footer">
      <div class="license-card">
        <a class="cc-badge" rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant">
          <img src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons BY-NC-SA 4.0 授權標章">
        </a>
        <div>
          <h2>授權與使用聲明</h2>
          <p>
            除另有標示外，本網站文字教材與自製教學圖片採用
            <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant">Creative Commons 姓名標示-非商業性-相同方式分享 4.0 國際授權條款</a>。
          </p>
          <p>
            程式碼、第三方素材、PDF、PPT、商標、外部引用圖片與原始教材檔案，依各自檔案或來源授權為準。教材與程式仍在驗證中，實際上課前請先由教師測試。
          </p>
        </div>
      </div>
    </footer>
"""


def render_case(case: dict[str, object], open_first: bool = False) -> str:
    sections_html = []
    for section in case["sections"]:  # type: ignore[index]
        sections_html.append(
            '<article class="case-section">'
            f'<h3>{html.escape(section["title"])}</h3>'
            f'{render_fragment(section["body"])}'
            "</article>"
        )
    open_attr = " open" if open_first else ""
    number = case["number"]
    title = html.escape(str(case["title"]))
    return f"""        <details class="case-detail"{open_attr} id="case-{number}">
          <summary>
            <span class="download-type">Case {number}</span>
            <strong>{title}</strong>
          </summary>
          <div class="case-body">
{chr(10).join(sections_html)}
          </div>
        </details>"""


def render_mainline_section(
    eyebrow: str = "Microcar Path",
    title: str = "從零到能操控小車的主線",
    intro: str = "如果學生的目標是完整操控小車，建議先走這條主線。06-08 可以在核心能力完成後再作為進階與延伸。",
) -> str:
    cards = []
    for label, step_title, description, href in MAINLINE_STEPS:
        cards.append(
            f"""          <article class="content-card resource-step">
            <span class="zone-badge student">{html.escape(label)}</span>
            <strong>{html.escape(step_title)}</strong>
            <p>{html.escape(description)}</p>
            <a class="button ghost" href="{href}">前往這一步</a>
          </article>"""
        )
    return f"""
      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">{html.escape(eyebrow)}</p>
          <h2>{html.escape(title)}</h2>
          <p>{html.escape(intro)}</p>
        </div>
        <div class="resource-roadmap">
{chr(10).join(cards)}
        </div>
      </section>
"""


def render_preflight_section(topic_output: str) -> str:
    if topic_output in {"topic-01-intro.html", "topic-02-sensor-output.html"}:
        focus = "這一章可以直接從簡單輸出入開始，但若要跑到 RGB、超音波或後續小車任務，仍要先完成函式庫與腳位確認。"
    elif topic_output in {"topic-03-car-motion.html", "topic-04-autonomous-car.html", "topic-05-project-cases.html"}:
        focus = "這一章開始會真的驅動小車。請先確認馬達方向與 mango 函式庫，否則程式看起來正確，小車仍可能反向、原地轉或直接報錯。"
    elif topic_output == "topic-06-bluetooth-car.html":
        focus = "這是進階遙控主題。學生應先完成 03 小車移動，確認小車端五個基本動作都正確，再進入手機 App 與 BLE。"
    elif topic_output == "topic-08-fan-application.html":
        focus = "這是延伸作品主題，不是小車核心操控必修。建議學生先完成 01-05，再把控制概念移植到擺頭電扇。"
    else:
        focus = "這一章可以當成查表與除錯工具，協助學生把腳位、程式與實際板子對起來。"

    if topic_output == "topic-06-bluetooth-car.html":
        second_badge = "進階"
        second_title = "先完成主題 03"
        second_desc = "藍芽 App 只是把按鈕轉成指令。進入本章前，請先確認小車端的前進、後退、左右轉和停止都正確。"
        second_href = "topic-03-car-motion.html"
        second_label = "回主題 03"
    elif topic_output == "topic-07-board-python.html":
        second_badge = "查表"
        second_title = "把 PDF 當除錯地圖"
        second_desc = "遇到元件沒有反應時，先用腳位表確認接線、功能腳位與程式中的 Pin 是否一致。"
        second_href = "downloads/robot-programming-practice-python.pdf"
        second_label = "下載 Python PDF"
    elif topic_output == "topic-08-fan-application.html":
        second_badge = "延伸"
        second_title = "先完成小車核心主線"
        second_desc = "08 是作品延伸，不是小車操控必修。若學生還不會控制小車，請先完成 01-05。"
        second_href = "topic-05-project-cases.html"
        second_label = "回主題 05"
    else:
        second_badge = "校正"
        second_title = "先讓前進真的往前"
        second_desc = "小車程式最常見的問題不是語法，而是左右輪方向相反。進入避障或循跡前，請先跑馬達校正。"
        second_href = "downloads/motor-calibration.py"
        second_label = "下載馬達校正程式"

    return f"""
      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Before You Start</p>
          <h2>開始本主題前先確認</h2>
          <p>{html.escape(focus)}</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">必做</span>
            <h3>先完成開始前設定</h3>
            <p>包含 Thonny 連線、MicroPython 解譯器、mango 函式庫上傳、import 測試與馬達方向校正。</p>
            <a class="button primary" href="setup.html">打開開始設定</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">{html.escape(second_badge)}</span>
            <h3>{html.escape(second_title)}</h3>
            <p>{html.escape(second_desc)}</p>
            <a class="button ghost" href="{second_href}">{html.escape(second_label)}</a>
          </article>
        </div>
      </section>
"""


def render_completion_checklist(output: str) -> str:
    items = TOPIC_CHECKLISTS.get(output)
    if not items:
        return ""
    cards = []
    for index, item in enumerate(items, start=1):
        cards.append(
            f"""          <article class="check-card">
            <span class="zone-badge student">Check {index}</span>
            <h3>完成確認</h3>
            <p>{html.escape(item)}</p>
          </article>"""
        )
    return f"""
      <section id="completion-check" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Completion Check</p>
          <h2>完成這個主題前，學生應該做得到</h2>
          <p>這不是考試，而是讓學生知道自己是否已經準備好進入下一個主題。</p>
        </div>
        <div class="check-grid">
{chr(10).join(cards)}
        </div>
      </section>
"""


def render_file_location_section(page: str) -> str:
    guide = FILE_LOCATION_GUIDES.get(page)
    if not guide:
        return ""

    flow_items = "\n".join(
        f"            <li>{html.escape(step)}</li>"
        for step in guide["flow"]  # type: ignore[index]
    )
    computer_tree = "\n".join(guide["computer_tree"])  # type: ignore[index]
    pico_tree = "\n".join(guide["pico_tree"])  # type: ignore[index]
    return f"""
      <section id="file-location" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">File Location</p>
          <h2>{html.escape(str(guide["title"]))}</h2>
          <p>{html.escape(str(guide["intro"]))}</p>
        </div>
        <div class="file-map-grid">
          <article class="file-tree-card">
            <span class="zone-badge teacher">Computer</span>
            <h3>{html.escape(str(guide["computer_title"]))}</h3>
            <pre class="file-tree"><code>{html.escape(computer_tree)}</code></pre>
          </article>
          <article class="file-tree-card">
            <span class="zone-badge student">Pico</span>
            <h3>{html.escape(str(guide["pico_title"]))}</h3>
            <pre class="file-tree"><code>{html.escape(pico_tree)}</code></pre>
          </article>
        </div>
        <article class="content-card file-flow-card">
          <span class="zone-badge student">Class Flow</span>
          <h3>上課時學生照這樣做</h3>
          <ol class="file-flow-list">
{flow_items}
          </ol>
        </article>
      </section>
"""


def render_topic_page(topic: Topic) -> str:
    markdown = (SOURCE_DIR / topic.source).read_text(encoding="utf-8")
    intro, cases = split_cases(markdown)
    intro_html = render_fragment(re.sub(r"^# .+$", "", intro, count=1, flags=re.M).strip())
    case_cards = "\n".join(
        f"""          <a class="case-index-card" href="#case-{case['number']}">
            <span>Case {case['number']}</span>
            <strong>{html.escape(str(case['title']))}</strong>
          </a>"""
        for case in cases
    )
    cases_html = "\n".join(render_case(case, open_first=i == 0) for i, case in enumerate(cases))
    chips = "\n".join(f"<span>{html.escape(chip)}</span>" for chip in topic.chips)
    topic_order = all_topics()
    next_topic = topic_order[(topic_order.index(topic) + 1) % len(topic_order)]
    prev_topic = topic_order[(topic_order.index(topic) - 1) % len(topic_order)]

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(topic.title)} | Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="{html.escape(topic.summary)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VERSION}">
</head>
<body class="topic-page">
  <div class="page-shell">
{header_html(topic.output)}

    <main>
      <section class="subpage-hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">{html.escape(topic.label)}</p>
          <h1>{html.escape(topic.title)}</h1>
          <p class="hero-text">{html.escape(topic.summary)}</p>
          <div class="chip-list compact">
            {chips}
          </div>
          <div class="action-row">
            <a class="button primary" href="#case-map">查看 Case 地圖</a>
            <a class="button secondary" href="#case-list">開始閱讀 Cases</a>
            <a class="button ghost" href="downloads/case-md/{topic.source}">下載 Markdown</a>
          </div>
        </div>
        <div class="subpage-aside">
          <article class="aside-card">
            <img class="teaching-visual" src="{topic.image}" alt="{html.escape(topic.title)}教材示意圖">
            <p class="visual-note">{html.escape(topic.subtitle)}</p>
          </article>
          <article class="aside-card">
            <span class="zone-badge teacher">Topic Overview</span>
            <h3>本主題包含 {len(cases)} 個 cases</h3>
            <p>每個 case 都依照「主題、分階段教學、完整程式碼、最終成果、應用題與解答」整理，適合逐步教學與自學。</p>
          </article>
        </div>
      </section>

{render_preflight_section(topic.output)}

{render_file_location_section(topic.output)}

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Learning Context</p>
          <h2>這個主題在整門課的位置</h2>
          <p>{html.escape(topic.subtitle)}</p>
        </div>
        <div class="content-card markdown-intro">
{intro_html}
        </div>
      </section>

      <section id="case-map" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Case Map</p>
          <h2>先用地圖看完整學習順序</h2>
          <p>可以依序完成，也可以直接點選需要的 case。</p>
        </div>
        <div class="case-index-grid">
{case_cards}
        </div>
      </section>

      <section id="case-list" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Cases</p>
          <h2>逐步教學內容</h2>
          <p>點開每個 case 後，可以看到完整教學段落與可複製的程式碼。</p>
        </div>
        <div class="case-list">
{cases_html}
        </div>
      </section>

{render_completion_checklist(topic.output)}

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Continue</p>
          <h2>繼續下一個主題</h2>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">上一個</span>
            <h3>{html.escape(prev_topic.title)}</h3>
            <p>{html.escape(prev_topic.summary)}</p>
            <a class="button ghost" href="{prev_topic.output}">打開上一個主題</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">下一個</span>
            <h3>{html.escape(next_topic.title)}</h3>
            <p>{html.escape(next_topic.summary)}</p>
            <a class="button primary" href="{next_topic.output}">打開下一個主題</a>
          </article>
        </div>
      </section>
    </main>
{footer_html()}
  </div>
  <script src="script.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def render_code_card(title: str, code: str, note: str = "") -> str:
    note_html = f"<p>{html.escape(note)}</p>" if note else ""
    return (
        '<article class="case-code-card">'
        '<div class="code-toolbar">'
        f"<span>{html.escape(title)}</span>"
        '<button class="button ghost copy-md-code" type="button">複製程式碼</button>'
        "</div>"
        f'{note_html}<pre class="code-block markdown-code"><code>{html.escape(code.strip())}</code></pre>'
        "</article>"
    )


def render_static_topic_page(topic: StaticTopic, body_html: str) -> str:
    chips = "\n".join(f"<span>{html.escape(chip)}</span>" for chip in topic.chips)
    topic_order = all_topics()
    next_topic = topic_order[(topic_order.index(topic) + 1) % len(topic_order)]
    prev_topic = topic_order[(topic_order.index(topic) - 1) % len(topic_order)]
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(topic.title)} | Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="{html.escape(topic.summary)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VERSION}">
</head>
<body class="topic-page">
  <div class="page-shell">
{header_html(topic.output)}

    <main>
      <section class="subpage-hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">{html.escape(topic.label)}</p>
          <h1>{html.escape(topic.title)}</h1>
          <p class="hero-text">{html.escape(topic.summary)}</p>
          <div class="chip-list compact">
            {chips}
          </div>
          <div class="action-row">
            <a class="button primary" href="#learning-route">查看學習路徑</a>
            <a class="button secondary" href="#classroom-flow">進入教學流程</a>
            <a class="button ghost" href="{topic.download_href}">{html.escape(topic.download_label)}</a>
          </div>
        </div>
        <div class="subpage-aside">
          <article class="aside-card">
            <img class="teaching-visual" src="{topic.image}" alt="{html.escape(topic.title)}教材示意圖">
            <p class="visual-note">{html.escape(topic.subtitle)}</p>
          </article>
          <article class="aside-card">
            <span class="zone-badge teacher">Teaching Focus</span>
            <h3>這一頁是整理後的教學導讀</h3>
            <p>保留原教材檔案下載，同時把上課時需要先說明的概念、操作順序與關鍵程式整理成網頁版。</p>
          </article>
        </div>
      </section>

{render_preflight_section(topic.output)}

{render_file_location_section(topic.output)}

{body_html}

{render_completion_checklist(topic.output)}

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Continue</p>
          <h2>繼續下一個主題</h2>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">上一個</span>
            <h3>{html.escape(prev_topic.title)}</h3>
            <p>{html.escape(prev_topic.summary)}</p>
            <a class="button ghost" href="{prev_topic.output}">打開上一個主題</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">下一個</span>
            <h3>{html.escape(next_topic.title)}</h3>
            <p>{html.escape(next_topic.summary)}</p>
            <a class="button primary" href="{next_topic.output}">打開下一個主題</a>
          </article>
        </div>
      </section>
    </main>
{footer_html()}
  </div>
  <script src="script.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def render_bluetooth_topic_page(topic: StaticTopic) -> str:
    flutter_scan_code = """Future<void> startScan() async {
  await FlutterBluePlus.stopScan();
  await FlutterBluePlus.startScan(
    withNames: ["PicoCar"],
    withServices: [Guid("FFA0"), Guid("FFE0")],
    timeout: const Duration(seconds: 15),
  );
}"""
    pico_ble_code = """while True:
    buf = blue.read()
    if buf:
        data = blue.buf_to_text(buf).strip()

        if data == "1":
            bot.forward()
        elif data == "2":
            bot.backward()
        elif data == "3":
            bot.turn_left()
        elif data == "4":
            bot.turn_right()
        elif data == "0":
            bot.stop()"""
    body_html = f"""
      <section id="learning-route" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Learning Route</p>
          <h2>藍芽遙控小車的完整路徑</h2>
          <p>這個主題不是只看 App 畫面，而是把手機端、藍芽模組與 Pico 小車端程式串起來看。</p>
        </div>
        <div class="resource-roadmap">
          <article class="content-card resource-step">
            <span class="zone-badge student">Step 01</span>
            <strong>確認小車端可以基本移動</strong>
            <p>先回到主題 03，確認前進、後退、左轉、右轉、停止都正確。藍芽只是把手機按鈕變成指令，不會修正馬達方向問題。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge student">Step 02</span>
            <strong>上傳 Pico BLE 小車端檔案</strong>
            <p>標準版至少需要 <code>blue.py</code>、<code>bot.py</code>、<code>rcbot.py</code>。先讓 Pico 端可以讀取 BLE UART。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge teacher">Step 03</span>
            <strong>Flutter App 搜尋 PicoCar</strong>
            <p>App 掃描名稱為 <code>PicoCar</code> 的藍芽裝置，並尋找 <code>FFA0</code> 服務與 <code>FFA1</code> 可寫入特徵值。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge teacher">Step 04</span>
            <strong>指令對應馬達動作</strong>
            <p><code>1</code> 前進、<code>2</code> 後退、<code>3</code> 左轉、<code>4</code> 右轉、<code>0</code> 停止；變速版再加入速度指令。</p>
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Practice Order</p>
          <h2>學生自學時請照這個順序做</h2>
          <p>藍芽主題牽涉手機端和小車端，請先把每一層分開測通，再把它們接起來。</p>
        </div>
        <div class="resource-roadmap">
          <article class="content-card resource-step"><span class="zone-badge student">01</span><strong>先測小車端動作</strong><p>用 BootCamp 或主題 03 確認小車能正確做五個基本動作。</p><a class="button ghost" href="topic-03-car-motion.html">回主題 03</a></article>
          <article class="content-card resource-step"><span class="zone-badge student">02</span><strong>上傳標準版 Pico 檔案</strong><p>把標準版資料夾中的 <code>blue.py</code>、<code>bot.py</code>、<code>rcbot.py</code> 上傳到 Pico。</p><a class="button ghost" href="downloads/topic-06-bluetooth-car/controler_ble.7z">下載標準版壓縮檔</a></article>
          <article class="content-card resource-step"><span class="zone-badge teacher">03</span><strong>確認 BLE 名稱與 UUID</strong><p>App 端搜尋 <code>PicoCar</code>，服務與特徵值需和 Pico 端設定一致。</p><a class="button ghost" href="downloads/topic-06-bluetooth-car/main.dart">下載 Flutter main.dart</a></article>
          <article class="content-card resource-step"><span class="zone-badge teacher">04</span><strong>最後再測 App 控制</strong><p>若手機按鈕沒反應，先回頭查小車端是否收到資料，再查 App 是否找到可寫入特徵值。</p><a class="button ghost" href="downloads/topic-06-bluetooth-car/controler_ble_v2_speed-variable.7z">下載變速版壓縮檔</a></article>
        </div>
      </section>

      <section id="classroom-flow" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Classroom Flow</p>
          <h2>建議上課流程</h2>
          <p>這一章建議放在小車能基本移動之後，讓學生知道「按鈕不是直接控制馬達，而是透過藍芽送出指令」。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <img class="teaching-visual diagram-visual" src="assets/topic-06-flutter-app.png" alt="Flutter 藍芽小車 App 介面">
            <h3>先看 App 畫面</h3>
            <p>從搜尋裝置、連線按鈕、方向控制按鈕開始，讓學生先理解使用者看到的是控制介面。</p>
          </article>
          <article class="content-card">
            <img class="teaching-visual" src="assets/real-bootcamp-car.jpg" alt="Raspberry Pi Pico 小車">
            <h3>再看小車端反應</h3>
            <p>同一個按鈕會送出不同字元，小車端只要把字元對應到馬達函式，就能完成遙控。</p>
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Key Code</p>
          <h2>課堂上最值得解讀的兩段程式</h2>
          <p>完整 Flutter 程式與 Pico 小車端程式已放在下載區，網頁先呈現最關鍵的藍芽掃描與指令對應。</p>
        </div>
        <div class="page-grid">
          {render_code_card("Flutter：搜尋 PicoCar", flutter_scan_code, "學生先理解 App 如何找到小車。")}
          {render_code_card("Pico：收到指令後控制小車", pico_ble_code, "學生再理解小車端如何把 1/2/3/4/0 轉成動作。")}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Teacher Notes</p>
          <h2>藍芽遙控的授課重點</h2>
          <p>這裡適合讓老師快速確認 App 與 Pico 小車端是否使用同一組通訊設定。</p>
        </div>
        {render_table([
            "| 項目 | 教材設定 | 教學提醒 |",
            "|---|---|---|",
            "| 藍芽裝置名稱 | `PicoCar` | App 掃描不到時，先確認小車端 BLE 名稱是否一致 |",
            "| 服務 UUID | `FFA0`，備用 `FFE0` | 新設定失敗時可能仍會出現原廠預設 UUID |",
            "| 寫入特徵值 | `FFA1` 或 `FFE1` | Flutter 端必須找到可 write 的 characteristic |",
            "| 基本指令 | `1/2/3/4/0` | 分別對應前進、後退、左轉、右轉、停止 |",
            "| 變速版指令 | `5/6/7` | 低速、中速、高速，適合做進階挑戰 |",
        ])}
      </section>
"""
    return render_static_topic_page(topic, body_html)


def render_board_topic_page(topic: StaticTopic) -> str:
    board_code = """from machine import Pin
import time

led = Pin(25, Pin.OUT)
button = Pin(3, Pin.IN)

while True:
    if button.value() == 1:
        led.on()
    else:
        led.off()
    time.sleep(0.05)"""
    motor_logic_code = """# M1 右馬達：GP12 / GP13
# M2 左馬達：GP11 / GP10

def set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)"""
    body_html = f"""
      <section id="learning-route" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Learning Route</p>
          <h2>把 PDF 變成一張可上課的板子地圖</h2>
          <p>這個主題不再拆成「電路板基礎教學」，而是用 PDF 作為主教材，先建立老師與學生都能查閱的腳位導讀。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <img class="teaching-visual diagram-visual" src="assets/ppt-pinout-overview.png" alt="Pico 腳位總覽">
            <h3>先認識主板可以控制什麼</h3>
            <p>LED、按鈕、蜂鳴器、RGB、超音波、馬達、I2C 循跡感測器都可以從同一塊板子出發。</p>
          </article>
          <article class="content-card">
            <img class="teaching-visual diagram-visual" src="assets/topic-07-python-pdf-page.png" alt="Python PDF 馬達邏輯頁面">
            <h3>再把腳位連到程式</h3>
            <p>從 <code>Pin</code>、<code>PWM</code>、<code>ADC</code>、<code>I2C</code> 到馬達方向邏輯，讓硬體位置對應到程式語法。</p>
          </article>
        </div>
      </section>

      <section id="classroom-flow" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Board Map</p>
          <h2>目前教材採用的腳位對照</h2>
          <p>以下整理自 Python PDF 與相容性驗證報告，方便老師備課時快速確認各章節的硬體依賴。</p>
        </div>
        {render_table([
            "| 功能 | 教材腳位 | 網頁教材使用方式 |",
            "|---|---|---|",
            "| 內建 LED | `GP25` | 入門 cases 使用 `Pin(25, Pin.OUT)` |",
            "| 按鈕 | `GP3` | 數位輸入，適合說明上拉/下拉與狀態判斷 |",
            "| 蜂鳴器 | `GP6` | 使用 `PWM(Pin(6))` 製作聲音回饋 |",
            "| RGB 彩燈條 | `GP2`，6 顆 WS2812B | 感測輸出主題用來呈現顏色狀態 |",
            "| 超音波 / 距離 RGB | RGB `GP14`，聲波 `GP15` | 感測輸出與避障任務使用 |",
            "| 右馬達 M1 | `GP12` / `GP13` | 小車移動與無人車任務使用 |",
            "| 左馬達 M2 | `GP11` / `GP10` | 小車移動與無人車任務使用 |",
            "| I2C | SDA `GP20`，SCL `GP21` | 四路循跡感測器使用 |",
            "| 類比輸入 A0 | `GP26` | 電位器與類比輸入 cases 使用 |",
            "| 外接 LED D7 | `GP7` | PWM LED cases 使用 |",
        ])}
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Key Code</p>
          <h2>用兩段程式把板子概念接起來</h2>
          <p>第一段讓學生理解輸入與輸出，第二段讓老師銜接到馬達控制邏輯。</p>
        </div>
        <div class="page-grid">
          {render_code_card("LED 與按鈕：輸入輸出最小範例", board_code)}
          {render_code_card("馬達方向：兩個腳位決定一個馬達狀態", motor_logic_code)}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">How To Use</p>
          <h2>這份 PDF 在網站中的角色</h2>
        </div>
        <div class="resource-roadmap">
          <article class="content-card resource-step">
            <span class="zone-badge teacher">課前</span>
            <strong>先用腳位表確認硬體</strong>
            <p>確認課堂要用的 LED、按鈕、蜂鳴器、感測器或馬達是否與主板腳位一致。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge student">課中</span>
            <strong>讓學生從一個元件開始</strong>
            <p>先做 LED 或按鈕，再逐步銜接蜂鳴器、RGB、感測器與馬達。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge teacher">除錯</span>
            <strong>先查腳位，再查程式</strong>
            <p>如果程式沒反應，優先檢查腳位、接線與元件方向，再檢查程式邏輯。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge student">延伸</span>
            <strong>把元件組合成任務</strong>
            <p>學生熟悉單一元件後，再把輸入、輸出、馬達與感測器組成小作品。</p>
          </article>
        </div>
      </section>
"""
    return render_static_topic_page(topic, body_html)


def render_fan_topic_page(topic: StaticTopic) -> str:
    fan_pwm_code = """from machine import Pin, PWM
import time

# 概念範例：用 PWM 改變馬達輸出強度
# 實際腳位請依擺頭電扇簡報與電路接線調整。
fan_motor = PWM(Pin(9))
fan_motor.freq(1000)

speeds = [0, 22000, 42000, 65535]

for duty in speeds:
    fan_motor.duty_u16(duty)
    time.sleep(2)

fan_motor.duty_u16(0)"""
    body_html = f"""
      <section id="learning-route" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Learning Route</p>
          <h2>從小車走到真實作品：智慧型可擺動電風扇</h2>
          <p>這個主題是延伸作品，不是小車核心操控必修。學生會看到機構、電路、感測器與程式如何合成一件作品。</p>
        </div>
        <div class="visual-story-grid">
          <article class="content-card">
            <img class="teaching-visual" src="assets/fan-assembled.png" alt="擺頭電扇成品">
            <h3>作品目標</h3>
            <p>做出可以擺頭、調速、接收控制訊號的智慧型電風扇。</p>
          </article>
          <article class="content-card">
            <img class="teaching-visual" src="assets/fan-gear.png" alt="齒輪傳動機構">
            <h3>機構原理</h3>
            <p>用蝸桿齒輪改變方向並減速，再把旋轉運動傳到連桿。</p>
          </article>
          <article class="content-card">
            <img class="teaching-visual" src="assets/fan-linkage.png" alt="連桿機構">
            <h3>擺頭運動</h3>
            <p>四連桿把旋轉型動力轉成左右搖擺，這是風扇擺頭的核心。</p>
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Extension Role</p>
          <h2>這一章在整門課中的角色</h2>
          <p>如果課程目標是「完整操控小車」，請先完成 01-05。08 的價值是讓學生知道同一套輸入、輸出、PWM、感測與控制流程，也可以移植到非小車作品。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">小車主線</span>
            <h3>先完成 01-05</h3>
            <p>LED、感測器、馬達、避障、循跡與專題整合是小車操控的核心能力。</p>
            <a class="button ghost" href="topic-05-project-cases.html">回到主題 05</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">作品延伸</span>
            <h3>再轉到擺頭電扇</h3>
            <p>把小車課程中的 PWM 調速、按鈕控制、感測判斷與藍芽遙控概念，放進風扇這個真實機構作品。</p>
            <a class="button ghost" href="downloads/topic-08-fan-application/fan-course-slides.pptx">下載擺頭電扇簡報</a>
          </article>
        </div>
      </section>

      <section id="classroom-flow" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Classroom Flow</p>
          <h2>建議教學順序</h2>
          <p>先讓學生看見作品與機構，再回到板子、腳位與程式，理解「控制」如何進入作品。</p>
        </div>
        <div class="resource-roadmap">
          <article class="content-card resource-step">
            <span class="zone-badge student">01</span>
            <strong>觀察風扇如何擺頭</strong>
            <p>先看成品與零件，討論為什麼馬達一直轉，風扇卻會左右擺。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge student">02</span>
            <strong>認識齒輪與連桿</strong>
            <p>齒輪負責改變方向與減速，連桿負責把旋轉變成搖擺。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge teacher">03</span>
            <strong>對照 Pico X2 腳位</strong>
            <p>說明馬達、舵機、蜂鳴器、感測器與 I2C/SPI/UART 等接口。</p>
          </article>
          <article class="content-card resource-step">
            <span class="zone-badge teacher">04</span>
            <strong>加入智慧控制</strong>
            <p>用按鈕、電位器、感測器或藍芽，把風扇變成可互動的裝置。</p>
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Pico X2 Board</p>
          <h2>擺頭電扇簡報中的腳位重點</h2>
          <p>以下整理自擺頭電扇課程簡報的 Pico X2 腳位頁，適合放在作品控制前講解。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <img class="teaching-visual diagram-visual" src="assets/fan-board.png" alt="智慧型控制電路板">
            <h3>智慧型控制電路板</h3>
            <p>簡報中特別標示電源、電機接口、感測器接口、OLED、I2C、蜂鳴器、藍芽模組與開放腳位。</p>
          </article>
          <article class="content-card">
            {render_table([
                "| 接口 | 對應腳位 | 說明 |",
                "|---|---|---|",
                "| UART | `GP0` / `GP1` | 第一組 UART TX/RX，可用於通訊 |",
                "| GPIO / PWM | `GP2` / `GP3` / `GP4` | 開放式數位輸入輸出，也可做 PWM |",
                "| ADC | `GP26` / `GP27` / `GP28` | 類比輸入，適合電位器 |",
                "| I2C | `GP21` / `GP20` | SCL / SDA 通訊介面 |",
                "| SPI | `GP18` / `GP19` / `GP16` / `GP17` | SCLK / MOSI / MISO / CS |",
                "| M1 / M2 | `GP9` / `GP8` / `GP11` / `GP10` | 電機接口 |",
                "| Servo | `GP6` / `GP7` | 舵機或控制輸出 |",
                "| Buzzer | `GP22` | 蜂鳴器 |",
                "| Sensor 1 / 2 | `GP12` / `GP13`、`GP14` / `GP15` | 可做超音波或紅外線感測器接口 |",
            ])}
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Control Ideas</p>
          <h2>可以放進作品的控制概念</h2>
          <p>擺頭電扇簡報中的智慧控制包含按鈕、電機轉動、調速、感測開關、訊息顯示與藍芽遙控。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <img class="teaching-visual diagram-visual" src="assets/fan-block-code.png" alt="擺頭電扇積木程式示意">
            <h3>從積木邏輯轉成 Python 思維</h3>
            <p>先用積木看流程，再回到 Python 的變數、判斷與 PWM 輸出，學生會比較容易理解。</p>
          </article>
          {render_code_card("PWM 調速概念片段", fan_pwm_code, "這是概念範例，實際接線腳位請依課程簡報與現場電路調整。")}
        </div>
      </section>
"""
    return render_static_topic_page(topic, body_html)


def render_setup_page() -> str:
    import_test_code = """# mango-import-test.py
# 先確認 mango 函式庫已經放到 Pico 根目錄

from mango import Motor, RUS04, WS2812B

print("mango import OK")
print("現在可以繼續做馬達、超音波與 RGB cases。")"""
    calibration_code = """from machine import Pin
import time

# Raspberry Pi Pico 小車馬達校正
# 教材統一腳位：
#   右馬達 M1 = GP12 / GP13
#   左馬達 M2 = GP11 / GP10

RIGHT_A = Pin(12, Pin.OUT)
RIGHT_B = Pin(13, Pin.OUT)
LEFT_A = Pin(11, Pin.OUT)
LEFT_B = Pin(10, Pin.OUT)

# 如果某一邊前進方向相反，把 1 改成 -1。
RIGHT_SIGN = 1
LEFT_SIGN = 1


def _set_motor(pin_a, pin_b, direction):
    if direction > 0:
        pin_a.value(1)
        pin_b.value(0)
    elif direction < 0:
        pin_a.value(0)
        pin_b.value(1)
    else:
        pin_a.value(0)
        pin_b.value(0)


def drive(left, right):
    _set_motor(LEFT_A, LEFT_B, left * LEFT_SIGN)
    _set_motor(RIGHT_A, RIGHT_B, right * RIGHT_SIGN)


def stop():
    drive(0, 0)


tests = [
    ("右輪往前", 0, 1),
    ("左輪往前", 1, 0),
    ("整台前進", 1, 1),
    ("整台後退", -1, -1),
    ("原地左轉", -1, 1),
    ("原地右轉", 1, -1),
]

print("Motor calibration start")
print("如果方向相反，先按 Ctrl+C 停止，再修改 RIGHT_SIGN 或 LEFT_SIGN。")

for label, left, right in tests:
    print(label)
    drive(left, right)
    time.sleep(1.2)
    stop()
    time.sleep(0.8)

print("Motor calibration done")
stop()"""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>開始前設定 | Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="開始 Raspberry Pi Pico 小車課程前，先完成 Thonny、MicroPython、mango 函式庫、馬達校正與自學檢查。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VERSION}">
</head>
<body class="topic-page">
  <div class="page-shell">
{header_html("setup.html")}

    <main>
      <section class="subpage-hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">Start Here</p>
          <h1>開始前設定：先讓小車真的能跑</h1>
          <p class="hero-text">
            這一頁是 01-08 主題的前置檢查。學生先確認 Thonny 能連上 Pico、mango 函式庫已上傳、馬達方向正確，再進入正式主題，後面才不會一直卡在環境問題。
          </p>
          <div class="action-row">
            <a class="button primary" href="#setup-steps">照步驟設定</a>
            <a class="button secondary" href="downloads/extensions/board-library/mango-library.zip">下載 mango 函式庫</a>
            <a class="button ghost" href="downloads/motor-calibration.py">下載馬達校正程式</a>
          </div>
        </div>
        <div class="subpage-aside">
          <article class="aside-card">
            <img class="teaching-visual" src="assets/real-bootcamp-car.jpg" alt="Raspberry Pi Pico 小車">
            <p class="visual-note">這頁的目標不是講新概念，而是把會讓學生卡住的環境問題先排除。</p>
          </article>
          <article class="aside-card">
            <span class="zone-badge student">Goal</span>
            <h3>完成後應該能做到</h3>
            <p>Thonny 可以 Run 程式、<code>from mango import Motor</code> 不報錯、按下馬達校正後小車前進方向正確。</p>
          </article>
        </div>
      </section>

{render_file_location_section("setup.html")}

      <section id="setup-steps" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Required Steps</p>
          <h2>開始前先完成 6 件事</h2>
          <p>這 6 步完成後，學生再看 01-05 才會像是在學小車，而不是一直處理環境錯誤。</p>
        </div>
        <div class="resource-roadmap">
          <article class="content-card resource-step"><span class="zone-badge student">Step 01</span><strong>接上 Pico 小車</strong><p>用 USB 線連接電腦與 Raspberry Pi Pico，並確認小車放在平面上，輪子不要懸空亂轉。</p></article>
          <article class="content-card resource-step"><span class="zone-badge student">Step 02</span><strong>打開 Thonny</strong><p>右下角選擇 <code>MicroPython (Raspberry Pi Pico)</code>。如果看不到，先請老師協助安裝或更新 MicroPython。</p></article>
          <article class="content-card resource-step"><span class="zone-badge teacher">Step 03</span><strong>上傳 mango 函式庫</strong><p>下載 <code>mango-library.zip</code>，解壓縮後把整個 <code>mango</code> 資料夾放到 Pico 的根目錄。</p></article>
          <article class="content-card resource-step"><span class="zone-badge student">Step 04</span><strong>執行 import 測試</strong><p>貼上測試程式，看到 <code>mango import OK</code> 才進入 02-05 中需要 mango 的 cases。</p></article>
          <article class="content-card resource-step"><span class="zone-badge teacher">Step 05</span><strong>跑馬達校正</strong><p>先確認右輪、左輪、前進、後退、左右轉方向正確。若相反，修改 <code>RIGHT_SIGN</code> 或 <code>LEFT_SIGN</code>。</p></article>
          <article class="content-card resource-step"><span class="zone-badge student">Step 06</span><strong>再進入正式主題</strong><p>完成設定後，先做 BootCamp 或 01 入門；要真的控制小車移動時，再進入 03 小車移動。</p></article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Mango Library</p>
          <h2>mango 函式庫要先放進 Pico</h2>
          <p>許多主題會使用 <code>from mango import Motor</code>、<code>RUS04</code>、<code>WS2812B</code>、<code>GraySensor8</code>。如果沒有上傳函式庫，學生會看到 <code>ImportError</code> 或 <code>ModuleNotFoundError</code>。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge teacher">Upload</span>
            <h3>Thonny 上傳方式</h3>
            <p>下載 zip 後解壓縮，確認裡面有 <code>mango/__init__.py</code>。在 Thonny 檔案視窗中，把整個 <code>mango</code> 資料夾上傳到 Pico 根目錄。</p>
            <a class="button primary" href="downloads/extensions/board-library/mango-library.zip">下載 mango-library.zip</a>
          </article>
          {render_code_card("mango import 測試", import_test_code, "若這段程式可以正常執行，就代表函式庫已經放到 Pico 上。")}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Motor Calibration</p>
          <h2>馬達方向先校正，再談避障或循跡</h2>
          <p>如果左右輪方向錯了，後面的避障與循跡都會看起來像程式壞掉。先用這段程式確認每個方向，再進入主題 03。</p>
        </div>
        <div class="page-grid">
          {render_code_card("馬達校正程式", calibration_code, "先觀察每個動作是否符合中文提示；若方向相反，修改 RIGHT_SIGN 或 LEFT_SIGN。")}
          <article class="content-card">
            <span class="zone-badge student">Rule</span>
            <h3>教材統一腳位</h3>
            <p>右馬達 M1 使用 <code>GP12 / GP13</code>，左馬達 M2 使用 <code>GP11 / GP10</code>。若現場車子接線不同，請以這頁先建立自己的校正版本。</p>
            <a class="button ghost" href="topic-03-car-motion.html">校正後進入主題 03</a>
          </article>
        </div>
      </section>

{render_mainline_section()}

{render_completion_checklist("setup.html")}

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Next</p>
          <h2>完成設定後要去哪裡</h2>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">第一次上課</span>
            <h3>先做 BootCamp</h3>
            <p>如果只是要讓學生快速感受到小車會動，先做 1 小時 BootCamp。</p>
            <a class="button primary" href="bootcamp.html">打開 BootCamp</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">正式課程</span>
            <h3>從主題 01 開始</h3>
            <p>若要完整自學，就從 LED、按鈕、狀態控制開始，逐步建立到小車任務。</p>
            <a class="button ghost" href="topic-01-intro.html">進入主題 01</a>
          </article>
        </div>
      </section>
    </main>
{footer_html()}
  </div>
  <script src="script.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def render_supplement_topic_page(topic: StaticTopic) -> str:
    if topic.output == "topic-06-bluetooth-car.html":
        return render_bluetooth_topic_page(topic)
    if topic.output == "topic-07-board-python.html":
        return render_board_topic_page(topic)
    if topic.output == "topic-08-fan-application.html":
        return render_fan_topic_page(topic)
    raise ValueError(f"Unknown static topic: {topic.output}")


def render_index() -> str:
    panels = []
    roadmap = []
    download_cards = []
    for topic in all_topics():
        chips = "".join(f"<span>{html.escape(chip)}</span>" for chip in topic.chips)
        if isinstance(topic, Topic):
            download_href = f"downloads/case-md/{topic.source}"
            download_label = "下載 Markdown"
        else:
            download_href = topic.download_href
            download_label = topic.download_label
        panels.append(
            f"""          <article class="product-panel {topic.accent}">
            <span class="zone-badge teacher">{topic.label}</span>
            <h3>{html.escape(topic.title)}</h3>
            <p>{html.escape(topic.summary)}</p>
            <div class="chip-list compact">{chips}</div>
            <a class="button primary" href="{topic.output}">進入{html.escape(topic.label)}</a>
          </article>"""
        )
        roadmap.append(
            f"""          <article class="content-card">
            <span class="zone-badge student">{topic.label}</span>
            <h3>{html.escape(topic.title)}</h3>
            <p>{html.escape(topic.subtitle)}</p>
            <a class="button ghost" href="{topic.output}">打開主題頁</a>
          </article>"""
        )
        download_cards.append(
            f"""          <article class="download-card">
            <span class="download-type">{topic.label}</span>
            <h3>{html.escape(topic.title)}</h3>
            <p>{html.escape(topic.summary)}</p>
            <a class="button ghost block" href="{download_href}">{html.escape(download_label)}</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="以 8 個主題整理 Raspberry Pi Pico 小車教材：入門、感測輸出、小車移動、無人車、專題化、藍芽遙控、電路板教材與擺頭電扇應用。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VERSION}">
</head>
<body class="home-page">
  <div class="page-shell">
{header_html(None)}

    <main id="top">
      <section class="hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">Topic-based Learning</p>
          <h1>用 8 個主題完成 Raspberry Pi Pico 小車課程</h1>
          <p class="hero-text">
            本網站已改成依教材主題學習：從 LED、按鈕與狀態控制開始，逐步進入感測輸出、小車移動、無人車策略與專題化任務。
            後續再加入藍芽遙控小車、Python 電路板教材與擺頭電扇應用，讓課程可以從小車走到完整作品。
          </p>
          <div class="hero-actions">
            <a class="button primary" href="setup.html">先做開始設定</a>
            <a class="button secondary" href="bootcamp.html">一小時 BootCamp</a>
            <a class="button ghost" href="downloads.html">下載教材</a>
          </div>
          <div class="hero-points">
            <div class="point-card">
              <strong>8</strong>
              <span>個正式主題</span>
            </div>
            <div class="point-card">
              <strong>50+</strong>
              <span>個 case，含循跡演算法與應用專題</span>
            </div>
            <div class="point-card">
              <strong>Pico</strong>
              <span>Raspberry Pi Pico / MicroPython</span>
            </div>
          </div>
        </div>
        <div class="hero-gallery" aria-hidden="true">
          <article class="gallery-card">
            <img class="asset-preview" src="assets/real-bootcamp-car.jpg" alt="Raspberry Pi Pico 小車實拍">
            <div class="gallery-caption">
              <strong>Microcar</strong>
              <span>小車硬體與課堂實作</span>
            </div>
          </article>
          <article class="gallery-card">
            <img class="asset-preview" src="assets/control-board.png" alt="控制板示意">
            <div class="gallery-caption">
              <strong>Board</strong>
              <span>控制板、腳位與輸出入</span>
            </div>
          </article>
          <article class="gallery-card">
            <img class="asset-preview" src="assets/fan-assembled.png" alt="擺頭電扇作品">
            <div class="gallery-caption">
              <strong>Project</strong>
              <span>小車、藍芽與擺頭電扇應用</span>
            </div>
          </article>
        </div>
      </section>

{render_mainline_section()}

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Quick Start</p>
          <h2>BootCamp 保留為快速體驗課</h2>
          <p>BootCamp 是一小時活動入口，適合先讓學生用 Thonny 連上 Raspberry Pi Pico 小車，貼上程式並用鍵盤控制基本動作。它會保留在網站中，但不併入正式主題編號。</p>
        </div>
        <div class="page-grid">
          <article class="content-card tool-focus-card">
            <span class="zone-badge student">BootCamp</span>
            <h3>先完成連線與基本控制</h3>
            <p>學生照著 12 個步驟操作：開啟 Thonny、建立新檔、貼上完整程式、按 Run，最後用 W / A / S / D / X 控制小車。</p>
            <a class="button primary" href="bootcamp.html">打開 BootCamp</a>
          </article>
          <article class="content-card tool-focus-card">
            <span class="zone-badge teacher">正式主題</span>
            <h3>BootCamp 之後再進入 8 主題</h3>
            <p>完成快速體驗後，再依序進入入門、感測與輸出、小車移動、無人車、專題化、藍芽遙控、電路板教材與擺頭電扇應用。</p>
            <a class="button ghost" href="#topic-roadmap">查看 8 個主題</a>
          </article>
        </div>
      </section>

      <section class="section product-band reveal">
        <div class="section-heading">
          <p class="eyebrow">Current Topics</p>
          <h2>目前網站主線改為 8 個教材主題</h2>
          <p>01-05 是小車核心能力，06 是藍芽遙控延伸，07-08 則把電路板與擺頭電扇作品整理成可授課的應用主題。</p>
        </div>
        <div class="product-rail">
{chr(10).join(panels)}
        </div>
      </section>

      <section id="topic-roadmap" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Topic Roadmap</p>
          <h2>建議依序從主題 1 走到主題 8</h2>
          <p>這個順序會先建立輸出入與狀態概念，再逐步走向移動控制、無人車策略、藍芽遙控與電路板作品應用。</p>
        </div>
        <div class="page-grid-3">
{chr(10).join(roadmap)}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Downloads</p>
          <h2>教材檔與原始程式已放入下載區</h2>
          <p>01-05 保留 Markdown 原始教材；06-08 則提供 Flutter 程式、Python PDF 與擺頭電扇簡報等對應檔案。</p>
        </div>
        <div class="download-grid">
{chr(10).join(download_cards)}
        </div>
      </section>
    </main>
{footer_html()}
  </div>
  <script src="script.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def render_downloads() -> str:
    cards = []
    for topic in all_topics():
        if isinstance(topic, Topic):
            download_href = f"downloads/case-md/{topic.source}"
            download_label = "下載 Markdown"
        else:
            download_href = topic.download_href
            download_label = topic.download_label
        cards.append(
            f"""          <article class="download-card" id="{topic.output.removesuffix('.html')}">
            <span class="download-type">{topic.label}</span>
            <h3>{html.escape(topic.title)}</h3>
            <p>{html.escape(topic.summary)}</p>
            <a class="button primary block" href="{topic.output}">打開主題頁</a>
            <a class="button ghost block" href="{download_href}">{html.escape(download_label)}</a>
          </article>"""
        )
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>下載區 | Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="下載 Raspberry Pi Pico 小車 8 個主題教材、原始程式、PDF 與擺頭電扇簡報。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VERSION}">
</head>
<body class="downloads-page">
  <div class="page-shell">
{header_html("downloads.html")}

    <main>
      <section class="subpage-hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">Downloads</p>
          <h1>8 個主題教材下載區</h1>
          <p class="hero-text">
            下載區現在依照開始前設定與 8 個正式主題整理。每個主題都可以直接打開網頁閱讀，也可以下載對應的 Markdown、程式、PDF 或簡報教材。
          </p>
          <div class="action-row">
            <a class="button primary" href="#required-downloads">先看必備檔案</a>
            <a class="button secondary" href="#topic-downloads">查看主題教材</a>
            <a class="button ghost" href="index.html">回首頁</a>
          </div>
        </div>
        <div class="subpage-aside">
          <article class="aside-card">
            <span class="zone-badge teacher">Format</span>
            <h3>網頁與 Markdown 並存</h3>
            <p>網頁適合直接閱讀與投影，Markdown 適合教師備課、修改與整理。</p>
          </article>
        </div>
      </section>

{render_file_location_section("downloads.html")}

      <section id="required-downloads" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Required Files</p>
          <h2>開始前必備檔案</h2>
          <p>這些檔案不是額外補充，而是讓 01-05 小車主線能順利執行的前置工具。</p>
        </div>
        <div class="download-grid">
          <article class="download-card">
            <span class="download-type">Start Here</span>
            <h3>開始前設定頁</h3>
            <p>照步驟完成 Thonny、MicroPython、mango 函式庫、import 測試與馬達校正。</p>
            <a class="button primary block" href="setup.html">打開開始設定</a>
          </article>
          <article class="download-card">
            <span class="download-type">Library</span>
            <h3>mango 函式庫</h3>
            <p>02-05 中許多 RGB、超音波、馬達、循跡 cases 需要先把這個資料夾上傳到 Pico。</p>
            <a class="button ghost block" href="downloads/extensions/board-library/mango-library.zip">下載 mango-library.zip</a>
          </article>
          <article class="download-card">
            <span class="download-type">Calibration</span>
            <h3>馬達校正程式</h3>
            <p>進入 03 小車移動前，先確認左右輪與前後方向都正確。</p>
            <a class="button primary block" href="code-viewer.html?file=motor-calibration">檢視程式</a>
            <a class="button ghost block" href="downloads/motor-calibration.py">下載 motor-calibration.py</a>
          </article>
          <article class="download-card">
            <span class="download-type">Import Test</span>
            <h3>mango import 測試</h3>
            <p>用最短程式確認 Pico 上已經可以載入 mango 函式庫。</p>
            <a class="button primary block" href="code-viewer.html?file=mango-import-test">檢視程式</a>
            <a class="button ghost block" href="downloads/mango-import-test.py">下載 mango-import-test.py</a>
          </article>
        </div>
      </section>

      <section id="topic-downloads" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Topic Files</p>
          <h2>依主題下載教材</h2>
          <p>01-05 提供 Markdown cases；06-08 則提供藍芽小車、Python 電路板教材與擺頭電扇應用檔案。</p>
        </div>
        <div class="download-grid">
{chr(10).join(cards)}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Support</p>
          <h2>其他輔助頁面</h2>
          <p>若需要 1 小時體驗課或程式檢視器，仍可從這裡進入，但它們不再列為正式主題。</p>
        </div>
        <div class="page-grid">
          <article class="content-card">
            <span class="zone-badge student">Quick Class</span>
            <h3>BootCamp</h3>
            <p>適合短時間體驗用 Thonny 控制小車前進、後退、左轉、右轉與停止。</p>
            <a class="button ghost" href="bootcamp.html">打開 BootCamp</a>
          </article>
          <article class="content-card">
            <span class="zone-badge teacher">Code Viewer</span>
            <h3>程式檢視頁</h3>
            <p>可用來顯示目前網站中保留的獨立 Python 範例。</p>
            <a class="button ghost" href="code-viewer.html?file=keyboard-car-control">打開程式頁</a>
          </article>
        </div>
      </section>
    </main>
{footer_html()}
  </div>
  <script src="script.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def copy_markdown_sources() -> None:
    DOWNLOAD_MD_DIR.mkdir(parents=True, exist_ok=True)
    for topic in TOPICS:
        shutil.copy2(SOURCE_DIR / topic.source, DOWNLOAD_MD_DIR / topic.source)
    report = SOURCE_DIR / "教材相容性驗證報告.md"
    if report.exists():
        shutil.copy2(report, DOWNLOAD_MD_DIR / report.name)


def copy_extra_sources() -> None:
    DOWNLOAD_TOPIC_06_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_TOPIC_08_DIR.mkdir(parents=True, exist_ok=True)

    flutter_dir = ROBOT_WEB_DIR / "01_Flutter介面程式"
    preview_dir = ROBOT_WEB_DIR / "02_介面預覽與輸出"
    ble_dir = ROBOT_WEB_DIR / "03_藍牙小車專案"

    flutter_main = flutter_dir / "main.dart"
    if flutter_main.exists():
        shutil.copy2(flutter_main, DOWNLOAD_TOPIC_06_DIR / "main.dart")

    flutter_preview = preview_dir / "main.png"
    if flutter_preview.exists():
        shutil.copy2(flutter_preview, REPO / "assets" / "topic-06-flutter-app.png")
        shutil.copy2(flutter_preview, DOWNLOAD_TOPIC_06_DIR / "flutter-app-preview.png")

    for archive_name in ("controler_ble.7z", "controler_ble_v2_speed variable.7z"):
        archive_path = ble_dir / archive_name
        if archive_path.exists():
            safe_name = archive_name.replace(" ", "-")
            shutil.copy2(archive_path, DOWNLOAD_TOPIC_06_DIR / safe_name)

    for source_name, target_name in (
        ("標準版_controler_ble", "standard-controler-ble"),
        ("變速版_controler_ble_v2", "speed-variable-controler-ble-v2"),
    ):
        source_dir = ble_dir / source_name
        target_dir = DOWNLOAD_TOPIC_06_DIR / target_name
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)

    python_pdf = ROBOT_HANDOUT_DIR / "機器人程式設計實務-Python.pdf"
    if python_pdf.exists():
        shutil.copy2(python_pdf, REPO / "downloads" / "robot-programming-practice-python.pdf")
        try:
            import fitz  # type: ignore

            doc = fitz.open(str(python_pdf))
            page_index = 46 if len(doc) > 46 else 0
            pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
            pix.save(str(REPO / "assets" / "topic-07-python-pdf-page.png"))
        except Exception:
            pass

    fan_ppt = ROBOT_HANDOUT_DIR / "擺頭電扇-課程簡報.pptx"
    if fan_ppt.exists():
        shutil.copy2(fan_ppt, DOWNLOAD_TOPIC_08_DIR / "fan-course-slides.pptx")
        fan_assets = {
            "image28.png": "fan-assembled.png",
            "image26.png": "fan-board.png",
            "image7.png": "fan-gear.png",
            "image8.png": "fan-linkage.png",
            "image50.png": "fan-block-code.png",
        }
        with zipfile.ZipFile(fan_ppt) as archive:
            names = set(archive.namelist())
            for source_name, target_name in fan_assets.items():
                member = f"ppt/media/{source_name}"
                if member in names:
                    (REPO / "assets" / target_name).write_bytes(archive.read(member))


def main() -> None:
    copy_markdown_sources()
    copy_extra_sources()
    write_text(REPO / "index.html", render_index())
    write_text(REPO / "downloads.html", render_downloads())
    write_text(REPO / "setup.html", render_setup_page())
    for topic in TOPICS:
        write_text(REPO / topic.output, render_topic_page(topic))
    for topic in SUPPLEMENT_TOPICS:
        write_text(REPO / topic.output, render_supplement_topic_page(topic))


if __name__ == "__main__":
    main()

