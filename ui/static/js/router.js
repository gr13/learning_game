// ==============================
// router.js (Response Router)
// ==============================

import { 
    renderExplanation,
    renderExercise,
    renderMicroDrill,
    appendAssistantText
} from "./renderer.js";

export function handleBackendResponse(data) {

    if (!data || !data.message) {
        appendAssistantText("Invalid backend response.");
        return;
    }

    if (data.mode === "text") {
        appendAssistantText(data.message);
        return;
    }

    if (data.mode === "json") {

        const payload = data.message;

        if (Array.isArray(payload)) {
            payload.forEach(routeLessonPayload);
            return;
        }

        routeLessonPayload(payload);
        return;
    }

    appendAssistantText("Unsupported response type.");
}

function routeLessonPayload(payload) {

    if (!payload || !payload.mode) {
        appendAssistantText("Malformed lesson payload.");
        return;
    }

    switch (payload.mode) {

        case "explanation":
            renderExplanation(payload);
            break;

        case "exercise":
            renderExercise(payload);
            break;

        case "micro_drill":
            renderMicroDrill(payload);
            break;

        default:
            appendAssistantText("Unknown lesson type.");
    }
}
