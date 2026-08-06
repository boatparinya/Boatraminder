import os
import sys
import pickle
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def update_schedule_sheet():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('sheets', 'v4', credentials=creds)

    # Use the existing Spreadsheet ID
    spreadsheet_id = "1k2TJpfnSNRA2v7AR-xyOC1i6ynMELcsdZEGvqtdwAME"

    # Clear previous values and formatting
    # Clear values
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='Schedule!A1:Z100'
    ).execute()

    # Clear grid formatting (unmerge cells first to avoid overlapping merge errors)
    clear_unmerge_request = {
        "unmergeCells": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 100,
                "startColumnIndex": 0,
                "endColumnIndex": 26
            }
        }
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [clear_unmerge_request]}
    ).execute()

    # Define all values in Thai
    values = [
        # 0, 1: Title & Subtitle
        ["ตารางกำหนดการสอบและกิจกรรมวิชา Physiology (321242)"],
        ["ภาคการศึกษาที่ 1 ปีการศึกษา 2569 | คณะเภสัชศาสตร์ มหาวิทยาลัยเชียงใหม่"],
        [], # 2: empty
        
        # 3: Section 1 Title
        ["ตารางสอบรายภาค (Summative Exams)"],
        # 4: Table 1 Headers
        ["สอบครั้งที่", "วัน-เวลาที่สอบ", "ระบบ / หัวข้อที่สอบ", "จำนวนข้อสอบ", "เวลาสอบ", "สถานะ & กฎการสอบซ่อม"],
        # 5-8: Table 1 Data
        ["1", "21 ก.ค. 2569 (09:00 - 12:00 น.)", "Basic & N&M, CVS", "100 ข้อ", "3 ชั่วโมง", "สอบเสร็จสิ้นแล้ว (สอบซ่อมหากคะแนน < Mean-2SD)"],
        ["2", "25 ส.ค. 2569 (09:00 - 11:00 น.)", "RES, MR & BT", "70 ข้อ", "2 ชั่วโมง", "สอบซ่อมหากคะแนน < Mean-2SD"],
        ["3", "22 ก.ย. 2569 (09:00 - 12:00 น.)", "KUB, Endo", "100 ข้อ", "3 ชั่วโมง", "สอบซ่อมหากคะแนน < Mean-2SD"],
        ["4", "20 ต.ค. 2569 (09:00 - 12:00 น.)", "Neuro & SS, GI", "100 ข้อ", "3 ชั่วโมง", "ไม่มีการจัดสอบซ่อมสำหรับระบบปลายภาค"],
        [], # 9: empty
        
        # 10: Section 2 Title
        ["ตารางสอบย่อยเก็บคะแนนออนไลน์ (Formative Exams)"],
        # 11: Table 2 Headers
        ["ครั้งที่", "ระบบ / หัวข้อสอบย่อย", "วันที่สอบย่อย", "ช่วงเวลาที่ระบบเปิด", "ช่องทางการสอบ", "สัดส่วนคะแนน"],
        # 12-19: Table 2 Data
        ["1", "Basic and N & M", "30 มิ.ย. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["2", "CVS", "14 ก.ค. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["3", "RES", "04 ส.ค. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["4", "MR & BT", "11 ส.ค. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["5", "KUB", "01 ก.ย. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["6", "Endo", "15 ก.ย. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["7", "Neuro & SS", "29 ก.ย. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        ["8", "GI", "06 ต.ค. 2569", "08:00 - 23:59 น.", "ออนไลน์ผ่าน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 10%"],
        [], # 20: empty
        
        # 21: Section 3 Title
        ["ตารางกิจกรรมและการเรียนสัมมนากลุ่ม (Group Discussions)"],
        # 22: Table 3 Headers
        ["ครั้งที่", "หัวข้อการเรียนสัมมนา", "วันที่จัดกิจกรรม", "เวลาสัมมนา", "วิธีการส่งงาน / สถานที่", "สัดส่วนคะแนน"],
        # 23-27: Table 3 Data
        ["1", "Physiology of NMJ & Muscle", "30 มิ.ย. 2569", "ในคาบเรียนตามตารางสอน", "ส่งรายงานกลุ่ม PDF บน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 18%"],
        ["2", "Arterial BP in Dog", "14 ก.ค. 2569", "ในคาบเรียนตามตารางสอน", "ส่งรายงานกลุ่ม PDF บน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 18%"],
        ["3", "Respiration in Dog", "04 ส.ค. 2569", "ในคาบเรียนตามตารางสอน", "ส่งรายงานกลุ่ม PDF บน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 18%"],
        ["4", "Urine Excretion in Dog", "01 ก.ย. 2569", "ในคาบเรียนตามตารางสอน", "ส่งรายงานกลุ่ม PDF บน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 18%"],
        ["5", "Case Study Endocrine", "15 ก.ย. 2569", "ในคาบเรียนตามตารางสอน", "ส่งรายงานกลุ่ม PDF บน Mango Canvas", "เป็นส่วนหนึ่งของสัดส่วน 18%"],
        [], # 28: empty
        
        # 29: Section 4 Title
        ["เกณฑ์และสัดส่วนการประเมินคะแนน (Grading Weights)"],
        # 30: Table 4 Headers
        ["ส่วนการประเมินคะแนน", "สัดส่วน %", "รายละเอียดและเกณฑ์ผ่านผ่าน"],
        # 31-34: Table 4 Data
        ["คะแนนสอบ MCQ (Summative)", "70%", "รวมทั้ง 8 ระบบ คะแนนสะสมต้อง >= Mean - 2SD จึงจะผ่านเกณฑ์ขั้นต่ำ (MPL) มิฉะนั้นได้ F ทันที"],
        ["คะแนนสอบย่อย (Formative)", "10%", "คะแนนการมีส่วนร่วมทำแบบทดสอบครบถ้วนตามแต่ละระบบ หากไม่ครบคิดสัดส่วนตามที่ทำจริง"],
        ["คะแนนงานสัมมนากลุ่ม (Group Discussion)", "18%", "ประเมินรายงานการสัมมนาของกลุ่ม โดยส่งไฟล์ PDF"],
        ["คะแนนพฤติกรรม / การเข้าชั้นเรียน", "2%", "การประเมินกระบวนวิชา ประเมินอาจารย์ผู้สอน การเข้าห้องเรียนและเข้าสอบตรงเวลา"],
        [], # 35: empty
        
        # 36: Table 5 Section Title
        ["⚠️ กฎเกณฑ์และนโยบายสำคัญที่ต้องปฏิบัติตาม:"],
        # 37-40: Table 5 Data
        ["- การตัดเกรดจะคิดคะแนนรวมสะสมทุกบล็อกทั้งกระบวนวิชา ไม่ได้ตัดเกรดแยกทีละบล็อก"],
        ["- นักศึกษาต้องผ่านเกณฑ์คะแนนเฉลี่ยลบสองเท่าส่วนเบี่ยงเบนมาตรฐาน (>= Mean - 2SD) จึงจะผ่านวิชานี้"],
        ["- การสอบซ่อมจัดขึ้นภายใน 1 สัปดาห์เฉพาะการสอบครั้งที่ 1, 2 และ 3 เท่านั้น โดยต้องยื่นเอกสารยินยอมในระบบ"],
        ["- คะแนนสูงสุดที่สามารถได้รับหลังจากการสอบซ่อมจะถูกกำหนดไว้ไม่เกินเกณฑ์ผ่านขั้นต่ำ (Mean - 2SD) เท่านั้น"]
    ]

    body = {
        'values': values
    }

    # Write data starting from Schedule!A1
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Schedule!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    # Define Formatting Requests for Font Size 18, Thai, Separated tables
    requests = [
        # 1. Dimension adjustments (Auto-fit Columns)
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 6
                }
            }
        },
        
        # 2. Row Heights (Compact height)
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 70}, "fields": "pixelSize" # Title
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 1, "endIndex": 2},
                "properties": {"pixelSize": 45}, "fields": "pixelSize" # Subtitle
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 2, "endIndex": 42},
                "properties": {"pixelSize": 40}, "fields": "pixelSize" # Data rows
            }
        },
        
        # 3. Global Text Style (Font size 18, fontFamily Lexend, vertical middle alignment, WRAP text)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 42, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "fontFamily": "Lexend",
                            "fontSize": 18,
                            "foregroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2}
                        }
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment,wrapStrategy,textFormat)"
            }
        },
        
        # 4. Center align columns A, D, E and sometimes B
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 4, "endRowIndex": 28, "startColumnIndex": 0, "endColumnIndex": 1},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 4, "endRowIndex": 28, "startColumnIndex": 3, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        },
        
        # 5. Merges
        # Title & Subtitle Merges
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        # Section Titles Merges
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 10, "endRowIndex": 11, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 21, "endRowIndex": 22, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 29, "endRowIndex": 30, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        
        # Table 4 (Grading weights) merge details column (Col C to F)
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 30, "endRowIndex": 31, "startColumnIndex": 2, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 31, "endRowIndex": 32, "startColumnIndex": 2, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 32, "endRowIndex": 33, "startColumnIndex": 2, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 33, "endRowIndex": 34, "startColumnIndex": 2, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 34, "endRowIndex": 35, "startColumnIndex": 2, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        
        # Table 5 Rules Merges (Col A to F)
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 36, "endRowIndex": 37, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 37, "endRowIndex": 38, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 38, "endRowIndex": 39, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 39, "endRowIndex": 40, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        {"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 40, "endRowIndex": 41, "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}},
        
        # 6. Colors and Styling
        # Title (A1)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 24, "foregroundColor": {"red": 0.1, "green": 0.2, "blue": 0.35}},
                        "backgroundColor": {"red": 0.82, "green": 0.88, "blue": 0.96}, # Pastel Blue
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        # Subtitle (A2)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": False, "fontSize": 16, "foregroundColor": {"red": 0.3, "green": 0.4, "blue": 0.5}},
                        "backgroundColor": {"red": 0.9, "green": 0.93, "blue": 0.98},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        
        # Section 1 Title: Summative Header - Pastel Purple
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 20, "foregroundColor": {"red": 0.35, "green": 0.2, "blue": 0.5}},
                        "backgroundColor": {"red": 0.93, "green": 0.88, "blue": 0.98}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Table 1 Header (Row 5)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": {"red": 0.35, "green": 0.2, "blue": 0.5}},
                        "backgroundColor": {"red": 0.96, "green": 0.93, "blue": 0.99},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        
        # Section 2 Title: Formative Header - Pastel Green
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 10, "endRowIndex": 11, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 20, "foregroundColor": {"red": 0.15, "green": 0.4, "blue": 0.2}},
                        "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Table 2 Header (Row 12)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 11, "endRowIndex": 12, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": {"red": 0.15, "green": 0.4, "blue": 0.2}},
                        "backgroundColor": {"red": 0.93, "green": 0.97, "blue": 0.93},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        
        # Section 3 Title: Discussions Header - Pastel Blue
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 21, "endRowIndex": 22, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 20, "foregroundColor": {"red": 0.1, "green": 0.3, "blue": 0.5}},
                        "backgroundColor": {"red": 0.88, "green": 0.93, "blue": 0.97}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Table 3 Header (Row 23)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 22, "endRowIndex": 23, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": {"red": 0.1, "green": 0.3, "blue": 0.5}},
                        "backgroundColor": {"red": 0.93, "green": 0.96, "blue": 0.98},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        
        # Section 4 Title: Weights Header - Pastel Orange
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 29, "endRowIndex": 30, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 20, "foregroundColor": {"red": 0.6, "green": 0.3, "blue": 0.1}},
                        "backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.84}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Table 4 Header (Row 31)
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 30, "endRowIndex": 31, "startColumnIndex": 0, "endColumnIndex": 3},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": {"red": 0.6, "green": 0.3, "blue": 0.1}},
                        "backgroundColor": {"red": 0.99, "green": 0.94, "blue": 0.9},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
            }
        },
        
        # Section 5 Title: Rules Header - Pastel Red
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 36, "endRowIndex": 37, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 20, "foregroundColor": {"red": 0.7, "green": 0.2, "blue": 0.2}},
                        "backgroundColor": {"red": 1.0, "green": 0.88, "blue": 0.88}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        # Rules Content Style
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 37, "endRowIndex": 41, "startColumnIndex": 0, "endColumnIndex": 6},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"italic": True, "fontSize": 18, "foregroundColor": {"red": 0.35, "green": 0.35, "blue": 0.35}},
                        "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.95}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        
        # 7. Borders
        # Borders Table 1 (Row 4 to 8)
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 4, "endRowIndex": 9, "startColumnIndex": 0, "endColumnIndex": 6},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}
            }
        },
        # Borders Table 2 (Row 11 to 19)
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 11, "endRowIndex": 20, "startColumnIndex": 0, "endColumnIndex": 6},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}
            }
        },
        # Borders Table 3 (Row 22 to 27)
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 22, "endRowIndex": 28, "startColumnIndex": 0, "endColumnIndex": 6},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}
            }
        },
        # Borders Table 4 (Row 30 to 34)
        {
            "updateBorders": {
                "range": {"sheetId": 0, "startRowIndex": 30, "endRowIndex": 35, "startColumnIndex": 0, "endColumnIndex": 6},
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "left": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "right": {"style": "SOLID", "width": 1, "color": {"red": 0.8, "green": 0.8, "blue": 0.8}},
                "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}},
                "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

if __name__ == '__main__':
    url = update_schedule_sheet()
    print(f"SUCCESS_URL:{url}")
