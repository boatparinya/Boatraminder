// Backend API URL
const API_URL = '/api';

// State management
let reminders = [];
let activeTab = 'active'; // 'active' or 'completed'

// DOM Elements
const reminderForm = document.getElementById('reminder-form');
const titleInput = document.getElementById('reminder-title');
const dateInput = document.getElementById('reminder-date');
const timeInput = document.getElementById('reminder-time');
const notesInput = document.getElementById('reminder-notes');

const tabActive = document.getElementById('tab-active');
const tabCompleted = document.getElementById('tab-completed');

const activeDashboard = document.getElementById('active-dashboard');
const completedDashboard = document.getElementById('completed-dashboard');

const todayList = document.getElementById('today-reminders-list');
const upcomingList = document.getElementById('upcoming-reminders-list');
const completedList = document.getElementById('completed-reminders-list');

const statToday = document.getElementById('stat-today');
const statUpcoming = document.getElementById('stat-upcoming');
const statCompleted = document.getElementById('stat-completed');

const liveDateEl = document.getElementById('live-date');
const liveTimeEl = document.getElementById('live-time');
const greetingEl = document.getElementById('gigi-greeting');
const toastContainer = document.getElementById('toast-container');

// Set default date to today
function setDefaultDate() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  dateInput.value = `${yyyy}-${mm}-${dd}`;
  
  // Default time is current hour + 1, rounded to nearest 30 mins
  const nextHour = new Date(today);
  nextHour.setHours(today.getHours() + 1);
  const hh = String(nextHour.getHours()).padStart(2, '0');
  timeInput.value = `${hh}:00`;
}

