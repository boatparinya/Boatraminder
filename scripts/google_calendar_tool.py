import os
import sys
import pickle
import datetime
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_calendar_events():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('calendar', 'v3', credentials=creds)

    # ช่วงเวลา: ตั้งแต่เวลาปัจจุบันของวันนี้ (23 ก.ค. 2569) จนถึงสิ้นเดือน (31 ก.ค. 2569)
    time_min = "2026-07-23T23:56:45+07:00"
    time_max = "2026-07-31T23:59:59+07:00"

    print(f"กำลังดึงข้อมูลกิจกรรมจากปฏิทินตั้งแต่วันที่ {time_min[:10]} ถึง {time_max[:10]}...")
    
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print("ไม่มีกิจกรรมการทำงานใดๆ ในช่วงเวลาที่กำหนดของเดือนนี้ค่ะ")
        return
        
    print("\n--- รายการกิจกรรมของคุณในช่วงที่เหลือของเดือนนี้ ---")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # Format the start time for clean display
        clean_start = start
        if 'T' in start:
            # Parse ISO timestamp and format it
            try:
                dt = datetime.datetime.fromisoformat(start)
                clean_start = dt.strftime('%d/%m/%Y เวลา %H:%M น.')
            except Exception:
                pass
        
        summary = event.get('summary', 'ไม่มีชื่อกิจกรรม')
        description = event.get('description', '')
        desc_str = f" ({description})" if description else ""
        print(f"- [{clean_start}] {summary}{desc_str}")

if __name__ == '__main__':
    try:
        get_calendar_events()
    except Exception as e:
        print("Error:", e)
