/* ================================================================
   HOSTEL MANAGEMENT SYSTEM — Main JavaScript
   ================================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar Mobile Toggle ──────────────────────────────────────
  const toggleBtn    = document.getElementById('sidebarToggle');
  const sidebar      = document.getElementById('sidebar');
  const overlay      = document.getElementById('sidebarOverlay');

  function openSidebar()  { sidebar?.classList.add('open'); overlay?.classList.add('open'); }
  function closeSidebar() { sidebar?.classList.remove('open'); overlay?.classList.remove('open'); }

  toggleBtn?.addEventListener('click', openSidebar);
  overlay?.addEventListener('click', closeSidebar);

  // ── Auto-dismiss Alerts ────────────────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    const closeBtn = alert.querySelector('.alert-close');
    closeBtn?.addEventListener('click', () => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.2s ease';
      setTimeout(() => alert.remove(), 200);
    });
    // Auto-dismiss after 5s
    setTimeout(() => {
      if (alert.parentNode) {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.4s ease';
        setTimeout(() => alert.remove(), 400);
      }
    }, 5000);
  });

  // ── Active Nav Highlight ───────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    }
  });

  // ── Occupancy Bar Colors ───────────────────────────────────────
  document.querySelectorAll('.occ-fill').forEach(bar => {
    const pct = parseFloat(bar.style.width);
    if (pct >= 90) bar.classList.add('high');
    else if (pct >= 60) bar.classList.add('medium');
    else bar.classList.add('low');
  });

  // ── Confirm Dangerous Actions ──────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
  });

  // ── File Input Preview ─────────────────────────────────────────
  document.querySelectorAll('input[type="file"][data-preview]').forEach(input => {
    input.addEventListener('change', function () {
      const previewId = this.dataset.preview;
      const preview   = document.getElementById(previewId);
      if (preview && this.files[0]) {
        const reader = new FileReader();
        reader.onload = e => { preview.src = e.target.result; };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // ── Table Row Click to Detail ──────────────────────────────────
  document.querySelectorAll('tr[data-href]').forEach(row => {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function (e) {
      if (!e.target.closest('a, button, .btn')) {
        window.location.href = this.dataset.href;
      }
    });
  });

  // ── Animate stat counters ──────────────────────────────────────
  document.querySelectorAll('.stat-card-value[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count, 10);
    let current  = 0;
    const step   = Math.max(1, Math.floor(target / 20));
    const timer  = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 30);
  });

});
