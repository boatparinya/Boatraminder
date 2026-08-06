---
description: ดึงข้อมูล/เอกสารจาก Mango Canvas มาสรุปแล้วสร้างเป็นไฟล์ Google Docs
---

You are running the /mangotodocs command.

When the user runs this skill, perform the following steps in sequence:

### Steps:
1. **ดึงข้อมูลจาก Canvas:**
   - รันสคริปต์ `python scripts/canvas_tool.py` เพื่ออ่านเนื้อหา ประกาศ หรือการบ้านล่าสุดจาก Mango Canvas
   
2. **ประมวลผลและสรุปเนื้อหา:**
   - สรุปข้อมูลที่ดึงมาให้อยู่ในรูปแบบที่อ่านง่าย โดยแบ่งเป็น 3 หัวข้อหลัก:
     - 📌 **สรุปสาระสำคัญ/เนื้อหาเรียน** (ภาษาไทย ย่อยง่าย)
     - 📅 **กำหนดการส่งงาน/ตารางสอบที่ต้องระวัง**
     - 💡 **Action Items ที่นักศึกษาต้องทำต่อ**

3. **ส่งข้อมูลไปยัง Google Docs:**
   - นำข้อความสรุปที่ได้ รันผ่านสคริปต์ `python scripts/google_docs_tool.py "<ชื่อหัวข้อเอกสาร>" "<เนื้อหาที่สรุปแล้ว>"`
   
4. **รายงานผล:**
   - นำลิงก์ Google Docs ที่ได้จากสคริปต์ มาแสดงในช่องแชตเพื่อให้ผู้ใช้คลิกเปิดดูได้ทันที
