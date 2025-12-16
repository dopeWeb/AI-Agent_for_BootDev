import os

def write_file(working_directory, file_path, content):
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
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
    except Exception as e:
        return f"Error: {e}"
    

    try:
        # Ensure parent directories exist
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            # Write (overwrite) the file
        with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
            return f"Error: {e}"