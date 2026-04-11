from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math


BASE = Path(r"C:\Users\User\Documents\Lecture materials\microcar\assets")
W, H = 1280, 800
BG = "#f4efe7"
PANEL = "#fffaf4"
NAVY = "#1d4f7a"
TEAL = "#227c74"
GOLD = "#f2b544"
TEXT = "#1f2b3a"
MUTED = "#586577"
LINE = "#d8d2c8"
ACCENT = "#e8f3ff"
GREEN = "#dff2e2"
RED = "#e67c73"
ROSE = "#fde6e3"
LIGHT = "#dde7f1"

THEMES = {
    "setup": {"pill": "#dcecff", "panel": "#eef7ff", "label": "#9cc7ff", "spark": "#b7d7ff"},
    "thonny": {"pill": "#dcf4ea", "panel": "#edf9f3", "label": "#8ed7b5", "spark": "#bfe9d3"},
    "code": {"pill": "#ffe9c8", "panel": "#fff5e4", "label": "#ffc96f", "spark": "#ffe0aa"},
    "drive": {"pill": "#ffe0d8", "panel": "#fff1ed", "label": "#f5ad9c", "spark": "#ffd1c5"},
    "challenge": {"pill": "#efe3ff", "panel": "#f7f0ff", "label": "#cab1f3", "spark": "#e1d3fb"},
}


def step_theme(step_no: int):
    if step_no <= 4:
        return THEMES["setup"]
    if step_no <= 8:
        return THEMES["thonny"]
    if step_no <= 12:
        return THEMES["code"]
    if step_no <= 17:
        return THEMES["drive"]
    return THEMES["challenge"]


def load_font(size: int):
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


TITLE_FONT = load_font(56)
BODY_FONT = load_font(34)
SMALL_FONT = load_font(24)
MINI_FONT = load_font(22)


def base_card(step_no: int, title: str, subtitle: str):
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)
    theme = step_theme(step_no)
    d.rounded_rectangle((36, 36, W - 36, H - 36), radius=36, fill=PANEL, outline=LINE, width=3)

    # notebook-style guide lines
    for y in range(74, H - 70, 40):
        d.line((56, y, W - 56, y), fill="#f1ece4", width=1)

    # left teaching panel
    d.rounded_rectangle((56, 146, 540, 464), radius=34, fill="#fffdf9", outline="#efe5d8", width=2)
    d.rounded_rectangle((72, 72, 286, 130), radius=28, fill=theme["pill"])
    d.text((108, 88), f"STEP {step_no}", font=SMALL_FONT, fill=NAVY)
    d.text((72, 174), title, font=TITLE_FONT, fill=TEXT)
    d.text((72, 252), subtitle, font=BODY_FONT, fill=MUTED)

    # right illustration panel
    d.rounded_rectangle((584, 120, 1188, 684), radius=38, fill=theme["panel"], outline="#e4dacb", width=3)
    d.rounded_rectangle((606, 142, 1166, 662), radius=30, fill="#fffaf3", outline="#f0e7d9", width=2)

    # playful decoration
    d.ellipse((1090, 82, 1132, 124), fill=theme["spark"])
    d.ellipse((1138, 96, 1164, 122), fill=theme["spark"])
    d.rounded_rectangle((994, 88, 1076, 118), radius=14, fill=theme["pill"])
    d.text((1014, 94), "LOOK", font=MINI_FONT, fill=TEXT)
    return img, d


def draw_label(d, x, y, w, h, text, fill):
    d.rounded_rectangle((x + 6, y + 8, x + w + 6, y + h + 8), radius=18, fill="#e9ddd0")
    d.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=fill, outline="#dfd1c0", width=2)
    bbox = d.textbbox((0, 0), text, font=MINI_FONT)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((x + (w - tw) / 2, y + (h - th) / 2 - 2), text, font=MINI_FONT, fill=TEXT)


