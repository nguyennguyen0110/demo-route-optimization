// static/js/main.js

// =========================
// Theme handling
// =========================

const THEME_KEY = "theme";

function getStoredTheme() {
    return localStorage.getItem(THEME_KEY) || "system";
}

function shouldUseDark(mode) {
    if (mode === "dark") return true;
    if (mode === "light") return false;

    // mode === "system"
    if (window.matchMedia) {
        return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false; // default to light if no info
}

function applyTheme(mode) {
    if (shouldUseDark(mode)) {
        document.documentElement.classList.add("dark-mode");
    } else {
        document.documentElement.classList.remove("dark-mode");
    }
}

// Apply theme as soon as script loads
(function initTheme() {
    const mode = getStoredTheme();
    applyTheme(mode);
})();


// =========================
// DOM wiring
// =========================

document.addEventListener("DOMContentLoaded", () => {
    const themeSelect = document.getElementById("theme-select");

    // ----- Theme select -----
    if (themeSelect) {
        const stored = getStoredTheme();
        themeSelect.value = stored;
        applyTheme(stored);

        themeSelect.addEventListener("change", () => {
            const mode = themeSelect.value;
            localStorage.setItem(THEME_KEY, mode);
            applyTheme(mode);
        });

        // Live update in "system" mode when OS theme changes
        if (window.matchMedia) {
            const media = window.matchMedia("(prefers-color-scheme: dark)");

            if (media.addEventListener) {
                media.addEventListener("change", () => {
                    const current = getStoredTheme();
                    if (current === "system") {
                        applyTheme("system");
                    }
                });
            } else if (media.addListener) {
                // Older browsers
                media.addListener(() => {
                    const current = getStoredTheme();
                    if (current === "system") {
                        applyTheme("system");
                    }
                });
            }
        }
    }
});
