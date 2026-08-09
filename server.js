require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve Frontend files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/app.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'app.js'));
});

app.get('/style.css', (req, res) => {
  res.sendFile(path.join(__dirname, 'style.css'));
});

// Helper: Safe time parsing for Thai Timezone (UTC+7)
function parseReminderTime(dateStr, timeStr) {
  if (!dateStr || !timeStr) return new Date(NaN);
  const parts = timeStr.split(':');
  const hh = (parts[0] || '0').padStart(2, '0');
  const mm = (parts[1] || '00').padStart(2, '0');
  const ss = (parts[2] || '00').padStart(2, '0');
  return new Date(`${dateStr}T${hh}:${mm}:${ss}+07:00`);
}

// Helper: คำนวณว่าควร skip notification ไหนบ้าง (พร้อมกำหนดเวลามาตรฐานประเทศไทย +07:00)
function calcNotificationFlags(date, time) {
  const now = new Date();
  const reminderTime = parseReminderTime(date, time);
  if (isNaN(reminderTime.getTime())) {
    return { notified1Day: false, notified1Hour: false, notified: false };
  }
  const diffMs = reminderTime - now;
  const ONE_DAY_MS  = 24 * 60 * 60 * 1000;
  const ONE_HOUR_MS = 60 * 60 * 1000;

  return {
    notified1Day:  diffMs < ONE_DAY_MS,   // เหลือ < 1 วัน → ข้ามแจ้ง 1 วัน
    notified1Hour: diffMs < ONE_HOUR_MS,  // เหลือ < 1 ชม → ข้ามแจ้ง 1 ชม
    notified:      diffMs < 0             // เวลาผ่านไปแล้วตอนสร้าง → ข้ามการแจ้งเตือนย้อนหลัง
  };
}

// API Routes

// Get all reminders
app.get('/api/reminders', async (req, res) => {
  try {
    const reminders = await db.getAll();
    res.json(reminders);
  } catch (error) {
    console.error('Error fetching reminders:', error);
    res.status(500).json({ error: 'Failed to fetch reminders' });
  }
});

// Add a new reminder
app.post('/api/reminders', async (req, res) => {
  const { title, date, time, notes } = req.body;

  if (!title || !date || !time) {
    return res.status(400).json({ error: 'Title, date, and time are required' });
  }

  try {
    const flags = calcNotificationFlags(date, time);
    const saved = await db.create({
      title,
      date,
      time,
      notes: notes || '',
      completed: false,
      ...flags
    });

    res.status(201).json(saved);
  } catch (error) {
    console.error('Error creating reminder:', error);
    res.status(500).json({ error: 'Failed to create reminder' });
  }
});

// Update a reminder
app.put('/api/reminders/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const reminder = await db.getById(id);
    if (!reminder) {
      return res.status(404).json({ error: 'Reminder not found' });
    }

    const updates = {};

    // Toggle complete state
    if (req.body.hasOwnProperty('completed')) {
      updates.completed = req.body.completed;
      if (req.body.completed === false) {
        updates.notified = false; // Reset if marked active again
      }
    }

    if (req.body.title) updates.title = req.body.title;

    // ถ้าแก้ date หรือ time → คำนวณ flags ใหม่
    if (req.body.date || req.body.time) {
      const newDate = req.body.date || reminder.date;
      const newTime = req.body.time || reminder.time;
      updates.date = newDate;
      updates.time = newTime;

      const flags = calcNotificationFlags(newDate, newTime);
      updates.notified1Day  = flags.notified1Day;
      updates.notified1Hour = flags.notified1Hour;
      updates.notified      = false;
    }

    if (req.body.notes !== undefined) updates.notes = req.body.notes;

    const updated = await db.update(id, updates);
    res.json(updated);
  } catch (error) {
    console.error('Error updating reminder:', error);
    res.status(500).json({ error: 'Failed to update reminder' });
  }
});

// Delete a reminder
app.delete('/api/reminders/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const deleted = await db.delete(id);
    if (!deleted) {
      return res.status(404).json({ error: 'Reminder not found' });
    }
    res.json({ message: 'Reminder deleted successfully', id });
  } catch (error) {
    console.error('Error deleting reminder:', error);
    res.status(500).json({ error: 'Failed to delete reminder' });
  }
});
app.get('/api/ping', async (req, res) => {
  try {
    const { checkAndNotifyReminders } = require('./scheduler');
    await checkAndNotifyReminders();
    res.json({ status: 'ok', message: 'Pong! Gigi checked reminders successfully 🌸', time: new Date().toISOString() });
  } catch (err) {
    console.error('Error during ping check:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// Start Server after Database Initialization
db.init().then(() => {
  // Start background scheduler
  require('./scheduler');

  app.listen(PORT, () => {
    console.log(`==================================================`);
    console.log(`🚀 Gigi's Personal Reminder App is running!`);
    console.log(`🔗 Local Server: http://localhost:${PORT}`);
    console.log(`==================================================`);
  });
});
