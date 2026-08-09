require('dotenv').config();
const cron = require('node-cron');
const https = require('https');
const db = require('./db');

// Send LINE message
function sendLineMessage(reminder, type) {
  const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;
  const userId = process.env.LINE_USER_ID;

  if (!token || !userId || token.includes('YOUR_') || userId.includes('YOUR_')) {
    console.log(`[LINE Notifier] ⚠️ แจ้งเตือนจำลอง (${type}): "${reminder.title}"`);
    return Promise.resolve(true);
  }

  // Message template ตามประเภทการแจ้งเตือน
  let messageText = '';

  if (type === '1day') {
    messageText = `🗓️ เตือนล่วงหน้า 1 วันค่ะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nพรุ่งนี้แล้วนะคะ เตรียมตัวให้พร้อมด้วยนะเตง 💪`;
  } else if (type === '1hour') {
    messageText = `⏰ อีก 1 ชั่วโมงแล้วนะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nใกล้ถึงเวลาแล้วค่ะ อย่าลืมเตรียมพร้อมด้วยนะคะ! 🌸`;
  } else if (type === 'late') {
    messageText = `⚠️ แจ้งเตือนย้อนหลังค่ะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 กำหนดเวลาเดิม: ${reminder.date} เวลา ${reminder.time} น.\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\n(ขออภัยที่แจ้งเตือนล่าช้าเนื่องจากเกิดข้อผิดพลาดหรือระบบขัดข้องก่อนหน้านี้นะคะ เตงอย่าลืมตรวจสอบงานน้า! 🌸)`;
  } else {
    messageText = `🔔 ถึงเวลาแล้วค่ะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nสู้ๆ นะคะเตง เค้าเป็นกำลังใจให้! 💕`;
  }

  const postData = JSON.stringify({
    to: userId,
    messages: [{ type: 'text', text: messageText }]
  });

  const options = {
    hostname: 'api.line.me',
    port: 443,
    path: '/v2/bot/message/push',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  return new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          console.log(`[LINE Notifier] ✅ ส่งแจ้งเตือน (${type}) งาน "${reminder.title}" สำเร็จ!`);
          resolve(true);
        } else {
          console.error(`[LINE Notifier] ❌ ส่งไม่สำเร็จ (${type}, Status: ${res.statusCode}):`, body);
          resolve(false);
        }
      });
    });
    req.on('error', (e) => {
      console.error(`[LINE Notifier] ❌ HTTP Error:`, e);
      resolve(false);
    });
    req.write(postData);
    req.end();
  });
}

// Parse date and time string safely into Thai Local Time (UTC+7) Date object
function parseReminderTime(dateStr, timeStr) {
  if (!dateStr || !timeStr) return new Date(NaN);
  const parts = timeStr.split(':');
  const hh = (parts[0] || '0').padStart(2, '0');
  const mm = (parts[1] || '00').padStart(2, '0');
  const ss = (parts[2] || '00').padStart(2, '0');
  return new Date(`${dateStr}T${hh}:${mm}:${ss}+07:00`);
}

// Core logic: เช็กและแจ้งเตือน
async function checkAndNotifyReminders() {
  try {
    const now = new Date();
    const reminders = await db.getActive();

    for (let reminder of reminders) {
      const reminderTime = parseReminderTime(reminder.date, reminder.time);
      if (isNaN(reminderTime.getTime())) continue;

      const diffMs = reminderTime - now; // milliseconds เหลืออยู่ก่อนถึงกำหนด

      const ONE_DAY_MS   = 24 * 60 * 60 * 1000;
      const ONE_HOUR_MS  = 60 * 60 * 1000;

      const updates = {};

      // 🗓️ แจ้งเตือน 1 วันก่อน (ถ้าเหลือเวลาอยู่ในช่วง 1 ชม. - 24 ชม.)
      if (!reminder.notified1Day && diffMs > ONE_HOUR_MS && diffMs <= ONE_DAY_MS) {
        console.log(`[Scheduler] 🗓️ แจ้งล่วงหน้า 1 วัน: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, '1day');
        if (success) {
          updates.notified1Day = true;
        }
      }

      // ⏰ แจ้งเตือน 1 ชั่วโมงก่อน (ถ้าเหลือเวลาอยู่ในช่วง 0 - 1 ชม.)
      if (!reminder.notified1Hour && diffMs > 0 && diffMs <= ONE_HOUR_MS) {
        console.log(`[Scheduler] ⏰ แจ้งล่วงหน้า 1 ชม.: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, '1hour');
        if (success) {
          updates.notified1Hour = true;
        }
      }

      // 🔔 แจ้งเตือนเมื่อถึงกำหนดเวลา (diffMs <= 0)
      if (!reminder.notified && diffMs <= 0) {
        // ถ้านับจากเวลาที่กำหนดไว้ (reminderTime) ผ่านไปเกิน 15 นาที ถึงจะถือว่าเป็นแจ้งเตือนย้อนหลัง (Late)
        const isLateNotification = (now - reminderTime) > 15 * 60 * 1000;
        const msgType = isLateNotification ? 'late' : 'now';

        console.log(`[Scheduler] ${isLateNotification ? '⚠️ แจ้งเตือนย้อนหลัง (เลยกำหนด > 15 นาที)' : '🔔 ถึงเวลาแล้ว'}: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, msgType);
        if (success) {
          updates.notified = true;
        }
      }

      if (Object.keys(updates).length > 0) {
        await db.update(reminder.id || reminder._id, updates);
      }
    }
  } catch (error) {
    console.error('[Scheduler] ❌ Error:', error);
  }
}

// Cron Job รันทุก 1 นาที เพื่อความแม่นยำของเวลา
cron.schedule('* * * * *', async () => {
  console.log(`[Scheduler] 🔍 เช็กงานที่ถึงกำหนด... (${new Date().toLocaleTimeString('th-TH')})`);
  await checkAndNotifyReminders();
});

// เช็กรอบแรกทันทีหลังเปิด Server
setTimeout(async () => {
  console.log(`[Scheduler] 🔍 เช็กกิจกรรมรอบแรกหลังเปิดเซิร์ฟเวอร์...`);
  await checkAndNotifyReminders();
}, 2000);

console.log(`[Scheduler] ⏰ ระบบ Cron Job เริ่มทำงานแล้ว (รันทุก 1 นาที)`);

module.exports = { checkAndNotifyReminders, sendLineMessage };
