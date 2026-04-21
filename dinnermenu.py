from PIL import Image, ImageDraw, ImageFont
import calendar, random, os
from datetime import date

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 1200
YEAR = date.today().year
MONTH = date.today().month
LINE_HEIGHT = 32

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

# ---------- Helpers ----------
def decorate(draw):
    for _ in range(400):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 3)
        draw.ellipse((x, y, x + r, y + r), fill="white")

def draw_centered_text(draw, text, y, font):
    w = draw.textlength(text, font=font)
    draw.text(((WIDTH - w) // 2, y), text, fill="white", font=font)

def draw_wrapped_text(draw, x, y, text, font, max_width=55):
    import textwrap
    for line in textwrap.wrap(text, max_width):
        draw.text((x, y), line, fill="white", font=font)
        y += LINE_HEIGHT
    return y

# ---------- Generate ----------
def generate_current_month(folder="images"):
    os.makedirs(folder, exist_ok=True)

    theme_name = MONTH_THEME[MONTH]
    bg_color, emoji = THEMES[theme_name]

    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    decorate(draw)

    month_name = calendar.month_name[MONTH]
    draw_centered_text(draw, f"{month_name} {YEAR} Dinner Menu {emoji}", 30, TITLE)

    _, days = calendar.monthrange(YEAR, MONTH)

    menu = {}

    # ---------- SIMPLE PATTERN ----------
    # Day 1 = Pizza
    # Days 2–3 = Nuggets
    # Days 4 = Pizza
    # Days 5–6 = Nuggets
    # repeat

    for d in range(1, days + 1):
        if d == 1:
            menu[d] = "🍕 Pizza"
        else:
            chunk = (d - 2) // 2
            if chunk % 2 == 0:
                menu[d] = "🍗 Chicken Nuggets"
            else:
                menu[d] = "🍕 Pizza"

    # ---------- Draw ----------
    y = 120
    for d in range(1, days + 1):
        label = f"{month_name[:3]} {d:02d}: {menu[d]}"
        y = draw_wrapped_text(draw, 80, y, label, BODY)

    # ---------- Save ----------
    file_path = os.path.join(folder, "menu.png")
    img.save(file_path)
    print(f"Saved current month image: {file_path}")

# ---------- Run ----------
generate_current_month()
