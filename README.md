# README.me

There are two parts to this README. The first part is the README made by CodeCrafters when I started the project. The second part is my README made using this project! (only difference in first part is markdown header level). I completed this challenge when it was in the early access stage.

## README.md pre Finishing the project
[![progress-banner](https://backend.codecrafters.io/progress/claude-code/369a33e4-c873-4a23-83de-ec4a91fb56b7)](https://app.codecrafters.io/users/nkugler2?r=2qF)

This is a starting point for Python solutions to the
["Build Your own Claude Code" Challenge](https://codecrafters.io/challenges/claude-code).

Claude Code is an AI coding assistant that uses Large Language Models (LLMs) to
understand code and perform actions through tool calls. In this challenge,
you'll build your own Claude Code from scratch by implementing an LLM-powered
coding assistant.

Along the way you'll learn about HTTP RESTful APIs, OpenAI-compatible tool
calling, agent loop, and how to integrate multiple tools into an AI assistant.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

### Passing the first stage

The entry point for your `claude-code` implementation is in `app/main.py`. Study
and uncomment the relevant code, and submit to pass the first stage:

```sh
codecrafters submit
```

### Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `uv` installed locally.
2. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
3. Run `codecrafters submit` to submit your solution to CodeCrafters. Test
   output will be streamed to your terminal.

## README.md post Finishing the project

### Overview
This script is a CLI-based AI agent that provides an interactive chat interface with file system and shell capabilities. It uses an OpenAI-compatible API to create a conversation loop where the AI can call tools to read files, write files, and execute shell commands.

### Key Features

1. **Command-line Interface**: Uses `argparse` to accept a required `-p` argument for the initial user prompt.

2. **OpenAI Integration**: Configures an OpenAI client using settings from `app.config` (specifically `ACTIVE_PROVIDER`, api_key, base_url, and model).

3. **Tool Integration**: The AI has access to three tools:
   - **Read**: Reads and returns the contents of a specified file
   - **Write**: Writes content to a specified file
   - **Bash**: Executes a shell command and returns the output (stdout or stderr)

4. **Conversation Loop**:
   - Starts with the user's initial prompt
   - Sends the conversation to the AI
   - If the AI calls a tool, the script executes it and adds the result back to the conversation
   - Continues looping until the AI provides a final response without tool calls
   - Prints the final AI response

5. **Provider Support**: Includes special logging for Ollama and OpenRouter providers.

### How It Works

1. The script parses the command-line argument to get the user's initial prompt.
2. It creates an OpenAI client with the configured provider.
3. It enters a loop where it:
   - Calls the AI with the current conversation history and available tools
   - Checks if the AI response includes tool calls
   - Executes each tool call (Read/Write/Bash) and appends the result as a "tool" message
   - Continues the loop until no more tool calls are made
4. Finally, it prints the AI's content-only response to the console.

### Use Case
This allows users to interact with an AI assistant that can directly manipulate files and execute commands, making it useful for tasks like code review, file editing, system administration, and automated workflows - all through natural language prompts.

