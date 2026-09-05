from pydantic import BaseModel, ValidationError
from typing import Literal, Optional

HealthEventType = Literal[
    "symptom",
    "medication",
    "menstrual_change",
    "mentioned_condition"
]


class CreateEventRequest(BaseModel):
    """
    This is the shape we expect EACH extracted event to match
    before it's trusted. If Gemini returns something that doesn't
    fit this shape, Pydantic will reject it here instead of letting
    bad data flow further into the app.
    """
    type: HealthEventType
    name: str
    context: Optional[str] = None
    duration: Optional[str] = None
    source: Literal["journal", "manual"] = "journal"


def validate_events(raw_events):
    """
    Takes a list of raw dicts (straight from Gemini) and returns
    two lists: valid ones (as validated objects) and invalid ones
    (with the error explaining why they failed).
    """
    valid_events = []
    invalid_events = []

    for raw_event in raw_events:
        try:
            validated = CreateEventRequest(**raw_event)
            valid_events.append(validated)
        except ValidationError as e:
            invalid_events.append({
                "raw_event": raw_event,
                "error": str(e)
            })

    return valid_events, invalid_events


if __name__ == "__main__":
    good_event = {
        "type": "symptom",
        "name": "fatigue",
        "context": "around periods",
        "duration": "3 months",
        "source": "journal"
    }

    bad_event = {
        "type": "headache", 
        "name": "migraine",
        "source": "journal"
    }

    test_events = [good_event, bad_event]

    valid, invalid = validate_events(test_events)

    print(f"\nValid events: {len(valid)}")
    for v in valid:
        print(v)

    print(f"\nInvalid events: {len(invalid)}")
    for i in invalid:
        print(i)
