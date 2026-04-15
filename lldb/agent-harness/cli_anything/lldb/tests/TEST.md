# TEST.md - LLDB CLI Test Plan

## Test Inventory Plan

- `test_core.py`: 24 unit tests planned
- `test_full_e2e.py`: 9 E2E tests planned

## Unit Test Plan

### `utils/lldb_backend.py`
- Validate import fallback behavior using mocked `subprocess.run`
- Validate error path when `lldb` binary is not found
- Validate invalid `lldb -P` output handling
- Planned tests: 4

### `utils/output.py`
- Validate JSON emission and newline termination
- Validate simple table rendering and empty table behavior
- Planned tests: 3

### `utils/errors.py`
- Validate structured error dict
- Validate debug traceback inclusion
- Planned tests: 2

### `core/session.py`
- Validate target/process guards and high-level wrappers with mocked LLDB objects
- Validate breakpoint set/list/delete/enable operations
- Validate step/continue/backtrace/locals/evaluate return schemas
- Validate thread/frame select logic
- Planned tests: 9

### `lldb_cli.py`
- Validate `--help` for root and command groups
- Validate JSON error behavior when no target/process exists
- Validate subprocess invocation entrypoint
- Planned tests: 6

## E2E Test Plan

### Prerequisites
- LLDB installed and available in PATH
- A debuggable executable path via `LLDB_TEST_EXE`

### Workflows to validate
- Create target -> launch process -> inspect process state
- Set breakpoint -> continue -> inspect frame/locals/backtrace
- Evaluate expression and read memory
- Load core dump (optional; controlled by `LLDB_TEST_CORE`)

### Output validation
- All command responses parse as valid JSON in `--json` mode
- Required keys exist (`pid`, `state`, `breakpoints`, `threads`, `frames`, etc.)
- Commands fail with structured error payloads when prerequisites are missing

## Realistic Workflow Scenarios

### Workflow name: `hello_debug_session`
- Simulates: attaching CLI agent to a simple debug loop executable
- Operations chained:
  1. `target create`
  2. `process launch`
  3. `breakpoint set`
  4. `process continue`
  5. `thread backtrace`
  6. `frame locals`
  7. `expr`
- Verified:
  - execution state changes
  - backtrace frame list shape
  - expression result object shape

### Workflow name: `inspect_memory_window`
- Simulates: low-level memory inspection around known buffer addresses
- Operations chained:
  1. `target create`
  2. `process launch`
  3. `memory read`
  4. `memory find`
- Verified:
  - deterministic hex payload length
  - successful needle lookup format

## Test Results

### Commands run

```bash
python -m pytest cli_anything/lldb/tests/test_core.py -v
LLDB_TEST_EXE=C:\Users\aimidi\AppData\Local\Programs\Python\Python311\python.exe python -m pytest cli_anything/lldb/tests/test_full_e2e.py -v -s
```

### Result summary

- `test_core.py`: 15 passed
- `test_full_e2e.py`: 3 passed, 1 skipped
- Skip reason: `LLDB_TEST_CORE` was not provided, so the optional core-dump scenario was not exercised

### Notes

- Verified the installed `cli-anything-lldb` entrypoint on Windows after editable install
- Fixed REPL fallback behavior for non-interactive subprocess execution on Windows
- Fixed Windows REPL command parsing so quoted paths and inherited `--json` mode work correctly
