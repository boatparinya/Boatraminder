require('dotenv').config();
const https = require('https');
const querystring = require('querystring');
const fs = require('fs');
const path = require('path');

// Helper to get credentials from env or fallback to local token.pickle
function getCredentials() {
  let clientId = process.env.GOOGLE_CLIENT_ID;
  let clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  let refreshToken = process.env.GOOGLE_REFRESH_TOKEN;

  if (clientId && clientSecret && refreshToken) {
    return { clientId, clientSecret, refreshToken };
  }

  // Fallback: Try reading token.pickle or credentials.json if present
  try {
    const credsPath = path.join(__dirname, 'credentials.json');
    if (fs.existsSync(credsPath)) {
      const c = JSON.parse(fs.readFileSync(credsPath, 'utf8'));
      const installed = c.installed || c.web || {};
      clientId = clientId || installed.client_id;
      clientSecret = clientSecret || installed.client_secret;
    }
  } catch (e) {}

  if (clientId && clientSecret && refreshToken) {
    return { clientId, clientSecret, refreshToken };
  }

  return null;
}

// Exchange refresh_token for a fresh access_token
function getAccessToken() {
  const creds = getCredentials();
  if (!creds || !creds.refreshToken) {
    return Promise.reject(new Error('Google OAuth credentials not configured'));
  }

  const postData = querystring.stringify({
    client_id: creds.clientId,
    client_secret: creds.clientSecret,
    refresh_token: creds.refreshToken,
    grant_type: 'refresh_token'
  });

  const options = {
    hostname: 'oauth2.googleapis.com',
    port: 443,
    path: '/token',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          if (res.statusCode === 200 && parsed.access_token) {
            resolve(parsed.access_token);
          } else {
            reject(new Error(`Failed to refresh token (${res.statusCode}): ${body}`));
          }
        } catch (err) {
          reject(err);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// Add event to Google Calendar
async function addCalendarEvent({ title, date, time, description }) {
  try {
    const accessToken = await getAccessToken();

    let startObj = {};
    let endObj = {};

    if (time) {
      // Calculate end time (+1 hour by default)
      const parts = time.split(':');
      const startHour = parseInt(parts[0], 10);
      const startMin = parseInt(parts[1], 10);
      const endHour = (startHour + 1) % 24;
      const endTime = `${String(endHour).padStart(2, '0')}:${String(startMin).padStart(2, '0')}`;

      startObj = {
        dateTime: `${date}T${time}:00+07:00`,
        timeZone: 'Asia/Bangkok'
      };
      endObj = {
        dateTime: `${date}T${endTime}:00+07:00`,
        timeZone: 'Asia/Bangkok'
      };
    } else {
      // All day event
      const d = new Date(date);
      d.setDate(d.getDate() + 1);
      const nextDate = d.toISOString().split('T')[0];

      startObj = {
        date: date,
        timeZone: 'Asia/Bangkok'
      };
      endObj = {
        date: nextDate,
        timeZone: 'Asia/Bangkok'
      };
    }

    const eventPayload = JSON.stringify({
      summary: title,
      description: description || 'บันทึกผ่าน Gigi Reminder via LINE 🌸',
      start: startObj,
      end: endObj
    });

    const options = {
      hostname: 'www.googleapis.com',
      port: 443,
      path: '/calendar/v3/calendars/primary/events',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Content-Length': Buffer.byteLength(eventPayload)
      }
    };

    return new Promise((resolve, reject) => {
      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            const data = JSON.parse(body);
            if (res.statusCode === 200 || res.statusCode === 201) {
              console.log(`[Google Calendar] ✅ สร้างกิจกรรมสำเร็จ: "${title}" ลิงก์: ${data.htmlLink}`);
              resolve({ success: true, link: data.htmlLink, id: data.id });
            } else {
              console.error(`[Google Calendar] ❌ ไม่สามารถสร้างกิจกรรมได้ (${res.statusCode}):`, body);
              resolve({ success: false, error: body });
            }
          } catch (err) {
            resolve({ success: false, error: err.message });
          }
        });
      });

      req.on('error', (err) => {
        console.error('[Google Calendar] ❌ Network Error:', err.message);
        resolve({ success: false, error: err.message });
      });

      req.write(eventPayload);
      req.end();
    });
  } catch (err) {
    console.warn('[Google Calendar] ⚠️ ข้ามการลงปฏิทิน:', err.message);
    return { success: false, error: err.message };
  }
}

module.exports = {
  getAccessToken,
  addCalendarEvent
};
