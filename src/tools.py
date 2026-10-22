import subprocess
import sys
from langchain_core.tools import tool


@tool
def run_python_code(code: str) -> str:
    """Execute a Python code snippet and return stdout or stderr.

    Runs the code in a subprocess using the current Python interpreter.
    Returns stdout on success, or a prefixed ERROR string on failure.
    Enforces a 15-second timeout to prevent runaway execution.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],  # run as: python -c "<code>"
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        # Surface stderr so the agent can self-correct on errors
        if error:
            return f"ERROR:\n{error}"
        return output or "(no output)"

    except subprocess.TimeoutExpired:
        return "ERROR: code execution timed out (15s limit)"
    except Exception as e:
        return f"ERROR: {e}"