def draw_laptop(d, x, y, w=360, h=240, screen="#ffffff"):
    d.rounded_rectangle((x, y, x + w, y + h), radius=24, fill="#dde7f1", outline=NAVY, width=4)
    d.rounded_rectangle((x + 20, y + 20, x + w - 20, y + h - 20), radius=16, fill=screen)
    d.rounded_rectangle((x - 28, y + h - 8, x + w + 28, y + h + 28), radius=18, fill="#c8d4df", outline=NAVY, width=3)


def draw_car(d, x, y, scale=1.0, color=GOLD):
    w = int(260 * scale)
    h = int(125 * scale)
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(26 * scale), fill=color, outline=TEXT, width=4)
    d.rounded_rectangle(
        (x + int(42 * scale), y - int(30 * scale), x + w - int(42 * scale), y + int(40 * scale)),
        radius=int(18 * scale),
        fill="#fff7dc",
        outline=TEXT,
        width=4,
    )
    for wx in (int(x + 44 * scale), int(x + w - 86 * scale)):
        d.ellipse((wx, int(y + h - 16 * scale), wx + int(50 * scale), int(y + h + 34 * scale)), fill="#2d3748")
        d.ellipse(
            (wx + int(12 * scale), int(y + h - 2 * scale), wx + int(38 * scale), int(y + h + 24 * scale)),
            fill="#dbe6ef",
        )
    d.rectangle(
        (int(x + w * 0.5 - 18 * scale), int(y - 62 * scale), int(x + w * 0.5 + 18 * scale), int(y - 18 * scale)),
        fill=TEAL,
        outline=TEXT,
        width=3,
    )
    d.rectangle(
        (int(x + w * 0.5 - 64 * scale), int(y - 82 * scale), int(x + w * 0.5 + 64 * scale), int(y - 54 * scale)),
        fill=TEAL,
        outline=TEXT,
        width=3,
    )


def draw_usb(d, x1, y1, x2, y2, connected=True):
    if connected:
        d.line((x1, y1, x2, y2), fill=TEXT, width=8)
    d.rounded_rectangle((x1 - 22, y1 - 14, x1 + 22, y1 + 14), radius=8, fill="#b8c6d1", outline=TEXT, width=3)
    d.rounded_rectangle((x2 - 22, y2 - 14, x2 + 22, y2 + 14), radius=8, fill="#d7e0e8", outline=TEXT, width=3)


def draw_teacher(d, x, y):
    d.ellipse((x + 30, y, x + 110, y + 80), fill="#ffe0bd", outline=TEXT, width=3)
    d.rounded_rectangle((x, y + 76, x + 140, y + 220), radius=28, fill=TEAL, outline=TEXT, width=4)
    d.rectangle((x - 30, y + 116, x + 14, y + 132), fill=TEXT)
    d.polygon([(x - 60, y + 124), (x - 30, y + 108), (x - 30, y + 140)], fill=TEXT)


def draw_check(d, x, y, fill=GREEN):
    d.ellipse((x, y, x + 86, y + 86), fill=fill, outline=TEAL, width=4)
    d.line((x + 22, y + 46, x + 38, y + 62), fill=TEXT, width=7)
    d.line((x + 38, y + 62, x + 64, y + 28), fill=TEXT, width=7)


def draw_thonny(d, x, y, title="keyboard_car.py", highlight=None, paste_lines=0, shell_lines=None, file_name=None):
    w, h = 420, 340
    d.rounded_rectangle((x, y, x + w, y + h), radius=28, fill="#f5f5f1", outline=TEXT, width=4)
    d.rounded_rectangle((x, y, x + w, y + 52), radius=28, fill="#6f866b")
    for i in range(3):
        d.ellipse((x + 24 + i * 22, y + 18, x + 36 + i * 22, y + 30), fill="#e4ece1")
    d.text((x + 110, y + 10), title, font=BODY_FONT, fill="#f8fbf5")
    for label, bx in (("Open", x + 24), ("Run", x + 132), ("Shell", x + 240)):
        active = highlight == label
        fill = "#67ab64" if active else "#ffffff"
        tfill = "#ffffff" if active else TEXT
        d.rounded_rectangle((bx, y + 72, bx + 92, y + 110), radius=18, fill=fill, outline="#c7d0d8", width=2)
        d.text((bx + 18, y + 80), label, font=SMALL_FONT, fill=tfill)
    d.rounded_rectangle((x + 24, y + 132, x + w - 24, y + h - 24), radius=18, fill="#fffaf0", outline="#d8d2c8", width=2)
    if file_name:
        d.rounded_rectangle((x + 56, y + 270, x + w - 56, y + 320), radius=14, fill=GREEN, outline=TEAL, width=3)
        d.text((x + 82, y + 282), file_name, font=SMALL_FONT, fill=TEXT)
    if paste_lines:
        for i in range(paste_lines):
            yy = y + 162 + i * 24
            d.rounded_rectangle((x + 48, yy, x + w - 48, yy + 16), radius=8, fill="#7da2c4")
    if shell_lines:
        yy = y + 162
        for line in shell_lines:
            d.text((x + 48, yy), line, font=BODY_FONT, fill=TEXT)
            yy += 42


