# AGENTS.md

## Purpose
This repository builds a structured AI-assisted language learning app with:
- `ui` (browser frontend)
- `api` (Flask + SQLAlchemy backend)
- `mysql` (schema + seed data)
- `nginx` (reverse proxy)

The main goal is reliable, step-by-step training with persisted progress.

## Main Project Goals
1. Build a language learning app that mitigates ChatGPT context/memory limitations in a dementia-like way:
- ChatGPT acts as the teacher.
- Training is structured into small, predictable, step-by-step exercises.

2. Build a simple app for `1..n` users, but in this version run without login:
- Use one default user in the system.
- Keep the full app flow working end-to-end without authentication.

3. Keep this as a personal single-developer project (not for release).

4. Long-term direction: iPhone companion workflow:
- Extract a small portion of training data to the phone.
- Run daily training on iPhone.
- Export results back to the main app via Wi-Fi or cable sync.

## Current Reality
- Module `CORE` is the only module reliably wired in runtime registry.
- Data contracts between API and UI are partially inconsistent and need alignment.
- Some DB schema names and ORM model names are inconsistent.

Treat stability and contract consistency as priority over adding features.

## Architecture Rules
1. Keep strict layering:
- UI: rendering + user input only.
- API resources: HTTP validation and orchestration only.
- Module engines/exercises: learning logic only.
- Models: persistence only.

2. Avoid business logic in Flask resources.

3. Any new response payload must have an explicit UI contract documented in code comments.

## Data Contract Rules
1. Use one canonical session progress field everywhere:
- Prefer `sessions.exercise_index`.

2. Use one canonical message model naming everywhere:
- Prefer `session_messages.session_id` + `role`.

3. If schema changes, update all three in one PR:
- `mysql/init.sql`
- SQLAlchemy models
- tests/fixtures

## Coding Rules
1. Keep modules small and explicit; avoid hidden magic.
2. Prefer typed signatures and predictable return shapes (`dict` schemas).
3. No silent fallback behavior for invalid module types or unknown exercise indexes.
4. Do not mix archived code into active execution paths.
5. Respect flake8 requirements for all new and updated code.
6. Before finalizing code changes, run flake8 on changed scope when available.
7. Do not suppress flake8 errors (`# noqa`) without explicit user approval.

## Testing Rules
1. Add/adjust tests for every behavioral change.
2. Minimum checks before merge:
- Unit tests for touched models/engines
- One API flow test for changed endpoint contract
3. If MySQL is required, state it clearly in PR notes.

## Priority Backlog (Near-Term)
1. Fix `Module` resource integration bugs (`run_module` call args, `session.id` usage).
2. Align API response envelope with frontend router (`mode` + `message` or unified alternative).
3. Normalize `exercise_index` usage across templates/analyzers/runners.
4. Align `session_messages` SQL schema with ORM model.
5. Implement or hide non-core module buttons until backend support exists.

## Definition of Done
A change is done only when:
1. Runtime path works end-to-end for the affected flow.
2. DB/model/API/UI contracts are consistent.
3. Tests pass for changed behavior.
4. README or inline docs are updated if contract/flow changed.

## Collaboration Notes
When proposing changes:
1. State the contract impact first.
2. List tradeoffs briefly.
3. Prefer incremental, reversible refactors.

## Access Policy
1. The agent always has read-only access to all project files.
2. Read-only access is for analysis, review, and proposing changes.
3. File modifications require explicit user permission via:
- `update mode on <file_path>`
4. `update mode off` revokes all write permissions.
5. Creating new files is allowed only with explicit user permission.
6. Deleting files is suggestion-only unless explicitly approved by the user.

## Versioning Policy
1. Every change to this file must append one line to `Version History`.
2. Use this format:
- `DD.MM.YYYY HH:MM version X.XXXX short description`
3. Keep versions incremental and monotonic (`0.0001`, `0.0002`, ...).

## Version History
- 09.03.2026 08:11 version 0.0001 created initial AGENTS.md
- 09.03.2026 08:12 version 0.0002 added explicit file-level edit permission policy
- 09.03.2026 08:13 version 0.0003 added main project goals
- 09.03.2026 08:14 version 0.0004 added versioning policy and changelog format
- 09.03.2026 08:17 version 0.0005 added update mode on/off logic, create allowed, delete by suggestion only
- 09.03.2026 10:01 version 0.0006 replaced edit policy with always-read access + explicit write permission model
- 09.03.2026 14:57 version 0.0007 added mandatory flake8 compliance rules
