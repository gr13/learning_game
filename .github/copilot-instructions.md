# Copilot Chat Instructions for this Workspace

## 🧭 Purpose
This repo implements a **structured AI-assisted language learning system** (frontend + Flask API + MySQL). The goal is to make the project stable and predictable by enforcing strict layering, clear contracts, and small incremental changes.

This instructions file is the primary way Copilot Chat should understand the project conventions, how to run the system, and how to safely make changes.

---

## 🚀 How to Run

### 1) Start the full stack (recommended)
```bash
docker compose up --build
```

### 2) API only (inside the `api/` folder)
```bash
cd api
python run.py
```

### 3) Run tests
```bash
pytest api/tests
```

---

## 🧱 Architecture & Conventions

### Layers
- **UI**: frontend only handles rendering + user input.
- **API resources**: perform HTTP validation/serialization + orchestration.
- **Engine/modules**: learning logic only.
- **Models/ORM**: persistence only.

### Contracts
- Use `sessions.exercise_index` as the canonical progress field.
- Use `session_messages.session_id + role` as the canonical message model.

Any change to schema must be reflected in:
- `mysql/init.sql`
- SQLAlchemy models
- tests/fixtures

### Coding rules
- Keep modules small and explicit.
- Prefer typed signatures and predictable return shapes (plain `dict` payloads).
- Never silently fallback for invalid module types or indexes.
- Avoid mixing archived code into active execution paths.
- **Flake8 must pass** for all modified files.

---

## 🧪 Testing Rules
- Add/adjust tests for each behavioral change.
- Minimum checks before merge:
  1) Unit tests for touched modules/models.
  2) One API flow test for any changed endpoint contract.
- If a change requires MySQL, note it clearly in your response.

---

## 🛡️ Change Policy (Assistant Behavior)
- The assistant has **read-only access by default**.
- File modifications require explicit user permission via: `update mode on <file_path>`.
- Creating new files requires explicit permission.
- Deletions are suggestion-only unless explicitly authorized.

---

## 🧭 Quick Navigation
- Core API: `api/app/`  
- Module engines: `api/app/lessons/`  
- Models: `api/app/models/`  
- Tests: `api/tests/`

---

## 🔍 Notes for Copilot Chat
When asked to implement changes:
1) State the contract impact first.
2) List tradeoffs briefly.
3) Prefer incremental, reversible refactors.

---

## ✅ Example Prompts (use when collaborating)
- "Help me add a new exercise type to the `ReadingExam` module while keeping the API contract stable."
- "The `start_module` endpoint is returning incorrect `session_id`; help me trace the call path."
- "Update the `sessions` schema and make sure the API + tests stay in sync."