def draw_arrow(d, start, end, color=GOLD, width=12):
    d.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 24
    left = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    right = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    d.polygon([end, left, right], fill=color)


def draw_curved_arrow(d, bbox, start_deg, end_deg, color, width=12):
    d.arc(bbox, start=start_deg, end=end_deg, fill=color, width=width)
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    rx = (bbox[2] - bbox[0]) / 2
    ry = (bbox[3] - bbox[1]) / 2
    ang = math.radians(end_deg)
    ex = cx + rx * math.cos(ang)
    ey = cy + ry * math.sin(ang)
    tangent = ang + math.pi / 2
    size = 22
    left = (ex - size * math.cos(tangent - math.pi / 6), ey - size * math.sin(tangent - math.pi / 6))
    right = (ex - size * math.cos(tangent + math.pi / 6), ey - size * math.sin(tangent + math.pi / 6))
    d.polygon([(ex, ey), left, right], fill=color)


def draw_keyboard(d, x, y, active=None):
    positions = {"W": (x + 120, y), "A": (x, y + 100), "S": (x + 120, y + 100), "D": (x + 240, y + 100), "X": (x + 120, y + 200)}
    for key, (kx, ky) in positions.items():
        fill = GOLD if key == active else "#ffffff"
        d.rounded_rectangle((kx, ky, kx + 88, ky + 88), radius=22, fill=fill, outline=TEXT, width=4)
        bbox = d.textbbox((0, 0), key, font=BODY_FONT)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text((kx + (88 - tw) / 2, ky + (88 - th) / 2 - 4), key, font=BODY_FONT, fill=TEXT)


def save_gif(name: str, frames, durations):
    pal = [frame.convert("P", palette=Image.ADAPTIVE) for frame in frames]
    pal[0].save(BASE / name, save_all=True, append_images=pal[1:], duration=durations, loop=0)


def step_01():
    frames = []
    for i, offset in enumerate((0, -8, 0)):
        img, d = base_card(1, "Ready the car", "Place it on a flat desk")
        draw_car(d, 820, 330 + offset, 1.2)
        draw_label(d, 72, 315, 250, 58, "Stable position", GOLD if i == 1 else ACCENT)
        frames.append(img)
    return frames, [900, 650, 900]


def step_02():
    frames = []
    for i, glow in enumerate((False, True, False)):
        img, d = base_card(2, "Make some space", "Keep the desk clear")
        draw_laptop(d, 650, 250, 330, 220)
        draw_car(d, 930, 545, 0.9)
        fill = "#fce0dc" if glow else "#f4efe6"
        d.rounded_rectangle((620, 220, 1180, 690), radius=34, outline=RED if glow else LINE, width=6, fill=None)
        draw_label(d, 72, 315, 250, 58, "Leave clear space", GOLD if glow else ACCENT)
        frames.append(img)
    return frames, [800, 800, 1000]


