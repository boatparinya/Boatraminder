import os
import sys
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), '..', 'token.pickle')
    creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def search_starred_videos(keyword=None):
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Query: starred = true and mimeType is video
    query = "starred = true and mimeType contains 'video/'"
    
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink, description)",
        orderBy="modifiedTime desc"
    ).execute()

    files = results.get('files', [])

    if not files:
        print("ไม่พบไฟล์วิดีโอที่ติดดาวไว้ใน Google Drive เลยค่ะ")
        return

    print(f"พบวิดีโอที่ติดดาวทั้งหมด {len(files)} ไฟล์ค่ะ\n")
    print("=" * 70)

    # Filter by keyword if provided
    if keyword:
        filtered = [f for f in files if keyword.lower() in f['name'].lower()]
        print(f"🔍 ค้นหาคำว่า: \"{keyword}\"")
        print(f"พบ {len(filtered)} ไฟล์ที่ตรงกับการค้นหาค่ะ\n")
        display_files = filtered
    else:
        display_files = files

    if not display_files:
        print("ไม่พบวิดีโอที่ชื่อตรงกับคำค้นหาค่ะ")
        print("\nแสดงรายการวิดีโอที่ติดดาวทั้งหมดแทนค่ะ:\n")
        display_files = files

    for i, f in enumerate(display_files, 1):
        print(f"{i}. 🎬 {f['name']}")
        print(f"   🔗 ลิงก์: {f.get('webViewLink', 'ไม่มีลิงก์')}")
        print(f"   📅 แก้ไขล่าสุด: {f.get('modifiedTime', 'ไม่ทราบ')[:10]}")
        if f.get('description'):
            print(f"   📝 คำอธิบาย: {f.get('description')}")
        print()

if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    search_starred_videos(keyword)