// Live Time & Greetings Clock
function updateClock() {
  const now = new Date();
  
  // Format local date string (Thai Buddhist Era format automatically handled by th-TH locale)
  const dateStr = now.toLocaleDateString('th-TH', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
  if (liveDateEl) {
    liveDateEl.textContent = dateStr;
  }
  
  // Format local time string
  const timeStr = now.toLocaleTimeString('th-TH', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  liveTimeEl.textContent = timeStr;
  
  // Update Gigi's greeting based on hour
  const hour = now.getHours();
  let greeting = '';
  
  if (hour >= 5 && hour < 12) {
    greeting = 'สวัสดีตอนเช้าค่ะเตง ☀️ วันนี้มีภารกิจอะไรรออยู่บ้างนะมาดูกัน!';
  } else if (hour >= 12 && hour < 17) {
    greeting = 'สวัสดีตอนบ่ายค่ะเตง 🌤️ พักสายตาสักนิดแล้วลุยต่อกันค่ะ!';
  } else if (hour >= 17 && hour < 21) {
    greeting = 'สวัสดีตอนเย็นค่ะเตง 🌇 อย่าลืมหาของอร่อยๆ ทานด้วยนะคะ!';
  } else {
    greeting = 'สวัสดีตอนค่ำค่ะเตง 🌙 ดึกแล้วอย่าลืมพักผ่อนน้า เค้าเป็นห่วง!';
  }
  
  // Only update text content if it changed to avoid layout flashes
  if (greetingEl.textContent.trim() !== greeting) {
    greetingEl.textContent = greeting;
  }
}

// Show custom cute notification toast
function showToast(message, type = 'success', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast-item glass-card flex items-center gap-3 px-4 py-3 rounded-2xl border shadow-lg max-w-sm text-sm font-medium text-slate-800`;
  
  let icon = 'info';
  let borderClass = 'border-slate-200';
  let iconColor = 'text-blue-500';
  
  if (type === 'success') {
    icon = 'check-circle-2';
    borderClass = 'border-emerald-100 bg-emerald-50/70';
    iconColor = 'text-emerald-500';
  } else if (type === 'error') {
    icon = 'alert-triangle';
    borderClass = 'border-rose-100 bg-rose-50/70';
    iconColor = 'text-rose-500';
  } else if (type === 'delete') {
    icon = 'trash-2';
    borderClass = 'border-amber-100 bg-amber-50/70';
    iconColor = 'text-amber-500';
  }
  
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-5 h-5 ${iconColor}"></i>
    <span>${message}</span>
  `;
  
  toast.classList.add(...borderClass.split(' '));
  toastContainer.appendChild(toast);
  lucide.createIcons();
  
  // Remove toast after duration with animation
  setTimeout(() => {
    toast.classList.add('leaving');
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, duration);
}

// Calculate remaining relative time
function getRelativeTime(dateStr, timeStr) {
  const target = new Date(`${dateStr}T${timeStr}`);
  const now = new Date();
  
  const diffMs = target - now;
  const diffMins = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffMs < 0) {
    const targetDate = new Date(dateStr);
    const nowDate = new Date(now.toISOString().split('T')[0]);
    if (targetDate < nowDate) {
      return `<span class="text-rose-500 font-semibold flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> เลยกำหนดแล้วนะเตง!</span>`;
    }
    return `<span class="text-rose-500 font-semibold flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> เลยเวลาวันนี้แล้วน้า</span>`;
  }

  if (diffDays === 0) {
    if (diffHours === 0) {
      return `<span class="text-amber-500 font-semibold flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5 animate-pulse"></i> อีก ${diffMins} นาที</span>`;
    }
    return `<span class="text-amber-500 font-semibold flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> อีก ${diffHours} ชม. ${diffMins % 60} นาที</span>`;
  } else if (diffDays === 1) {
    return `<span class="text-slate-600 font-medium flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5"></i> พรุ่งนี้ตอน ${timeStr} น.</span>`;
  } else {
    return `<span class="text-slate-500 flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5"></i> อีก ${diffDays} วันค่ะ</span>`;
  }
}

// Fetch reminders from backend
async function fetchReminders() {
  try {
    const response = await fetch(`${API_URL}/reminders`);
    if (!response.ok) throw new Error('Failed to fetch data');
    const data = await response.json();
    // Normalize MongoDB _id → id so all code works consistently
    reminders = data.map(r => ({ ...r, id: r._id || r.id }));
    updateStats();
    renderReminders();
  } catch (error) {
    console.error('Error fetching reminders:', error);
    showToast('ดึงข้อมูลนัดหมายไม่สำเร็จค่ะเตง 😢', 'error');
  }
}


// Update Dashboard Statistics
function updateStats() {
  const todayStr = new Date().toISOString().split('T')[0];
  
  const activeReminders = reminders.filter(r => !r.completed);
  const completedCount = reminders.filter(r => r.completed).length;
  
  const todayCount = activeReminders.filter(r => r.date === todayStr).length;
  const upcomingCount = activeReminders.filter(r => r.date > todayStr).length;
  
  statToday.textContent = todayCount;
  statUpcoming.textContent = upcomingCount;
  statCompleted.textContent = completedCount;
}

// Render reminders into lists
function renderReminders() {
  // Clear lists
  todayList.innerHTML = '';
  upcomingList.innerHTML = '';
  completedList.innerHTML = '';
  
  const todayStr = new Date().toISOString().split('T')[0];
  
  // Sort reminders: active by date & time ascending, completed by modified/created date descending
  const activeReminders = reminders
    .filter(r => !r.completed)
    .sort((a, b) => new Date(`${a.date}T${a.time}`) - new Date(`${b.date}T${b.time}`));
    
  const completedReminders = reminders
    .filter(r => r.completed)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  // 1. Render Active reminders
  const todayTasks = activeReminders.filter(r => r.date === todayStr);
  const upcomingTasks = activeReminders.filter(r => r.date !== todayStr); // can be past due or future
  
  // Render Today
  if (todayTasks.length === 0) {
    todayList.innerHTML = `
      <div class="glass-card rounded-2xl p-6 text-center text-slate-400 text-sm">
        ไม่มีนัดหมายสำหรับวันนี้ค่ะเตง พักผ่อนให้เต็มที่น้า 🛌
      </div>
    `;
  } else {
    todayTasks.forEach(r => {
      todayList.appendChild(createReminderCard(r));
    });
  }
  
  // Render Upcoming & Overdue
  if (upcomingTasks.length === 0) {
    upcomingList.innerHTML = `
      <div class="glass-card rounded-2xl p-6 text-center text-slate-400 text-sm">
        ไม่มีกิจกรรมอื่นรออยู่เลยค่ะเตง ชิวมาก! 🏖️
      </div>
    `;
  } else {
    upcomingTasks.forEach(r => {
      upcomingList.appendChild(createReminderCard(r));
    });
  }
  
  // 2. Render Completed reminders
  if (completedReminders.length === 0) {
    completedList.innerHTML = `
      <div class="glass-card rounded-2xl p-6 text-center text-slate-400 text-sm">
        ยังไม่มีรายการที่ทำเสร็จเลยค่ะเตง สู้ๆ นะเค้าเป็นกำลังใจให้! ✊
      </div>
    `;
  } else {
    completedReminders.forEach(r => {
      completedList.appendChild(createReminderCard(r));
    });
  }
  
  lucide.createIcons();
}

// Create Card HTML Element for a Reminder
function createReminderCard(reminder) {
  const card = document.createElement('div');
  
  card.className = `reminder-card glass-card rounded-2xl p-5 relative flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition-all duration-300`;
  card.dataset.id = reminder.id;
  
  // Format Date to Local Thai
  const eventDate = new Date(reminder.date);
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  const thaiDateStr = eventDate.toLocaleDateString('th-TH', options);
  
  // Calculate relative warning time
  const timeInfo = reminder.completed ? 
    `<span class="text-green-600 font-semibold flex items-center gap-1"><i data-lucide="check-circle" class="w-3.5 h-3.5"></i> ทำเสร็จแล้วน้าเตง</span>` : 
    getRelativeTime(reminder.date, reminder.time);

  card.innerHTML = `
    <div class="flex items-start gap-4 flex-1">
      <!-- Custom Styled Circle Checkbox -->
      <button onclick="toggleReminder('${reminder.id}', ${reminder.completed})" 
              class="mt-1 flex-shrink-0 w-6.5 h-6.5 rounded-full border-2 border-slate-300 hover:border-indigo-400 flex items-center justify-center cursor-pointer transition-all duration-200 ${reminder.completed ? 'bg-indigo-500 border-indigo-500 text-white' : 'hover:bg-slate-50 text-transparent'}">
        <i data-lucide="check" class="w-4 h-4"></i>
      </button>
      
      <div class="space-y-1.5">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-slate-400 text-xs flex items-center gap-1 font-medium">
            <i data-lucide="calendar-days" class="w-3 h-3"></i> ${thaiDateStr}
          </span>
          <span class="text-slate-400 text-xs flex items-center gap-1 font-medium">
            <i data-lucide="clock-4" class="w-3 h-3"></i> ${reminder.time} น.
          </span>
        </div>
        <h4 class="text-base font-bold text-slate-800 leading-snug ${reminder.completed ? 'line-through text-slate-400' : ''}">
          ${reminder.title}
        </h4>
        ${reminder.notes ? `<p class="text-xs text-slate-500 leading-relaxed font-normal bg-slate-50/50 p-2 rounded-xl border border-slate-100/50">${reminder.notes}</p>` : ''}
      </div>
    </div>
        <div class="flex items-center gap-2 justify-between w-full md:w-auto border-t md:border-t-0 border-slate-100/70 pt-3 md:pt-0">
      <div class="text-xs">
        ${timeInfo}
      </div>
      
      <div class="flex items-center gap-1">
        <button onclick="openEditModal('${reminder.id}')" 
                class="p-2 text-slate-400 hover:text-indigo-500 hover:bg-indigo-50 rounded-xl transition-all duration-200 cursor-pointer" 
                title="แก้ไขรายการ">
          <i data-lucide="pencil" class="w-4 h-4"></i>
        </button>
        <button onclick="deleteReminder('${reminder.id}')" 
                class="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-all duration-200 cursor-pointer" 
                title="ลบรายการ">
          <i data-lucide="trash-2" class="w-4.5 h-4.5"></i>
        </button>
      </div>
    </div>
  `;
  
  return card;
}

// Add reminder handler
reminderForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const title = titleInput.value.trim();
  const date = dateInput.value;
  const time = timeInput.value;
  const notes = notesInput.value.trim();
  
  if (!title || !date || !time) return;
  
  try {
    const response = await fetch(`${API_URL}/reminders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title, date, time, notes })
    });
    
    if (!response.ok) throw new Error('Failed to create reminder');
    
    const newReminder = await response.json();
    reminders.push(newReminder);
    
    // Reset Form
    titleInput.value = '';
    notesInput.value = '';
    setDefaultDate();
    
    updateStats();
    renderReminders();
    showToast('เค้าบันทึกนัดหมายให้แล้วนะคะเตง! 🔔', 'success');
  } catch (error) {
    console.error('Error adding reminder:', error);
    showToast('เพิ่มข้อมูลไม่สำเร็จ ลองใหม่อีกทีนะคะเตง', 'error');
  }
});

// Toggle completed status
async function toggleReminder(id, currentStatus) {
  try {
    const response = await fetch(`${API_URL}/reminders/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ completed: !currentStatus })
    });
    
    if (!response.ok) throw new Error('Failed to update status');
    
    const updated = await response.json();
    
    // Update local state
    const index = reminders.findIndex(r => r.id === id);
    if (index !== -1) {
      reminders[index] = updated;
    }
    
    updateStats();
    renderReminders();
    
    if (updated.completed) {
      showToast('เก่งมากเลยเตง! ทำเสร็จเพิ่มอีกหนึ่งงานแล้วค่า 🎉🥳', 'success');
    } else {
      showToast('ดึงงานกลับมาเริ่มใหม่แล้วนะคะเตง 🔄', 'success');
    }
  } catch (error) {
    console.error('Error toggling status:', error);
    showToast('อัปเดตสถานะไม่สำเร็จค่ะเตง', 'error');
  }
}

