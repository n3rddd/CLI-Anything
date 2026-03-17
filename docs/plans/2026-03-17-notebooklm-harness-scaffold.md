# NotebookLM Harness Scaffold Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an experimental `cli-anything-notebooklm` scaffold that wraps an installed `notebooklm` CLI, includes attribution files, and establishes the first round of tests and docs.

**Architecture:** Create a service-style harness under `notebooklm/agent-harness/` that mirrors the existing CLI-Anything package layout. The backend adapter will shell out to the installed `notebooklm` command, sanitize sensitive errors, and keep notebook context in a lightweight session file for REPL use.

**Tech Stack:** Python 3.10+, Click, prompt-toolkit, pytest, subprocess-based backend wrapper

### Task 1: Establish the tracked scaffold area

**Files:**
- Modify: `.gitignore`
- Create: `docs/plans/2026-03-17-notebooklm-harness-scaffold.md`

**Step 1: Write the failing test**

No behavior test for this task. It is repository plumbing needed to track the new harness path and plan document.

**Step 2: Run test to verify it fails**

Not applicable.

**Step 3: Write minimal implementation**

- Allow `docs/`
- Allow `notebooklm/`
- Allow `notebooklm/agent-harness/`

**Step 4: Run test to verify it passes**

Run: `git status --short`
Expected: new scaffold files are visible to git

**Step 5: Commit**

```bash
git add .gitignore docs/plans/2026-03-17-notebooklm-harness-scaffold.md
git commit -m "chore: prepare notebooklm harness scaffold"
```

### Task 2: Write the first failing backend tests

**Files:**
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_core.py`
- Test: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_core.py`

**Step 1: Write the failing test**

Cover:
- backend finds `notebooklm` on PATH
- backend raises clear install guidance if missing
- backend builds explicit commands with `-n <id>`
- backend sanitizes secret-bearing auth path output
- session file stores current notebook context

**Step 2: Run test to verify it fails**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py -q`
Expected: FAIL with import errors because the package does not exist yet

**Step 3: Write minimal implementation**

Create:
- `cli_anything/notebooklm/utils/notebooklm_backend.py`
- `cli_anything/notebooklm/core/session.py`

**Step 4: Run test to verify it passes**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/cli_anything/notebooklm
git commit -m "feat: add notebooklm backend scaffold"
```

### Task 3: Write the first failing CLI tests

**Files:**
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_cli_smoke.py`
- Test: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_cli_smoke.py`

**Step 1: Write the failing test**

Cover:
- root `--help` shows experimental NotebookLM wording
- root `--help` exposes command groups
- `auth status --help` and `notebook list --help` execute

**Step 2: Run test to verify it fails**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_cli_smoke.py -q`
Expected: FAIL because `notebooklm_cli.py` is missing

**Step 3: Write minimal implementation**

Create:
- `cli_anything/notebooklm/notebooklm_cli.py`
- `cli_anything/notebooklm/__init__.py`
- `cli_anything/notebooklm/__main__.py`

Use placeholder command handlers that route through the backend wrapper.

**Step 4: Run test to verify it passes**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_cli_smoke.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/cli_anything/notebooklm/notebooklm_cli.py
git commit -m "feat: add notebooklm cli skeleton"
```

### Task 4: Add packaging and attribution docs

**Files:**
- Create: `notebooklm/agent-harness/setup.py`
- Create: `notebooklm/agent-harness/NOTEBOOKLM.md`
- Create: `notebooklm/agent-harness/ATTRIBUTION.md`
- Create: `notebooklm/agent-harness/THIRD_PARTY_NOTICES.md`
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/README.md`
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/skills/SKILL.md`
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/tests/TEST.md`
- Create: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_manual_e2e.md`

**Step 1: Write the failing test**

Add assertions that:
- `setup.py` exposes `cli-anything-notebooklm`
- skill file exists
- README includes acknowledgement text

**Step 2: Run test to verify it fails**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py -q`
Expected: FAIL on missing files and packaging metadata

**Step 3: Write minimal implementation**

Create all packaging and documentation files with explicit attribution and experimental disclaimers.

**Step 4: Run test to verify it passes**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py cli_anything/notebooklm/tests/test_cli_smoke.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add notebooklm/agent-harness
git commit -m "docs: add notebooklm harness attribution and packaging"
```

### Task 5: Verify the scaffold end to end

**Files:**
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/tests/TEST.md`

**Step 1: Write the failing test**

No new behavior. This task is verification and documentation.

**Step 2: Run test to verify it fails**

Not applicable.

**Step 3: Write minimal implementation**

Run:
- `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py cli_anything/notebooklm/tests/test_cli_smoke.py -q`
- `cd notebooklm/agent-harness && python3 -m cli_anything.notebooklm.notebooklm_cli --help`

Append the verification notes to `TEST.md`.

**Step 4: Run test to verify it passes**

Expected:
- targeted tests PASS
- CLI help exits 0

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/cli_anything/notebooklm/tests/TEST.md
git commit -m "test: verify notebooklm harness scaffold"
```
