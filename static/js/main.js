/**
 * SAMS Main Application Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile sidebar toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('show');
    });
  }

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) bsAlert.close();
      } catch (e) {}
    }, 5000);
  });

  // Table client-side quick filter
  const tableSearchInput = document.getElementById('clientTableSearch');
  if (tableSearchInput) {
    tableSearchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      const rows = document.querySelectorAll('.data-table tbody tr');
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }
});
