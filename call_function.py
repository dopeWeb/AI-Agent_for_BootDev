from google.genai import types  # type: ignore

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file


# Tool declarations exposed to Gemini (used by main.py)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call, verbose: bool = False) -> types.Content:
    """
    Handle execution of a tool function chosen by the LLM.

    - function_call: types.FunctionCall
      - .name: function name (string)
      - .args: dict of keyword arguments
    - verbose: whether to print full debug info
    """

    function_name = function_call.name

    # Print per assignment rules
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Map function name -> actual callable
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    func = function_map.get(function_name)
    if not func:
        # Invalid function name
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Prepare kwargs from model-provided args
    kwargs = dict(function_call.args) if function_call.args else {}

    # Never trust the model with working_directory
    kwargs.pop("working_directory", None)

    # Inject required working directory (assignment requirement)
    kwargs["working_directory"] = "./calculator"

    # Call the function and capture result
    try:
        function_result = func(**kwargs)
    except Exception as e:
        function_result = f"Error: {e}"

    # Return tool response as types.Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
