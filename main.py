import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
import argparse
from prompts import system_prompt



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(api_key) == 0:
        raise RuntimeError("Your API key is empty")
    print("Hello from ai-agent-max!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),
    
    )
    usage = response.usage_metadata
    prompt_tokens = usage.prompt_token_count
    response_tokens = usage.candidates_token_count

    if len(args.user_prompt) == 0:
        raise RuntimeError("Empty prompt")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
