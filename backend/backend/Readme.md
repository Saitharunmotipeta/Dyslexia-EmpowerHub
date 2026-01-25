# 🧠 Dyslexia Learning Platform – Backend

A **FastAPI + PostgreSQL** backend designed to support **dyslexic learners** through structured learning, open practice, and confidence-building assessments.

This system prioritizes:

* clarity over complexity
* encouragement over judgment
* scalability without overengineering

---

## 🌟 Core Philosophy

This backend is built around one idea:

> **Learning should feel safe, progressive, and confidence-boosting — especially for dyslexic users.**

Every API, score, and report is designed with that principle in mind.

---

## 🏗️ Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Auth:** JWT-based authentication
* **Speech-to-Text:** Vosk
* **Audio Processing:** FFmpeg
* **Phoneme Analysis:** Custom phoneme model
* **Reports:** On-the-fly PDF generation

---

## 🔐 Authentication

* JWT-based authentication
* Protected routes use `get_current_user_id()`
* Users table includes:

  * learning preferences
  * streak tracking
  * speech pace (TTS)
  * personalization settings

---

## 📘 Learning Module (`/learning`)

**Purpose:** Structured skill-building with progress tracking.

### Features

* Level-based learning
* Word lists per level
* Mastery tracking per word
* Adjustable TTS pace
* Automated feedback & recommendations

### Core Tables

* `levels`
* `words`
* `level_words`

---

## 🎙️ Practice Module (`/practice`)

**Purpose:** Open pronunciation practice without pressure.

### Flow

1. User uploads audio
2. Audio converted to WAV
3. STT via Vosk
4. Spoken text compared with expected text
5. Feedback + insights returned

This module is **flexible and retry-friendly**.

---

## 🧪 Mock Test Module (`/mock`)

**Purpose:** Gentle assessment to reinforce confidence, not induce stress.

### Key Principles

* Accessible only after sufficient mastery (≥ 70%)
* Unlimited attempts
* Time-bounded per word (supportive, not punitive)
* Small test size (3 words by default)
* Motivational feedback always

### Mock Test Flow

1. Unlock check (mastery-based)
2. Start test → attempt created
3. Per-word interaction:

   * understand
   * listen (TTS)
   * speak (STT)
4. Evaluation + insights
5. Final report generation

---

## 📄 Downloadable Reports (Option A)

* Reports are generated **on demand**
* No files stored on disk or DB
* Backend generates a **PDF**
* Frontend simply triggers download

### Report Includes

* Overall score & verdict
* Word-wise breakdown
* Feedback & tips
* Confidence message
* Clear next steps

---

## 🧠 Phoneme-Aware Evaluation

To provide **precise and helpful feedback**, the system uses phoneme-level analysis:

* Expected word → phoneme breakdown
* Recognized speech → phoneme breakdown
* Comparison generates:

  * sound-level insights
  * better feedback
  * smarter recommendations

Phonemes **enhance** evaluation — they do not replace text similarity.

---

## 🗂️ Directory Structure (High-Level)

```
backend/
├── app/
│   ├── auth/
│   ├── learning/
│   ├── practice/
│   ├── mock/
│   └── common/
│||||||||||||||
├── media/
│   └── ffmpeg_utils.py
│
└── softwaremodels/
    ├── vosk/
    ├── phenonememodel/
    └── ffmpeg/
```

Each module follows:

* `routes/` → API endpoints
* `services/` → core logic
* `models/` → DB models
* `schemas/` → request/response contracts
* `utils/` → reusable rules

---

## 🧪 Testing Philosophy (Upcoming)

Manual testing is minimized by design.

### Planned Enhancements

* Automated mock test execution
* One-click test runner
* End-to-end flow validation
* Reduced developer fatigue

---

## 🚀 Upcoming Roadmap

### 1️⃣ Mock Test Automation

* Full automation flow
* Stress-tested logic
* Reliable scoring

### 2️⃣ Single-Click Testing

* Automated setup
* No manual DB updates
* One command → full validation

### 3️⃣ Dynamic Learning Module

* User-provided words
* Automated learning + practice together
* Same intelligence, fully dynamic input

---

## 💙 Design Values

* No “fail” language
* No harsh scoring
* Feedback explains *what to focus on*
* Progress is always highlighted
* System adapts to the learner — not the other way around

---

## 🤝 Final Note

This backend is not just an API.

It’s a **learning companion** — designed to grow with the learner, respect their challenges, and celebrate their progress.

If you’re reading this as a developer:

* keep it clean
* keep it kind
* keep it scalable

---







psql -U postgres
psql -U postgres -d dyslexia_learning
\c dyslexia_learning


TRUNCATE TABLE words RESTART IDENTITY CASCADE;
