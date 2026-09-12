require('dotenv').config();
const crypto = require('crypto');
const https = require('https');
const db = require('./db');

// Verify LINE Signature
function verifySignature(rawBody, signature, secret) {
  if (!secret) return true; // Graceful fallback
  if (!signature || !rawBody) return false;
  const hash = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('base64');
  return hash === signature;
}

// Helper: Parse Thai Date & Time safely into Thai Timezone (UTC+7) Date
function getBangkokNow() {
  const now = new Date();
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
  return new Date(utc + (3600000 * 7));
}

function parseReminderTime(dateStr, timeStr) {
  if (!dateStr || !timeStr) return new Date(NaN);
  const parts = timeStr.split(':');
  const hh = (parts[0] || '0').padStart(2, '0');
  const mm = (parts[1] || '00').padStart(2, '0');
  const ss = (parts[2] || '00').padStart(2, '0');
  return new Date(`${dateStr}T${hh}:${mm}:${ss}+07:00`);
}

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
    notified1Day:  diffMs < ONE_DAY_MS,
    notified1Hour: diffMs < ONE_HOUR_MS,
    notified:      diffMs < 0
  };
}

// Month Mapping for Thai Months
const THAI_MONTHS = {
  'ม.ค.': 1, 'มกรา': 1, 'มกราคม': 1,
  'ก.พ.': 2, 'กุมภา': 2, 'กุมภาพันธ์': 2,
  'มี.ค.': 3, 'มีนา': 3, 'มีนาคม': 3,
  'เม.ย.': 4, 'เมษา': 4, 'เมษายน': 4,
  'พ.ค.': 5, 'พฤษภา': 5, 'พฤษภาคม': 5,
  'มิ.ย.': 6, 'มิถุนา': 6, 'มิถุนายน': 6,
  'ก.ค.': 7, 'กรกฎา': 7, 'กรกฎาคม': 7,
  'ส.ค.': 8, 'สิงหา': 8, 'สิงหาคม': 8,
  'ก.ย.': 9, 'กันยา': 9, 'กันยายน': 9,
  'ต.ค.': 10, 'ตุลา': 10, 'ตุลาคม': 10,
  'พ.ย.': 11, 'พฤศจิกา': 11, 'พฤศจิกายน': 11,
  'ธ.ค.': 12, 'ธันวา': 12, 'ธันวาคม': 12
};

const THAI_WEEKDAYS = {
  'อาทิตย์': 0,
  'จันทร์': 1,
  'อังคาร': 2,
  'พุธ': 3,
  'พฤหัส': 4, 'พฤหัสบดี': 4,
  'ศุกร์': 5,
  'เสาร์': 6
};

