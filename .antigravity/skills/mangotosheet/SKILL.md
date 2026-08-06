---
description: ดึงข้อมูลการบ้านและกำหนดส่งงานจาก Mango Canvas ไปบันทึกลง Google Sheets
---

You are running the /mangotosheet command.

When the user runs this skill, perform the following steps in sequence:

### Steps:
1. **ดึงข้อมูลจาก Mango Canvas เท่านั้น:**
   - รันสคริปต์ `python scripts/canvas_tool.py` เพื่อดึงรายการการบ้าน วิชาเรียน และกำหนดวันส่งงานล่าสุด
2. **ประมวลผลข้อมูล:**
   - จัดกลุ่มข้อมูลให้อยู่ในรูปแบบตาราง ได้แก่: [ชื่อวิชา] | [ชื่อการบ้าน/งาน] | [วัน/เวลาที่ต้องส่ง] | [สถานะ]
3. **บันทึกลง Google Sheets:**
   - รันสคริปต์ `python scripts/google_sheets_tool.py` เพื่อนำข้อมูลตารางดังกล่าวไปเขียนต่อท้าย (Append) หรืออัปเดตใน Google Sheets
4. **รายงานผล:**
   - แสดงข้อความยืนยันการบันทึกข้อมูล พร้อมแนบลิงก์ Google Sheets ให้ผู้ใช้คลิกเปิดดูได้ทันที
