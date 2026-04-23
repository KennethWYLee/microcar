from __future__ import annotations

import html
import re
import shutil
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
    links = [("bootcamp.html", "Boot Camp")] + [
        (topic.output, topic.title.split("：", 1)[0].replace("入門", "入門")) for topic in TOPICS
    ]
    link_html = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if href == active_output else ""}>{label}</a>'
        for href, label in links
    )
    return f"""      <nav class="site-nav" aria-label="主題導覽">
{link_html}
        <a href="downloads.html">下載區</a>
      </nav>"""


def header_html(active_output: str | None = None) -> str:
    return f"""    <header class="site-header">
      <a class="brand" href="index.html">
        <span class="brand-mark">MC</span>
        <span class="brand-copy">
          <strong>Raspberry Pi Pico 小車主題教材</strong>
          <small>Topic-based Microcar Course</small>
        </span>
      </a>
{nav_html(active_output)}
      <a class="button ghost" href="https://github.com/KennethWYLee/microcar" target="_blank" rel="noreferrer">GitHub</a>
    </header>"""


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
    next_topic = TOPICS[(TOPICS.index(topic) + 1) % len(TOPICS)]
    prev_topic = TOPICS[(TOPICS.index(topic) - 1) % len(TOPICS)]

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
  <link rel="stylesheet" href="styles.css?v=20260423-cases">
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
  </div>
  <script src="script.js?v=20260423-cases"></script>
</body>
</html>
"""


def render_index() -> str:
    panels = []
    roadmap = []
    download_cards = []
    for topic in TOPICS:
        chips = "".join(f"<span>{html.escape(chip)}</span>" for chip in topic.chips)
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
            <a class="button ghost block" href="downloads/case-md/{topic.source}">下載 Markdown</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="以 5 個主題整理 Raspberry Pi Pico 小車教材：入門、感測輸出、小車移動、無人車、專題化。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v=20260423-cases">
</head>
<body class="home-page">
  <div class="page-shell">
{header_html(None)}

    <main id="top">
      <section class="hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">Topic-based Learning</p>
          <h1>用 5 個主題完成 Raspberry Pi Pico 小車課程</h1>
          <p class="hero-text">
            本網站已改成依教材主題學習：從 LED、按鈕與狀態控制開始，逐步進入感測輸出、小車移動、無人車策略與專題化任務。
            每個主題都提供 cases、完整程式碼、成果說明與應用題。
          </p>
          <div class="hero-actions">
            <a class="button primary" href="bootcamp.html">先看 1 hr Boot Camp</a>
            <a class="button secondary" href="topic-01-intro.html">從主題 1 開始</a>
            <a class="button ghost" href="downloads.html">下載教材</a>
          </div>
          <div class="hero-points">
            <div class="point-card">
              <strong>5</strong>
              <span>個正式主題</span>
            </div>
            <div class="point-card">
              <strong>54</strong>
              <span>個 case，含新增循跡演算法 cases</span>
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
            <img class="asset-preview" src="assets/video-line-following-demo-poster.jpg" alt="循跡實作畫面">
            <div class="gallery-caption">
              <strong>Project</strong>
              <span>循跡、避障與專題任務</span>
            </div>
          </article>
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Quick Start</p>
          <h2>1 hr Boot Camp 保留為快速體驗課</h2>
          <p>Boot Camp 是一小時活動入口，適合先讓學生用 Thonny 連上 Raspberry Pi Pico 小車，貼上程式並用鍵盤控制基本動作。它會保留在網站中，但不併入 5 個正式教材主題。</p>
        </div>
        <div class="page-grid">
          <article class="content-card tool-focus-card">
            <span class="zone-badge student">1 hr Boot Camp</span>
            <h3>先完成連線與基本控制</h3>
            <p>學生照著 12 個步驟操作：開啟 Thonny、建立新檔、貼上完整程式、按 Run，最後用 W / A / S / D / X 控制小車。</p>
            <a class="button primary" href="bootcamp.html">打開 Boot Camp</a>
          </article>
          <article class="content-card tool-focus-card">
            <span class="zone-badge teacher">正式主題</span>
            <h3>Boot Camp 之後再進入 5 主題</h3>
            <p>完成快速體驗後，再依序進入入門、感測與輸出、小車移動、無人車、專題化五個正式主題。</p>
            <a class="button ghost" href="#topic-roadmap">查看 5 個主題</a>
          </article>
        </div>
      </section>

      <section class="section product-band reveal">
        <div class="section-heading">
          <p class="eyebrow">Current Topics</p>
          <h2>目前網站主線改為 5 個教材主題</h2>
          <p>規則式、P、PD、PID 的循跡控制內容已整合進第 5 主題，網站主線維持 5 個正式教材主題。</p>
        </div>
        <div class="product-rail">
{chr(10).join(panels)}
        </div>
      </section>

      <section id="topic-roadmap" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Topic Roadmap</p>
          <h2>建議依序從主題 1 走到主題 5</h2>
          <p>這個順序會先建立輸出入與狀態概念，再逐步走向移動控制、無人車策略與專題整合。</p>
        </div>
        <div class="page-grid-3">
{chr(10).join(roadmap)}
        </div>
      </section>

      <section class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Downloads</p>
          <h2>Markdown 原始教材也已放入下載區</h2>
          <p>網頁內容由 Markdown 教材產生，下載區保留原始 Markdown，方便備課或二次整理。</p>
        </div>
        <div class="download-grid">
{chr(10).join(download_cards)}
        </div>
      </section>
    </main>
  </div>
  <script src="script.js?v=20260423-cases"></script>
</body>
</html>
"""


