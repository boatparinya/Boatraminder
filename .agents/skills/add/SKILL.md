---
name: add
description: >-
  Add a new task or meeting reminder to the user's personal reminder application.
  Trigger this skill when the user explicitly uses the /add slash command or asks to add/schedule a reminder.
argument-hint: "<title> <date> <time> [notes]"
---

# Skill: Add Reminder Command

This skill allows the agent to quickly insert new reminders into the local database (supporting both MongoDB Atlas and reminders.json fallback) using the project's internal database module.

## Procedures

1. **Parse Arguments & Detect Dates**:
   - Parse `<title>`, `<date>`, `<time>`, and optionally `[notes]`.
   - If the user uses relative terms like "พรุ่งนี้" (tomorrow) or "มะรืนนี้" (day after tomorrow), calculate the exact date in `YYYY-MM-DD` format relative to today's local date (Thailand timezone, UTC+7).
   - If time is written in Thai format (e.g. "10โมง" -> "10:00", "บ่ายสาม" -> "15:00"), parse it to standard 24h `HH:MM` format.

2. **Generate Temporary Script**:
   Write a temporary Node.js script in the root directory named `temp_add_reminder.js`:
   ```javascript
   require('dotenv').config();
   const db = require('./db');
   async function run() {
     await db.init();
     const now = new Date();
     const reminderTime = new Date("<date>T<time>:00+07:00");
     const diffMs = reminderTime - now;
     const ONE_DAY_MS = 24 * 60 * 60 * 1000;
     const ONE_HOUR_MS = 60 * 60 * 1000;
     
     const flags = {
       notified1Day: diffMs < ONE_DAY_MS,
       notified1Hour: diffMs < ONE_HOUR_MS,
       notified: diffMs < 0
     };
     
     try {
       const saved = await db.create({
         title: "<title>",
         date: "<date>",
         time: "<time>",
         notes: "<notes>",
         completed: false,
         ...flags
       });
       console.log("SUCCESS:", saved.id);
     } catch (err) {
       console.error("ERROR:", err.message);
     }
     process.exit(0);
   }
   run();
   ```

3. **Execute and Clean up**:
   - Run the script: `node temp_add_reminder.js`
   - Delete the temporary script: `del temp_add_reminder.js` (on Windows) or `rm temp_add_reminder.js` (on Unix).
   - Inform the user that the reminder has been saved successfully.
