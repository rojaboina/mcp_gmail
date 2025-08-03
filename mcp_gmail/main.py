from fastapi import FastAPI

app = FastAPI(title="MCP Gmail Server", description="Read and summarize Gmail emails via MCP.")

@app.get("/")
def root():
    return {"message": "MCP Gmail server is running."}

# Gmail API integration imports
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
import os
import pathlib
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest
import pickle

# Set up paths and scopes
BASE_DIR = pathlib.Path(__file__).parent.parent
TOKEN_PATH = BASE_DIR / 'token.pickle'
CREDENTIALS_PATH = BASE_DIR / 'credentials.json'  # User must provide this file from Google Cloud Console
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Endpoint: Start Gmail OAuth2 flow
@app.get("/auth/gmail")
def gmail_auth():
    if not CREDENTIALS_PATH.exists():
        return JSONResponse({"error": "Missing credentials.json. Please download from Google Cloud Console and place in project root."}, status_code=400)
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri="http://localhost:8001/auth/gmail/callback"
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)

# Endpoint: OAuth2 callback
@app.get("/auth/gmail/callback")
def gmail_auth_callback(request: Request):
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri="http://localhost:8001/auth/gmail/callback"
    )
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)
    return {"message": "Gmail authentication successful. Token saved."}

# Endpoint: Fetch emails (requires authentication)
@app.get("/emails")
def get_emails():
    if not TOKEN_PATH.exists():
        return JSONResponse({"error": "Not authenticated. Please visit /auth/gmail first."}, status_code=401)
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            with open(TOKEN_PATH, 'wb') as token_file:
                pickle.dump(creds, token_file)
        else:
            return JSONResponse({"error": "Invalid credentials. Please re-authenticate."}, status_code=401)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])
    email_data = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_detail.get('snippet', '')
        email_data.append({
            'id': msg['id'],
            'snippet': snippet
        })
    return {"emails": email_data}

# Endpoint: Summarize all emails from Air India
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/summarize")
def summarize_air_india_emails():
    if not TOKEN_PATH.exists():
        return JSONResponse({"error": "Not authenticated. Please visit /auth/gmail first."}, status_code=401)
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            with open(TOKEN_PATH, 'wb') as token_file:
                pickle.dump(creds, token_file)
        else:
            return JSONResponse({"error": "Invalid credentials. Please re-authenticate."}, status_code=401)
    service = build('gmail', 'v1', credentials=creds)
    # Search for Spotify emails
    results = service.users().messages().list(userId='me', q='from:(spotify)', maxResults=10).execute()
    messages = results.get('messages', [])
    if not messages:
        return {"summary": "No Air India emails found."}
    email_bodies = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_detail.get('payload', {})
        parts = payload.get('parts', [])
        body = ''
        if 'data' in payload.get('body', {}):
            import base64
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        else:
            for part in parts:
                if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                    import base64
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                    break
        if not body:
            body = msg_detail.get('snippet', '')
        email_bodies.append(body)
    # Summarize using OpenAI
    if not OPENAI_API_KEY:
        return JSONResponse({"error": "OPENAI_API_KEY not set in environment."}, status_code=500)
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = "Summarize the following Spotify emails:\n" + "\n---\n".join(email_bodies)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        summary = response.choices[0].message.content.strip()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return {"summary": summary}
