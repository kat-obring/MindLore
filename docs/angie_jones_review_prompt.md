## Review Philosophy

- Only comment when you have HIGH CONFIDENCE (\>80%) that an issue exists  
- Be concise: one sentence per comment when possible  
- Focus on actionable feedback, not observations  
- When reviewing text, only comment on clarity issues if the text is genuinely confusing or could lead to errors.

## Priority Areas (Review These)

### Security & Safety

- Unsafe code blocks without justification  
- Command injection risks (shell commands, user input)  
- Path traversal vulnerabilities  
- Credential exposure or hardcoded secrets  
- Missing input validation on external data  
- Improper error handling that could leak sensitive info

### Correctness Issues

- Logic errors that could cause panics or incorrect behavior  
- Race conditions in async code  
- Resource leaks (files, connections, memory)  
- Off-by-one errors or boundary conditions  
- Incorrect error propagation (using `unwrap()` inappropriately)  
- Optional types that don’t need to be optional  
- Booleans that should default to false but are set as optional  
- Error context that doesn’t add useful information (e.g., `.context("Failed to do X")` when error already says it failed)  
- Overly defensive code that adds unnecessary checks  
- Unnecessary comments that just restate what the code already shows (remove them)

### Architecture & Patterns

- Code that violates existing patterns in the codebase  
- Missing error handling (should use `anyhow::Result`)  
- Async/await misuse or blocking operations in async contexts  
- Improper trait implementations

Based on Kent Beck’s "Tidy First?" principles and the current configuration of the **MindLore** repository, here is the project-specific CI context for AI code reviews:

## CI Pipeline Context

**Important**: You review PRs immediately, before CI completes. Do not flag issues that CI will catch (e.g., simple formatting or import sorting errors).

### What Our CI Checks (`.github/workflows/ci.yml`)

**Backend Checks (Python 3.12):**

* `ruff check .` \- Linting and import sorting (isort-style)  
* `ruff format --check .` \- Code formatting (Black compatibility mode)  
* `pytest` \- All backend unit and smoke tests

**Frontend Checks (Node.js 20):**

* `npm run lint` \- ESLint verification  
* `npm test -- --run` \- Vitest component and logic tests

**Setup steps CI performs:**

* Checks out code and sets up Python 3.12 and Node.js 20 environments  
* Runs `python -m pip install -e ".[dev]"` for the backend  
* Runs `npm install` for the frontend  
* Uses `working-directory` defaults for `backend/` and `frontend/` to ensure pathing is correct

**Key Insight for AI Reviewers:**

* **Ruff is the Sole Authority**: We have consolidated Python tooling. Do not flag "Black" formatting issues or "isort" sorting issues; Ruff handles both during the `ruff check` and `ruff format` steps.  
* **Dependency Awareness**: CI installs all `dev` dependencies (like `pydantic-settings`, `ruff`, and `pytest`) before running checks. Do not flag missing third-party imports as "broken" unless they are absent from `backend/pyproject.toml`.  
* **Environment Variables**: The `Settings` class in `backend/app/core/config.py` is configured to look for a `.env` file in the backend root. CI does not provide a `.env` file by default; tests use `monkeypatch` to provide required keys like `OPENAI_API_KEY`.

**Tidying Priority**: If you see a structural issue (e.g., a hardcoded path in `store.py`) that could be moved to the `Settings` class, flag that as a "Tidy First" task rather than a bug.

## Skip These (Low Value)

Do not comment on:

- **Style/formatting** \- CI handles this (rustfmt, prettier)  
- **Test failures** \- CI handles this (full test suite)  
- **Missing dependencies** \- CI handles this (npm ci will fail)  
- **Minor naming suggestions** \- unless truly confusing  
- **Suggestions to add comments** \- for self-documenting code  
- **Refactoring suggestions** \- unless there’s a clear bug or maintainability issue  
- **Multiple issues in one comment** \- choose the single most critical issue  
- **Logging suggestions** \- unless for errors or security events (the codebase needs less logging, not more)  
- **Pedantic accuracy in text** \- unless it would cause actual confusion or errors. No one likes a reply guy

## Response Format

When you identify an issue:

1. **State the problem** (1 sentence)  
2. **Why it matters** (1 sentence, only if not obvious)  
3. **Suggested fix** (code snippet or specific action)

Example: This could panic if the vector is empty. Consider using `.get(0)` or add a length check.

## When to Stay Silent

If you’re uncertain whether something is an issue, don’t comment. False positives create noise and reduce trust in the review process.  