def render_downloads() -> str:
    cards = []
    for topic in TOPICS:
        cards.append(
            f"""          <article class="download-card" id="{topic.output.removesuffix('.html')}">
            <span class="download-type">{topic.label}</span>
            <h3>{html.escape(topic.title)}</h3>
            <p>{html.escape(topic.summary)}</p>
            <a class="button primary block" href="{topic.output}">打開主題頁</a>
            <a class="button ghost block" href="downloads/case-md/{topic.source}">下載 Markdown</a>
          </article>"""
        )
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>下載區 | Raspberry Pi Pico 小車主題教材</title>
  <meta name="description" content="下載 Raspberry Pi Pico 小車 5 個主題教材的 Markdown 原始檔。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v=20260423-cases">
</head>
<body class="downloads-page">
  <div class="page-shell">
{header_html("downloads.html")}

    <main>
      <section class="subpage-hero reveal">
        <div class="hero-copy">
          <p class="eyebrow">Downloads</p>
          <h1>5 個主題教材下載區</h1>
          <p class="hero-text">
            下載區現在依照 5 個正式主題整理。每個主題都可以直接打開網頁閱讀，也可以下載 Markdown 原始教材。
          </p>
          <div class="action-row">
            <a class="button primary" href="#topic-downloads">查看主題教材</a>
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

      <section id="topic-downloads" class="section reveal">
        <div class="section-heading">
          <p class="eyebrow">Topic Files</p>
          <h2>依主題下載教材</h2>
          <p>第 5 主題已加入循跡演算法延伸 cases，因此 case 數比其他主題更多。</p>
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
            <h3>1 hr Boot Camp</h3>
            <p>適合短時間體驗用 Thonny 控制小車前進、後退、左轉、右轉與停止。</p>
            <a class="button ghost" href="bootcamp.html">打開 Boot Camp</a>
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
  </div>
  <script src="script.js?v=20260423-cases"></script>
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


def main() -> None:
    copy_markdown_sources()
    write_text(REPO / "index.html", render_index())
    write_text(REPO / "downloads.html", render_downloads())
    for topic in TOPICS:
        write_text(REPO / topic.output, render_topic_page(topic))


if __name__ == "__main__":
    main()
