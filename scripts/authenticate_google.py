import os
import sys
import pickle
import re
from google_auth_oauthlib.flow import InstalledAppFlow

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
    if not os.path.exists('credentials.json'):
        print("Error: ไม่พบไฟล์ 'credentials.json' ในโฟลเดอร์หลัก")
        return None

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # เซฟสิทธิ์ token.pickle ในเครื่อง
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    # อัปเดตไฟล์ .env อัตโนมัติสำหรับระบบ Node.js
    if os.path.exists('.env') and hasattr(creds, 'refresh_token') and creds.refresh_token:
        with open('.env', 'r', encoding='utf-8') as ef:
            env_content = ef.read()
        if 'GOOGLE_REFRESH_TOKEN=' in env_content:
            env_content = re.sub(r'GOOGLE_REFRESH_TOKEN=.*', f'GOOGLE_REFRESH_TOKEN={creds.refresh_token}', env_content)
        else:
            env_content += f"\nGOOGLE_REFRESH_TOKEN={creds.refresh_token}\n"
        with open('.env', 'w', encoding='utf-8') as ef:
            ef.write(env_content)
        print(f"[+] อัปเดต GOOGLE_REFRESH_TOKEN ใน .env เรียบร้อยแล้วค่ะ!")

    print("🎉 ล็อกอินสำเร็จแล้วค่ะเตง! ระบบพร้อมเชื่อมต่อ Google Calendar เรียบร้อยแล้วค่ะ")
    return creds

if __name__ == '__main__':
    get_credentials()
