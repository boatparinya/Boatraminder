import os
import sys
import pickle
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_calendar_sheet():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: ไม่พบไฟล์ token.pickle กรุณารัน scripts/authenticate_google.py ก่อนนะคะ")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('sheets', 'v4', credentials=creds)

    # 1. Create a new Spreadsheet with Sheet1
    spreadsheet_body = {
        'properties': {
            'title': 'July 2026 Calendar'
        },
        'sheets': [
            {
                'properties': {
                    'title': 'Calendar',
                    'sheetId': 0
                }
            }
        ]
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet_body, fields='spreadsheetId').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')

    # 2. Define the calendar values in English
    values = [
        ["JULY 2026"],
        ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        ["", "", "", "1", "2", "3", "4"],
        ["5", "6", "7", "8", "9", "10", "11"],
        ["12", "13", "14", "15", "16", "17", "18"],
        ["19", "20", "21", "22", "23", "24", "25"],
        ["26", "27", "28", "29", "30", "31", ""]
    ]

    body = {
        'values': values
    }

    # Write data
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Calendar!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    # 3. Format requests for beautiful pastel styling
    requests = [
        # Merge A1:G1
        {
            "mergeCells": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "mergeType": "MERGE_ALL"
            }
        },
        # Global alignment and font (Lexend)
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 7,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {
                            "fontFamily": "Lexend",
                            "fontSize": 11,
                            "foregroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2}
                        }
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,textFormat)"
            }
        },
        # Title (A1) Formatting
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True,
                            "fontSize": 18,
                            "fontFamily": "Lexend",
                            "foregroundColor": {"red": 0.2, "green": 0.26, "blue": 0.35}
                        },
                        "backgroundColor": {
                            "red": 0.88,
                            "green": 0.92,
                            "blue": 0.96
                        } # Pastel Blue-Grey
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Headers (Row 2) - Sunday (Col A) Pink
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.6, "green": 0.2, "blue": 0.2}},
                        "backgroundColor": {"red": 1.0, "green": 0.88, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Headers (Row 2) - Weekdays (Col B-F) Soft Green
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 1,
                    "endColumnIndex": 6
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.2, "green": 0.4, "blue": 0.2}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Headers (Row 2) - Saturday (Col G) Lavender
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 6,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.4, "green": 0.2, "blue": 0.6}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Days Sunday column (Col A) soft light pink
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 2,
                    "endRowIndex": 7,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 0.97, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor)"
            }
        },
        # Days Saturday column (Col G) soft light lavender
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 2,
                    "endRowIndex": 7,
                    "startColumnIndex": 6,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.98, "green": 0.97, "blue": 1.0}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor)"
            }
        },
        # Borders for the calendar (A2:G7)
        {
            "updateBorders": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 1,
                    "endRowIndex": 7,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.88, "green": 0.88, "blue": 0.88}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.88, "green": 0.88, "blue": 0.88}}
            }
        },
        # Set Columns widths to 130
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 7
                },
                "properties": {
                    "pixelSize": 130
                },
                "fields": "pixelSize"
            }
        },
        # Set Row Heights
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": 0,
                    "endIndex": 1
                },
                "properties": {
                    "pixelSize": 60
                },
                "fields": "pixelSize"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": 1,
                    "endIndex": 2
                },
                "properties": {
                    "pixelSize": 35
                },
                "fields": "pixelSize"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": 2,
                    "endIndex": 7
                },
                "properties": {
                    "pixelSize": 75
                },
                "fields": "pixelSize"
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

if __name__ == "__main__":
    url = create_calendar_sheet()
    print(f"SUCCESS_URL:{url}")
