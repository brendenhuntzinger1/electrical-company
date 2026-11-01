(function () {
  // Breaker panel (homepage)
  var note = document.getElementById('panelNote');
  var status = document.getElementById('panelStatus');
  var statusText = document.getElementById('panelStatusText');
  document.querySelectorAll('.circuit').forEach(function (c) {
    c.addEventListener('click', function () {
      var on = c.getAttribute('aria-pressed') === 'true';
      c.setAttribute('aria-pressed', on ? 'false' : 'true');
      note.textContent = on ? 'Tripped. That is a call we get every day. Tap it again to reset.' : c.dataset.note;
      var offCount = document.querySelectorAll('.circuit[aria-pressed="false"]').length;
      status.classList.toggle('warn', offCount > 0);
      statusText.textContent = offCount ? offCount + ' tripped' : 'All circuits on';
    });
  });

  // Hurricane season countdown (June 1 to November 30)
  var daysEl = document.getElementById('stormDays');
  var textEl = document.getElementById('stormText');
  if (daysEl && textEl) {
    var now = new Date();
    var y = now.getFullYear();
    var day = 864e5;
    var today = new Date(y, now.getMonth(), now.getDate());
    var start = new Date(y, 5, 1), end = new Date(y, 10, 30);
    if (today >= start && today <= end) {
      daysEl.textContent = Math.round((end - today) / day);
      textEl.textContent = 'days left in hurricane season. Install now and beat next year’s rush.';
    } else {
      var next = today > end ? new Date(y + 1, 5, 1) : start;
      daysEl.textContent = Math.round((next - today) / day);
      textEl.textContent = 'days until hurricane season starts June 1.';
    }
  }

  // Quote form (demo until it is wired to email/SMS)
  var photo = document.getElementById('q-photo');
  if (photo) {
    photo.addEventListener('change', function () {
      var n = photo.files.length;
      document.getElementById('photoLabel').textContent = n ? n + (n > 1 ? ' files' : ' file') + ' added' : 'Add a photo or inspection report';
    });
  }
  var form = document.getElementById('quoteForm');
  if (form) {
    var params = new URLSearchParams(location.search);
    var svc = params.get('service');
    var sel = document.getElementById('q-service');
    if (svc && sel) {
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === svc) sel.selectedIndex = i;
      }
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      document.getElementById('sentMsg').hidden = false;
    });
  }
})();
