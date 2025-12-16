import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Get absolute paths for the security check
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))

        # 1. Security Check: Outside working directory
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. Existence Check
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'

        # 3. Extension Check: Must end with .py
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # 4. Execution
        completed_process = subprocess.run(
            [sys.executable, file_path, *args],
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 5. Handle Non-zero Exit Code
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
            
        # 6. Handle No Output
        # We strip() to ensure strings with only whitespace/newlines are treated as empty
        if not completed_process.stdout.strip() and not completed_process.stderr.strip():
            return "No output produced"
            
        # 7. Success Output
        return f"STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}"

    except Exception as e:
        # 8. Handle Execution Exceptions (Timeouts, etc.)
        return f"Error: executing Python file: {e}"
