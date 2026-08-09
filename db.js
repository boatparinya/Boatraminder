const fs = require('fs');
const path = require('path');
const dns = require('dns');
const mongoose = require('mongoose');
const ReminderModel = require('./models/Reminder');

// Fix Windows DNS SRV lookup issue for MongoDB Atlas (mongodb+srv://)
try {
  dns.setServers(['8.8.8.8', '1.1.1.1']);
} catch (e) {
  // Fallback if custom DNS setting is not permitted
}

const FILE_PATH = path.join(__dirname, 'data', 'reminders.json');

let isMongo = false;

// Ensure data directory and file exist
if (!fs.existsSync(path.join(__dirname, 'data'))) {
  fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });
}
if (!fs.existsSync(FILE_PATH)) {
  fs.writeFileSync(FILE_PATH, '[]', 'utf-8');
}

function readJsonFile() {
  try {
    const data = fs.readFileSync(FILE_PATH, 'utf-8');
    return JSON.parse(data || '[]');
  } catch (e) {
    return [];
  }
}

function writeJsonFile(items) {
  try {
    fs.writeFileSync(FILE_PATH, JSON.stringify(items, null, 2), 'utf-8');
  } catch (e) {
    console.error('[DB] File write error:', e.message);
  }
}

const db = {
  async init() {
    if (process.env.MONGODB_URI) {
      try {
        await mongoose.connect(process.env.MONGODB_URI);
        isMongo = true;
        console.log('==================================================');
        console.log('✅ เชื่อมต่อ MongoDB Atlas สำเร็จแล้วค่ะ!');
        console.log('==================================================');
        return true;
      } catch (err) {
        console.warn('⚠️ เชื่อมต่อ MongoDB ไม่สำเร็จ สลับมาใช้ data/reminders.json:', err.message);
        isMongo = false;
        return false;
      }
    } else {
      console.log('==================================================');
      console.log('ℹ️ ไม่พบคีย์ MONGODB_URI -> ใช้งานระบบไฟล์ data/reminders.json');
      console.log('==================================================');
      isMongo = false;
      return false;
    }
  },

  isMongoConnected() {
    return isMongo;
  },

  async getAll() {
    if (isMongo) {
      const items = await ReminderModel.find().sort({ createdAt: -1 });
      const plain = items.map(r => ({ ...r.toObject(), id: r._id.toString() }));
      writeJsonFile(plain);
      return plain;
    }
    const items = readJsonFile();
    return items.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));
  },

  async getActive() {
    if (isMongo) {
      const items = await ReminderModel.find({ completed: false });
      return items.map(r => ({ ...r.toObject(), id: r._id.toString() }));
    }
    const items = readJsonFile();
    return items.filter(r => !r.completed);
  },

  async getById(id) {
    if (isMongo) {
      const doc = await ReminderModel.findById(id);
      return doc ? { ...doc.toObject(), id: doc._id.toString() } : null;
    }
    const items = readJsonFile();
    return items.find(r => (r._id || r.id) === id) || null;
  },

  async create(data) {
    if (isMongo) {
      const newDoc = new ReminderModel(data);
      const saved = await newDoc.save();
      await db.syncToFile();
      return { ...saved.toObject(), id: saved._id.toString() };
    }
    const items = readJsonFile();
    const newId = 'id-' + Date.now();
    const newItem = {
      id: newId,
      _id: newId,
      ...data,
      createdAt: data.createdAt || new Date().toISOString()
    };
    items.unshift(newItem);
    writeJsonFile(items);
    return newItem;
  },

  async update(id, updates) {
    if (isMongo) {
      const doc = await ReminderModel.findById(id);
      if (!doc) return null;
      Object.assign(doc, updates);
      const saved = await doc.save();
      await db.syncToFile();
      return { ...saved.toObject(), id: saved._id.toString() };
    }
    const items = readJsonFile();
    const index = items.findIndex(r => (r._id || r.id) === id);
    if (index === -1) return null;
    items[index] = { ...items[index], ...updates };
    writeJsonFile(items);
    return items[index];
  },

  async delete(id) {
    if (isMongo) {
      const deleted = await ReminderModel.findByIdAndDelete(id);
      await db.syncToFile();
      return deleted;
    }
    let items = readJsonFile();
    const target = items.find(r => (r._id || r.id) === id);
    if (!target) return null;
    items = items.filter(r => (r._id || r.id) !== id);
    writeJsonFile(items);
    return target;
  },

  async syncToFile() {
    if (isMongo) {
      try {
        const all = await ReminderModel.find().sort({ createdAt: -1 });
        writeJsonFile(all.map(r => ({ ...r.toObject(), id: r._id.toString() })));
      } catch (err) {}
    }
  }
};

module.exports = db;