def step_03():
    frames = []
    img, d = base_card(3, "Connect USB", "Link the car and laptop")
    draw_laptop(d, 630, 230, 390, 250)
    draw_car(d, 930, 540, 0.95)
    draw_usb(d, 870, 500, 970, 530, connected=False)
    draw_label(d, 72, 315, 220, 58, "No USB yet", RED)
    frames.append(img)

    img, d = base_card(3, "Connect USB", "Link the car and laptop")
    draw_laptop(d, 630, 230, 390, 250)
    draw_car(d, 930, 540, 0.95)
    draw_usb(d, 870, 500, 970, 530, connected=False)
    draw_arrow(d, (875, 498), (948, 518), color=GOLD)
    draw_label(d, 72, 315, 220, 58, "Plug in USB", GOLD)
    frames.append(img)

    img, d = base_card(3, "Connect USB", "Link the car and laptop")
    draw_laptop(d, 630, 230, 390, 250)
    draw_car(d, 930, 540, 0.95)
    draw_usb(d, 870, 500, 970, 530, connected=True)
    draw_label(d, 72, 315, 230, 58, "USB connected", GREEN)
    draw_check(d, 1035, 300)
    d.text((1135, 320), "Connected", font=BODY_FONT, fill=TEXT)
    frames.append(img)
    return frames, [900, 800, 1200]


def step_04():
    frames = []
    for i, checked in enumerate((False, True, True)):
        img, d = base_card(4, "Teacher check", "Wait for the green light")
        draw_teacher(d, 720, 260)
        draw_laptop(d, 920, 310, 220, 150)
        draw_car(d, 860, 530, 0.9)
        if checked:
            draw_check(d, 1020, 220)
            draw_label(d, 72, 315, 220, 58, "Teacher says OK", GREEN)
        else:
            draw_label(d, 72, 315, 220, 58, "Please wait", ACCENT)
        frames.append(img)
    return frames, [700, 800, 1100]


def step_05():
    frames = []
    for active in ("Open", "Run", "Run"):
        img, d = base_card(5, "Open Thonny", "Launch the coding tool")
        draw_thonny(d, 680, 220, title="Thonny", highlight=active)
        draw_label(d, 72, 315, 220, 58, "Open the app", GOLD if active == "Open" else GREEN)
        frames.append(img)
    return frames, [700, 700, 1000]


def step_06():
    frames = []
    for glow in (False, True, False):
        img, d = base_card(6, "Check interpreter", "It should say Pico")
        draw_thonny(d, 650, 220, title="Thonny", highlight="Run")
        outline = GOLD if glow else LINE
        d.rounded_rectangle((770, 520, 1115, 610), radius=18, outline=outline, width=6)
        d.text((815, 550), "MicroPython (Pico)", font=SMALL_FONT, fill=TEXT)
        draw_label(d, 72, 315, 240, 58, "Look at bottom right", GOLD if glow else ACCENT)
        frames.append(img)
    return frames, [700, 900, 900]


def step_07():
    frames = []
    img, d = base_card(7, "Switch to Pico", "Change it before coding")
    draw_thonny(d, 650, 220, title="Thonny", highlight="Run")
    d.rounded_rectangle((700, 520, 930, 610), radius=18, fill=ROSE, outline="#d08b84", width=4)
    d.text((760, 550), "Wrong", font=BODY_FONT, fill=TEXT)
    draw_label(d, 72, 315, 230, 58, "Wrong setting", RED)
    frames.append(img)

    img, d = base_card(7, "Switch to Pico", "Change it before coding")
    draw_thonny(d, 650, 220, title="Thonny", highlight="Run")
    d.rounded_rectangle((700, 520, 930, 610), radius=18, fill=ROSE, outline="#d08b84", width=4)
    d.text((760, 550), "Wrong", font=BODY_FONT, fill=TEXT)
    draw_arrow(d, (945, 565), (1060, 565), color=GOLD)
    draw_label(d, 72, 315, 220, 58, "Switch to Pico", GOLD)
    frames.append(img)

    img, d = base_card(7, "Switch to Pico", "Change it before coding")
    draw_thonny(d, 650, 220, title="Thonny", highlight="Run")
    d.rounded_rectangle((1070, 520, 1210, 610), radius=18, fill=GREEN, outline=TEAL, width=4)
    d.text((1105, 550), "Pico", font=BODY_FONT, fill=TEXT)
    draw_label(d, 72, 315, 220, 58, "Correct now", GREEN)
    frames.append(img)
    return frames, [800, 750, 1100]


