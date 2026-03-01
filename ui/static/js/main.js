/**
 * ============================================================
 * Language Learning App - Frontend Controller
 * ============================================================
 *
 * This file is responsible for:
 *
 * 1. Handling module button clicks
 * 2. Communicating with the backend API
 * 3. Rendering structured lesson data
 * 4. Managing basic UI state (menu vs lesson view)
 *
 * Architecture principle:
 * - Backend controls lesson logic.
 * - Frontend only renders structured JSON.
 * - No business logic is implemented here.
 *
 * ============================================================
 */

let currentModuleId = null;
let currentSessionId = null;



/**
 * ============================================================
 * MODULE REQUEST HANDLER
 * ============================================================
 *
 * Triggered when user clicks a module button.
 *
 * Responsibilities:
 * - Hide module menu
 * - Show content section
 * - Call backend endpoint
 * - Validate response structure
 * - Pass lesson data to renderer
 *
 * @param {number} id - Module number (1–6)
 */
function requestModule(id) {

    /* ------------------------------------------------------------
       UI STATE TRANSITION
       ------------------------------------------------------------
       Switch from module menu to lesson view.
       This creates a simple SPA-like behavior.
    ------------------------------------------------------------ */
    
    document.getElementById("app-title").style.display = "none";
    document.getElementById("module-menu").style.display = "none";
    document.getElementById("lesson-area").style.display = "block";

    /* ------------------------------------------------------------
       BACKEND REQUEST
       ------------------------------------------------------------
       We call the API endpoint dynamically based on module ID.
       Example:
           /api/modules/1
           /api/modules/2
    ------------------------------------------------------------ */

    fetch(`/api/modules/${id}`)

        /* Convert HTTP response to JSON */
        .then(response => response.json())

        /* Handle parsed JSON data */
        .then(data => {
            currentModuleId = id;
            console.log("Full response:", data);
            console.log("Session ID:", data.session_id);
            currentSessionId = data.session_id;

            /* Defensive validation */
            if (!data || !data.message) {
                document.getElementById("message").textContent =
                    "Invalid backend response.";
                return;
            }

            if (data.mode === "text") {
                appendAssistantText(data.message);
                return;
            }

            if (data.mode === "json") {

                const payload = data.message;

                if (!payload) {
                    appendAssistantText("Empty JSON payload.");
                    return;
                }

                if (Array.isArray(payload)) {
                    payload.forEach(item => {
                        routeLessonPayload(item);
                    });
                    return;
                }

                routeLessonPayload(payload);
                return;
            }

            appendAssistantText("Unsupported response type.");
        })

        /* Catch network / server errors */
        .catch(error => {

            document.getElementById("message").textContent =
                "Error contacting server";

            console.error("API Error:", error);
        });
}



/**
 * ============================================================
 * LESSON RENDERING ENGINE
 * ============================================================
 *
 * Receives normalized lesson object from backend and
 * dynamically constructs HTML.
 *
 * IMPORTANT:
 * - This function assumes backend returns stable JSON schema.
 * - It does NOT attempt to interpret free-form GPT text.
 *
 * @param {Object} data - Structured lesson object
 */
function renderModuleContent(data) {
    console.log("waipoint 2");
    console.log(data);
    console.log(data.word);

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";

    block.innerHTML = `
        <div class="assistant-full">
            <strong>${data.word}</strong><br>
            <strong>Part of Speech:</strong> ${data.partOfSpeech}<br>
            <strong>Pronunciation:</strong> ${data.pronunciation}<br>
            <strong>Definition:</strong> ${data.definition}
        </div>
    `;

    if (data.examples) {
        const examples = document.createElement("div");
        examples.innerHTML = "<h3>Examples:</h3>";

        data.examples.forEach(example => {
            examples.innerHTML += `
                <div class="example">
                    <div><strong>${example.de}</strong></div>
                    <div class="translation">${example.en}</div>
                </div>
            `;
        });
        block.appendChild(examples);
    }

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;

}