// Delete reminder
async function deleteReminder(id) {
  // Confirm deletion
  const targetReminder = reminders.find(r => r.id === id);
  if (!targetReminder) return;
  
  if (!confirm(`เตงแน่ใจใช่ไหมคะว่าจะลบงาน "${targetReminder.title}"?`)) {
    return;
  }
  
  try {
    const response = await fetch(`${API_URL}/reminders/${id}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('Failed to delete reminder');
    
    // Update local state
    reminders = reminders.filter(r => r.id !== id);
    
    updateStats();
    renderReminders();
    showToast('ลบประวัติงานเรียบร้อยแล้วค่ะเตง 🗑️', 'delete');
  } catch (error) {
    console.error('Error deleting reminder:', error);
    showToast('เกิดข้อผิดพลาดในการลบงานค่ะเตง', 'error');
  }
}

// Global scope references for inline HTML onclick handlers
window.toggleReminder = toggleReminder;
window.deleteReminder = deleteReminder;
window.openEditModal = openEditModal;

// Edit Modal Logic
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const closeEditModalBtn = document.getElementById('close-edit-modal');
const cancelEditBtn = document.getElementById('cancel-edit-btn');

function openEditModal(id) {
  const reminder = reminders.find(r => r.id === id || r._id === id);
  if (!reminder) return;

  const reminderId = reminder._id || reminder.id;

  // Populate form fields
  document.getElementById('edit-id').value = reminderId;
  document.getElementById('edit-title').value = reminder.title;
  document.getElementById('edit-date').value = reminder.date;
  document.getElementById('edit-time').value = reminder.time;
  document.getElementById('edit-notes').value = reminder.notes || '';

  // Show modal
  editModal.classList.remove('hidden');
  lucide.createIcons();
  document.getElementById('edit-title').focus();
}

function closeEditModal() {
  editModal.classList.add('hidden');
  editForm.reset();
}

closeEditModalBtn.addEventListener('click', closeEditModal);
cancelEditBtn.addEventListener('click', closeEditModal);

// Close modal when clicking backdrop
editModal.addEventListener('click', (e) => {
  if (e.target === editModal) closeEditModal();
});

// Save edit
editForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const id = document.getElementById('edit-id').value;
  const title = document.getElementById('edit-title').value.trim();
  const date = document.getElementById('edit-date').value;
  const time = document.getElementById('edit-time').value;
  const notes = document.getElementById('edit-notes').value.trim();

  if (!title || !date || !time) return;

  try {
    const response = await fetch(`${API_URL}/reminders/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, date, time, notes })
    });

    if (!response.ok) throw new Error('Failed to update');

    const updated = await response.json();

    // Update local state
    const index = reminders.findIndex(r => (r._id || r.id) === id);
    if (index !== -1) reminders[index] = updated;

    closeEditModal();
    updateStats();
    renderReminders();
    showToast('อัปเดตนัดหมายเรียบร้อยแล้วค่ะเตง ✏️', 'success');
  } catch (error) {
    console.error('Error updating reminder:', error);
    showToast('แก้ไขข้อมูลไม่สำเร็จค่ะเตง ลองใหม่นะคะ', 'error');
  }
});

// Tab switcher logic
tabActive.addEventListener('click', () => {
  activeTab = 'active';
  
  // Update styles
  tabActive.className = 'flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer bg-white text-indigo-700 shadow-sm border border-slate-100';
  tabCompleted.className = 'flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer text-slate-500 hover:text-slate-800 hover:bg-white/50';
  
  // Show/Hide divs
  activeDashboard.classList.remove('hidden');
  completedDashboard.classList.add('hidden');
  
  renderReminders();
});

tabCompleted.addEventListener('click', () => {
  activeTab = 'completed';
  
  // Update styles
  tabCompleted.className = 'flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer bg-white text-indigo-700 shadow-sm border border-slate-100';
  tabActive.className = 'flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer text-slate-500 hover:text-slate-800 hover:bg-white/50';
  
  // Show/Hide divs
  completedDashboard.classList.remove('hidden');
  activeDashboard.classList.add('hidden');
  
  renderReminders();
});

// App initialization
document.addEventListener('DOMContentLoaded', () => {
  setDefaultDate();
  
  // Init Clock & greeting
  updateClock();
  setInterval(updateClock, 1000);
  
  // Fetch initial data
  fetchReminders();
});
