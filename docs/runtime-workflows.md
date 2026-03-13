# Planned Runtime Workflows

This document describes the intended runtime flow of the active learning system.
It is a target workflow document, not a description of accidental current behavior.

## 1. Start New Module

Use case: user clicks a module button such as `1 - Core Vocabulary`.

1. UI calls `requestModule(module_type_id)`.
2. UI sends `POST /api/modules/start-module/<module_type_id>`.
3. Backend validates `module_type_id`.
4. If no `session_id` is provided, backend creates a new `training_lesson`.
5. Backend creates a new `module` inside that training lesson.
6. Backend creates a new `session`.
7. Backend links the new session to the new module.
8. Backend creates `exercise #1` with `exercise_index = 1`.
9. Backend calls orchestrator start logic.
10. For modules with intro step, orchestrator runs step 0 intro.
11. Orchestrator builds the GPT request.
12. GPT returns structured lesson payload.
13. Backend returns `{ mode, message, session_id }`.
14. UI stores `session_id` and renders the response.

## 2. Continue Current Exercise

Use case: user enters an answer for the current exercise.

1. UI sends `POST /api/modules/<module_type_id>`.
2. Request body contains `session_id` and `user_input`.
3. Backend validates `session_id`, `module_type_id`, and `user_input`.
4. Backend resolves session and module.
5. Backend calls orchestrator continue logic.
6. Orchestrator builds the continue-package for the current exercise.
7. Orchestrator sends GPT request in teacher mode.
8. GPT returns feedback, correction, or follow-up payload.
9. Backend returns `{ mode, message }`.
10. UI renders assistant response.

## 3. Next Exercise

Use case: user clicks `Next Exercise`.

1. UI sends `POST /api/modules/next-exercise`.
2. Request body contains current `session_id`.
3. Backend validates `session_id`.
4. Backend loads current session.
5. Backend loads current module from the session.
6. Backend loads current exercise from the session.
7. Backend reads `exercise_index` from the current exercise.
8. Backend creates a new session for the next step.
9. Backend links the new session to the same module.
10. Backend creates a new exercise with `exercise_index + 1`.
11. Backend calls orchestrator start-exercise logic.
12. Orchestrator loads general plan and drill plan for that exercise index.
13. Orchestrator builds the GPT request.
14. GPT returns structured exercise payload.
15. Backend returns `{ mode, message, session_id }` or `{ mode, message }` depending on final contract choice.
16. UI updates current session if a new session id is returned, then renders the next exercise.

## 4. End Module

Use case: user clicks `End Module`.

This flow is planned, not fully implemented yet.

1. UI sends `POST /api/modules/end-module`.
2. Request body contains current `session_id`.
3. Backend validates `session_id` and resolves current session and module.
4. Backend asks ChatGPT for `show_introduced`.
5. Backend uses that result to update database state for introduced vocabulary.
6. Backend asks ChatGPT for `show_learned`.
7. Backend uses that result to update database state for learned vocabulary.
8. Backend asks ChatGPT for `show_status` in teacher mode.
9. Backend returns teacher-style status/summary to UI.
10. Backend marks current module as done.
11. Backend returns enough result/context for UI to trigger `Continue to Next Module` with the next `module_type_id`.
12. UI can then start the next module from the continuation action, not from the main menu.

## 5. Continue To Next Module

Use case: after ending the current module, user continues to the next module inside the same training lesson.

0. Attention: TODO: the current training_lesson is required for the Next Module
1. UI triggers `Continue to Next Module`.
2. UI sends next `module_type_id`.
3. Backend resolves the current `training_lesson`.
4. Backend creates a new module of the requested type inside that training lesson.
5. Backend creates a new session for the new module.
6. Backend links the new session to the new module.
7. Backend creates `exercise #1` for the new module.
8. Backend calls orchestrator start logic for the new module.
9. Orchestrator runs intro or first exercise depending on module design.
10. GPT returns structured payload.
11. Backend returns `{ mode, message, session_id }`.
12. UI stores the new session id and renders the first step of the next module.

## 6. Button Mapping

Planned UI button meaning:

- Module menu button: starts a new module from menu entry.
- `Next Exercise`: advances inside the current module.
- `End Module`: closes the current module and produces end-of-module results.
- `Continue to Next Module`: starts the next module in sequence using the same training lesson context.

## 7. Source Of Truth For Runtime Design

When implementing or reviewing runtime behavior, use these files first:

- `api/app/resources/start_module.py`
- `api/app/resources/module.py`
- `api/app/resources/next_exercise.py`
- `ui/static/js/app.js`
- `ui/static/js/api.js`

This document defines intended behavior. If runtime code differs, the code should be considered not yet aligned with the planned workflow.
