<<<<<<< HEAD
# Smart Task Analyzer

This repository implements the Smart Task Analyzer described in the assignment PDF. :contentReference[oaicite:1]{index=1}

## What this includes
- Django backend with two endpoints:
  - `POST /api/tasks/analyze/` — accepts list of tasks + options; returns tasks sorted with `score` and `explanation`.
  - `GET  /api/tasks/suggest/` — returns top 3 suggested tasks (accepts JSON `tasks` query param or uses example).
- Frontend: `frontend/index.html`, `styles.css`, `script.js` — simple UI to add tasks, paste JSON, analyze, and get suggestions.
- `tasks/scoring.py` contains the priority algorithm.
- Unit tests: `tasks/tests.py` (3 tests).

## Setup (local)
1. Ensure Python 3.8+ is installed.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
=======
# task-analyzer
>>>>>>> 9e4cdd5612fd10ca6ae887557eecc72d7ef5ceea
