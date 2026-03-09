# PLAN.md

Continuous project plan and issue tracker.

## Workflow Rules
1. Keep only active, unfinished issues in this file.
2. As soon as an issue is implemented, remove it from this file.
3. One issue = one clear expected result.
4. Use priority tags: `P1` (critical), `P2` (important), `P3` (nice-to-have).
5. Use status tags: `todo`, `in_progress`, `blocked`.

## Step-by-Step Execution Plan (Core Module)
Keep this table until all rows are marked done.

| Step | Item | Done | Done Criteria |
|---|---|---|---|
| 1 | Start Module: user clicks Core button, UI calls `GET /modules/1`, backend creates/loads session | `expected_dev` | First teacher intro response is shown in UI (module seed can be manual in dev mode) |
| 2 | Intro Package: backend builds base plan + word intro context and sends it to ChatGPT | `not_done` | Intro response is saved to message history and returned to UI |
| 3 | Exercise Start: backend starts first exercise (`new_word_drill`) and returns tasks | `not_done` | UI shows exercise payload without contract/render errors |
| 4 | Answer Loop: user submits answer, backend sends full history + current task context to ChatGPT, returns teacher feedback | `not_done` | User answer and assistant feedback are both saved and shown |
| 5 | Micro-Drill Loop (optional): user requests drill, backend sends history to ChatGPT, receives short drill, evaluates response, returns teacher feedback | `not_done` | At least one drill cycle completes end-to-end |
| 6 | Next Exercise: user presses next, backend finalizes current exercise and starts next one | `not_done` | Exercise index increments and next exercise prompt is shown |
| 7 | Vocabulary Sync: backend requests introduced/learned words from ChatGPT and updates `core_vocabulary` / `domain_vocabulary` (`introduced`, `dt_introduced`, `learned`, `dt_learned`) | `not_done` | DB updates are persisted for current session results |
| 8 | Finish Module: user presses finish module button (manual completion) | `not_done` | Module state is marked done and next module can start |
| 9 | Repeat: same structure for remaining module exercises | `not_done` | All 5 exercises in module are completed |

`expected_dev` means known non-release gap accepted during development.

## Active Issues

### [P1][todo] Core runtime: API/Frontend response contract mismatch
- Expected result: module 1 flow does not produce `Invalid backend response` in UI.

### [P1][todo] Core runtime: module completion flow behavior definition
- Expected result: backend behavior is explicitly defined (manual completion only, no accidental auto-finalize).

### [P1][in_progress] Schema/model alignment for active tables
- Expected result: active SQL schema fields fully match ORM model fields.

### [P2][todo] Frontend controls wired to real handlers
- Expected result: visible buttons do not throw runtime JS errors when clicked.

## Continuous Checks (Hidden Error Scan)
Run these checks repeatedly during development:
1. Runtime path check: `GET /modules/1` then `POST /modules/1`.
2. Contract check: backend payload keys match frontend router expectations.
3. Schema/model check: table columns, nullability, enum names, and indexes match ORM.
4. Progression check: one source of truth for exercise progression.
5. Typing check: no broad/untyped core runtime signatures.

## Backlog Ideas
- Explicit endpoint for manual module completion.
- Lightweight smoke tests for module 1 API flow.
- Typed response contracts for resources.
- Response-type detector (JSON vs plain text auto handler).
- Robust JSON vs plain-text detection in runtime responses.
- Rendering crash prevention for malformed/partial payloads.
- Clean separation of response modes.
- Refactor to `PromptBuilder`-based architecture for cleaner scaling.
- Centralized prompt generation.
- Clean separation of concerns across module/exercise layers.
- Scalable module architecture for Modules 2–5.
