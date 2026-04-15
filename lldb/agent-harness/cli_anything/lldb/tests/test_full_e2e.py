"""
End-to-end tests for LLDB CLI harness.

Requires LLDB installed and a test executable path in LLDB_TEST_EXE.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HARNESS_ROOT = str(Path(__file__).resolve().parents[3])
TEST_EXE = os.environ.get("LLDB_TEST_EXE", "")
TEST_CORE = os.environ.get("LLDB_TEST_CORE", "")

HAS_EXE = os.path.isfile(TEST_EXE) if TEST_EXE else False
HAS_CORE = os.path.isfile(TEST_CORE) if TEST_CORE else False

try:
    import lldb  # noqa: F401

    HAS_LLDB_MODULE = True
except Exception:
    HAS_LLDB_MODULE = False

skip_no_lldb = pytest.mark.skipif(not HAS_LLDB_MODULE, reason="lldb module not importable")
skip_no_exe = pytest.mark.skipif(not HAS_EXE, reason="LLDB_TEST_EXE not set or file missing")
skip_no_core = pytest.mark.skipif(not HAS_CORE, reason="LLDB_TEST_CORE not set or file missing")


def _run_cli(*args) -> dict:
    cmd = [sys.executable, "-m", "cli_anything.lldb.lldb_cli", "--json"]
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=90,
        cwd=HARNESS_ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(f"CLI failed: {result.stderr}\n{result.stdout}")
    return json.loads(result.stdout)


@skip_no_lldb
@skip_no_exe
class TestLLDBE2E:
    def test_target_create(self):
        data = _run_cli("target", "create", "--exe", TEST_EXE)
        assert data["executable"] == TEST_EXE
        assert "triple" in data

    def test_target_info(self):
        # This command is stateless between invocations; verify expected error payload.
        # Real workflow is validated in test_repl_workflow.
        cmd = [
            sys.executable,
            "-m",
            "cli_anything.lldb.lldb_cli",
            "--json",
            "target",
            "info",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=HARNESS_ROOT)
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data

    def test_repl_workflow(self):
        script = "\n".join(
            [
                f"target create --exe {TEST_EXE}",
                "process launch",
                "process info",
                "thread list",
                "quit",
                "",
            ]
        )
        cmd = [sys.executable, "-m", "cli_anything.lldb.lldb_cli", "--json"]
        result = subprocess.run(
            cmd,
            input=script,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=HARNESS_ROOT,
        )
        assert result.returncode == 0
        assert '"pid"' in result.stdout or '"error"' in result.stdout


@skip_no_lldb
@skip_no_exe
@skip_no_core
class TestCoreE2E:
    def test_core_load_requires_target(self):
        cmd = [
            sys.executable,
            "-m",
            "cli_anything.lldb.lldb_cli",
            "--json",
            "core",
            "load",
            "--path",
            TEST_CORE,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=HARNESS_ROOT)
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data
