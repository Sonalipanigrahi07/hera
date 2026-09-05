import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")


client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
You are a health information extractor for an app called HERA.

Your job: read a short journal entry written by a patient, and extract
ONLY the health information the user explicitly stated. Do NOT diagnose,
do NOT guess causes, do NOT infer anything the user did not say.

Return ONLY valid JSON, with no markdown formatting, no code fences,
and no extra text before or after it. The JSON must match this exact shape:

{
  "events": [
    {
      "type": "symptom" | "medication" | "menstrual_change" | "mentioned_condition",
      "name": "string",
      "context": "string or null",
      "duration": "string or null",
      "source": "journal"
    }
  ]
}

If the journal entry contains no relevant health information, return:
{"events": []}
"""


def extract_health_events(journal_entry):
    """
    Takes a raw journal entry (plain text) and returns a list of
    draft HealthEvent dictionaries extracted by Gemini.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"{SYSTEM_PROMPT}\n\nJournal entry:\n{journal_entry}"
    )

    raw_text = response.text.strip()

    
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        print("Gemini did not return valid JSON. Raw response was:")
        print(raw_text)
        return []

    return parsed.get("events", [])



if __name__ == "__main__":
    test_entry = "I've been very tired around my periods this month and my cramps have become worse."

    print("Sending test journal entry to Gemini...")
    events = extract_health_events(test_entry)

    print("\nExtracted events:")
    print(json.dumps(events, indent=2))
