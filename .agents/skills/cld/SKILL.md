---
name: cld
description: >-
  Add a new task, event, or meeting to Google Calendar.
  Trigger this skill when the user explicitly uses the /cld slash command or asks to add/schedule an event in Google Calendar.
argument-hint: "<title> <date> [start_time] [end_time] [description]"
---

# Skill: Add Google Calendar Event Command (/cld)

This skill allows the agent to quickly insert new events, tasks, or meetings into the user's Google Calendar using the project's internal `scripts/add_calendar_event.py` script.

## Procedures

1. **Parse Arguments & Detect Dates/Times**:
   - Parse `<title>`, `<date>`, optional `[start_time]`, optional `[end_time]`, and optional `[description]`.
   - **Relative Dates**:
     - If the user uses relative terms like "วันนี้" (today), "พรุ่งนี้" (tomorrow), "มะรืนนี้" (day after tomorrow), calculate the exact date in `YYYY-MM-DD` format relative to today's local date (Thailand timezone, UTC+7).
     - If the user mentions a day of the week (e.g. "วันศุกร์นี้", "วันจันทร์หน้า"), calculate the target date accordingly.
     - If the user writes a date in Thai format (e.g. "12 ส.ค.", "5 ก.ย. 2026"), format it to `YYYY-MM-DD`.
   - **Time Parsing**:
     - If time is written in Thai colloquial terms (e.g., "10โมง" -> "10:00", "บ่ายสอง" -> "14:00", "ทุ่มครึ่ง" -> "19:30"), convert it to standard 24h `HH:MM` format.
     - If no time is specified by the user, you may treat it as an all-day event using the `--all-day` flag, or prompt the user if time is essential.

2. **Execute Python Calendar Script**:
   Run `scripts/add_calendar_event.py` using `run_command`:
   ```bash
   python scripts/add_calendar_event.py --title "<title>" --date "<YYYY-MM-DD>" --start-time "<HH:MM>" --end-time "<HH:MM>" --description "<description>"
   ```
   *Note: If it's an all-day event, use:*
   ```bash
   python scripts/add_calendar_event.py --title "<title>" --date "<YYYY-MM-DD>" --all-day
   ```

3. **Respond to User**:
   - Report the outcome to the user in Gigi's persona (calling the user "เตง", self "เค้า", and polite particles "ค่ะ/นะคะ").
   - Include the event title, formatted date, time interval, and Google Calendar link provided by the script output.
