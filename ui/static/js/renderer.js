// ==============================
// renderer.js (Rendering Layer)
// ==============================

export function appendAssistantText(text) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";
    block.innerHTML =
        `<div class="assistant-full">${text.replace(/\n/g, "<br>")}</div>`;

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}

export function appendUserText(text) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "user-message";
    block.innerHTML = `<div class="user-bubble">${text}</div>`;

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}

// --------------------------------
// Explanation Renderer
// --------------------------------
export function renderExplanation(data) {

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

    // -------------------------
    // Forms (if present)
    // -------------------------
    if (data.forms) {

        const formsDiv = document.createElement("div");
        formsDiv.innerHTML = `
            <h3>Forms:</h3>
            <div><strong>Präsens:</strong> ${data.forms.praesens || ""}</div>
            <div><strong>Präteritum:</strong> ${data.forms.praeteritum || ""}</div>
            <div><strong>Perfekt:</strong> ${data.forms.perfekt || ""}</div>
        `;

        block.appendChild(formsDiv);
    }

    // -------------------------
    // Examples
    // -------------------------
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

// --------------------------------
// Exercise Renderer
// --------------------------------
export function renderExercise(data) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";

    block.innerHTML = `
        <div class="assistant-full">
            <strong>Exercise ${data.exerciseNumber}</strong><br>
            <em>${data.exerciseType}</em>
        </div>
    `;

    if (data.tasks) {
        data.tasks.forEach((task, index) => {
            const taskDiv = document.createElement("div");
            taskDiv.className = "example";
            taskDiv.innerHTML =
                `<strong>Task ${index + 1}:</strong> ${task.instruction}`;
            block.appendChild(taskDiv);
        });
    }

    container.appendChild(block);
    container.scrollTop = container.scrollHeight;
}

// --------------------------------
export function renderMicroDrill(data) {
    appendAssistantText("Micro drill started.");
}
