from PIL import Image, ImageDraw, ImageFont
import calendar, random

YEAR = 2026
WIDTH, HEIGHT = 900, 1200

# Fonts
try:
    TITLE = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
    BODY = ImageFont.truetype("DejaVuSans.ttf", 26)
except:
    TITLE = BODY = ImageFont.load_default()

# Seasonal themes
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

def decorate(draw, bg):
    for _ in range(350):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 3)
        draw.ellipse((x, y, x + r, y + r), fill="white")

def generate_month(year, month):
    theme = THEMES[MONTH_THEME[month]]
    img = Image.new("RGB", (WIDTH, HEIGHT), theme[0])
    draw = ImageDraw.Draw(img)
    decorate(draw, theme[0])

    month_name = calendar.month_name[month]
    draw.text((WIDTH//2 - 260, 30),
              f"{month_name} {year} Dinner Menu {theme[1]}",
              fill="white", font=TITLE)

    _, days = calendar.monthrange(year, month)
    menu = {d: "TBD" for d in range(1, days + 1)}

    # Fixed rules
    if month == 1:
        menu[29] = "🍗 Chicken Nuggets"
        menu[30] = "🍗 Chicken Nuggets"
        menu[31] = "🍕 Pizza"
    if month == 2:
        menu[1] = "🍕 Pizza"

    y = 120
    for d in range(1, days + 1):
        draw.text((80, y),
                  f"{month_name[:3]} {d:02d}: {menu[d]}",
                  fill="white", font=BODY)
        y += 30

    img.show()

# Generate all months
for m in range(1, 13):
    generate_month(YEAR, m)
