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
       1️⃣  UI STATE TRANSITION
       ------------------------------------------------------------
       Switch from module menu to lesson view.
       This creates a simple SPA-like behavior.
    ------------------------------------------------------------ */

    document.getElementById("module-menu").style.display = "none";
    document.getElementById("module-content").style.display = "block";


    /* ------------------------------------------------------------
       2️⃣  BACKEND REQUEST
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
    console.log(data);
    console.log(data.word);

    const container = document.getElementById("message");
    container.innerHTML = "";

    container.innerHTML += `<h2>${data.word}</h2>`;
    container.innerHTML += `<p><strong>Part of Speech:</strong> ${data.partOfSpeech}</p>`;
    container.innerHTML += `<p><strong>Pronunciation:</strong> ${data.pronunciation}</p>`;
    container.innerHTML += `<p><strong>Definition:</strong> ${data.definition}</p>`;

    // examples
    if (data.examples) {
        container.innerHTML += "<h3>Examples:</h3>";
        data.examples.forEach(example => {
            container.innerHTML += `
                <div class="example">
                    <div><strong>${example.de}</strong></div>
                    <div class="translation">${example.en}</div>
                </div>
            `;
        });
    }

    // Conjugation
    if (data.conjugationPresent) {
        container.innerHTML += "<h3>Present Tense:</h3><ul>";
        for (const person in data.conjugationPresent) {
            container.innerHTML += `<li>${person}: ${data.conjugationPresent[person]}</li>`;
        }
        container.innerHTML += "</ul>";
    }

    if (data.simplePast) {
        container.innerHTML += `<p><strong>Simple Past:</strong> ${data.simplePast}</p>`;
    }

    if (data.pastParticiple) {
        container.innerHTML += `<p><strong>Past Participle:</strong> ${data.pastParticiple}</p>`;
    }

    if (data.usageNotes) {
        container.innerHTML += `<p><strong>Notes:</strong> ${data.usageNotes}</p>`;
    }
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

    document.getElementById("module-menu").style.display = "block";
    document.getElementById("module-content").style.display = "none";
}
