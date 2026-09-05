from google import genai
import json

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
    parsed = json.loads(raw_text)
    return parsed

# Test it
if __name__ == "__main__":
    test_entry = "I have been very tired this week."
    result = extract(test_entry)
    print("PARSED RESULT:")
    print(json.dumps(result, indent=2))