// Natural Thai Message Parser
function parseTaskFromText(rawText) {
  let text = rawText.trim();
  const now = getBangkokNow();
  let targetDate = null;
  let targetTime = null;

  // ----------------------------------------------------
  // STEP 1: PARSE TIME FIRST (To avoid confusion with numeric date)
  // ----------------------------------------------------

  // 1.1 Numeric time: e.g. "18:00", "18.30", "18.30 น.", "9:00", "09.15"
  const numTimeMatch = text.match(/(?:เวลา\s*)?(\d{1,2})[:.](\d{2})(?:\s*น\.?)?/);
  if (numTimeMatch) {
    const hh = parseInt(numTimeMatch[1], 10);
    const mm = parseInt(numTimeMatch[2], 10);
    if (hh >= 0 && hh <= 23 && mm >= 0 && mm <= 59) {
      targetTime = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}`;
      text = text.replace(numTimeMatch[0], ' ');
    }
  }

  // 1.2 Thai Colloquial Time (บ่าย, ทุ่ม, โมง, เที่ยง)
  if (!targetTime) {
    if (/เที่ยงคืน/i.test(text)) {
      targetTime = '00:00';
      text = text.replace(/เที่ยงคืน/g, ' ');
    } else if (/เที่ยงวัน|เที่ยง/i.test(text)) {
      targetTime = '12:00';
      text = text.replace(/เที่ยงวัน|เที่ยง/g, ' ');
    } else {
      // บ่าย X (บ่ายโมง, บ่ายสอง, บ่ายสาม, บ่ายสี่, บ่ายห้า)
      const baiMatch = text.match(/บ่าย\s*([โมง1-5]|หนึ่ง|สอง|สาม|สี่|ห้า)?(\s*ครึ่ง)?/);
      if (baiMatch) {
        let h = 13;
        const val = baiMatch[1];
        if (val === 'สอง' || val === '2') h = 14;
        else if (val === 'สาม' || val === '3') h = 15;
        else if (val === 'สี่' || val === '4') h = 16;
        else if (val === 'ห้า' || val === '5') h = 17;
        const m = baiMatch[2] ? '30' : '00';
        targetTime = `${String(h).padStart(2, '0')}:${m}`;
        text = text.replace(baiMatch[0], ' ');
      }

      // X ทุ่ม (1 ทุ่ม -> 19:00, 2 ทุ่ม -> 20:00, ..., 6 ทุ่ม -> 00:00)
      const toomMatch = text.match(/(\d{1}|หนึ่ง|สอง|สาม|สี่|ห้า|หก)\s*ทุ่ม(\s*ครึ่ง)?/);
      if (toomMatch && !targetTime) {
        let base = 1;
        const v = toomMatch[1];
        if (v === '1' || v === 'หนึ่ง') base = 1;
        else if (v === '2' || v === 'สอง') base = 2;
        else if (v === '3' || v === 'สาม') base = 3;
        else if (v === '4' || v === 'สี่') base = 4;
        else if (v === '5' || v === 'ห้า') base = 5;
        else if (v === '6' || v === 'หก') base = 6;
        let h = (18 + base) % 24;
        const m = toomMatch[2] ? '30' : '00';
        targetTime = `${String(h).padStart(2, '0')}:${m}`;
        text = text.replace(toomMatch[0], ' ');
      }

      // X โมงเช้า / X โมงเย็น / X โมง
      const mongMatch = text.match(/(\d{1,2})\s*โมง(\s*เช้า|\s*เย็น)?(\s*ครึ่ง)?/);
      if (mongMatch && !targetTime) {
        let h = parseInt(mongMatch[1], 10);
        if (mongMatch[2] && mongMatch[2].includes('เย็น')) {
          if (h <= 6) h += 12; // 4 โมงเย็น -> 16:00
        }
        const m = mongMatch[3] ? '30' : '00';
        targetTime = `${String(h).padStart(2, '0')}:${m}`;
        text = text.replace(mongMatch[0], ' ');
      }
    }
  }

  // ----------------------------------------------------
  // STEP 2: PARSE DATE
  // ----------------------------------------------------

  // 2.1 Check relative date keywords (วันนี้, พรุ่งนี้, มะรืนนี้)
  if (/มะรืนนี้|วันมะรืน/i.test(text)) {
    const d = new Date(now);
    d.setDate(d.getDate() + 2);
    targetDate = d.toISOString().split('T')[0];
    text = text.replace(/มะรืนนี้|วันมะรืน/g, ' ');
  } else if (/พรุ่งนี้/i.test(text)) {
    const d = new Date(now);
    d.setDate(d.getDate() + 1);
    targetDate = d.toISOString().split('T')[0];
    text = text.replace(/พรุ่งนี้/g, ' ');
  } else if (/วันนี้/i.test(text)) {
    targetDate = now.toISOString().split('T')[0];
    text = text.replace(/วันนี้/g, ' ');
  }

  // 2.2 Check Day of the Week (e.g. วันศุกร์นี้, วันจันทร์หน้า, วันพุธ)
  const weekdayMatch = text.match(/วัน(อาทิตย์|จันทร์|อังคาร|พุธ|พฤหัสบดี|พฤหัส|ศุกร์|เสาร์)(\s*(นี้|หน้า))?/);
  if (weekdayMatch && !targetDate) {
    const targetDayIndex = THAI_WEEKDAYS[weekdayMatch[1]];
    const currentDayIndex = now.getDay();
    let diff = targetDayIndex - currentDayIndex;
    if (diff <= 0) diff += 7; // Next occurrence
    if (weekdayMatch[3] === 'หน้า' && diff < 7) diff += 7;
    const d = new Date(now);
    d.setDate(d.getDate() + diff);
    targetDate = d.toISOString().split('T')[0];
    text = text.replace(weekdayMatch[0], ' ');
  }

  // 2.3 Check Thai Month Date format: e.g. "15 ก.ย.", "25 กันยายน 2569", "5 ส.ค. 69"
  const thaiMonthRegex = /(\d{1,2})\s*(ม\.?ค\.?|มกราคม|ก\.?พ\.?|กุมภาพันธ์|มี\.?ค\.?|มีนาคม|เม\.?ย\.?|เมษายน|พ\.?ค\.?|พฤษภาคม|มิ\.?ย\.?|มิถุนายน|ก\.?ค\.?|กรกฎาคม|ส\.?ค\.?|สิงหาคม|ก\.?ย\.?|กันยายน|ต\.?ค\.?|ตุลาคม|พ\.?ย\.?|พฤศจิกายน|ธ\.?ค\.?|ธันวาคม)(?:\s*(?:พ\.?ศ\.?|ปี)?\s*(25\d{2}|20\d{2}|\d{2}))?/i;
  const monthMatch = text.match(thaiMonthRegex);
  if (monthMatch && !targetDate) {
    const day = parseInt(monthMatch[1], 10);
    const mStr = monthMatch[2].replace(/\s+/g, '');
    const month = THAI_MONTHS[mStr] || (now.getMonth() + 1);
    let year = now.getFullYear();

    if (monthMatch[3]) {
      let rawYear = parseInt(monthMatch[3], 10);
      if (rawYear > 2500) rawYear -= 543;
      else if (rawYear < 100) rawYear += 2000;
      year = rawYear;
    }

    const mm = String(month).padStart(2, '0');
    const dd = String(day).padStart(2, '0');
    targetDate = `${year}-${mm}-${dd}`;
    text = text.replace(monthMatch[0], ' ');
  }

  // 2.4 Check numeric date: YYYY-MM-DD or DD/MM/YYYY or DD-MM-YYYY
  const numDateMatch = text.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (numDateMatch && !targetDate) {
    targetDate = `${numDateMatch[1]}-${numDateMatch[2].padStart(2, '0')}-${numDateMatch[3].padStart(2, '0')}`;
    text = text.replace(numDateMatch[0], ' ');
  } else {
    const slashMatch = text.match(/(\d{1,2})[-/](\d{1,2})(?:[-/](\d{2,4}))?/);
    if (slashMatch && !targetDate) {
      const day = slashMatch[1].padStart(2, '0');
      const month = slashMatch[2].padStart(2, '0');
      let year = now.getFullYear();
      if (slashMatch[3]) {
        let rawYear = parseInt(slashMatch[3], 10);
        if (rawYear > 2500) rawYear -= 543;
        else if (rawYear < 100) rawYear += 2000;
        year = rawYear;
      }
      targetDate = `${year}-${month}-${day}`;
      text = text.replace(slashMatch[0], ' ');
    }
  }

  // Fallback defaults
  if (!targetDate) targetDate = now.toISOString().split('T')[0];
  if (!targetTime) targetTime = '09:00';

  // ----------------------------------------------------
  // STEP 3: CLEAN UP TITLE
  // ----------------------------------------------------
  let cleanTitle = text
    .replace(/^(\+|เพิ่มงาน|เพิ่ม|add|เตือน|ช่วยเตือน|นัดหมาย|จดบันทึก|แจ้งเตือน)\s*:?/i, '')
    .replace(/(?:^|\s)(วันที่|เวลา|ตอน|ช่วง|มี|ให้)(?=\s|$)/g, ' ')
    .replace(/(?:^|\s)(นะ|คะ|ค่ะ|ครับ)(?=\s|$)/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  // Strip leading and trailing symbols
  cleanTitle = cleanTitle.replace(/^["':\-\s]+|["':\-\s]+$/g, '');

  if (!cleanTitle) {
    cleanTitle = 'นัดหมายใหม่';
  }

  return {
    title: cleanTitle,
    date: targetDate,
    time: targetTime
  };
}

// Send Reply via LINE Reply API
function sendLineReply(replyToken, messages) {
  const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;
  if (!token || !replyToken) return Promise.resolve(false);

  const postData = JSON.stringify({
    replyToken: replyToken,
    messages: Array.isArray(messages) ? messages : [{ type: 'text', text: messages }]
  });

  const options = {
    hostname: 'api.line.me',
    port: 443,
    path: '/v2/bot/message/reply',
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
          resolve(true);
        } else {
          console.error(`[LINE Webhook Reply] ❌ Failed (${res.statusCode}):`, body);
          resolve(false);
        }
      });
    });
    req.on('error', (e) => {
      console.error('[LINE Webhook Reply] ❌ HTTP Error:', e.message);
      resolve(false);
    });
    req.write(postData);
    req.end();
  });
}

// Main Webhook Route Handler
async function handleLineWebhook(req, res) {
  // Always return 200 OK immediately for LINE
  res.status(200).send('OK');

  const signature = req.headers['x-line-signature'];
  const secret = process.env.LINE_CHANNEL_SECRET;

  // Verify Signature
  if (secret && req.rawBody) {
    const isValid = verifySignature(req.rawBody, signature, secret);
    if (!isValid) {
      console.warn('[LINE Webhook] ⚠️ Invalid signature received!');
      return;
    }
  }

  const events = req.body && req.body.events;
  if (!events || !Array.isArray(events) || events.length === 0) {
    // Ping / Verify test from LINE Developers Console
    console.log('[LINE Webhook] ℹ️ Webhook verification check received successfully.');
    return;
  }

  for (const event of events) {
    if (event.type !== 'message' || event.message.type !== 'text') continue;

    const replyToken = event.replyToken;
    const userMsg = event.message.text.trim();
    console.log(`[LINE Webhook] 📩 ได้รับข้อความ: "${userMsg}"`);

    // 1. คำสั่งช่วยเหลือ / วิธีใช้
    if (/^(วิธีใช้|คำสั่ง|help|คู่มือ)$/i.test(userMsg)) {
      const helpText = `🌸 สวัสดีค่ะเตง! Gigi พร้อมช่วยจดบันทึกงานให้แล้วนะคะ 💕\n\n` +
        `📝 ตัวอย่างการพิมพ์เพิ่มงาน:\n` +
        `• เพิ่ม ซ้อมดนตรี พรุ่งนี้ 18:00\n` +
        `• + ส่งการบ้าน 15 ก.ย. 10.30\n` +
        `• เตือน สอบแลป วันศุกร์นี้ บ่ายสอง\n` +
        `• พรุ่งนี้มีนัดคุยงานตอนสองทุ่มครึ่ง\n\n` +
        `🔎 คำสั่งอื่นๆ:\n` +
        `• พิมพ์ "ดูงาน" หรือ "งานวันนี้" เพื่อเช็กรายการงาน\n\n` +
        `🌐 เปิดดูบนเว็บ: https://boatraminder.onrender.com`;

      await sendLineReply(replyToken, [{ type: 'text', text: helpText }]);
      continue;
    }

    // 2. คำสั่งดูงาน / งานวันนี้ / การบ้าน
    if (/^(ดูงาน|งานวันนี้|เช็กงาน|การบ้าน|ตารางงาน)$/i.test(userMsg)) {
      try {
        const activeTasks = await db.getActive();
        if (!activeTasks || activeTasks.length === 0) {
          await sendLineReply(replyToken, [{
            type: 'text',
            text: `🎉 ตอนนี้ไม่มีนัดหมายหรืองานค้างเลยค่ะเตง! ชิวมากๆ พักผ่อนให้เต็มที่น้า 🛌🌸`
          }]);
          continue;
        }

        // Sort by date and time
        activeTasks.sort((a, b) => new Date(`${a.date}T${a.time}`) - new Date(`${b.date}T${b.time}`));

        let listText = `📋 รายการนัดหมายปัจจุบันของเตงค่ะ:\n\n`;
        activeTasks.slice(0, 5).forEach((t, idx) => {
          listText += `${idx + 1}. 📌 ${t.title}\n   📅 วันที่: ${t.date} เวลา: ${t.time} น.\n`;
        });

        if (activeTasks.length > 5) {
          listText += `\n...และยังมีอีก ${activeTasks.length - 5} รายการค่ะเตง`;
        }
        listText += `\n🌐 เปิดดูทั้งหมด: https://boatraminder.onrender.com`;

        await sendLineReply(replyToken, [{ type: 'text', text: listText }]);
      } catch (err) {
        console.error('[LINE Webhook] Error fetching tasks:', err);
        await sendLineReply(replyToken, [{ type: 'text', text: 'เกิดข้อผิดพลาดในการดึงข้อมูลค่ะเตง ลองใหม่อีกทีนะคะ 😢' }]);
      }
      continue;
    }

    // 3. เพิ่มงาน / บันทึกนัดหมาย
    try {
      const parsed = parseTaskFromText(userMsg);
      const flags = calcNotificationFlags(parsed.date, parsed.time);

      const saved = await db.create({
        title: parsed.title,
        date: parsed.date,
        time: parsed.time,
        notes: 'เพิ่มผ่านแชท LINE 💬',
        completed: false,
        ...flags
      });

      console.log(`[LINE Webhook] ✅ บันทึกงานสำเร็จ: "${saved.title}" (${saved.date} ${saved.time}) ID: ${saved.id || saved._id}`);

      // Format Date in Thai for confirmation
      const dateParts = parsed.date.split('-');
      const y = parseInt(dateParts[0], 10);
      const m = parseInt(dateParts[1], 10);
      const d = parseInt(dateParts[2], 10);
      const mNames = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
      const thaiFormattedDate = `${d} ${mNames[m]} ${y + 543}`;

      const replyMsg = `🌸 Gigi บันทึกนัดหมายให้เรียบร้อยแล้วค่ะเตง! 💕\n\n` +
        `📌 ชื่องาน: ${saved.title}\n` +
        `📅 วันที่: ${thaiFormattedDate} (${saved.date})\n` +
        `⏰ เวลา: ${saved.time} น.\n\n` +
        `เค้าจะคอยช่วยเตือนล่วงหน้าให้เหมือนเดิมนะคะ สู้ๆ ค่ะเตง! ✊✨\n` +
        `🌐 ตรวจสอบบนเว็บ: https://boatraminder.onrender.com`;

      await sendLineReply(replyToken, [{ type: 'text', text: replyMsg }]);
    } catch (err) {
      console.error('[LINE Webhook] Error creating reminder:', err);
      await sendLineReply(replyToken, [{
        type: 'text',
        text: `เกิดข้อผิดพลาดในการบันทึกงานค่ะเตง 😢 ลองพิมพ์แบบ: "เพิ่ม [ชื่องาน] [วันที่] [เวลา]" ดูนะคะ!`
      }]);
    }
  }
}

module.exports = {
  handleLineWebhook,
  parseTaskFromText,
  verifySignature
};
