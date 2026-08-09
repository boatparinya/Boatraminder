import os
import sys
import pickle
from googleapiclient.discovery import build

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return {
        "red": int(hex_str[0:2], 16) / 255.0,
        "green": int(hex_str[2:4], 16) / 255.0,
        "blue": int(hex_str[4:6], 16) / 255.0
    }

def update_beautiful_sheet():
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: token.pickle not found. Please run authenticate_google.py first.")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = "1k2TJpfnSNRA2v7AR-xyOC1i6ynMELcsdZEGvqtdwAME"

    # Get sheetId of 'Schedule' or first sheet
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_id = sheets[0]['properties']['sheetId'] if sheets else 0

    # 1. Unmerge and clear sheet
    unmerge_request = {
        "unmergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 200,
                "startColumnIndex": 0,
                "endColumnIndex": 10
            }
        }
    }
    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [unmerge_request]}
        ).execute()
    except Exception as e:
        print("Unmerge notice:", e)

    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='Schedule!A1:Z200'
    ).execute()

    # Define Row Data Structure (5 Columns: A, B, C, D, E)
    values = [
        # Row 0: Title Banner
        ["สรุปข้อมูล 3 วิชา: สัดส่วนการคิดคะแนน & ตารางสอบสำคัญ (จาก Mango Canvas)", "", "", "", ""],
        # Row 1: Subtitle
        ["ภาคการศึกษาที่ 1 ปีการศึกษา 2569 | คณะเภสัชศาสตร์ มหาวิทยาลัยเชียงใหม่", "", "", "", ""],
        # Row 2: Empty
        ["", "", "", "", ""],

        # =========================================================================
        # 1. ANATOMY (301241)
        # =========================================================================
        # Row 3: Anat Banner
        ["1. วิชา Anatomy for Pharmacy Students (301241) - กายวิภาคศาสตร์", "", "", "", ""],
        # Row 4: Table 1.1 Title
        ["📋 ตารางที่ 1.1: สัดส่วนการคิดคะแนนและเกณฑ์การตัดเกรด", "", "", "", ""],
        # Row 5: Table 1.1 Header
        ["ส่วนการประเมินคะแนน", "สัดส่วนคะแนน (%)", "รูปแบบข้อสอบ / วิธีการเก็บคะแนน", "รายละเอียดและเงื่อนไขการวัดผล", "เกณฑ์การตัดเกรด"],
        # Row 6-9: Data
        ["1. คะแนนสอบภาคทฤษฎี (Theory)", "50%", "MCQ 5 ตัวเลือก (บทละ 12 ข้อ)", "ประเมินจากการสอบรายภาคทั้ง 3 ครั้ง", "อิงเกณฑ์:"],
        ["2. คะแนนสอบภาคปฏิบัติ (Lab)", "35%", "เติมคำสั้น TSE จับเวลา 1 นาที/ข้อ", "สอบบทละ 7 ข้อ (ข้อละ 2 ข้อย่อย) จากร่างชำแหละ หุ่นจำลอง รูปภาพ สไลด์", "A : 80.00 - 100%\nB+ : 73.75 - 79.99%\nB : 67.50 - 73.74%\nC+ : 61.25 - 67.49%\nC : 55.00 - 61.24%\nD+ : 52.50 - 54.99%\nD : 50.00 - 52.49%\nF : 0 - 49.99%"],
        ["3. แบบทดสอบก่อนแลป (Pre-quiz)", "10%", "MCQ / ถูก-ผิด / เติมคำ", "ทดสอบความรู้ล่วงหน้าก่อนเข้าแลป ครอบคลุมเนื้อหาคู่มือปฏิบัติการ", ""],
        ["4. คะแนนเจตคติ (Attitude)", "5%", "ตรวจการทำคู่มือแลป", "ประเมินความเรียบร้อยในการทำและส่งคู่มือปฏิบัติการตรงเวลา", ""],
        # Row 10: Empty
        ["", "", "", "", ""],
        # Row 11: Table 1.2 Title
        ["📅 ตารางที่ 1.2: กำหนดการสอบสำคัญ วันที่ เวลา และหัวข้อที่ออกสอบ", "", "", "", ""],
        # Row 12: Table 1.2 Header
        ["การสอบครั้งที่", "วันที่สอบ", "เวลาสอบ", "หัวข้อ / บทที่ออกสอบ", "สถานที่ / หมายเหตุ"],
        # Row 13-15: Data
        ["สอบครั้งที่ 1 (Exam I)", "ศุกร์ 31 ก.ค. 2569", "13:00 - 17:00 น.", "บทที่ 1-5:\n- บทที่ 1: Introduction to human body & cytology\n- บทที่ 2: Cytogenetic, epithelium, gland & cellular attachment\n- บทที่ 3: Connective tissue & integumentary system\n- บทที่ 4: Cartilage & skeletal system\n- บทที่ 5: Muscular system", "สอบทฤษฎีและแลป\nอาคาร 50 ปี / อาคารบัณฑิตศึกษา"],
        ["สอบครั้งที่ 2 (Exam II)", "ศุกร์ 18 ก.ย. 2569", "Lab: 10:00 - 12:00 น.\nLec: 13:00 - 15:00 น.", "บทที่ 6-10:\n- บทที่ 6: Nervous system I\n- บทที่ 7: Nervous system II\n- บทที่ 8: Special sense organs\n- บทที่ 9: Cardiovascular system\n- บทที่ 10: Respiratory & lymphatic system", "สอบทฤษฎีและแลป"],
        ["สอบครั้งที่ 3 (Exam III - ปลายภาค)", "ศุกร์ 30 ต.ค. 2569", "08:00 - 12:00 น.", "บทที่ 11-15:\n- บทที่ 11: Digestive system\n- บทที่ 12: Urinary system\n- บทที่ 13: Male reproductive system\n- บทที่ 14: Female reproductive system\n- บทที่ 15: Endocrine system", "สอบทฤษฎีและแลปปลายภาค"],
        # Row 16-17: Empty
        ["", "", "", "", ""],
        ["", "", "", "", ""],

        # =========================================================================
        # 2. PHYSIOLOGY (321242)
        # =========================================================================
        # Row 18: Phso Banner
        ["2. วิชา Physiology for Pharmacy Students (321242) - สรีรวิทยา", "", "", "", ""],
        # Row 19: Table 2.1 Title
        ["📋 ตารางที่ 2.1: สัดส่วนการคิดคะแนนและเกณฑ์การตัดเกรด", "", "", "", ""],
        # Row 20: Table 2.1 Header
        ["ส่วนการประเมินคะแนน", "สัดส่วนคะแนน (%)", "รูปแบบข้อสอบ / วิธีการเก็บคะแนน", "รายละเอียดและเงื่อนไขการวัดผล", "เกณฑ์การตัดเกรด & กฎสอบซ่อม"],
        # Row 21-24: Data
        ["1. คะแนนสอบรายภาค (Knowledge)", "70%", "MCQ 5 ตัวเลือก (4 ครั้ง)", "ต้องได้คะแนนรวมสะสม >= Mean - 2SD จึงจะผ่านเกณฑ์ขั้นต่ำ (MPL) มิฉะนั้นได้ F ทันที", "• ตัดเกรด Combination Grade (8 เกรด A ถึง F)\n• อนุญาตให้สอบซ่อมเฉพาะสอบครั้งที่ 1, 2, 3 หากคะแนน < Mean - 2SD\n• คะแนนหลังสอบซ่อมจะได้ไม่เกินเกณฑ์ Mean - 2SD\n• การสอบครั้งที่ 4 (ปลายภาค) ไม่มีสอบซ่อม"],
        ["2. คะแนนสอบย่อยออนไลน์ (Formative)", "10%", "MCQ 4 ตัวเลือก (8 ครั้ง)", "สอบผ่าน Mango Canvas ช่วง 08:00 - 23:59 น. คิดตามสัดส่วนที่เข้าทำจริง", ""],
        ["3. คะแนนรายงานกลุ่ม (Group Discussion)", "18%", "รายงานกลุ่ม 5 กิจกรรม", "ศึกษาคลิป ค้นคว้า อภิปราย และส่งไฟล์รายงาน PDF บน Mango Canvas", ""],
        ["4. คะแนนเจตคติ (Attitude)", "2%", "ประเมินออนไลน์ & การเข้าเรียน", "• ประเมินกระบวนวิชา CMU SIS (0.5%)\n• ประเมินผู้สอน CMU SIS (0.5%)\n• เข้าห้องสอบตรงเวลา (0.25%)\n• เข้าห้องเรียน (0.25%)\n• Quiz ท้ายแลป/Discussion (0.5%)", ""],
        # Row 25: Empty
        ["", "", "", "", ""],
        # Row 26: Table 2.2 Title
        ["📅 ตารางที่ 2.2: กำหนดการสอบสำคัญ วันที่ เวลา และหัวข้อที่ออกสอบ", "", "", "", ""],
        # Row 27: Table 2.2 Header
        ["การสอบครั้งที่ / รูปแบบ", "วันที่สอบ", "เวลาสอบ", "หัวข้อ / ระบบที่ออกสอบ", "จำนวนข้อสอบ & เงื่อนไข"],
        # Row 28-32: Data
        ["สอบรายภาค ครั้งที่ 1", "อังคาร 21 ก.ค. 2569", "09:00 - 12:00 น.", "• Basic and N & M (กล้ามเนื้อและเส้นประสาท)\n• CVS (ระบบไหลเวียนโลหิต)", "100 ข้อ (3 ชั่วโมง)\n(สอบซ่อมได้หากคะแนน < Mean-2SD)"],
        ["สอบรายภาค ครั้งที่ 2", "อังคาร 25 ส.ค. 2569", "09:00 - 11:00 น.", "• RES (ระบบหายใจ)\n• MR & BT (เมแทบอลิซึมพลังงานและการปรับอุณหภูมิ)", "70 ข้อ (2 ชั่วโมง)\n(สอบซ่อมได้หากคะแนน < Mean-2SD)"],
        ["สอบรายภาค ครั้งที่ 3", "อังคาร 22 ก.ย. 2569", "09:00 - 12:00 น.", "• KUB (ระบบขับถ่ายปัสสาวะ)\n• Endo (ระบบต่อมไร้ท่อ)", "100 ข้อ (3 ชั่วโมง)\n(สอบซ่อมได้หากคะแนน < Mean-2SD)"],
        ["สอบรายภาค ครั้งที่ 4 (ปลายภาค)", "อังคาร 20 ต.ค. 2569", "09:00 - 12:00 น.", "• Neuro & SS (ระบบประสาทและการรับสัมผัสพิเศษ)\n• GI (ระบบทางเดินอาหาร)", "100 ข้อ (3 ชั่วโมง)\n(ไม่มีจัดสอบซ่อมสำหรับปลายภาค)"],
        ["สอบย่อย Formative Exams (8 ครั้ง)", "30 มิ.ย. - 6 ต.ค. 2569", "08:00 - 23:59 น.", "1. Basic&NM (30 มิ.ย.)  2. CVS (14 ก.ค.)  3. RES (4 ส.ค.)  4. MR&BT (11 ส.ค.)\n5. KUB (1 ก.ย.)  6. Endo (15 ก.ย.)  7. Neuro&SS (29 ก.ย.)  8. GI (6 ต.ค.)", "สอบออนไลน์ผ่าน Mango Canvas\n(3 - 8 ข้อ ต่อระบบ)"],
        # Row 33-34: Empty
        ["", "", "", "", ""],
        ["", "", "", "", ""],

        # =========================================================================
        # 3. PHARMACEUTICAL TECHNOLOGY 2 (465221)
        # =========================================================================
        # Row 35: PharmTech Banner
        ["3. วิชา Pharmaceutical Technology 2 (465221) - เทคโนโลยีเภสัชกรรม 2", "", "", "", ""],
        # Row 36: Table 3.1 Title
        ["📋 ตารางที่ 3.1: สัดส่วนการคิดคะแนนและเกณฑ์การตัดเกรด", "", "", "", ""],
        # Row 37: Table 3.1 Header
        ["ส่วนการประเมินคะแนน", "สัดส่วนคะแนน (%)", "รูปแบบข้อสอบ / วิธีการเก็บคะแนน", "รายละเอียดและเงื่อนไขการวัดผล", "เกณฑ์การตัดเกรด & เงื่อนไขสิทธิ์"],
        # Row 38-45: Data
        ["1. สอบกลางภาค (Midterm Exam)", "32.5%", "ข้อสอบภาคทฤษฎีกลางภาค", "สอบหัวข้อบรรยายที่ 2-5 (รวม 15 ชั่วโมง): ระบบการกระจายตัว, คอลลอยด์, ยาน้ำแขวนตะกอน, ยาน้ำอิมัลชัน", "เกณฑ์การตัดเกรด (อิงเกณฑ์):\nA : >= 80.0%\nB+ : 75.0 - 79.9%\nB : 70.0 - 74.9%\nC+ : 65.0 - 69.9%\nC : 60.0 - 64.9%\nD+ : 55.0 - 59.9%\nD : 50.0 - 54.9%\nF : < 50.0%\n\n🚨 **เงื่อนไขสำคัญ:**\nต้องมีเวลาเรียนภาคปฏิบัติการไม่น้อยกว่า 80% จึงจะมีสิทธิ์เข้าสอบปลายภาค"],
        ["2. สอบปลายภาค (Final Exam)", "32.5%", "ข้อสอบภาคทฤษฎีปลายภาค", "สอบหัวข้อบรรยายที่ 6-8 (รวม 15 ชั่วโมง): ยารูปแบบกึ่งแข็ง (ขี้ผึ้ง ครีม เพสต์ เจล Transdermal), ยาเหน็บ, การควบคุมคุณภาพ", ""],
        ["3. คะแนนเข้าเรียนบรรยาย", "2.0%", "เช็กชื่อ/การมีส่วนร่วม", "ประเมินความร่วมมือและการเข้าเรียนในคาบบรรยาย", ""],
        ["4. สอบย่อยปฏิบัติการ (Lab Quizzes)", "10.0%", "สอบย่อย 10 นาที", "สอบก่อนหรือหลังทำปฏิบัติการแต่ละบท ทดสอบความรู้ความเข้าใจแลป", ""],
        ["5. รายงานและผลิตภัณฑ์แลป", "5.0%", "ประเมินผลิตภัณฑ์ & รายงาน", "ส่งผลิตภัณฑ์ที่เตรียมหลังจบคาบแลป และส่งรายงานปฏิบัติการตามกำหนด", ""],
        ["6. งานมอบหมาย (Group Assignment)", "7.0%", "พัฒนาตำรับยา (งานกลุ่ม)", "ฝึกตั้งสูตรและพัฒนาตำรับกึ่งแข็ง/คอลลอยด์/อิมัลชัน ส่งชิ้นงานและรายงานฉบับสมบูรณ์", ""],
        ["7. สอบทักษะทางเภสัชกรรม", "8.0%", "สอบปฏิบัติการทักษะ", "ทดสอบทักษะการชั่ง ผสม เตรียม และบรรจุยาน้ำ/ยากึ่งแข็งตามแลป 1-13", ""],
        ["8. คะแนนเตรียมความพร้อมแลป", "3.0%", "ตรวจเตรียมแลป & วินัย", "สุ่มตรวจตารางบันทึก/คำนวณ/สมบัติสาร 2 ครั้ง (1%) + หักคะแนนเข้าสาย/แต่งกายไม่เรียบร้อยครั้งละ 0.5%", ""],
        # Row 46: Empty
        ["", "", "", "", ""],
        # Row 47: Table 3.2 Title
        ["📅 ตารางที่ 3.2: กำหนดการสอบสำคัญ วันที่ เวลา และหัวข้อที่ออกสอบ", "", "", "", ""],
        # Row 48: Table 3.2 Header
        ["การสอบ / กิจกรรมสำคัญ", "ช่วงวันที่สอบ", "เวลาสอบ", "หัวข้อที่ออกสอบ", "สถานที่ / หมายเหตุ"],
        # Row 49-51: Data
        ["สอบกลางภาค (Midterm Exam)", "17 - 30 สิงหาคม 2569", "ตามตารางสอบคณะ", "หัวข้อบรรยายที่ 2-5:\n- ระบบการกระจายตัว (Disperse systems)\n- ระบบคอลลอยด์ (Colloidal systems)\n- ยาน้ำแขวนตะกอน (Suspensions)\n- ยาน้ำอิมัลชัน (Emulsions)", "สอบภาคทฤษฎีกลางภาค\n(จัดสอบโดยคณะ/มหาวิทยาลัย)"],
        ["สอบทักษะทางเภสัชกรรม (Pharmacy Skill Exam)", "พุธ 14 ตุลาคม 2569", "13:30 - 16:30 น.", "สอบปฏิบัติการทดสอบทักษะทางเภสัชกรรม:\n- การชั่งสาร การคำนวณตำรับ\n- การผสมและการเตรียมยาน้ำ/ยากึ่งแข็ง\n- การบรรจุและการปิดป้ายฉลาก", "ห้องปฏิบัติการเทคโนโลยีเภสัชกรรม\nอาคาร 5 ร้านขายยา ชั้น 2"],
        ["สอบปลายภาค (Final Exam)", "19 ต.ค. - 2 พ.ย. 2569", "ตามตารางสอบคณะ", "หัวข้อบรรยายที่ 6-8:\n- ยารูปแบบกึ่งแข็ง (ขี้ผึ้ง, ครีม, เพสต์, เจล, ระบบส่งยาผ่านผิวหนัง)\n- ยาเหน็บ (Suppositories)\n- การควบคุมคุณภาพและการประเมินความคงสภาพของผลิตภัณฑ์", "สอบภาคทฤษฎีปลายภาค\n*(ต้องมีเวลาเรียนแลป >= 80%)*"]
    ]

    body = {'values': values}

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Schedule!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    # Styling formatting requests
    requests = []

    # 1. Set explicit column widths
    col_widths = [240, 180, 170, 480, 360]
    for idx, width in enumerate(col_widths):
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": idx,
                    "endIndex": idx + 1
                },
                "properties": {"pixelSize": width},
                "fields": "pixelSize"
            }
        })

    # 2. Set default font (Lexend), vertical alignment MIDDLE, wrap strategy WRAP
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 60,
                "startColumnIndex": 0,
                "endColumnIndex": 5
            },
            "cell": {
                "userEnteredFormat": {
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP",
                    "textFormat": {
                        "fontFamily": "Lexend",
                        "fontSize": 11,
                        "foregroundColor": hex_to_rgb("222222")
                    }
                }
            },
            "fields": "userEnteredFormat(verticalAlignment,wrapStrategy,textFormat)"
        }
    })

    # 3. Main Title & Subtitle Styling (Rows 0 & 1)
    requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})
    requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})
    
    requests.append({
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 5},
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "backgroundColor": hex_to_rgb("1B365D"), # Deep Navy
                    "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": hex_to_rgb("FFFFFF")}
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,backgroundColor,textFormat)"
        }
    })
    requests.append({
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 5},
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "backgroundColor": hex_to_rgb("2C4D75"),
                    "textFormat": {"bold": False, "fontSize": 12, "foregroundColor": hex_to_rgb("E2E8F0")}
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,backgroundColor,textFormat)"
        }
    })
    requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 55}, "fields": "pixelSize"}})
    requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 35}, "fields": "pixelSize"}})

    # Helper function to style a Subject Block
    def style_subject_section(start_row, main_banner_title_row, tbl1_title_row, tbl1_header_row, tbl1_data_rows, tbl2_title_row, tbl2_header_row, tbl2_data_rows, theme_colors, anat_merge_grade=False):
        # Theme colors: banner_bg, title_bg, header_bg, text_color
        banner_bg, title_bg, header_bg, text_color = theme_colors

        # Main Subject Banner
        requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": main_banner_title_row, "endRowIndex": main_banner_title_row + 1, "startColumnIndex": 0, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})
        requests.append({
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": main_banner_title_row, "endRowIndex": main_banner_title_row + 1, "startColumnIndex": 0, "endColumnIndex": 5},
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "LEFT",
                        "backgroundColor": hex_to_rgb(banner_bg),
                        "textFormat": {"bold": True, "fontSize": 15, "foregroundColor": hex_to_rgb("FFFFFF")}
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,backgroundColor,textFormat)"
            }
        })
        requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": main_banner_title_row, "endIndex": main_banner_title_row + 1}, "properties": {"pixelSize": 45}, "fields": "pixelSize"}})

        # Table Titles
        for t_row in [tbl1_title_row, tbl2_title_row]:
            requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": t_row, "endRowIndex": t_row + 1, "startColumnIndex": 0, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": t_row, "endRowIndex": t_row + 1, "startColumnIndex": 0, "endColumnIndex": 5},
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "backgroundColor": hex_to_rgb(title_bg),
                            "textFormat": {"bold": True, "fontSize": 13, "foregroundColor": hex_to_rgb(text_color)}
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,backgroundColor,textFormat)"
                }
            })
            requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": t_row, "endIndex": t_row + 1}, "properties": {"pixelSize": 38}, "fields": "pixelSize"}})

        # Table Headers
        for h_row in [tbl1_header_row, tbl2_header_row]:
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": h_row, "endRowIndex": h_row + 1, "startColumnIndex": 0, "endColumnIndex": 5},
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "backgroundColor": hex_to_rgb(header_bg),
                            "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": hex_to_rgb(text_color)}
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,backgroundColor,textFormat)"
                }
            })
            requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": h_row, "endIndex": h_row + 1}, "properties": {"pixelSize": 38}, "fields": "pixelSize"}})

        # Table Borders
        for start_r, end_r in [(tbl1_header_row, tbl1_data_rows[-1] + 1), (tbl2_header_row, tbl2_data_rows[-1] + 1)]:
            requests.append({
                "updateBorders": {
                    "range": {"sheetId": sheet_id, "startRowIndex": start_r, "endRowIndex": end_r, "startColumnIndex": 0, "endColumnIndex": 5},
                    "top": {"style": "SOLID", "width": 1, "color": hex_to_rgb("CBD5E1")},
                    "bottom": {"style": "SOLID", "width": 1, "color": hex_to_rgb("CBD5E1")},
                    "left": {"style": "SOLID", "width": 1, "color": hex_to_rgb("CBD5E1")},
                    "right": {"style": "SOLID", "width": 1, "color": hex_to_rgb("CBD5E1")},
                    "innerHorizontal": {"style": "SOLID", "width": 1, "color": hex_to_rgb("E2E8F0")},
                    "innerVertical": {"style": "SOLID", "width": 1, "color": hex_to_rgb("E2E8F0")}
                }
            })

        # Center Align Column B & C for Date & Time rows
        for d_row in tbl2_data_rows:
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": d_row, "endRowIndex": d_row + 1, "startColumnIndex": 1, "endColumnIndex": 3},
                    "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                    "fields": "userEnteredFormat(horizontalAlignment)"
                }
            })
            # Row heights for data rows
            requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": d_row, "endIndex": d_row + 1}, "properties": {"pixelSize": 50}, "fields": "pixelSize"}})

        for d_row in tbl1_data_rows:
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": d_row, "endRowIndex": d_row + 1, "startColumnIndex": 1, "endColumnIndex": 2},
                    "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                    "fields": "userEnteredFormat(horizontalAlignment)"
                }
            })
            requests.append({"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": d_row, "endIndex": d_row + 1}, "properties": {"pixelSize": 50}, "fields": "pixelSize"}})

    # Apply styling for 1. Anatomy (Blue Theme)
    style_subject_section(
        start_row=3,
        main_banner_title_row=3,
        tbl1_title_row=4,
        tbl1_header_row=5,
        tbl1_data_rows=[6, 7, 8, 9],
        tbl2_title_row=11,
        tbl2_header_row=12,
        tbl2_data_rows=[13, 14, 15],
        theme_colors=("2563EB", "DBEAFE", "EFF6FF", "1E40AF")
    )
    # Merge Grade column for Anat (Col E rows 6 to 9)
    requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": 6, "endRowIndex": 10, "startColumnIndex": 4, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})

    # Apply styling for 2. Physiology (Green Theme)
    style_subject_section(
        start_row=18,
        main_banner_title_row=18,
        tbl1_title_row=19,
        tbl1_header_row=20,
        tbl1_data_rows=[21, 22, 23, 24],
        tbl2_title_row=26,
        tbl2_header_row=27,
        tbl2_data_rows=[28, 29, 30, 31, 32],
        theme_colors=("16A34A", "DCFCE7", "F0FDF4", "166534")
    )
    # Merge Grade column for Phso (Col E rows 21 to 24)
    requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": 21, "endRowIndex": 25, "startColumnIndex": 4, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})

    # Apply styling for 3. Pharm Tech 2 (Purple/Amber Theme)
    style_subject_section(
        start_row=35,
        main_banner_title_row=35,
        tbl1_title_row=36,
        tbl1_header_row=37,
        tbl1_data_rows=[38, 39, 40, 41, 42, 43, 44, 45],
        tbl2_title_row=47,
        tbl2_header_row=48,
        tbl2_data_rows=[49, 50, 51],
        theme_colors=("D97706", "FEF3C7", "FFFBEB", "92400E")
    )
    # Merge Grade column for PharmTech (Col E rows 38 to 45)
    requests.append({"mergeCells": {"range": {"sheetId": sheet_id, "startRowIndex": 38, "endRowIndex": 46, "startColumnIndex": 4, "endColumnIndex": 5}, "mergeType": "MERGE_ALL"}})

    # Execute all batchUpdate requests
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

if __name__ == '__main__':
    url = update_beautiful_sheet()
    print(f"SUCCESS_URL:{url}")
