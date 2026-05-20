// admin_custom.js - optional small JS, safe to include
document.addEventListener("DOMContentLoaded", function() {
  // add a small logo element into header branding if present
  try {
    const header = document.getElementById('header');
    const branding = header.querySelector('.branding');
    if (branding) {
      const logoDiv = document.createElement('div');
      logoDiv.className = 'logo';
      // background image will be set by base_site.html inline style
      branding.insertBefore(logoDiv, branding.firstChild);
    }
  } catch (e) {
    // silently ignore errors
    console.log('admin_custom.js init', e);
  }
});
