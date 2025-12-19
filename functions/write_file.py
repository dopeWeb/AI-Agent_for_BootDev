import os
from google.genai import types  # type: ignore


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(
            os.path.normpath(os.path.join(working_dir_abs, file_path))
        )

        # Ensure target_path is inside working_dir_abs
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directories exist (based on target_path!)
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Write (overwrite) the file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Create or overwrite a file inside the permitted working directory. "
        "Parent directories are created if needed. Writes outside the permitted directory are blocked."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file (overwrites existing content).",
            ),
        },
        required=["file_path", "content"],
    ),
)




