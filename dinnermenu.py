import os
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
SLIDE_INDEX = 1  # Slide 2 (0-based)
MENU_IMAGE_URL = "https://jacefink2-eng.github.io/dinner-menu/images/menu.png"  # Must be a publicly hosted image URL
PRESENTATION_ID = "1CfOub_Ulj0yT89RGfEK4D2ZFdIp3qi-KVjmS8xdi8u8"  # Replace with your Google Slides ID

# ---------------- Authenticate using service account ----------------
def get_service_account_credentials():
    client_secrets_json = os.environ.get("CLIENT_SECRETS_JSON")
    if not client_secrets_json:
        raise Exception("Environment variable CLIENT_SECRETS_JSON not set!")

    sa_info = json.loads(client_secrets_json)
    scopes = ['https://www.googleapis.com/auth/presentations']
    creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
    return creds

# ---------------- Update Google Slides ----------------
def update_slide_with_image(service, image_url):
    if not image_url:
        raise Exception("MENU_IMAGE_URL is not set!")

    presentation = service.presentations().get(presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')
    slide_id = slides[SLIDE_INDEX]['objectId']

    # Delete existing elements
    requests_list = [{'deleteObject': {'objectId': e['objectId']}} for e in slides[SLIDE_INDEX]['pageElements']]

    # Insert new image from URL
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
    print(f"Slide {SLIDE_INDEX + 1} updated with menu image URL: {image_url}")

# ---------------- Main ----------------
if __name__ == "__main__":
    creds = get_service_account_credentials()
    slides_service = build('slides', 'v1', credentials=creds)
    update_slide_with_image(slides_service, MENU_IMAGE_URL)
