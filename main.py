import argparse
import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    MAX_ITERATIONS = 20

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            raise RuntimeError(f"Fatal error calling Gemini API: {e}")

        if not response.candidates:
            raise RuntimeError("Gemini API returned no candidates")

        # 1. Add model responses (candidates) to messages
        model_requested_tool = False

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        # 2. Check if the model requested any tools
        model_requested_tool = bool(response.function_calls)

        # 3. If no tool calls and we have text → finished
        if not model_requested_tool and response.text:
            print("Response:")
            print(response.text)
            break

        # 3. Execute tool calls
        tool_response_parts = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=verbose)

            # Validate tool response
            if (
                not function_call_result.parts
                or not hasattr(function_call_result.parts[0], "function_response")
                or function_call_result.parts[0].function_response is None
                or function_call_result.parts[0].function_response.response is None
            ):
                raise RuntimeError(
                    "Fatal: tool response missing function_response.response"
                )

            tool_response_parts.append(function_call_result.parts[0])

            if verbose:
                print(
                    f"-> {function_call_result.parts[0].function_response.response}"
                )

        # 4. Convert tool responses into a user message and append
        if tool_response_parts:
            messages.append(
                types.Content(
                    role="user",
                    parts=tool_response_parts,
                )
            )

    else:
        raise RuntimeError(
            "Maximum number of iterations reached without completing the task"
        )


if __name__ == "__main__":
    main()