# Samaritan

**A terminal-based AI assistant built with Python, OpenRouter, and
SQLite.**

Samaritan is a practical Python project that demonstrates how to connect
an AI model to a command-line application, stream responses, expose
selected local tools, and store user-approved memories in a local
database.

> **Project level:** Beginner to intermediate\
> **Platform:** Windows 10/11\
> **Language:** Python 3.11+\
> **AI API:** OpenRouter\
> **Database:** SQLite\
> **Interface:** Windows Command Prompt (CMD)

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [How It Works](#how-it-works)
-   [Project Structure](#project-structure)
-   [Requirements](#requirements)
-   [Setup](#setup)
-   [Configuration](#configuration)
-   [Run Samaritan](#run-samaritan)
-   [Available Commands](#available-commands)
-   [Example Requests](#example-requests)
-   [Memory](#memory)
-   [Security Notes](#security-notes)
-   [Troubleshooting](#troubleshooting)
-   [Limitations](#limitations)
-   [Ideas for Improvement](#ideas-for-improvement)

## Overview

Samaritan runs in the Windows terminal. You can chat with an AI model,
ask it to use specific Python tools, and save selected information so it
can be retrieved in later sessions.

The project is designed to teach the building blocks of an AI-powered
application. It does **not** train or run a large language model
locally. The Python application runs on your computer, while AI
inference is performed through OpenRouter.

## Features

-   Custom terminal greeting and configured assistant identity (`root`).
-   AI responses through OpenRouter's API.
-   Conversation history during the current run.
-   Streaming responses, where supported by the selected model and
    provider.
-   Basic system information.
-   Selected local tools for tasks such as listing a directory, creating
    a folder, and reading a text file.
-   SQLite-backed persistent memory.
-   Memory search, listing, and deletion.
-   Built-in terminal commands such as `/help`, `/system`, `/tools`, and
    `/exit`.

### What Samaritan Does Not Do

The starter version does not run arbitrary AI-generated shell commands,
control the entire computer independently, or run its AI model fully
offline. Its actions are limited to the Python functions explicitly made
available by the application.

## How It Works

1.  You enter a request in the terminal.
2.  Python sends the request and relevant conversation history to
    OpenRouter.
3.  The model returns a response or requests one of the application's
    available tools.
4.  If a tool is requested, Python executes the corresponding predefined
    function.
5.  The tool result is sent back to the model so it can formulate a
    response.
6.  If you explicitly ask Samaritan to remember something, the memory
    function can save it to SQLite.
7.  Saved memories remain in the local database after the application
    closes, until you delete them.

## Project Structure

The project should have a structure similar to this:

``` text
Samaritan/
├── .venv/                 # Local Python virtual environment
├── .env                   # OpenRouter API key (keep private)
├── .gitignore             # Files Git should ignore
├── memory.py              # SQLite memory functions
├── samaritan.py           # Main application
└── samaritan_memory.db    # Created automatically for persistent memory
```

The database file may not appear until Samaritan initializes the memory
system.

## Requirements

-   Windows 10 or Windows 11.
-   Python 3.11 or newer.
-   Internet access.
-   An OpenRouter account and API key.
-   A text editor such as Notepad or Visual Studio Code.

The project uses Python's built-in `sqlite3` module. You do not need to
install a separate SQLite server.

## Setup

### 1. Install Python

Download Python for Windows from the official site:

https://www.python.org/downloads/windows/

During installation, enable **Add python.exe to PATH** if that option is
offered.

Open CMD and verify the installation:

``` cmd
python --version
python -m pip --version
```

If `python` is not recognized, try `py --version` and use `py` instead
of `python` in the setup commands.

### 2. Create the project folder

``` cmd
cd %USERPROFILE%\Desktop
mkdir Samaritan
cd Samaritan
```

If the folder already exists, do not run `mkdir Samaritan` again. Simply
navigate into it.

### 3. Create and activate a virtual environment

``` cmd
python -m venv .venv
.venv\Scripts\activate
```

When activated, the terminal prompt should show `(.venv)`.

If you use the Python launcher instead:

``` cmd
py -m venv .venv
.venv\Scripts\activate
```

### 4. Install dependencies

``` cmd
python -m pip install --upgrade pip
python -m pip install openai python-dotenv rich
```

Verify the packages:

``` cmd
python -m pip show openai python-dotenv rich
```

### 5. Create the project files

Create `samaritan.py`, `memory.py`, `.env`, and `.gitignore` inside the
`Samaritan` folder. Add the code provided in the project guide to the
matching Python files.

## Configuration

### OpenRouter API key

1.  Sign in at https://openrouter.ai/
2.  Create an API key in your account.
3.  Create a file named `.env` in the project directory.
4.  Add the following line, replacing the placeholder with your own key:

``` dotenv
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
```

Do not include the placeholder literally. Keep the key private and never
commit `.env` to a public repository.

### Select a model

The model identifier is configured in `samaritan.py`. For example, the
project may use:

``` python
MODEL = "openai/gpt-oss-20b:free"
```

Check OpenRouter for current model availability, pricing, rate limits,
and support for both tool calling and streaming:

-   https://openrouter.ai/models
-   https://openrouter.ai/docs

Free model access can be limited, and availability may change. If the
chosen model does not support the required workflow, select a compatible
model and update the identifier in the code. Some models or usage levels
may require credits.

### `.gitignore`

Use a `.gitignore` file containing at least:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
samaritan_memory.db
```

The database can contain personal information, so do not publish it
unless you have deliberately reviewed and sanitized its contents.

## Run Samaritan

Open CMD, navigate to the project directory, and activate the virtual
environment:

``` cmd
cd %USERPROFILE%\Desktop\Samaritan
.venv\Scripts\activate
python samaritan.py
```

Samaritan should initialize its memory database and display its startup
greeting. Type a request at the prompt to begin.

To close the application, enter:

``` text
/exit
```

## Available Commands

  -----------------------------------------------------------------------
  Command                             Purpose
  ----------------------------------- -----------------------------------
  `/help`                             Display available commands.

  `/clear`                            Clear the current conversation
                                      history.

  `/system`                           Display basic system information.

  `/tools`                            List available tools.

  `/memory`                           Display saved memories.

  `/forget ID`                        Delete a memory by its ID. Replace
                                      `ID` with the actual memory ID.

  `/memory-clear`                     Delete all saved memories. Use
                                      carefully.

  `/exit`                             Exit Samaritan.
  -----------------------------------------------------------------------

The exact behavior depends on the implementation in `samaritan.py`.

## Example Requests

Try these after launching the application:

``` text
Explain Python functions in beginner-friendly language.
List the files in the current project directory.
Create a folder called PracticeLab.
Read the sample text file in my project workspace.
Remember that my current project is called Samaritan.
What do you remember about my current project?
```

For file operations, use a test workspace and harmless sample files.
Confirm that a folder was actually created or that a file was read
successfully rather than relying only on the assistant's
natural-language response.

## Memory

Samaritan uses SQLite to store memories locally. The `memory.py` module
provides operations to:

-   Save a memory.
-   List stored memories.
-   Search memory content.
-   Delete a selected memory.
-   Clear all stored memories.

Persistent memory is different from conversation history. Conversation
history is maintained during the running session, while saved memories
are stored in the database file and can remain available after restart.

Do not save passwords, API keys, recovery codes, or other secrets as
memories. The AI's instructions alone are not a complete privacy or
security control; stronger versions should validate memory requests in
Python and require confirmation where appropriate.

## Security Notes

This is an educational prototype. Follow these precautions:

-   **Protect your API key.** Keep it in `.env`; never commit it or
    share it in screenshots.
-   **Review costs and limits.** Check OpenRouter's current model
    pricing and account limits before use.
-   **Restrict file access.** The starter implementation should be
    improved to confine file tools to a designated workspace and
    validate paths.
-   **Avoid arbitrary command execution.** Do not add a feature that
    blindly executes shell commands generated by the model.
-   **Treat file contents carefully.** If the application sends a local
    file's contents to the model, that content is transmitted to the
    external AI provider.
-   **Protect the database.** The memory database may contain personal
    information. Keep it out of public repositories.
-   **Validate tool results.** Handle errors and verify that requested
    operations succeeded.
-   **Use human oversight.** Review important outputs and do not rely on
    the assistant as the sole authority for security-sensitive
    decisions.

The configured assistant name `root` is only an application identity. It
does not grant Windows administrator privileges.

## Troubleshooting

### `python` is not recognized

Try:

``` cmd
py --version
```

If that works, use `py` for Python setup commands. Otherwise, install
Python again and ensure it is available on PATH.

### `No module named ...`

Activate the virtual environment and install the dependencies again:

``` cmd
.venv\Scripts\activate
python -m pip install openai python-dotenv rich
```

### API key missing or authentication error

-   Confirm that `.env` is in the same project directory as
    `samaritan.py`.
-   Check that the variable is named `OPENROUTER_API_KEY`.
-   Ensure the key is valid and has not been revoked.
-   Do not paste the key into error reports or public messages.

### Model unavailable or rate limited

Check OpenRouter's current model listing, provider status, account
limits, and any usage requirements. A free model may be temporarily
unavailable or may impose request limits.

### Tool calls do not work

Confirm that the selected model supports tool calling and that the model
identifier is correct. Review the terminal error output and test each
Python tool independently. Provider and model behavior can differ.

### Memory does not persist

Confirm that `memory.py` is present and that Samaritan initializes the
database. Check that the program can write to the project directory and
that the memory-saving tool completed successfully.

## Limitations

-   AI inference requires an internet connection and an available
    OpenRouter model.
-   Free access is not guaranteed to be unlimited.
-   The model may misunderstand requests or produce incorrect
    information.
-   Tool calling depends on the selected model and provider.
-   The starter memory system is a simple database, not human-like
    memory.
-   The project requires additional security work before it should be
    used with sensitive files or in a production environment.

## Ideas for Improvement

Possible extensions include:

-   Add a dedicated workspace and enforce path restrictions for file
    tools.
-   Add explicit confirmation before file changes or memory deletion.
-   Improve error handling, logging, and automated tests.
-   Add export and import for selected memories.
-   Add a configuration screen or a richer terminal interface.
-   Add unit tests for the memory module and each local tool.
-   Add configurable model selection and usage reporting.
-   Explore carefully controlled, authorized cybersecurity workflows
    such as summarizing sample logs or organizing incident notes.

## Learning Goals

By completing Samaritan, you practise:

-   Python application structure and functions.
-   Virtual environments and package management.
-   API integration and environment-based configuration.
-   Conversation history and streaming.
-   AI tool calling.
-   File operations and basic system information.
-   SQLite and persistent storage.
-   Command-line interface design.
-   Basic security and privacy considerations for AI applications.

## License

No license has been specified for this project. If you plan to publish
or distribute the code, choose and add an appropriate license file.

------------------------------------------------------------------------

**Samaritan is a learning project:** understand each component, test it
carefully, and improve it one feature at a time.
