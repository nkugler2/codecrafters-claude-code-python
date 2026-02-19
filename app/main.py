import argparse
import os
import sys
import json

# from config import settings
from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
#API_KEY = settings.OPENROUTER_API_KEY

# The request body
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # Users inital message
    messages = [{"role": "user", "content": args.p}]

    while True:
        # This is the response message
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            ##model="openrouter/aurora-alpha",
            messages=messages,
            tools=[
                {
                    # Read function
                    "type": "function",
                    "function": {
                        "name": "Read",
                        "description": "Read and return the contents of a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path to the file to read",
                                }
                            },
                            "required": ["file_path"],
                        },
                    },
                }
            ],
        )

        # Append the message object after the api call
        messages.append(chat.choices[0].message)

        # if there are any tool calls
        if chat.choices[0].message.tool_calls:
            # if the tool call is Read
            for tool_call in chat.choices[0].message.tool_calls:
                if tool_call.function.name == "Read":
                    # variable for for the function arguments
                    func_args = json.loads(tool_call.function.arguments)
                    # grab the file path
                    file_path = func_args["file_path"]
                    # with the file path in read mode as f
                    with open(file_path, "r") as f:
                        content = f.read()
                    # make the object the api needs
                    Read_tool_response = {"role": "tool",
                                           "tool_call_id": tool_call.id,
                                           "content": content,
                                          }
                    messages.append(Read_tool_response)

                ########## Add more tool calls here ###############
        else:
            # print null if not used
            print(chat.choices[0].message.content)
            break

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

if __name__ == "__main__":
    main()
