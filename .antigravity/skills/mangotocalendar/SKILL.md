---
description: ดึงกำหนดวันส่งงาน/ตารางสอบจาก Mango Canvas ไปสร้างเป็น Event ใน Google Calendar
---

You are running the /mangotocalendar command.

When the user runs this skill, perform the following steps in sequence:

### Steps:
1. **ดึงข้อมูลจาก Mango Canvas เท่านั้น:**
   - รันสคริปต์ `python scripts/canvas_tool.py` เพื่อดึงตารางกำหนดวันส่งงาน หรือวันสอบวิชาต่างๆ
2. **คัดกรองวันและเวลา:**
   - แปลงวันและเวลาที่ต้องส่งงานให้อยู่ในรูปแบบวันที่/เวลามาตรฐาน (YYYY-MM-DD HH:MM)
3. **สร้าง Event บน Google Calendar:**
   - รันสคริปต์ `python scripts/google_calendar_tool.py` เพื่อนำชื่อวิชา กำหนดส่งงาน และรายละเอียด ไปสร้างเป็นกิจกรรม (Event) พร้อมตั้งการแจ้งเตือนเตือนล่วงหน้าใน Google Calendar
4. **รายงานผล:**
   - สรุปรายการกิจกรรมที่เพิ่มลงปฏิทินสำเร็จให้ผู้ใช้ทราบในช่องแชต
