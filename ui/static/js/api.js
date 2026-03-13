// ==============================
// api.js (Backend Layer)
// ==============================

export async function getModule(id, sessionId = null) {
    const body = {};
    if (sessionId !== null) {
        body.session_id = sessionId;
    }
    const res = await fetch(`/api/modules/start-module/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    return res.json();
}

export async function postAnswer(moduleId, sessionId, text) {

    const res = await fetch(`/api/modules/${moduleId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            module_id: moduleId,
            session_id: sessionId,
            user_input: text
        })
    });

    return res.json();
}

export async function postNextExercise(sessionId) {

    const res = await fetch("/api/modules/next-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId
        })
    });

    return res.json();
}

export async function postEndModule(sessionId) {

    const res = await fetch("/api/modules/end-module", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId
        })
    });

    return res.json();
}
