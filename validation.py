from google import genai
import json
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Literal

client = genai.Client(api_key="AQ.Ab8RN6JvtGFbwtMppQx5piVMDwNICDk_LFP_Kqtgs7zsX7-VCA")

system_prompt = """You extract health information from a patient's journal entry.

Rules:
- Extract ONLY what is explicitly stated by the patient
- Do NOT diagnose or infer a medical condition
- Do NOT infer causes
- Do NOT invent dates, durations, or medications not mentioned
- If the patient mentions a condition name (like "PCOS"), record it as something they mentioned, not as a confirmed fact
- Return ONLY valid JSON matching this schema, with no other text before or after, no markdown code fences:

{
  "events": [
    {
      "type": "symptom" | "medication" | "menstrual_change" | "mentioned_condition",
      "name": "string",
      "context": "string or null",
      "duration": "string or null"
    }
  ]
}
"""

class HealthEvent(BaseModel):
    type: Literal["symptom", "medication", "menstrual_change", "mentioned_condition"]
    name: str
    context: Optional[str] = None
    duration: Optional[str] = None

class ExtractionResult(BaseModel):
    events: List[HealthEvent]

def extract(journal_entry):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=journal_entry,
        config={
            "system_instruction": system_prompt,
            "response_mime_type": "application/json"
        }
    )
    raw_text = response.text
    print("RAW OUTPUT FROM GEMINI:")
    print(raw_text)
    print()

    parsed_dict = json.loads(raw_text)

    try:
        validated = ExtractionResult(**parsed_dict)
        print("VALIDATION PASSED. Clean events:")
        for event in validated.events:
            print(f"  - {event.type}: {event.name} (context: {event.context}, duration: {event.duration})")
        return validated
    except ValidationError as e:
        print("VALIDATION FAILED. Rejecting this output, NOT saving to database.")
        print(e)
        return None

if __name__ == "__main__":
    test_entry = "I have been very tired this week."
    result = extract(test_entry)

    print()
    print("--- Now testing the rejection path with deliberately broken data ---")
    fake_bad_data = {
        "events": [
            {"type": "diagnosis", "name": "PCOS confirmed"}
        ]
    }
    try:
        validated = ExtractionResult(**fake_bad_data)
        print("Uh oh, this should NOT have passed validation")
    except ValidationError as e:
        print("CORRECTLY REJECTED bad data:")
        print(e)
