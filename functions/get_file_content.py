import os
from config import MAX_FILE_CHARS
from google.genai import types # type: ignore


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"

    try:
        target_path = os.path.abspath(
            os.path.normpath(os.path.join(working_dir_abs, file_path))
        )
    except Exception as e:
        return f"Error: {e}"

    # Ensure target_path is inside working_dir_abs
    try:
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
    except Exception as e:
        return f"Error: {e}"

    # Ensure it exists and is a regular file
    try:
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Error: {e}"

    # Read content
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return f'Error: {e}'

    # Truncate if needed
    try:
        if len(content) > MAX_FILE_CHARS:
            content = (
                content[:MAX_FILE_CHARS]
                + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            )
    except Exception as e:
        return f"Error: {e}"

    return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read the contents of a file inside the permitted working directory. "
        "If the file is larger than the maximum allowed characters, the content is truncated."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


