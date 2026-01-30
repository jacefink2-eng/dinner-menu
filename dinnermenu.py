from PIL import Image, ImageDraw, ImageFont
import calendar, random, os
from datetime import date

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 1200
YEAR = date.today().year
MONTH = date.today().month  # Current month only

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
        draw.ellipse((x, y, x+r, y+r), fill="white")

# ---------- Generate current month image ----------
def generate_current_month(folder="images"):
    os.makedirs(folder, exist_ok=True)

    theme = THEMES[MONTH_THEME[MONTH]]
    img = Image.new("RGB", (WIDTH, HEIGHT), theme[0])
    draw = ImageDraw.Draw(img)
    decorate(draw)

    month_name = calendar.month_name[MONTH]
    draw.text((WIDTH//2 - 260, 30),
              f"{month_name} {YEAR} Dinner Menu {theme[1]}",
              fill="white", font=TITLE)

    _, days = calendar.monthrange(YEAR, MONTH)
    menu = {d: "TBD" for d in range(1, days+1)}

    # Fixed meals example for Jan/Feb 2026
    if YEAR == 2026 and MONTH == 1:
        menu[29] = "🍗 Chicken Nuggets"
        menu[30] = "🍗 Chicken Nuggets"
        menu[31] = "🍕 Pizza"
    if YEAR == 2026 and MONTH == 2:
        menu[1] = "🍕 Pizza"

    y = 120
    for d in range(1, days+1):
        draw.text((80, y),
                  f"{month_name[:3]} {d:02d}: {menu[d]}",
                  fill="white", font=BODY)
        y += 30

    # Save only the current month
    file_path = os.path.join(folder, f"menu.png")
    img.save(file_path)
    print(f"Saved current month image: {file_path}")

# ---------- Run ----------
generate_current_month()
