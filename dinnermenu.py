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

# ---------- FIXED PATTERN ANCHOR ----------
START_CYCLE_DATE = date(2026, 4, 20)

# ---------- ALERT SYSTEM ----------
def get_weather_alert():
    now = datetime.utcnow() + timedelta(hours=CST_OFFSET)

    start_watch = datetime(2026, 4, 24, 17, 0)
    end_watch   = datetime(2026, 4, 25, 6, 0)

    start_warn  = datetime(2026, 4, 25, 6, 0)
    end_warn    = datetime(2026, 4, 25, 18, 0)

    if start_watch <= now < end_watch:
        return {
            "text": "EXTREME FIRE WATCH IN EFFECT FROM 5PM APR 24 UNTIL 6AM APR 25 FOR NORTHLAND AND NORTH SHORE and details: look on slide 1",
            "color": (255, 220, 0)
        }

    if start_warn <= now < end_warn:
        return {
            "text": "EXTREME FIRE WARNING IN EFFECT FROM 6AM APR 25 UNTIL 6PM APR 25 FOR NORTHLAND AND NORTH SHORE and details: look on slide 1",
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

    # ---------- ALERT (FIXED FIT VERSION) ----------
    alert = get_weather_alert()

    if alert:
        flash = int(time.time()) % 2 == 0
        color = alert["color"] if flash else (255, 255, 255)

        # banner
        draw.rectangle([0, 0, WIDTH, 110], fill=color)

        # WRAP TEXT so it ALWAYS fits
        import textwrap
        lines = textwrap.wrap(alert["text"], width=50)

        y_text = 10
        for line in lines:
            w = draw.textlength(line, font=BODY)
            draw.text(((WIDTH - w) // 2, y_text),
                      line,
                      fill="black",
                      font=BODY)
            y_text += 28

    # ---------- TITLE ----------
    title_y = 130 if alert else 40
    month_name = calendar.month_name[MONTH]
    draw_centered_text(draw, f"{month_name} {YEAR} Dinner Menu {emoji}", title_y, TITLE)

    # ---------- MENU ----------
    _, days = calendar.monthrange(YEAR, MONTH)
    today = date.today()

    menu = {}

    for d in range(1, days + 1):
        current_date = date(YEAR, MONTH, d)

        delta = (current_date - START_CYCLE_DATE).days
        cycle = (delta // 2) % 2

        menu[d] = "🍕 Pizza" if cycle == 0 else "🍗 Chicken Nuggets"

    # ---------- DRAW ----------
    y = title_y + 110

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
