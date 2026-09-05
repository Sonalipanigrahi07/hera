# HERA API Contract

This is the single source of truth for how the frontend and backend communicate.
Any change to this file should be agreed on by the frontend, backend, and AI/extraction leads before implementation changes.

**Base URL:** `http://localhost:5000/api`

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

## GET /health

Simple check to confirm the backend is running.

**Response:**
```json
{
  "status": "ok",
  "service": "HERA backend"
}
```

---

## POST /extract

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
      "type": "symptom",
      "name": "fatigue",
      "context": "around periods",
      "duration": "3 months",
      "date": "2026-09-05",
      "source": "journal",
      "status": "draft"
    }
  ]
}
```

---

## POST /events

Creates one confirmed Health Event (called once per event the user confirms/edits on the verification screen).

**Request:**
```json
{
  "type": "symptom",
  "name": "fatigue",
  "context": "around periods",
  "duration": "3 months",
  "date": "2026-09-05",
  "source": "journal"
}
```

**Response:**
```json
{
  "id": "event_001",
  "status": "confirmed"
}
```

---

## GET /events

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

## GET /changes

*(Not yet built — confirm with backend lead who's picking this up.)*

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

## POST /appointment

*(Not yet built — confirm with backend lead who's picking this up.)*

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

## POST /share

*(Not yet built — confirm with backend lead who's picking this up.)*

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

## GET /share/\<token\>

*(Not yet built — confirm with backend lead who's picking this up.)*

Returns only the information the patient authorized, for the doctor viewing the link. No login required.

**Response:**
```json
{
  "valid": true,
  "brief": { "...": "same shape as /appointment response" },
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

## POST /share/\<token\>/revoke

*(Not yet built — confirm with backend lead who's picking this up.)*

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
- The AI never writes directly to the database — extracted events are always `status: "draft"` until the user confirms them via `POST /events`.
- `/changes` is computed with plain Python logic, not AI.
- Do not add fields to `HealthEvent` without updating this file and notifying the whole team first.

---

## Status

- ✅ `/health`, `/extract`, `POST /events`, `GET /events` — confirmed matching backend lead's description (pending verification against actual pushed code)
- ⏳ `/changes`, `/appointment`, `/share`, `/share/<token>`, `/share/<token>/revoke` — not yet built, need an owner
