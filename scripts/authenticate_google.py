import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
    # เปิดหน้าเบราว์เซอร์ให้คุณกดเลือกบัญชี Google ของคุณเอง
    if not os.path.exists('credentials.json'):
        print("Error: ไม่พบไฟล์ 'credentials.json' ในโฟลเดอร์หลัก")
        print("กรุณาดาวน์โหลดไฟล์ credentials.json จาก Google Cloud Console แล้วนำมาวางในโฟลเดอร์นี้ก่อนนะคะ")
        return None
        
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # เซฟสิทธิ์ไว้ในเครื่อง ต่อไปไม่ต้องล็อกอินซ้ำ
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    print("ล็อกอินสำเร็จ! Antigravity พร้อมเข้าถึง Google Docs ของคุณแล้ว")
    return creds

if __name__ == '__main__':
    get_credentials()
