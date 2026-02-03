import json
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account

# ---------- Config ----------
CREDENTIALS_URL = "https://example.com/credentials.json"  # URL of your service account JSON
SCOPES = ['https://www.googleapis.com/auth/presentations']
PRESENTATION_ID = 'YOUR_PRESENTATION_ID_HERE'  # Replace with your Slides ID
SLIDE_INDEX = 1  # Slide 2 (0-based index)
IMAGE_URL = 'https://example.com/menu.png'  # Replace with your hosted menu image URL

# ---------- Download credentials JSON from URL ----------
response = requests.get(CREDENTIALS_URL)
if response.status_code != 200:
    raise Exception(f"Failed to download credentials.json from {CREDENTIALS_URL}")

service_account_info = response.json()

# ---------- Authenticate using service account info ----------
creds = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)
slides_service = build('slides', 'v1', credentials=creds)

# ---------- Get slide ID ----------
presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
slides = presentation.get('slides')
slide_id = slides[SLIDE_INDEX]['objectId']

# ---------- Optional: delete existing elements on slide 2 ----------
requests_list = [
    {
        'deleteObject': {
            'objectId': element['objectId']
        }
    } for element in slides[SLIDE_INDEX]['pageElements']
]

# ---------- Insert new image from URL ----------
requests_list.append({
    'createImage': {
        'url': IMAGE_URL,
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'height': {'magnitude': 600, 'unit': 'PT'},  # adjust as needed
                'width': {'magnitude': 450, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 50,  # adjust position
                'translateY': 50,
                'unit': 'PT'
            }
        }
    }
})

# ---------- Execute batch update ----------
response = slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests_list}
).execute()

print("Slide 2 updated with new image from URL!")
