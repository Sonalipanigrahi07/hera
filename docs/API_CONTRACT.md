# HERA API Contract

This is the single source of truth for how the frontend and backend communicate.
Any change to this file should be agreed on by the frontend, backend, and AI/extraction leads before implementation changes.

---

## Canonical Data Model: HealthEvent

Every part of the system (AI extraction, database, timeline, comparison, appointment brief, sharing) uses this same object shape.

```json
{
  "id": "event_001",
  "type": "symptom",
  "name": "fatigue",
  "context": "around periods",
  "duration": "3 months",
  "date": "2026-09-05",
  "source": "journal",
  "status": "confirmed"
}
```

**Allowed `type` values:**
- `symptom`
- `medication`
- `menstrual_change`
- `mentioned_condition`

**Allowed `status` values:**
- `draft` — AI-extracted, not yet reviewed by user
- `confirmed` — user has reviewed and approved
- `deleted` — user rejected it

---

## POST /api/extract

Sends a raw journal entry to the AI and gets back draft health events.

**Request:**
```json
{
  "journal_entry": "I've been exhausted around my periods for the last three months."
}
```

**Response:**
```json
{
  "events": [
    {
      "id": "event_temp_001",
      "type": "symptom",
      "name": "fatigue",
      "context": "around periods",
      "duration": "3 months",
      "date": null,
      "source": "journal",
      "status": "draft"
    }
  ]
}
```

---

## POST /api/events

Saves user-confirmed events (after the user reviews/edits the draft from `/api/extract`).

**Request:**
```json
{
  "events": [
    {
      "id": "event_001",
      "type": "symptom",
      "name": "fatigue",
      "context": "around periods",
      "duration": "3 months",
      "date": "2026-09-05",
      "source": "journal",
      "status": "confirmed"
    }
  ]
}
```

**Response:**
```json
{
  "saved": true,
  "count": 1
}
```

---

## GET /api/events

Returns all confirmed events for the user, for the timeline view.

**Response:**
```json
{
  "events": [
    {
      "id": "event_001",
      "type": "symptom",
      "name": "fatigue",
      "context": "around periods",
      "duration": "3 months",
      "date": "2026-09-05",
      "source": "journal",
      "status": "confirmed"
    }
  ]
}
```

---

## GET /api/changes

Returns a deterministic (non-AI) comparison between recent and previous history, for the "What Changed?" screen.

**Response:**
```json
{
  "changes": [
    {
      "name": "fatigue",
      "previous_count": 2,
      "recent_count": 6,
      "description": "Fatigue reported more frequently"
    }
  ]
}
```

---

## POST /api/appointment

Generates an appointment brief from confirmed events and detected changes.

**Request:**
```json
{
  "event_ids": ["event_001", "event_002"]
}
```

**Response:**
```json
{
  "brief": {
    "recent_concerns": ["Fatigue around periods", "Increased cramps"],
    "changes": ["Fatigue reported more frequently"],
    "summary_text": "Patient reports increased fatigue around periods over the last 3 months, with cramps worsening recently."
  }
}
```

---

## POST /api/share

Creates a temporary, read-only share link for a healthcare provider.

**Request:**
```json
{
  "selected_event_ids": ["event_001", "event_002"],
  "expires_in_hours": 48
}
```

**Response:**
```json
{
  "share_token": "abc123xyz",
  "share_url": "https://hera-app.example.com/share/abc123xyz",
  "expires_at": "2026-09-08T12:00:00Z"
}
```

---

## GET /api/share/\<token\>

Returns only the information the patient authorized, for the doctor viewing the link. No login required.

**Response:**
```json
{
  "valid": true,
  "brief": { "...": "same shape as /api/appointment response" },
  "expires_at": "2026-09-08T12:00:00Z"
}
```

If expired or revoked:
```json
{
  "valid": false,
  "reason": "expired"
}
```

---

## POST /api/share/\<token\>/revoke

Immediately invalidates a share link.

**Response:**
```json
{
  "revoked": true
}
```

---

## General Rules

- All requests/responses are JSON.
- All dates use ISO 8601 format (`YYYY-MM-DD` or full timestamp for expiry).
- The AI never writes directly to the database — extracted events are always `status: "draft"` until the user confirms them via `/api/events`.
- `/api/changes` is computed with plain Python logic, not AI.
- Do not add fields to `HealthEvent` without updating this file and notifying the whole team first.
