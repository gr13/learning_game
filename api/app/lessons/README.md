# Lessons Package

This package contains a full lesson cycle blueprint for:
- `GET` start request
- `POST` continuation request
- ChatGPT call with full message history
- response validation and normalization
- persistence of system/user/assistant messages

## Entry Points
- `LessonRouter.handle_get(module_id, session_id)`
- `LessonRouter.handle_post(module_id, session_id, user_input)`

## CORE Flow
1. `handle_get` builds system payload from `plans/*.json` + runtime.
2. Appends system/user bootstrap messages to session history.
3. Calls ChatGPT with full history.
4. Validates JSON (intro schema when expected), persists assistant reply.
5. Returns normalized envelope:
   - `{ "mode": "json", "message": ... }` or
   - `{ "mode": "text", "message": ... }`

## Notes
- This package is self-contained under `api/app/lessons`.
- Integration into `api/app/resources/module.py` can call `LessonRouter` later.
