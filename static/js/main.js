// ============================================
// PULSE — Main JavaScript
// CodeAlpha Internship Task 2
// ============================================

// ---- CSRF Token Helper ----
function getCsrfToken() {
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1].trim() : '';
}

// ---- Like Toggle ----
function toggleLike(postId, btn) {
  fetch(`/post/${postId}/like/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrfToken(),
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
  .then(r => r.json())
  .then(data => {
    const icon = btn.querySelector('i');
    const countEl = btn.querySelector('.like-count');

    if (data.is_liked) {
      btn.classList.add('liked');
      icon.className = 'bi bi-heart-fill';
    } else {
      btn.classList.remove('liked');
      icon.className = 'bi bi-heart';
    }

    if (countEl) countEl.textContent = data.likes_count;

    // Animate
    btn.style.transform = 'scale(1.15)';
    setTimeout(() => { btn.style.transform = ''; }, 200);
  })
  .catch(err => console.error('Like error:', err));
}

// ---- Follow Toggle (small button) ----
function toggleFollowBtn(btn) {
  const username = btn.dataset.username;
  fetch(`/users/${username}/follow/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrfToken(),
      'Content-Type': 'application/json',
    },
  })
  .then(r => r.json())
  .then(data => {
    if (data.is_following) {
      btn.textContent = 'Following';
      btn.style.background = 'transparent';
      btn.style.color = 'var(--text-muted)';
      btn.style.borderColor = 'var(--border-strong)';
    } else {
      btn.textContent = 'Follow';
      btn.style.background = '';
      btn.style.color = '';
      btn.style.borderColor = '';
    }
  })
  .catch(err => console.error('Follow error:', err));
}

// ---- Post Menu Toggle ----
function toggleMenu(btn) {
  const dropdown = btn.nextElementSibling;
  const allDropdowns = document.querySelectorAll('.post-dropdown.open');
  allDropdowns.forEach(d => { if (d !== dropdown) d.classList.remove('open'); });
  dropdown.classList.toggle('open');
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
  if (!e.target.closest('.post-menu')) {
    document.querySelectorAll('.post-dropdown.open').forEach(d => d.classList.remove('open'));
  }
});

// ---- Create Post Form Toggle ----
function togglePostForm() {
  const form = document.getElementById('postFormCollapse');
  if (!form) return;
  if (form.style.display === 'none' || form.style.display === '') {
    form.style.display = 'block';
    form.querySelector('textarea').focus();
  } else {
    form.style.display = 'none';
  }
}

// ---- Character Count ----
const postContent = document.getElementById('postContent');
const charCount = document.getElementById('charCount');
if (postContent && charCount) {
  postContent.addEventListener('input', () => {
    const len = postContent.value.length;
    charCount.textContent = len;
    charCount.style.color = len > 1800 ? 'var(--danger)' : 'var(--text-muted)';
  });
}

// ---- Image Preview ----
function previewImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const preview = document.getElementById('imagePreview');
      const img = document.getElementById('previewImg');
      img.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function removeImage() {
  document.getElementById('id_image').value = '';
  document.getElementById('imagePreview').style.display = 'none';
  document.getElementById('previewImg').src = '';
}

// ---- Toggle Password Visibility ----
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon = btn.querySelector('i');
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'bi bi-eye-slash';
  } else {
    input.type = 'password';
    icon.className = 'bi bi-eye';
  }
}

// ---- Share Post ----
function sharePost(url) {
  const fullUrl = window.location.origin + url;
  if (navigator.share) {
    navigator.share({ title: 'Check out this post on Pulse', url: fullUrl });
  } else if (navigator.clipboard) {
    navigator.clipboard.writeText(fullUrl).then(() => {
      showToast('Link copied to clipboard!', 'success');
    });
  }
}

// ---- Toast Notification ----
function showToast(message, type = 'info') {
  const container = document.querySelector('.messages-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `flash-message flash-${type}`;
  toast.innerHTML = `<i class="bi bi-info-circle-fill"></i>${message}<button class="flash-close" onclick="this.parentElement.remove()"><i class="bi bi-x"></i></button>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function createToastContainer() {
  const el = document.createElement('div');
  el.className = 'messages-container';
  document.body.appendChild(el);
  return el;
}

// ---- Auto-dismiss flash messages ----
document.querySelectorAll('.flash-message').forEach(msg => {
  setTimeout(() => {
    msg.style.opacity = '0';
    msg.style.transition = 'opacity 0.4s';
    setTimeout(() => msg.remove(), 400);
  }, 4500);
});

// ---- Active nav highlight fix ----
document.querySelectorAll('.nav-link').forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});
