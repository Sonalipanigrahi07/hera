# hera
# HERA

### Connecting Her Health Story, Empowering Her Care

HERA is a patient-owned health memory platform designed to help women organize and communicate their health experiences over time.

Women often experience symptoms, treatments, medications, and health changes across weeks or months, while important details can become fragmented between appointments. HERA converts everyday health notes into structured health events, helping users build a clear personal health history, identify changes over time, prepare for appointments, and control what information they share with healthcare providers.

---

## Problem

Women's health concerns can be dismissed or normalized, delaying diagnosis and care. Health experiences may also become fragmented across brief clinical visits, personal notes, medications, and different healthcare providers.

Language and health-literacy barriers can further make it difficult for women to communicate their experiences clearly.

HERA addresses the information and context gap by helping patients maintain an organized record of their own health experiences.

---

## Our Solution

HERA follows the workflow:

**Personalize → Capture → Structure → Remember → Compare → Prepare → Control → Share**

### 1. Personalize
Users select the health areas relevant to them, such as:

- PCOS
- Menstrual Health
- Endometriosis
- Pregnancy
- Postpartum
- Menopause
- General Health

### 2. Capture
Users record their experiences naturally through written entries and quick logs.

Example:

> "I've been exhausted around my periods for the last three months. My periods have also become heavier and I started iron tablets two weeks ago."

### 3. Structure
AI converts the user's entry into structured health events such as:

- Fatigue
- Context: Around periods
- Duration: 3 months
- Heavier periods
- Iron tablets started

The original entry is retained, and the user can review, edit, confirm, or delete the extracted information.

### 4. Remember
Confirmed information becomes part of the user's personal health timeline.

### 5. Compare
HERA compares recent information with the user's previous history to identify changes such as:

- Symptoms becoming more frequent
- New symptoms being recorded
- Medication changes
- Changes in recorded patterns

### 6. Prepare
HERA generates an appointment brief containing relevant history, recent changes, medications, and topics the user may want to discuss with a healthcare professional.

### 7. Control
The user decides what information should be included in a shared context.

### 8. Share
Users can generate temporary access for healthcare providers and control how long the shared information remains available.

---

## Key Features

- Personalized health spaces
- Natural-language health journaling
- AI-based health-event extraction
- User verification and editing of AI output
- Personal health timeline
- "What Changed?" comparison
- Appointment preparation
- Patient-controlled information sharing
- Temporary access and revocation
- English/Tamil accessibility support

---

## What HERA Does Not Do

HERA is designed as a health-context and organization tool.

It does **not**:

- Diagnose medical conditions
- Prescribe medication
- Recommend treatment
- Claim that a symptom is caused by a particular disease
- Replace a healthcare professional

The system organizes information provided by the user and helps prepare that information for healthcare conversations.

---

## Technology

### Frontend
- [Add final choice: React / Next.js / HTML, CSS & JavaScript]

### Backend
- Python
- Flask

### Database
- SQLite for the MVP

### AI
- LLM API for structured health-event extraction and summarization

### Additional Services
- Translation API for English/Tamil support
- Temporary token-based sharing for clinician access

> The technology stack is subject to change during development as the MVP is refined.

---

## System Workflow

```text
User Input
    ↓
Health Journal / Quick Log
    ↓
AI Extraction
    ↓
Structured Health Events
    ↓
User Review & Confirmation
    ↓
Personal Health Timeline
    ↓
"What Changed?"
    ↓
Appointment Brief
    ↓
Patient-Controlled Sharing
    ↓
Healthcare Provider
