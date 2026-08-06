import os
import sys
import pickle
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def add_event():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'ซ้อมกิจกรรม first meet ค่ายจิตอาสา',
        'start': {
            'dateTime': '2026-08-02T13:00:00+07:00',
            'timeZone': 'Asia/Bangkok',
        },
        'end': {
            'dateTime': '2026-08-02T17:00:00+07:00',
            'timeZone': 'Asia/Bangkok',
        },
    }

    print("กำลังสร้างกิจกรรมใน Google Calendar...")
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"สร้างกิจกรรมสำเร็จแล้ว! ลิงก์กิจกรรม: {created_event.get('htmlLink')}")

if __name__ == '__main__':
    try:
        add_event()
    except Exception as e:
        print("Error:", e)