function appendUserMessage(text) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "user-message";

    block.innerHTML = `
        <div class="user-bubble">
            ${text}
        </div>
    `;

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}

function appendAssistantText(text) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";

    block.innerHTML = `
        <div class="assistant-full">
            ${text}
        </div>
    `;

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}

/**
 * ============================================================
 * UI NAVIGATION: BACK TO MODULE MENU
 * ============================================================
 *
 * Restores module selection screen.
 * Does not reload page.
 */
function showMenu() {

    document.getElementById("app-title").style.display = "block";
    // Show module selection
    document.getElementById("module-menu").style.display = "block";
    // Hide lesson area
    document.getElementById("lesson-area").style.display = "none";

    document.getElementById("message").innerHTML = "";
}

document.addEventListener("DOMContentLoaded", function () {

    const textarea = document.getElementById("user-input");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    textarea.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendAnswer();
        }

    });

});

function sendAnswer() {
    const textarea = document.getElementById("user-input");
    const text = textarea.value.trim();

    if (!text) return;

    appendUserMessage(text);
    textarea.value = "";
    textarea.style.height = "auto";

    fetch(`/api/modules/${currentModuleId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            module_id: currentModuleId,
            session_id: currentSessionId,
            user_input: text
        })
    })
    .then(res => res.json())
    .then(data => {

        if (!data || !data.message) {
            appendAssistantText("Invalid backend response.");
            return;
        }

        // TEXT MODE
        if (data.mode === "text") {
            appendAssistantText(data.message);
            return;
        }

        // JSON MODE
        if (data.mode === "json") {

            const payload = data.message;

            if (!payload) {
                appendAssistantText("Empty JSON payload.");
                return;
            }

            // 🔵 CASE 1: Array of exercises
            if (Array.isArray(payload)) {
                payload.forEach(item => {
                    routeLessonPayload(item);
                });
                return;
            }

            // 🔵 CASE 2: Single object
            routeLessonPayload(payload);
            return;
        }

        appendAssistantText("Unsupported response type.");
    })
    .catch(error => {
        console.error("POST Error:", error);
    });;
}

let endClickTimeout = null;
let endClickArmed = false;

function endModule() {

    const btn = document.querySelector(".end-button");

    if (!endClickArmed) {
        endClickArmed = true;

        btn.textContent = "Click again to confirm";
        btn.style.color = "#ff6b6b";

        endClickTimeout = setTimeout(() => {
            endClickArmed = false;
            btn.textContent = "End Module";
            btn.style.color = "#ccc";
        }, 2000);

        return;
    }

    clearTimeout(endClickTimeout);

    // 🔥 Disable input properly
    const textarea = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    textarea.disabled = true;
    sendBtn.disabled = true;

    // Optional: visually indicate end
    textarea.placeholder = "Module ended";

    btn.textContent = "Module Ended";
    btn.disabled = true;

    console.log("Module ended safely");
}

function routeLessonPayload(payload) {

    if (!payload || !payload.mode) {
        appendAssistantText("Malformed lesson payload.");
        return;
    }

    switch (payload.mode) {

        case "explanation":
            renderModuleContent(payload);
            break;

        case "exercise":
            renderExercise(payload);
            break;

        case "micro_drill":
            renderMicroDrill(payload);
            break;

        default:
            console.warn("Unknown lesson mode:", payload.mode);
            appendAssistantText("Unknown lesson type.");
    }
}

function renderExercise(data) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";

    block.innerHTML = `
        <div class="assistant-full">
            <strong>Exercise ${data.exerciseNumber || ""}</strong><br>
            <em>${data.exerciseType || ""}</em>
        </div>
    `;

    if (data.tasks) {
        data.tasks.forEach((task, index) => {
            const taskDiv = document.createElement("div");
            taskDiv.className = "example";
            taskDiv.innerHTML = `
                <div><strong>Task ${index + 1}:</strong> ${task.instruction}</div>
            `;
            block.appendChild(taskDiv);
        });
    }

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}