def step_08():
    frames = []
    img, d = base_card(8, "New file", "Open a blank .py file")
    draw_thonny(d, 650, 220, title="Thonny", highlight="Open")
    draw_label(d, 72, 315, 220, 58, "Click File > New", GOLD)
    frames.append(img)

    img, d = base_card(8, "New file", "Open a blank .py file")
    draw_thonny(d, 650, 220, title="Thonny", highlight="Open")
    d.rounded_rectangle((840, 330, 1070, 460), radius=18, fill="#ffffff", outline=TEXT, width=4)
    d.text((900, 375), "New .py", font=BODY_FONT, fill=TEXT)
    draw_label(d, 72, 315, 220, 58, "Blank file ready", GREEN)
    frames.append(img)
    return frames, [850, 1100]


def step_09():
    frames = []
    for pos in (240, 380, 520):
        img, d = base_card(9, "Find the code", "Scroll to the full program")
        d.rounded_rectangle((650, 200, 1140, 650), radius=26, fill="#f6f7fb", outline=TEXT, width=4)
        d.text((705, 215), "Lesson page", font=BODY_FONT, fill=TEXT)
        for i in range(5):
            d.rounded_rectangle((700, 260 + i * 68, 1090, 306 + i * 68), radius=12, fill=LIGHT)
        d.rounded_rectangle((860, pos, 1090, pos + 70), radius=20, fill=GOLD)
        d.text((900, pos + 16), "Code block", font=BODY_FONT, fill=TEXT)
        draw_arrow(d, (1160, 240), (1160, 610), color=TEAL)
        draw_label(d, 72, 315, 220, 58, "Scroll down", GOLD if pos != 520 else GREEN)
        frames.append(img)
    return frames, [700, 700, 1100]


def step_10():
    frames = []
    img, d = base_card(10, "Copy code", "Copy from the web page")
    draw_label(d, 72, 315, 220, 58, "1. Click COPY", GOLD)
    draw_web_card(d, 620, 180, highlight=True)
    draw_thonny(d, 920, 220, paste_lines=0)
    frames.append(img)

    img, d = base_card(10, "Copy code", "Copy from the web page")
    draw_label(d, 72, 315, 250, 58, "2. Move to Thonny", ACCENT)
    draw_web_card(d, 620, 180, highlight=True)
    draw_thonny(d, 920, 220, paste_lines=0)
    draw_arrow(d, (870, 390), (920, 390), color=GOLD)
    frames.append(img)

    img, d = base_card(10, "Copy code", "Copy from the web page")
    draw_label(d, 72, 315, 240, 58, "3. Paste code", GREEN)
    draw_web_card(d, 650, 180, highlight=False)
    draw_thonny(d, 920, 220, paste_lines=3)
    draw_arrow(d, (890, 390), (940, 390), color=TEAL)
    frames.append(img)

    img, d = base_card(10, "Copy code", "Copy from the web page")
    draw_label(d, 72, 315, 260, 58, "4. Ready to run", GREEN)
    draw_web_card(d, 620, 180, highlight=False)
    draw_thonny(d, 920, 220, paste_lines=6)
    frames.append(img)
    return frames, [800, 700, 700, 1100]


def draw_web_card(d, x, y, highlight=False):
    w, h = 250, 420
    d.rounded_rectangle((x, y, x + w, y + h), radius=28, fill="#ffffff", outline=TEXT, width=4)
    d.text((x + 58, y + 26), "Web code", font=BODY_FONT, fill=TEXT)
    for i in range(5):
        d.rounded_rectangle((x + 40, y + 92 + i * 64, x + w - 40, y + 124 + i * 64), radius=10, fill=LIGHT)
    btn_fill = GOLD if highlight else "#f3e2b3"
    d.rounded_rectangle((x + 42, y + h - 78, x + w - 42, y + h - 18), radius=18, fill=btn_fill)
    d.text((x + 88, y + h - 62), "Copy", font=BODY_FONT, fill=TEXT)


