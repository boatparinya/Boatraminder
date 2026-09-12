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
    
    # อัปเดต .env อัตโนมัติสำหรับ Node.js และระบบหลังบ้าน
    if os.path.exists('.env') and hasattr(creds, 'refresh_token') and creds.refresh_token:
        with open('.env', 'r', encoding='utf-8') as ef:
            env_content = ef.read()
        import re
        if 'GOOGLE_REFRESH_TOKEN=' in env_content:
            env_content = re.sub(r'GOOGLE_REFRESH_TOKEN=.*', f'GOOGLE_REFRESH_TOKEN={creds.refresh_token}', env_content)
        else:
            env_content += f"\nGOOGLE_REFRESH_TOKEN={creds.refresh_token}\n"
        with open('.env', 'w', encoding='utf-8') as ef:
            ef.write(env_content)
        print("[+] อัปเดต GOOGLE_REFRESH_TOKEN ลงในไฟล์ .env เรียบร้อยแล้วค่ะ!")

    print("ล็อกอินสำเร็จ! ระบบพร้อมเข้าถึง Google Calendar และ Google Services ของคุณแล้ว")
    return creds

if __name__ == '__main__':
    get_credentials()
