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
    document.getElementById("module-content").style.display = "block";
    document.getElementById("answer-section").style.display = "flex";

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
            const message = JSON.parse(data.message);

            /* Render structured lesson object */
            renderModuleContent(message);
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
    document.getElementById("module-menu").style.display = "block";
    document.getElementById("module-content").style.display = "none";
    document.getElementById("answer-section").style.display = "none";
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
    const text = document.getElementById("user-input").value.trim();

    if (!text) return;

    appendUserMessage(text);

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
        console.log("waipoint 1");
        appendAssistantText(data.message);

        textarea.value = "";
        textarea.style.height = "auto";
    })
    .catch(error => {
        console.error("POST Error:", error);
    });;
}
