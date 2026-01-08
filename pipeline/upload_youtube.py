import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload(path, title, description):
    creds = Credentials(
        None,
        refresh_token=os.getenv("YT_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YT_CLIENT_ID"),
        client_secret=os.getenv("YT_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    yt = build("youtube","v3",credentials=creds)

    yt.videos().insert(
        part="snippet,status",
        body={
            "snippet":{"title":title[:95],"description":description,"categoryId":"24"},
            "status":{"privacyStatus":"public"}
        },
        media_body=MediaFileUpload(path)
    ).execute()
