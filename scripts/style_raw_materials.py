import os
import sys
import pickle
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def style_sheets():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = "1-4WNibPQeIQ0dRGJFITde0KoLucA-nYVaPtrOH15c6Y"

    # ==========================================
    # SHEET 1: มื้อหลัก (sheetId: 0)
    # ==========================================
    requests_mua_lak = [
        # Global alignment & font
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 135, "startColumnIndex": 0, "endColumnIndex": 15},
                "cell": {
                    "userEnteredFormat": {
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {
                            "fontFamily": "Lexend",
                            "fontSize": 11,
                            "foregroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2}
                        }
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment,textFormat)"
            }
        },
        # Center align columns B, C, D (Qty, Price, Total)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 132, "startColumnIndex": 1, "endColumnIndex": 4},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        # Center align columns G, J, M (Recipe Qty)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 110, "startColumnIndex": 6, "endColumnIndex": 7},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 110, "startColumnIndex": 9, "endColumnIndex": 10},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 110, "startColumnIndex": 12, "endColumnIndex": 13},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        # Left align columns A, F, I, L (Item names)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 132, "startColumnIndex": 0, "endColumnIndex": 1},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        # Custom Column Widths
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 13},
                "properties": {"pixelSize": 120},
                "fields": "pixelSize"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 250}, "fields": "pixelSize" # Col A (รายการ)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
                "properties": {"pixelSize": 160}, "fields": "pixelSize" # Col C (ราคาต่อหน่วย)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
                "properties": {"pixelSize": 30}, "fields": "pixelSize" # Spacer Col E
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 5, "endIndex": 6},
                "properties": {"pixelSize": 240}, "fields": "pixelSize" # Col F (Recipe Item 1)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 7, "endIndex": 8},
                "properties": {"pixelSize": 30}, "fields": "pixelSize" # Spacer Col H
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 8, "endIndex": 9},
                "properties": {"pixelSize": 240}, "fields": "pixelSize" # Col I (Recipe Item 2)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 10, "endIndex": 11},
                "properties": {"pixelSize": 30}, "fields": "pixelSize" # Spacer Col K
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 11, "endIndex": 12},
                "properties": {"pixelSize": 240}, "fields": "pixelSize" # Col L (Recipe Item 3)
            }
        },
        # Custom Row Heights
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 0, "endIndex": 135},
                "properties": {"pixelSize": 28},
                "fields": "pixelSize"
            }
        },
        
        # Header Rows Styling - Pastel Blue
        # Rows: 2 (index 1), 69 (index 68), 92 (index 91), 106 (index 105)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.25, "blue": 0.45}},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 68, "endRowIndex": 69, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.25, "blue": 0.45}},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 91, "endRowIndex": 92, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.25, "blue": 0.45}},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 105, "endRowIndex": 106, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.25, "blue": 0.45}},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Section Titles Styling - Pastel Green
        # Row 68 (index 67) "ผัก", Row 91 (index 90) "ข้าว แป้ง ", Row 105 (index 104) "เครื่องปรุง", Row 126 (index 125) "ข้าวกล่อง  2 มื้อ"
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 67, "endRowIndex": 68, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.35, "blue": 0.15}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 90, "endRowIndex": 91, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.35, "blue": 0.15}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 104, "endRowIndex": 105, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.35, "blue": 0.15}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 125, "endRowIndex": 126, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.35, "blue": 0.15}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Totals Rows Styling - Pastel Orange/Peach
        # Rows: 65 (index 64), 90 (index 89), 98 (index 97), 124 (index 123), 128 (index 127) "รวม", 130 (index 129)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 64, "endRowIndex": 65, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 89, "endRowIndex": 90, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 97, "endRowIndex": 98, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 123, "endRowIndex": 124, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 127, "endRowIndex": 128, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 129, "endRowIndex": 130, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.55, "green": 0.25, "blue": 0.05}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Dish Titles (Recipe Card Headers) - Pastel Purple
        # F66, F72, F80, I64, I73, I89
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 65, "endRowIndex": 66, "startColumnIndex": 5, "endColumnIndex": 7},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 71, "endRowIndex": 72, "startColumnIndex": 5, "endColumnIndex": 7},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 79, "endRowIndex": 80, "startColumnIndex": 5, "endColumnIndex": 7},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 63, "endRowIndex": 64, "startColumnIndex": 8, "endColumnIndex": 10},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 72, "endRowIndex": 73, "startColumnIndex": 8, "endColumnIndex": 10},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 88, "endRowIndex": 89, "startColumnIndex": 8, "endColumnIndex": 10},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {"red": 0.35, "green": 0.15, "blue": 0.45}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Borders
        # Main Table A2:D65
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 65, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Main Table A68:D90
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 67, "endRowIndex": 90, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Main Table A91:D98
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 90, "endRowIndex": 98, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Main Table A105:D124
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 104, "endRowIndex": 124, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Main Table A126:D126
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 125, "endRowIndex": 126, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}}
            }
        },
        # Main Table A128:D130
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 127, "endRowIndex": 130, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },

        # Right Recipe Cards Borders
        # F66:G70
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 65, "endRowIndex": 71, "startColumnIndex": 5, "endColumnIndex": 7},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # F72:G78
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 71, "endRowIndex": 79, "startColumnIndex": 5, "endColumnIndex": 7},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # F80:G88
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 79, "endRowIndex": 89, "startColumnIndex": 5, "endColumnIndex": 7},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # I64:J71
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 63, "endRowIndex": 72, "startColumnIndex": 8, "endColumnIndex": 10},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # I73:J86
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 72, "endRowIndex": 87, "startColumnIndex": 8, "endColumnIndex": 10},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # I89:J101
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 88, "endRowIndex": 102, "startColumnIndex": 8, "endColumnIndex": 10},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # L62:M65
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 61, "endRowIndex": 65, "startColumnIndex": 11, "endColumnIndex": 13},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.75, "green": 0.7, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        }
    ]

    # Execute batchUpdate for Sheet 1
    print("กำลังจัดรูปแบบชีต 'มื้อหลัก' (สไตล์พาสเทลและจัดระเบียบตาราง)...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests_mua_lak}
    ).execute()
    print("จัดรูปแบบชีต 'มื้อหลัก' สำเร็จเรียบร้อยแล้วค่ะ!")

    # ==========================================
    # SHEET 2: มื้อว่าง+จิปาถะ (sheetId: 1299810768)
    # ==========================================
    requests_mua_wang = [
        # Global alignment & font
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 0, "endRowIndex": 50, "startColumnIndex": 0, "endColumnIndex": 15},
                "cell": {
                    "userEnteredFormat": {
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {
                            "fontFamily": "Lexend",
                            "fontSize": 11,
                            "foregroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2}
                        }
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment,textFormat)"
            }
        },
        # Center align columns B, C, F, G, J, K (Qty, Prices)
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 21, "startColumnIndex": 1, "endColumnIndex": 3},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 21, "startColumnIndex": 5, "endColumnIndex": 7},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 21, "startColumnIndex": 9, "endColumnIndex": 11},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        # Column Widths
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 15},
                "properties": {"pixelSize": 120},
                "fields": "pixelSize"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 220}, "fields": "pixelSize" # Col A (รายการ)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4},
                "properties": {"pixelSize": 150}, "fields": "pixelSize" # Col D (หมายเหตุ)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
                "properties": {"pixelSize": 220}, "fields": "pixelSize" # Col E (รายการมื้อว่าง)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 7, "endIndex": 8},
                "properties": {"pixelSize": 150}, "fields": "pixelSize" # Col H (หมายเหตุมื้อว่าง)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 8, "endIndex": 9},
                "properties": {"pixelSize": 220}, "fields": "pixelSize" # Col I (รายการมื้อดึก)
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "COLUMNS", "startIndex": 11, "endIndex": 12},
                "properties": {"pixelSize": 150}, "fields": "pixelSize" # Col L (หมายเหตุมื้อดึก)
            }
        },
        # Custom Row Heights
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 1299810768, "dimension": "ROWS", "startIndex": 0, "endIndex": 50},
                "properties": {"pixelSize": 28},
                "fields": "pixelSize"
            }
        },

        # Top section styling (Headers for budget) - Pastel Yellow/Orange
        # Row 1 (index 0) & Row 2 (index 1)
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 0, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 2},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Row 3 (index 2) & Row 5 (index 4)
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Table Main Header Styling - Pastel Blue
        # Row 6 (index 5)
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 0, "endColumnIndex": 12},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.15, "green": 0.25, "blue": 0.45}},
                        "backgroundColor": {"red": 0.85, "green": 0.91, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Row 7 (index 6) Totals
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 6, "endRowIndex": 7, "startColumnIndex": 4, "endColumnIndex": 12},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Row 8 (index 7) inner headers
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 7, "endRowIndex": 8, "startColumnIndex": 4, "endColumnIndex": 12},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.93, "green": 0.96, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },

        # Borders
        # Miscellaneous table A6:D20
        {
            "updateBorders": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 20, "startColumnIndex": 0, "endColumnIndex": 4},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Afternoon snack table E6:H16
        {
            "updateBorders": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 16, "startColumnIndex": 4, "endColumnIndex": 8},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },
        # Late night snack table I6:L16
        {
            "updateBorders": {
                "range": {"sheetId": 1299810768, "startRowIndex": 5, "endRowIndex": 16, "startColumnIndex": 8, "endColumnIndex": 12},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            }
        },

        # Menu section styling (Column J, Row 31 to 40) - Pastel Purple list style
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 30, "endRowIndex": 40, "startColumnIndex": 9, "endColumnIndex": 10},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.3, "green": 0.2, "blue": 0.5}},
                        "backgroundColor": {"red": 0.96, "green": 0.93, "blue": 0.99}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Snack list section styling (Column N, Row 31 to 36) - Pastel Green list style
        {
            "repeatCell": {
                "range": {"sheetId": 1299810768, "startRowIndex": 30, "endRowIndex": 36, "startColumnIndex": 13, "endColumnIndex": 14},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "foregroundColor": {"red": 0.1, "green": 0.4, "blue": 0.1}},
                        "backgroundColor": {"red": 0.92, "green": 0.97, "blue": 0.92}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        }
    ]

    print("กำลังจัดรูปแบบชีต 'มื้อว่าง+จิปาถะ' (สไตล์พาสเทลและจัดระเบียบตาราง)...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests_mua_wang}
    ).execute()
    print("จัดรูปแบบชีต 'มื้อว่าง+จิปาถะ' สำเร็จเรียบร้อยแล้วค่ะ!")

if __name__ == '__main__':
    try:
        style_sheets()
    except Exception as e:
        print("Error styling sheets:", e)
