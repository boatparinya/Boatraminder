require('dotenv').config();
const cron = require('node-cron');
const https = require('https');
const Reminder = require('./models/Reminder');

// Send LINE message
function sendLineMessage(reminder, type) {
  const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;
  const userId = process.env.LINE_USER_ID;

  if (!token || !userId || token.includes('YOUR_') || userId.includes('YOUR_')) {
    console.log(`[LINE Notifier] ⚠️ แจ้งเตือนจำลอง (${type}): "${reminder.title}"`);
    return Promise.resolve(true);
  }

  const categoryLabel = {
    study: 'การเรียน 📚',
    faculty: 'กิจกรรมคณะ 👥',
    personal: 'เรื่องส่วนตัว 🏠'
  }[reminder.category] || 'ทั่วไป 📅';

  // Message template ตามประเภทการแจ้งเตือน
  let messageText = '';

  if (type === '1day') {
    messageText = `🗓️ เตือนล่วงหน้า 1 วันค่ะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n🏷️ หมวดหมู่: ${categoryLabel}\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nพรุ่งนี้แล้วนะคะ เตรียมตัวให้พร้อมด้วยนะเตง 💪`;
  } else if (type === '1hour') {
    messageText = `⏰ อีก 1 ชั่วโมงแล้วนะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n🏷️ หมวดหมู่: ${categoryLabel}\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nใกล้ถึงเวลาแล้วค่ะ อย่าลืมเตรียมพร้อมด้วยนะคะ! 🌸`;
  } else {
    messageText = `🔔 ถึงเวลาแล้วค่ะเตง!\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n🏷️ หมวดหมู่: ${categoryLabel}\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nสู้ๆ นะคะเตง เค้าเป็นกำลังใจให้! 💕`;
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

// Core logic: เช็กและแจ้งเตือน
async function checkAndNotifyReminders() {
  try {
    const now = new Date();
    const reminders = await Reminder.find({ completed: false });

    for (let reminder of reminders) {
      const reminderTime = new Date(`${reminder.date}T${reminder.time}`);
      const diffMs = reminderTime - now; // milliseconds เหลืออยู่

      const ONE_DAY_MS   = 24 * 60 * 60 * 1000;
      const ONE_HOUR_MS  = 60 * 60 * 1000;

      let hasChanges = false;

      // 🗓️ แจ้งเตือน 1 วันก่อน (diffMs อยู่ระหว่าง 23h55m ~ 24h5m)
      if (!reminder.notified1Day && diffMs > 0 && diffMs <= ONE_DAY_MS && diffMs > ONE_HOUR_MS) {
        console.log(`[Scheduler] 🗓️ แจ้งล่วงหน้า 1 วัน: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, '1day');
        if (success) {
          reminder.notified1Day = true;
          hasChanges = true;
        }
      }

      // ⏰ แจ้งเตือน 1 ชั่วโมงก่อน (diffMs อยู่ระหว่าง 0 ~ 1h)
      if (!reminder.notified1Hour && diffMs > 0 && diffMs <= ONE_HOUR_MS) {
        console.log(`[Scheduler] ⏰ แจ้งล่วงหน้า 1 ชม.: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, '1hour');
        if (success) {
          reminder.notified1Hour = true;
          hasChanges = true;
        }
      }

      // 🔔 แจ้งเตือนตรงเวลา (diffMs <= 0)
      if (!reminder.notified && diffMs <= 0) {
        console.log(`[Scheduler] 🔔 ถึงเวลาแล้ว: "${reminder.title}"`);
        const success = await sendLineMessage(reminder, 'now');
        if (success) {
          reminder.notified = true;
          hasChanges = true;
        }
      }

      if (hasChanges) {
        await reminder.save();
      }
    }
  } catch (error) {
    console.error('[Scheduler] ❌ Error:', error);
  }
}

// Cron Job ทุก 5 นาที
cron.schedule('*/5 * * * *', async () => {
  console.log(`[Scheduler] 🔍 เช็กงานที่ถึงกำหนด... (${new Date().toLocaleTimeString('th-TH')})`);
  await checkAndNotifyReminders();
});

// เช็กรอบแรกทันทีหลังเปิด Server
setTimeout(async () => {
  console.log(`[Scheduler] 🔍 เช็กกิจกรรมรอบแรกหลังเปิดเซิร์ฟเวอร์...`);
  await checkAndNotifyReminders();
}, 2000);

console.log(`[Scheduler] ⏰ ระบบ Cron Job เริ่มทำงานแล้ว (รันทุก 5 นาที)`);
