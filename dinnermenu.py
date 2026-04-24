from PIL import Image, ImageDraw, ImageFont
import calendar, random, os, time
from datetime import date, datetime, timedelta

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 1200
YEAR = date.today().year
MONTH = date.today().month
LINE_HEIGHT = 32
CST_OFFSET = -5  # match weather system

# ---------- Fonts ----------
try:
    TITLE = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
    BODY = ImageFont.truetype("DejaVuSans.ttf", 26)
except:
    TITLE = BODY = ImageFont.load_default()

# ---------- Themes ----------
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

# ---------- FIXED RULE ----------
START_CYCLE_DATE = date(2026, 4, 22)

# ---------- ALERT LOGIC ----------
def get_weather_alert():
    now = datetime.utcnow() + timedelta(hours=CST_OFFSET)

    start_watch = datetime(2026, 4, 24, 17, 0)
    end_watch   = datetime(2026, 4, 25, 6, 0)

    start_warn  = datetime(2026, 4, 25, 6, 0)
    end_warn    = datetime(2026, 4, 25, 18, 0)

    if start_watch <= now < end_watch:
        return {
            "text": "⚠️ PLEASE LOOK AT SLIDE 1: EXTREME FIRE WATCH (5PM APR 24 – 6AM APR 25)",
            "color": (255, 220, 0)
        }

    elif start_warn <= now < end_warn:
        return {
            "text": "🚨 PLEASE LOOK AT SLIDE 1: EXTREME FIRE WARNING (6AM – 6PM APR 25)",
            "color": (255, 140, 0)
        }

    return None

# ---------- Helpers ----------
def draw_centered_text(draw, text, y, font):
    w = draw.textlength(text, font=font)
    draw.text(((WIDTH - w) // 2, y), text, fill="white", font=font)

def draw_wrapped_text(draw, x, y, text, font, max_width=55):
    import textwrap
    for line in textwrap.wrap(text, max_width):
        draw.text((x, y), line, fill="white", font=font)
        y += LINE_HEIGHT
    return y

def decorate(draw):
    for _ in range(400):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 3)
        draw.ellipse((x, y, x + r, y + r), fill="white")

# ---------- GENERATE ----------
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

        text_w = draw.textlength(alert["text"], font=BODY)
        draw.text(((WIDTH - text_w) // 2, 25),
                  alert["text"],
                  fill="black",
                  font=BODY)

    # ---------- TITLE ----------
    title_y = 100 if alert else 30
    month_name = calendar.month_name[MONTH]
    draw_centered_text(draw, f"{month_name} {YEAR} Dinner Menu {emoji}", title_y, TITLE)

    # ---------- MENU ----------
    _, days = calendar.monthrange(YEAR, MONTH)
    menu = {}

    for d in range(1, days + 1):
        current_date = date(YEAR, MONTH, d)

        if current_date in [date(2026, 4, 20), date(2026, 4, 21)]:
            menu[d] = "🍕 Pizza"
            continue

        if current_date < START_CYCLE_DATE:
            menu[d] = "🍕 Pizza"
            continue

        delta = (current_date - START_CYCLE_DATE).days
        cycle = (delta // 2) % 2

        menu[d] = "🍕 Pizza" if cycle == 0 else "🍗 Chicken Nuggets"

    # ---------- DRAW MENU ----------
    y = title_y + 90

    for d in range(1, days + 1):
        label = f"{month_name[:3]} {d:02d}: {menu[d]}"
        y = draw_wrapped_text(draw, 80, y, label, BODY)

    # ---------- SAVE ----------
    file_path = os.path.join(folder, "menu.png")
    img.save(file_path)
    print("Saved:", file_path)

# ---------- RUN ----------
generate_current_month()
