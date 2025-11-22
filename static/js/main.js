// Global JS for Kaumahan Harvest Market
// Keep this file light; page-specific logic lives in templates when needed.

document.addEventListener('DOMContentLoaded', function () {
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
