const mongoose = require('mongoose');

const reminderSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  date: {
    type: String,
    required: true
  },
  time: {
    type: String,
    required: true
  },
  notes: {
    type: String,
    default: ''
  },
  completed: {
    type: Boolean,
    default: false
  },
  notified1Day: {
    type: Boolean,
    default: false
  },
  notified1Hour: {
    type: Boolean,
    default: false
  },
  notified: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: { createdAt: 'createdAt', updatedAt: 'updatedAt' }
});

module.exports = mongoose.model('Reminder', reminderSchema);
