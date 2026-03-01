// ==============================
// app.js (ENTRY POINT)
// ==============================

import { getModule, postAnswer } from "./api.js";
import { handleBackendResponse } from "./router.js";
import { setupAutoResize } from "./ui.js";

let currentModuleId = null;
let currentSessionId = null;

// ------------------------------
// Request Module
// ------------------------------
window.requestModule = async function (id) {

    currentModuleId = id;

    document.getElementById("app-title").style.display = "none";
    document.getElementById("module-menu").style.display = "none";
    document.getElementById("lesson-area").style.display = "block";

    try {
        const data = await getModule(id);
        currentSessionId = data.session_id;
        handleBackendResponse(data);
    } catch (err) {
        console.error(err);
    }
};

// ------------------------------
// Send Answer
// ------------------------------
window.sendAnswer = async function () {

    const textarea = document.getElementById("user-input");
    const text = textarea.value.trim();
    if (!text) return;

    textarea.value = "";

    try {
        const data = await postAnswer(
            currentModuleId,
            currentSessionId,
            text
        );

        handleBackendResponse(data);
    } catch (err) {
        console.error(err);
    }
};

// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    setupAutoResize();
});