def step_11():
    frames = []
    img, d = base_card(11, "Paste code", "Put it in your new file")
    draw_label(d, 72, 315, 220, 58, "Paste here", GOLD)
    draw_thonny(d, 760, 220, title="keyboard_car.py", paste_lines=0)
    draw_arrow(d, (700, 390), (760, 390), color=GOLD)
    frames.append(img)

    img, d = base_card(11, "Paste code", "Put it in your new file")
    draw_label(d, 72, 315, 240, 58, "Code inserted", GREEN)
    draw_thonny(d, 760, 220, title="keyboard_car.py", paste_lines=6)
    frames.append(img)
    return frames, [850, 1100]


def step_12():
    frames = []
    img, d = base_card(12, "Save file", "Use keyboard_car.py")
    draw_thonny(d, 650, 220, title="keyboard_car.py", paste_lines=6)
    draw_label(d, 72, 315, 220, 58, "Press Ctrl + S", GOLD)
    frames.append(img)

    img, d = base_card(12, "Save file", "Use keyboard_car.py")
    draw_thonny(d, 650, 220, title="keyboard_car.py", paste_lines=6, file_name="keyboard_car.py")
    draw_label(d, 72, 315, 210, 58, "Saved", GREEN)
    frames.append(img)
    return frames, [800, 1200]


def step_13():
    frames = []
    for glow in (False, True, False):
        img, d = base_card(13, "Run program", "Press the green Run button")
        draw_thonny(d, 650, 220, title="keyboard_car.py", highlight="Run" if glow else None, paste_lines=6)
        draw_label(d, 72, 315, 220, 58, "Click Run", GOLD if glow else ACCENT)
        frames.append(img)
    return frames, [700, 900, 1000]


def step_14():
    frames = []
    img, d = base_card(14, "Click Shell", "Type commands here")
    draw_thonny(d, 650, 220, title="Shell", highlight=None, shell_lines=["", "", ""])
    draw_label(d, 72, 315, 220, 58, "Click Shell", GOLD)
    frames.append(img)

    img, d = base_card(14, "Click Shell", "Type commands here")
    draw_thonny(d, 650, 220, title="Shell", highlight="Shell", shell_lines=[">>>", "cursor ready", ""])
    draw_label(d, 72, 315, 210, 58, "Ready to type", GREEN)
    frames.append(img)
    return frames, [850, 1200]


def step_15():
    frames = []
    img, d = base_card(15, "Type x first", "Stop is the safest start")
    draw_keyboard(d, 700, 220, active="X")
    draw_car(d, 930, 520, 0.85)
    draw_label(d, 72, 315, 220, 58, "Type x", GOLD)
    frames.append(img)

    img, d = base_card(15, "Type x first", "Stop is the safest start")
    draw_keyboard(d, 700, 220, active="X")
    draw_car(d, 930, 520, 0.85)
    draw_check(d, 1090, 300)
    draw_label(d, 72, 315, 220, 58, "Car can stop", GREEN)
    frames.append(img)
    return frames, [900, 1100]


def step_16():
    frames = []
    actions = [
        ("W", "Forward", (1035, 515), (1190, 515), TEAL, GOLD),
        ("A", "Turn left", None, None, TEAL, ACCENT),
        ("D", "Turn right", None, None, TEAL, ACCENT),
        ("S", "Backward", (1190, 515), (1035, 515), RED, ACCENT),
    ]
    for key, label, start, end, color, badge in actions:
        img, d = base_card(16, "Test the keys", label)
        draw_keyboard(d, 620, 220, active=key)
        draw_car(d, 900, 520, 0.95)
        if key == "W":
            draw_arrow(d, start, end, color=color)
        elif key == "S":
            draw_arrow(d, start, end, color=color)
        elif key == "A":
            draw_curved_arrow(d, (905, 345, 1185, 595), 210, 310, color)
        elif key == "D":
            draw_curved_arrow(d, (905, 345, 1185, 595), 330, 70, color)
        draw_label(d, 72, 315, 220, 58, f"Press {key}", badge)
        frames.append(img)
    return frames, [900, 900, 900, 1200]


