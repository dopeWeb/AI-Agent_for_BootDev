import os
from google.genai import types # type: ignore


def get_files_info(working_directory, directory="."):
    """
    Return information about the contents of `directory`
    (relative to `working_directory`) as a string.

    Each successful line looks like:
    - NAME: file_size=NN bytes, is_dir=True/False

    On error, returns a string starting with "Error:".
    """
    try:
        # Absolute path for the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Normalised absolute path to the target directory
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Ensure target_dir is inside working_dir_abs
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir])
            == working_dir_abs
        )
        if not valid_target_dir:
            return (
                f'Error: Cannot list "{directory}" as it is outside the '
                f'permitted working directory'
            )

        # Ensure the target is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Build result lines
        lines = []
        for name in os.listdir(target_dir):
            item_path = os.path.join(target_dir, name)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(
                f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            )

        return "\n".join(lines)

    except Exception as e:
        # Any unexpected error is turned into a string
        return f"Error: {e}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


