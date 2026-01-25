# 🧠 Dyslexia Learning Platform

A full-stack learning platform designed to support **dyslexic learners** through thoughtful speech practice, structured learning, and confidence-building assessments.

This repository contains **both backend and frontend codebases**, each documented independently.

---

## 📁 Repository Structure

```
dyslexia-learning-platform/
├── backend/
│   ├── app/
│   ├── media/
│   ├── softwaremodels/
│   └── README.md
│
└── frontend/
    └── README.md   (coming soon)
```

Each major part of the system is **self-contained** and documented in its own README.

---

## 🔙 Backend

The backend is a **FastAPI + PostgreSQL** system responsible for:

* authentication & authorization
* learning and practice flows
* mock tests & reports
* speech processing (STT, TTS)
* phoneme-aware evaluation
* feedback & recommendation engines

👉 **See [`backend/README.md`] for full backend details**, architecture, and API documentation.

---

## 🎨 Frontend (Coming Soon)

The frontend will handle:

* learner experience & UI
* accessibility-first design
* audio interaction & playback
* progress visualization
* report downloads

👉 **See [`frontend/README.md`] for frontend setup and design decisions** (to be added).

---

## 🧭 How to Navigate This Repo

* Start at the **backend README** if you’re working on APIs or data flows
* Start at the **frontend README** if you’re working on UI/UX
* Each module inside backend (`learning`, `practice`, `mock`, etc.) has its own structure and documentation
* No single “god document” — each part explains itself

---

## 💙 Design Philosophy

* supportive, non-punitive learning
* clarity over complexity
* scalable without overengineering
* learner confidence comes first

This project is built to grow — technically and humanly.

---

## 🤝 Contributing

* Read the README inside the area you’re working on
* Keep modules isolated
* Do not break existing endpoints
* Prefer small, incremental improvements
* Preserve the supportive tone throughout the system

---

## 📌 Final Note

This repository is intentionally **modular**.

If you’re exploring it for the first time:

* don’t rush
* open the READMEs
* follow the structure

The system is designed to make sense **one module at a time**.

---
