from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from extraction import extract_health_events
from validation import validate_events

app = Flask(__name__)
CORS(app) 

@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple endpoint to check the server is alive."""
    return jsonify({
        "status": "ok",
        "service": "HERA backend"
    })


@app.route("/api/extract", methods=["POST"])
def extract():
    """
    Expects JSON body:
    {
      "journal_entry": "some text",
      "date": "05-09-2026"   <-- dd-mm-yyyy, as chosen by the user on the frontend
    }

    Returns JSON:
    {
      "events": [...draft events, each with date in yyyy-mm-dd format...],
      "rejected": [...]
    }
    """
    data = request.get_json()

    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

   
    journal_entry = data.get("journal_entry", "")
    if not isinstance(journal_entry, str) or journal_entry.strip() == "":
        return jsonify({"error": "'journal_entry' is required and cannot be empty"}), 400

    raw_date = data.get("date", "")
    if not isinstance(raw_date, str) or raw_date.strip() == "":
        return jsonify({"error": "'date' is required in dd-mm-yyyy format"}), 400

    try:
        parsed_date = datetime.strptime(raw_date.strip(), "%d-%m-%Y")
        normalized_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "'date' must be a valid date in dd-mm-yyyy format"}), 400

    raw_events = extract_health_events(journal_entry)

    valid_events, invalid_events = validate_events(raw_events)

    events_for_response = []
    for event in valid_events:
        event_dict = event.model_dump()
        event_dict["date"] = normalized_date
        event_dict["status"] = "draft"
        events_for_response.append(event_dict)

    return jsonify({
        "events": events_for_response,
        "rejected": invalid_events
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
