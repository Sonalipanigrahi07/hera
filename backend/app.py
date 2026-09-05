from flask import Flask, request, jsonify
from flask_cors import CORS

from extraction import extract

app = Flask(__name__)
CORS(app)


@app.route("/extract", methods=["POST"])
def extract_endpoint():
    data = request.get_json()

    if not data or "journal_entry" not in data:
        return jsonify({
            "error": "Missing 'journal_entry' in request body"
        }), 400

    journal_entry = data["journal_entry"]

    if not isinstance(journal_entry, str) or not journal_entry.strip():
        return jsonify({
            "error": "journal_entry must be a non-empty string"
        }), 400

    try:
        result = extract(journal_entry)

        if result is None:
            return jsonify({
                "error": "AI output failed validation"
            }), 500

        return jsonify(result.model_dump())

    except Exception as e:
        print("Extraction error:", e)

        return jsonify({
            "error": "An error occurred while processing the journal entry"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "HERA backend is running"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
