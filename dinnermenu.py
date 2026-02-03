import os
import json
import calendar
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 900, 1200
LINE_HEIGHT = 32
SLIDE_INDEX = 1  # Slide 2
MENU_IMAGE_PATH = "https://jacefink2-eng.github.io/dinner-menu/images/menu.png"
PRESENTATION_ID = "2"  # Replace with your Slides ID

# ---------------- Fonts ----------------
try:
    TITLE = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
    BODY = ImageFont.truetype("DejaVuSans.ttf", 26)
except:
    TITLE = BODY = ImageFont.load_default()

# ---------------- Generate menu image ----------------
def generate_menu_image(path=MENU_IMAGE_PATH):
    today = date.today()
    year = today.year
    month = today.month

    img = Image.new("RGB", (WIDTH, HEIGHT), "#4a0f2e")  # Valentine/fallback theme
    draw = ImageDraw.Draw(img)

    # Title
    month_name = calendar.month_name[month]
    title_text = f"{month_name} {year} Dinner Menu ❤️"
    draw.text(((WIDTH - draw.textlength(title_text, TITLE)) // 2, 30), title_text, fill="white", font=TITLE)

    # Menu: Pizza / Chicken Nuggets 2/2 cycle
    _, days = calendar.monthrange(year, month)
    menu = {}
    for d in range(1, days + 1):
        if d == 1:
            menu[d] = "🍕 Pizza"
        else:
            cycle_day = (d - 2) % 4
            menu[d] = "🍗 Chicken Nuggets" if cycle_day < 2 else "🍕 Pizza"

    # Draw menu
    y = 120
    for d in range(1, days + 1):
        text = f"{month_name[:3]} {d:02d}: {menu[d]}"
        draw.text((80, y), text, fill="white", font=BODY)
        y += LINE_HEIGHT

    img.save(path)
    print(f"Saved menu image: {path}")

# ---------------- Authenticate service account ----------------
def get_service_account_credentials():
    client_secrets_json = os.environ.get("CLIENT_SECRETS_JSON")
    if not client_secrets_json:
        raise Exception("Environment variable CLIENT_SECRETS_JSON not set!")

    sa_info = json.loads(client_secrets_json)
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/presentations'
    ]
    creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
    return creds

# ---------------- Upload image to Google Drive and get public URL ----------------
def upload_to_drive(file_path, creds):
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='image/png', resumable=True)

    # Upload
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Make public
    drive_service.permissions().create(
        fileId=uploaded_file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    # Public URL
    public_url = f"https://drive.google.com/uc?id={uploaded_file['id']}"
    print(f"Uploaded menu image to Drive: {public_url}")
    return public_url

# ---------------- Update Google Slides ----------------
def update_slide_with_image(service, image_url):
    presentation = service.presentations().get(presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')
    slide_id = slides[SLIDE_INDEX]['objectId']

    # Delete existing elements
    requests_list = [{'deleteObject': {'objectId': e['objectId']}} for e in slides[SLIDE_INDEX]['pageElements']]

    # Insert new image using public URL
    requests_list.append({
        'createImage': {
            'url': image_url,
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'height': {'magnitude': 600, 'unit': 'PT'},
                         'width': {'magnitude': 450, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 50, 'unit': 'PT'}
            }
        }
    })

    service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={'requests': requests_list}
    ).execute()
    print(f"Slide {SLIDE_INDEX + 1} updated with menu image URL.")

# ---------------- Main ----------------
if __name__ == "__main__":
    generate_menu_image()
    creds = get_service_account_credentials()
    public_url = upload_to_drive(MENU_IMAGE_PATH, creds)
    slides_service = build('slides', 'v1', credentials=creds)
    update_slide_with_image(slides_service, public_url)
