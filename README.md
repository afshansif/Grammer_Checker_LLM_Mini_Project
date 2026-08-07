# Grammar Checker

A simple command-line tool that checks and corrects grammar using the Gemini API.

## What it does

- Accepts text either typed directly or from a file
- Sends it to the Gemini API for grammar/spelling/punctuation correction
- Prints the corrected text plus a bullet list of changes made
- Optionally saves the result to a file
- Handles missing API key, empty input, and API errors gracefully

## Install dependencies

```bash
pip install openai python-dotenv
```

## Configure the API key

Create a `.env` file in this folder:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com/) — no credit card needed.

## Run it

```bash
python grammar_checker.py
```

Follow the prompts to enter text or a file path.