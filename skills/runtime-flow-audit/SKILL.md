---
name: runtime-flow-audit
description: Use when reviewing or planning changes in this language-learning repo that require tracing one runtime path end-to-end, especially UI button -> api.js -> Flask resource -> orchestrator -> ChatGPT request -> UI response. Prioritize requested files only, reload them explicitly, obey AGENTS.md, and report contract mismatches before suggesting changes.
metadata:
  short-description: Audit one runtime flow end-to-end
---

# Runtime Flow Audit

Use this skill when the user asks to:
- reload specific files and check consistency
- trace a button, endpoint, or lesson step end-to-end
- verify whether a path reaches the ChatGPT request correctly
- find the first real mismatch in a runtime path
- suggest minimal changes without implementing them

## Repo Rules First

Before code analysis:
1. Read `AGENTS.md`.
2. Stay read-only unless the current collaboration mode allows implementation.
3. If the user says `reload <file>`, re-open that exact file before answering.
4. If the user says `check only this file`, do not expand scope.
5. If the user says `skip <path>`, exclude it from analysis.

## Default Audit Method

For a requested runtime path, trace only this chain as needed:

1. UI trigger
- button in HTML
- handler in `ui/static/js/app.js`
- request builder in `ui/static/js/api.js`

2. Backend entry
- route registration in `api/app/__init__.py`
- matching Flask resource in `api/app/resources/*`

3. Runtime flow
- resource validation
- transition into orchestrator/service layer
- plan loading and runtime payload shaping

4. GPT request
- exact call site to `ChatGPT().send_messages(...)` or chat loop
- system message shape
- user message shape
- response parsing path back to UI

## Output Style

Always answer in this order:
1. Is the flow consistent or not
2. First blocking mismatch
3. Minimal suggested change
4. Ignore unrelated unfinished paths unless the user asks

Keep answers short and concrete.

## Scope Discipline

- Prefer the smallest path that answers the question.
- Do not review unrelated endpoints.
- Do not drift into refactor proposals unless the user asks.
- If multiple issues exist, report the first true blocker first.

## Common Checks For This Repo

When tracing a flow, verify:
- UI endpoint path matches Flask route
- HTTP method matches
- request JSON keys match resource expectations
- resource calls orchestrator with the correct signature
- exercise index maps to the correct drill plan
- module type maps to the correct plan folder
- session/module linkage is preserved
- response envelope is `mode` + `message`
- GPT request is actually reached, not blocked earlier

## Known Project Preferences

Optimize for:
- simplification first
- working runtime path before architecture cleanup
- small explicit modules
- no hidden magic
- contract consistency over feature expansion

## Suggested Phrasing

Prefer phrases like:
- "This path is consistent."
- "The flow breaks before GPT here: ..."
- "Only this comment is outdated; runtime is fine."
- "Skip `continue_turn`; not in current tested scope."

Avoid:
- broad redesign advice when user asked for one path
- reviewing unrequested files
- speculative improvements unrelated to the active flow
