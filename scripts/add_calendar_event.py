import os
import sys
import pickle
import argparse
from datetime import datetime, timedelta
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_calendar_service():
    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'token.pickle')
    if not os.path.exists(token_path):
        # Fallback to current working directory
        token_path = 'token.pickle'
    
    if not os.path.exists(token_path):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
        
    return build('calendar', 'v3', credentials=creds)

def add_event(title, date_str, start_time_str=None, end_time_str=None, description=None, location=None, all_day=False):
    service = get_calendar_service()

    event = {
        'summary': title,
    }

    if description:
        event['description'] = description
    if location:
        event['location'] = location

    if all_day or not start_time_str:
        # All-day event
        event['start'] = {
            'date': date_str,
            'timeZone': 'Asia/Bangkok',
        }
        # For all-day events, end date is exclusive in Google Calendar
        # If it's a single day, end date is the next day
        try:
            start_date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            end_date_obj = start_date_obj + timedelta(days=1)
            end_date_str = end_date_obj.strftime("%Y-%m-%d")
        except Exception:
            end_date_str = date_str
            
        event['end'] = {
            'date': end_date_str,
            'timeZone': 'Asia/Bangkok',
        }
    else:
        # Timed event
        # Parse start datetime
        if len(start_time_str) == 5:
            start_dt_str = f"{date_str}T{start_time_str}:00+07:00"
        else:
            start_dt_str = f"{date_str}T{start_time_str}+07:00"

        # If end_time_str is not provided, default to 1 hour after start
        if not end_time_str:
            try:
                st_dt = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
                et_dt = st_dt + timedelta(hours=1)
                end_dt_str = et_dt.strftime("%Y-%m-%dT%H:%M:00+07:00")
            except Exception:
                end_dt_str = start_dt_str
        else:
            if len(end_time_str) == 5:
                end_dt_str = f"{date_str}T{end_time_str}:00+07:00"
            else:
                end_dt_str = f"{date_str}T{end_time_str}+07:00"

        event['start'] = {
            'dateTime': start_dt_str,
            'timeZone': 'Asia/Bangkok',
        }
        event['end'] = {
            'dateTime': end_dt_str,
            'timeZone': 'Asia/Bangkok',
        }

    print(f"[*] กำลังเพิ่มกิจกรรม: '{title}' ลงใน Google Calendar...")
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    link = created_event.get('htmlLink')
    print(f"[+] สร้างกิจกรรมสำเร็จเรียบร้อยแล้วค่ะ! 🎉")
    print(f"    - ชื่อกิจกรรม: {title}")
    print(f"    - วันที่: {date_str}")
    if all_day or not start_time_str:
        print(f"    - เวลา: ตลอดทั้งวัน")
    else:
        print(f"    - เวลา: {start_time_str} - {end_time_str if end_time_str else '1 ชม.'}")
    if description:
        print(f"    - รายละเอียด: {description}")
    print(f"    - ลิงก์ปฏิทิน: {link}")
    return created_event

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add event to Google Calendar")
    parser.add_argument("--title", "-t", required=True, help="Event title/summary")
    parser.add_argument("--date", "-d", required=True, help="Event date in YYYY-MM-DD format")
    parser.add_argument("--start-time", "-st", help="Start time in HH:MM format")
    parser.add_argument("--end-time", "-et", help="End time in HH:MM format")
    parser.add_argument("--description", "--notes", help="Event description or notes")
    parser.add_argument("--location", "-l", help="Event location")
    parser.add_argument("--all-day", action="store_true", help="Set as an all-day event")

    args = parser.parse_args()

    try:
        add_event(
            title=args.title,
            date_str=args.date,
            start_time_str=args.start_time,
            end_time_str=args.end_time,
            description=args.description,
            location=args.location,
            all_day=args.all_day
        )
    except Exception as e:
        print(f"[-] เกิดข้อผิดพลาด: {e}")
        sys.exit(1)
