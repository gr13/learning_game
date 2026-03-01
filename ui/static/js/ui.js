// ==============================
// ui.js (Pure UI Helpers)
// ==============================

export function setupAutoResize() {

    const textarea = document.getElementById("user-input");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    textarea.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            window.sendAnswer();
        }
    });
}