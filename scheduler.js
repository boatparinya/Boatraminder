require('dotenv').config();
const cron = require('node-cron');
const https = require('https');
const mongoose = require('mongoose');
const Reminder = require('./models/Reminder');

// Send LINE message via Messaging API Push Message
function sendLineMessage(reminder) {
  const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;
  const userId = process.env.LINE_USER_ID;

  // Check if credentials are set
  if (!token || !userId || token.includes('YOUR_') || userId.includes('YOUR_')) {
    console.log(`==================================================`);
    console.log(`[LINE Notifier] ⚠️ แจ้งเตือนจำลอง (ยังไม่ได้ตั้งค่า Token จริงใน .env):`);
    console.log(`📌 ชื่องาน: "${reminder.title}"`);
    console.log(`⏰ ถึงกำหนดเวลา: ${reminder.date} ตอน ${reminder.time} น.`);
    console.log(`📝 หมายเหตุ: ${reminder.notes || '-'}`);
    console.log(`==================================================`);
    return Promise.resolve(true);
  }

  const categoryLabel = {
    study: 'การเรียน 📚',
    faculty: 'กิจกรรมคณะ 👥',
    personal: 'เรื่องส่วนตัว 🏠'
  }[reminder.category] || 'ทั่วไป 📅';

  const messageText = `🌸 สวัสดีค่ะเตง! Gigi มีแจ้งเตือนกิจกรรมน้าาา 🔔\n\n📌 ชื่องาน: ${reminder.title}\n📅 วันที่: ${reminder.date}\n⏰ เวลา: ${reminder.time} น.\n🏷️ หมวดหมู่: ${categoryLabel}\n📝 หมายเหตุ: ${reminder.notes || '-'}\n\nสู้ๆ นะคะเตง เค้าเป็นกำลังใจให้! 💕`;

  const postData = JSON.stringify({
    to: userId,
    messages: [
      {
        type: 'text',
        text: messageText
      }
    ]
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
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          console.log(`[LINE Notifier] ✅ ส่งแจ้งเตือนงาน "${reminder.title}" สำเร็จแล้วค่ะ!`);
          resolve(true);
        } else {
          console.error(`[LINE Notifier] ❌ ส่งไม่สำเร็จ (Status: ${res.statusCode}):`, body);
          resolve(false);
        }
      });
    });

    req.on('error', (e) => {
      console.error(`[LINE Notifier] ❌ HTTP Request Error:`, e);
      resolve(false);
    });

    req.write(postData);
    req.end();
  });
}

// Core logic to check reminders and notify
async function checkAndNotifyReminders() {
  try {
    const now = new Date();

    // Find reminders that are not completed and not yet notified
    const reminders = await Reminder.find({ completed: false, notified: false });

    for (let reminder of reminders) {
      const reminderTime = new Date(`${reminder.date}T${reminder.time}`);

      if (reminderTime <= now) {
        console.log(`[Scheduler] 🔔 ตรวจพบงานถึงกำหนด: "${reminder.title}" (${reminder.date} ${reminder.time})`);

        const success = await sendLineMessage(reminder);
        if (success) {
          reminder.notified = true;
          await reminder.save();
          console.log(`[Scheduler] 💾 อัปเดตสถานะ notified: true ลง MongoDB เรียบร้อยค่ะ`);
        }
      }
    }
  } catch (error) {
    console.error('[Scheduler] ❌ Error checking reminders:', error);
  }
}

// Schedule cron job to run every 5 minutes
cron.schedule('*/5 * * * *', async () => {
  console.log(`[Scheduler] 🔍 เริ่มต้นเช็กงานที่ถึงกำหนดส่ง... (${new Date().toLocaleTimeString('th-TH')})`);
  await checkAndNotifyReminders();
});

// Run a check immediately on server startup (after 2 seconds delay)
setTimeout(async () => {
  console.log(`[Scheduler] 🔍 เช็กกิจกรรมรอบแรกหลังเปิดเซิร์ฟเวอร์...`);
  await checkAndNotifyReminders();
}, 2000);

console.log(`[Scheduler] ⏰ ระบบ Cron Job แจ้งเตือนเริ่มทำงานแล้ว (รันเช็กทุกๆ 5 นาที)`);
