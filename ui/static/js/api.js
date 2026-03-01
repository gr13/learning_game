// ==============================
// api.js (Backend Layer)
// ==============================

export async function getModule(id) {
    const res = await fetch(`/api/modules/${id}`);
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