def step_17():
    frames = []
    img, d = base_card(17, "Stop each time", "Press x between moves")
    draw_keyboard(d, 700, 220, active="W")
    draw_car(d, 930, 520, 0.85)
    draw_arrow(d, (1035, 515), (1150, 515), color=TEAL)
    draw_label(d, 72, 315, 220, 58, "Move first", GOLD)
    frames.append(img)

    img, d = base_card(17, "Stop each time", "Press x between moves")
    draw_keyboard(d, 700, 220, active="X")
    draw_car(d, 930, 520, 0.85)
    draw_label(d, 72, 315, 250, 58, "Then press X", GREEN)
    frames.append(img)
    return frames, [850, 1100]


def step_18():
    frames = []
    img, d = base_card(18, "Forward then stop", "Try w -> x")
    draw_keyboard(d, 680, 220, active="W")
    draw_car(d, 900, 520, 0.9)
    draw_arrow(d, (1020, 515), (1170, 515), color=TEAL)
    draw_label(d, 72, 315, 220, 58, "1. W", GOLD)
    frames.append(img)

    img, d = base_card(18, "Forward then stop", "Try w -> x")
    draw_keyboard(d, 680, 220, active="X")
    draw_car(d, 900, 520, 0.9)
    draw_check(d, 1090, 300)
    draw_label(d, 72, 315, 220, 58, "2. X", GREEN)
    frames.append(img)
    return frames, [850, 1100]


def step_19():
    frames = []
    img, d = base_card(19, "Turn challenge", "Try w -> a -> x")
    draw_keyboard(d, 620, 220, active="W")
    draw_car(d, 900, 520, 0.9)
    draw_arrow(d, (1020, 515), (1155, 515), color=TEAL)
    draw_label(d, 72, 315, 220, 58, "1. W", GOLD)
    frames.append(img)

    img, d = base_card(19, "Turn challenge", "Try w -> a -> x")
    draw_keyboard(d, 620, 220, active="A")
    draw_car(d, 900, 520, 0.9)
    draw_curved_arrow(d, (905, 345, 1185, 595), 210, 310, TEAL)
    draw_label(d, 72, 315, 220, 58, "2. A", ACCENT)
    frames.append(img)

    img, d = base_card(19, "Turn challenge", "Try w -> a -> x")
    draw_keyboard(d, 620, 220, active="X")
    draw_car(d, 900, 520, 0.9)
    draw_check(d, 1090, 300)
    draw_label(d, 72, 315, 220, 58, "3. X", GREEN)
    frames.append(img)
    return frames, [850, 850, 1100]


def step_20():
    frames = []
    labels = [
        ("W", "Forward"),
        ("A", "Left"),
        ("S", "Backward"),
        ("D", "Right"),
        ("X", "Stop"),
    ]
    for key, meaning in labels:
        img, d = base_card(20, "Know the keys", "Say what each key does")
        draw_keyboard(d, 650, 220, active=key)
        draw_car(d, 960, 520, 0.8)
        draw_label(d, 72, 315, 240, 58, f"{key} = {meaning}", GOLD if key == "W" else ACCENT)
        frames.append(img)
    return frames, [650, 650, 650, 650, 1000]


GENERATORS = {
    1: step_01,
    2: step_02,
    3: step_03,
    4: step_04,
    5: step_05,
    6: step_06,
    7: step_07,
    8: step_08,
    9: step_09,
    10: step_10,
    11: step_11,
    12: step_12,
    13: step_13,
    14: step_14,
    15: step_15,
    16: step_16,
    17: step_17,
    18: step_18,
    19: step_19,
    20: step_20,
}


def main():
    for step_no, generator in GENERATORS.items():
        frames, durations = generator()
        save_gif(f"bootcamp-step-{step_no:02d}.gif", frames, durations)
    print("generated", len(GENERATORS), "bootcamp step gifs")


if __name__ == "__main__":
    main()
