import os
import json
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ---------- Config ----------
SCOPES = ['https://www.googleapis.com/auth/presentations']
PRESENTATION_ID = '2'  # Replace with your Slides ID
SLIDE_INDEX = 1  # Slide 2 (0-based index)
IMAGE_URL = 'https://example.com/menu.png'  # Replace with your hosted menu image URL

# ---------- Load OAuth client info from environment ----------
client_secrets_json = os.environ.get("CLIENT_SECRETS_JSON")
if not client_secrets_json:
    raise Exception("Environment variable CLIENT_SECRETS_JSON not set!")
client_secrets = json.loads(client_secrets_json)

# ---------- Authenticate ----------
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_config(client_secrets, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

slides_service = build('slides', 'v1', credentials=creds)

# ---------- Get slide ID ----------
presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
slides = presentation.get('slides')
slide_id = slides[SLIDE_INDEX]['objectId']

# ---------- Delete existing elements on slide 2 ----------
requests_list = [
    {'deleteObject': {'objectId': element['objectId']}}
    for element in slides[SLIDE_INDEX]['pageElements']
]

# ---------- Insert new image from URL ----------
requests_list.append({
    'createImage': {
        'url': IMAGE_URL,
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'height': {'magnitude': 600, 'unit': 'PT'},
                'width': {'magnitude': 450, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 50,
                'translateY': 50,
                'unit': 'PT'
            }
        }
    }
})

# ---------- Execute batch update ----------
slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests_list}
).execute()

print("Slide 2 updated with new image from URL!")
