from PIL import Image, ImageDraw, ImageFont
import calendar, random, os, time
from datetime import date, datetime, timedelta

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 1200
YEAR = date.today().year
MONTH = date.today().month
LINE_HEIGHT = 32
CST_OFFSET = -5

# ---------- Fonts ----------
try:
    TITLE = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
    BODY = ImageFont.truetype("DejaVuSans.ttf", 26)
except:
    TITLE = BODY = ImageFont.load_default()

# ---------- THEMES ----------
THEMES = {
    "winter": ("#0b1d3a", "❄️"),
    "valentine": ("#4a0f2e", "❤️"),
    "spring": ("#1f4d2b", "🌸"),
    "summer": ("#1e4fa1", "☀️"),
    "fall": ("#5a2d0c", "🍂"),
}

MONTH_THEME = {
    1: "winter", 2: "valentine", 3: "spring", 4: "spring",
    5: "spring", 6: "summer", 7: "summer", 8: "summer",
    9: "fall", 10: "fall", 11: "fall", 12: "winter"
}

# ---------- FIXED PATTERN ANCHOR (DO NOT CHANGE) ----------
START_CYCLE_DATE = date(2026, 4, 20)  # locked pizza reference

# ---------- ALERT SYSTEM ----------
def get_weather_alert():
    now = datetime.utcnow() + timedelta(hours=CST_OFFSET)

    start_watch = datetime(2026, 4, 24, 17, 0)
    end_watch   = datetime(2026, 4, 25, 6, 0)

    start_warn  = datetime(2026, 4, 25, 6, 0)
    end_warn    = datetime(2026, 4, 25, 18, 0)

    if start_watch <= now < end_watch:
        return {
            "text": "⚠️ EXTREME FIRE WATCH (5PM APR 24 – 6AM APR 25)",
            "color": (255, 220, 0)
        }

    if start_warn <= now < end_warn:
        return {
            "text": "🚨 EXTREME FIRE WARNING (6AM – 6PM APR 25)",
            "color": (255, 140, 0)
        }

    return None

# ---------- HELPERS ----------
def draw_centered_text(draw, text, y, font):
    w = draw.textlength(text, font=font)
    draw.text(((WIDTH - w) // 2, y), text, fill="white", font=font)

def draw_wrapped_text(draw, x, y, text, font):
    import textwrap
    for line in textwrap.wrap(text, 60):
        draw.text((x, y), line, fill="white", font=font)
        y += LINE_HEIGHT
    return y

def decorate(draw):
    for _ in range(400):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        draw.ellipse((x, y, x+2, y+2), fill="white")

# ---------- MAIN ----------
def generate_current_month(folder="images"):
    os.makedirs(folder, exist_ok=True)

    theme_name = MONTH_THEME[MONTH]
    bg_color, emoji = THEMES[theme_name]

    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    decorate(draw)

    # ---------- ALERT ----------
    alert = get_weather_alert()

    if alert:
        flash = int(time.time()) % 2 == 0
        color = alert["color"] if flash else (255, 255, 255)

        draw.rectangle([0, 0, WIDTH, 80], fill=color)
        draw_centered_text(draw, alert["text"], 25, BODY)

    # ---------- TITLE ----------
    title_y = 110 if alert else 40
    month_name = calendar.month_name[MONTH]
    draw_centered_text(draw, f"{month_name} {YEAR} Dinner Menu {emoji}", title_y, TITLE)

    # ---------- DAYS ----------
    _, days = calendar.monthrange(YEAR, MONTH)
    today = date.today()

    menu = {}

    for d in range(1, days + 1):
        current_date = date(YEAR, MONTH, d)

        # 🔁 FIXED PATTERN (never changes)
        delta = (current_date - START_CYCLE_DATE).days
        cycle = (delta // 2) % 2

        menu[d] = "🍕 Pizza" if cycle == 0 else "🍗 Chicken Nuggets"

    # ---------- DRAW ----------
    y = title_y + 100

    for d in range(1, days + 1):
        label = f"{month_name[:3]} {d:02d}: {menu[d]}"

        # highlight today
        if date(YEAR, MONTH, d) == today:
            draw.rectangle([70, y-5, 850, y+28], outline="yellow", width=3)

        y = draw_wrapped_text(draw, 80, y, label, BODY)

    # ---------- SAVE ----------
    path = os.path.join(folder, "menu.png")
    img.save(path)
    print("Saved:", path)

# ---------- RUN ----------
generate_current_month()
