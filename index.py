"""
Grammar Checker - a simple LLM-powered utility.

Takes text input from the user, sends it to the Gemini API,
and returns a corrected version along with a short explanation
of the changes made.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import openai

# ---------- Setup ----------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.6-flash"


def get_client():
    """Create and return an API client, or exit with a clear error."""
    if not API_KEY:
        raise SystemExit(
            "Missing GEMINI_API_KEY. Add it to a .env file in this folder."
        )
    return OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


# ---------- Core logic ----------

def check_grammar(client, text):
    """Send text to the LLM and return corrected text + explanation."""
    prompt = (
        "You are a grammar checker. Correct the grammar, spelling, and "
        "punctuation in the following text. Then briefly list the changes "
        "you made as bullet points.\n\n"
        f"Text:\n{text}\n\n"
        "Respond in this format:\n"
        "Corrected:\n<corrected text>\n\nChanges:\n<bullet list>"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except openai.RateLimitError:
        return "Error: rate limit or quota exceeded. Check your API usage dashboard."
    except openai.AuthenticationError:
        return "Error: invalid API key. Check your .env file."
    except Exception as e:
        return f"Error: request failed ({e})"

    return response.choices[0].message.content


# ---------- File I/O helpers ----------

def read_from_file(path):
    """Read text from a file, return None if it fails."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None


def save_to_file(path, content):
    """Write result to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved result to {path}")


# ---------- Main program ----------

def main():
    client = get_client()

    print("Grammar Checker")
    print("1. Type text directly")
    print("2. Read text from a file")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "2":
        path = input("Enter file path: ").strip()
        text = read_from_file(path)
        if text is None:
            return
    else:
        text = input("Enter text to check: ").strip()

    if not text:
        print("No text provided. Exiting.")
        return

    result = check_grammar(client, text)

    print("\n--- Result ---\n")
    print(result)

    save = input("\nSave result to a file? (y/n): ").strip().lower()
    if save == "y":
        out_path = input("Enter output file name (e.g. result.txt): ").strip()
        save_to_file(out_path, result)


if __name__ == "__main__":
    main()