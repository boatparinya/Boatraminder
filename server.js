require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const mongoose = require('mongoose');
const Reminder = require('./models/Reminder');

const app = express();
const PORT = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    console.log('==================================================');
    console.log('✅ เชื่อมต่อ MongoDB Atlas สำเร็จแล้วค่ะ!');
    console.log('==================================================');
  })
  .catch((err) => {
    console.error('❌ เชื่อมต่อ MongoDB ไม่สำเร็จ:', err.message);
    process.exit(1);
  });

// Import and run background scheduler (after DB is ready)
mongoose.connection.once('open', () => {
  require('./scheduler');
});

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

// API Routes

// Get all reminders
app.get('/api/reminders', async (req, res) => {
  try {
    const reminders = await Reminder.find().sort({ createdAt: -1 });
    res.json(reminders);
  } catch (error) {
    console.error('Error fetching reminders:', error);
    res.status(500).json({ error: 'Failed to fetch reminders' });
  }
});

// Add a new reminder
app.post('/api/reminders', async (req, res) => {
  const { title, date, time, category, notes } = req.body;

  if (!title || !date || !time || !category) {
    return res.status(400).json({ error: 'Title, date, time, and category are required' });
  }

  try {
    const newReminder = new Reminder({
      title,
      date,
      time,
      category,
      notes: notes || '',
      completed: false,
      notified: false
    });

    const saved = await newReminder.save();
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
    const reminder = await Reminder.findById(id);
    if (!reminder) {
      return res.status(404).json({ error: 'Reminder not found' });
    }

    // Toggle complete state
    if (req.body.hasOwnProperty('completed')) {
      reminder.completed = req.body.completed;
      if (req.body.completed === false) {
        reminder.notified = false; // Reset if marked active again
      }
    }

    if (req.body.title) reminder.title = req.body.title;

    if (req.body.date) {
      reminder.date = req.body.date;
      reminder.notified = false; // Reset if date changes
    }

    if (req.body.time) {
      reminder.time = req.body.time;
      reminder.notified = false; // Reset if time changes
    }

    if (req.body.category) reminder.category = req.body.category;
    if (req.body.notes !== undefined) reminder.notes = req.body.notes;

    const updated = await reminder.save();
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
    const deleted = await Reminder.findByIdAndDelete(id);
    if (!deleted) {
      return res.status(404).json({ error: 'Reminder not found' });
    }
    res.json({ message: 'Reminder deleted successfully', id });
  } catch (error) {
    console.error('Error deleting reminder:', error);
    res.status(500).json({ error: 'Failed to delete reminder' });
  }
});

app.listen(PORT, () => {
  console.log(`==================================================`);
  console.log(`🚀 Gigi's Personal Reminder App is running!`);
  console.log(`🔗 Local Server: http://localhost:${PORT}`);
  console.log(`==================================================`);
});
