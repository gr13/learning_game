// ==============================
// renderer.js (Rendering Layer)
// ==============================

export function appendAssistantText(text) {

    const container = document.getElementById("message");

    const block = document.createElement("div");
    block.className = "assistant-message";
    block.innerHTML = `<div class="assistant-full">${text}</div>`;

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
