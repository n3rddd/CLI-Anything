# NotebookLM PR Polish Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Tighten the experimental NotebookLM harness into a more upstream-ready contribution with stronger docs, explicit attribution, and subprocess-level CLI smoke coverage.

**Architecture:** Keep the current service-style wrapper architecture intact. Improve PR readiness by expanding package-facing documentation and adding lightweight subprocess tests that verify the packaged CLI interface without requiring a live authenticated NotebookLM session.

**Tech Stack:** Python 3, Click, pytest, subprocess, Markdown docs

### Task 1: Add failing tests for PR-facing expectations

**Files:**
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_core.py`
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/tests/test_cli_smoke.py`

**Step 1: Write the failing test**

Add tests that require:
- README to document installation, test execution, safety boundaries, and references
- SKILL.md to include installation, usage, and explicit unofficial guidance
- subprocess CLI help to render through a resolved `cli-anything-notebooklm` entry path

**Step 2: Run test to verify it fails**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py cli_anything/notebooklm/tests/test_cli_smoke.py -q`

Expected: FAIL on missing README/SKILL sections or missing subprocess helper behavior

**Step 3: Write minimal implementation**

Expand documentation and add the smallest test helper needed for subprocess smoke coverage.

**Step 4: Run test to verify it passes**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py cli_anything/notebooklm/tests/test_cli_smoke.py -q`

Expected: PASS

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/cli_anything/notebooklm/tests notebooklm/agent-harness/cli_anything/notebooklm/README.md notebooklm/agent-harness/cli_anything/notebooklm/skills/SKILL.md
git commit -m "test: harden notebooklm harness smoke coverage"
```

### Task 2: Improve docs for upstream review

**Files:**
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/README.md`
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/skills/SKILL.md`
- Modify: `notebooklm/agent-harness/NOTEBOOKLM.md`

**Step 1: Write the failing test**

Covered by Task 1 doc assertions.

**Step 2: Run test to verify it fails**

Covered by Task 1.

**Step 3: Write minimal implementation**

Document:
- installation and local prerequisites
- run and test commands
- command group overview
- agent guidance and safe-by-default behavior
- explicit references and unofficial attribution boundary

**Step 4: Run test to verify it passes**

Run: `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests/test_core.py cli_anything/notebooklm/tests/test_cli_smoke.py -q`

Expected: PASS

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/NOTEBOOKLM.md notebooklm/agent-harness/cli_anything/notebooklm/README.md notebooklm/agent-harness/cli_anything/notebooklm/skills/SKILL.md
git commit -m "docs: polish notebooklm harness contribution docs"
```

### Task 3: Verify and record final state

**Files:**
- Modify: `notebooklm/agent-harness/cli_anything/notebooklm/tests/TEST.md`

**Step 1: Write the failing test**

No new behavior test. This task records verification evidence.

**Step 2: Run test to verify it fails**

Not applicable.

**Step 3: Write minimal implementation**

Run:
- `cd notebooklm/agent-harness && python3 -m pytest cli_anything/notebooklm/tests -q`
- `cd notebooklm/agent-harness && python3 -m cli_anything.notebooklm.notebooklm_cli --help`

Append fresh results to `TEST.md`.

**Step 4: Run test to verify it passes**

Expected:
- all NotebookLM scaffold tests PASS
- module help exits 0 and prints command groups

**Step 5: Commit**

```bash
git add notebooklm/agent-harness/cli_anything/notebooklm/tests/TEST.md
git commit -m "test: record notebooklm harness verification"
```
